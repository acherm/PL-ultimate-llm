#!/usr/bin/env python3
"""Local web UI for reviewing SWH samples → per-program PL ground truth.

Single-file, stdlib-only HTTP server. Storage is `tools/reviewstore.py`
(one immutable JSON file per review under `reviews/<sha1_git>/`); the
server itself is stateless — kill and restart it freely.

Usage
-----
    python3 tools/review_server.py                  # http://127.0.0.1:8765
    python3 tools/review_server.py --port 9000 --open
    python3 tools/review_server.py --as alice       # default reviewer id
    python3 tools/review_server.py --host 0.0.0.0   # LAN labelling session
    python3 tools/review_server.py --autocommit     # git-commit reviews on exit

Review independence: other humans' verdicts for a program are hidden
(count only) until you submit yours; what was on screen (predicted PL +
extension claimants) is recorded in each review's `shown` block.

The code pane is deliberately NOT syntax-highlighted: choosing a lexer
to colorize with would leak a language guess into the reviewer's eyes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reviewstore as store

ROOT = store.ROOT
MAX_CODE_CHARS = 120_000


# ---------------------------------------------------------------------------
# App state (taxonomy + samples loaded once; reviews re-read per request)
# ---------------------------------------------------------------------------

class App:
    def __init__(self, *, samples_dir: Path, reviews_dir: Path,
                 default_reviewer: str):
        self.samples_dir = samples_dir
        self.reviews_dir = reviews_dir
        self.default_reviewer = default_reviewer
        self.pl_index = store.load_pl_index()            # pl_id -> name
        self.known_pl_ids = set(self.pl_index)
        self.ext_claimants = store.load_ext_claimants()  # ext -> [claims]
        self.samples = store.load_samples_index(samples_dir)  # sha -> subject
        self.suggestions_rev = store.git_head_short()

    # -- suggestions --------------------------------------------------------

    def suggestions(self, subject: dict) -> dict:
        claims = self.ext_claimants.get(subject["ext"], [])
        return {
            "predicted_pl_id": subject["predicted_pl_id"],
            "predicted_via": subject["predicted_via"],
            "claimants": [
                dict(c, name=self.pl_index.get(c["pl_id"], c["pl_id"]))
                for c in claims
            ],
        }

    def shown_block(self, subject: dict) -> dict:
        return {
            "predicted_pl_id": subject["predicted_pl_id"],
            "claimants": [c["pl_id"] for c in
                          self.ext_claimants.get(subject["ext"], [])],
            "suggestions_rev": self.suggestions_rev,
        }

    # -- queue --------------------------------------------------------------

    def queue(self, *, strategy: str, ext: str, reviewer: str) -> list[str]:
        by_sha = store.reviews_by_sha(reviews_dir=self.reviews_dir)

        def human_reviewers(sha: str) -> set[str]:
            return {r["reviewer"]["id"] for r in by_sha.get(sha, [])
                    if (r.get("reviewer") or {}).get("kind") == "human"}

        shas = []
        for sha, subj in self.samples.items():
            if ext and subj["ext"] != ext:
                continue
            humans = human_reviewers(sha)
            if strategy == "unreviewed-by-me" and reviewer in humans:
                continue
            if strategy == "unreviewed" and humans:
                continue
            if strategy == "second-opinion" and (
                    not (humans - {reviewer}) or reviewer in humans):
                continue
            shas.append(sha)

        # Deterministic per-reviewer shuffle: every reviewer walks a different
        # permutation, so distributed coverage spreads without coordination.
        def key(sha: str) -> str:
            return hashlib.sha256(f"{reviewer}\0{sha}".encode()).hexdigest()
        shas.sort(key=key)
        return shas

    # -- reviews for one sha ------------------------------------------------

    def reviews_split(self, sha: str, reviewer: str) -> tuple[list, list]:
        """(mine, others) — full review dicts, oldest first."""
        mine, others = [], []
        for p, r in store.iter_reviews(sha, reviews_dir=self.reviews_dir):
            r["_file"] = p.name
            rv = r.get("reviewer") or {}
            if rv.get("kind") == "human" and rv.get("id") == reviewer:
                mine.append(r)
            else:
                others.append(r)
        return mine, others


# ---------------------------------------------------------------------------
# HTTP layer
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    app: App = None  # set by serve()

    # quieter logs: one line per request, no per-connection noise
    def log_message(self, fmt, *args):
        sys.stderr.write("  " + (fmt % args) + "\n")

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _err(self, code: int, msg: str):
        self._json({"error": msg}, code)

    # -- GET -----------------------------------------------------------------

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
        route = url.path.rstrip("/") or "/"
        app = self.app

        if route == "/":
            return self._send(200, PAGE.encode("utf-8"),
                              "text/html; charset=utf-8")

        if route == "/api/state":
            ext_counts: dict[str, int] = {}
            for s in app.samples.values():
                ext_counts[s["ext"]] = ext_counts.get(s["ext"], 0) + 1
            return self._json({
                "default_reviewer": app.default_reviewer,
                "total_samples": len(app.samples),
                "exts": sorted(ext_counts.items()),
                "strategies": ["unreviewed-by-me", "unreviewed",
                               "second-opinion", "all"],
                "rev": app.suggestions_rev,
                "fixed_labels": list(store.FIXED_LABELS),
                "confidences": list(store.CONFIDENCES),
            })

        if route == "/api/queue":
            reviewer = store.slugify(q.get("reviewer") or app.default_reviewer)
            strategy = q.get("strategy") or "unreviewed-by-me"
            queue = app.queue(strategy=strategy, ext=q.get("ext") or "",
                              reviewer=reviewer)
            return self._json({"queue": queue, "total": len(queue)})

        if route == "/api/sample":
            sha = (q.get("sha") or "").lower()
            subj = app.samples.get(sha)
            if not subj:
                return self._err(404, f"unknown sample sha {sha!r}")
            reviewer = store.slugify(q.get("reviewer") or app.default_reviewer)
            code_path = subj["dir"] / subj["filename"]
            try:
                text = code_path.read_bytes().decode("utf-8", errors="replace")
            except Exception as e:
                text = f"(could not read bytes: {e})"
            truncated = len(text) > MAX_CODE_CHARS
            mine, others = app.reviews_split(sha, reviewer)
            return self._json({
                "subject": {k: v for k, v in subj.items() if k != "dir"},
                "code": text[:MAX_CODE_CHARS],
                "truncated": truncated,
                "suggestions": app.suggestions(subj),
                "mine": mine,
                "others_count": len(others),
                # blind until the reviewer has their own verdict on record
                "others": others if mine else None,
            })

        if route == "/api/samples":
            reviewer = store.slugify(q.get("reviewer") or app.default_reviewer)
            by_sha = store.reviews_by_sha(reviews_dir=app.reviews_dir)
            rows = []
            for sha, s in app.samples.items():
                latest = store.latest_per_reviewer(by_sha.get(sha, []))
                mine = [r for r in latest
                        if r["reviewer"]["kind"] == "human"
                        and r["reviewer"]["id"] == reviewer]
                rows.append({
                    "sha1_git": sha,
                    "filename": s["filename"],
                    "ext": s["ext"],
                    "length": s["length"],
                    "slots": s["slots"],
                    "predicted_pl_id": s["predicted_pl_id"],
                    "n_human": sum(1 for r in latest
                                   if r["reviewer"]["kind"] == "human"),
                    "n_machine": sum(1 for r in latest
                                     if r["reviewer"]["kind"] != "human"),
                    # own verdict only — others stay blind in the browser too
                    "my_label": ((mine[0].get("verdict") or {}).get("label")
                                 if mine else None),
                    "reviewed_by_me": bool(mine),
                })
            rows.sort(key=lambda r: (r["ext"], r["filename"].lower()))
            return self._json({"rows": rows})

        if route == "/api/pls":
            needle = (q.get("q") or "").lower().strip()
            if not needle:
                return self._json({"results": []})
            res = []
            for pl_id, name in self.app.pl_index.items():
                if needle in pl_id.lower() or needle in name.lower():
                    res.append({"pl_id": pl_id, "name": name})
                if len(res) >= 200:
                    break
            res.sort(key=lambda r: (not r["pl_id"][3:].startswith(needle),
                                    len(r["pl_id"]), r["pl_id"]))
            return self._json({"results": res[:20]})

        return self._err(404, f"no route {route!r}")

    # -- POST ----------------------------------------------------------------

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        if url.path.rstrip("/") != "/api/review":
            return self._err(404, "no such route")
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length))
        except Exception as e:
            return self._err(400, f"bad JSON: {e}")

        app = self.app
        sha = (payload.get("sha") or "").lower()
        subj = app.samples.get(sha)
        if not subj:
            return self._err(404, f"unknown sample sha {sha!r}")
        reviewer_id = store.slugify(payload.get("reviewer") or
                                    app.default_reviewer)

        mine, others = app.reviews_split(sha, reviewer_id)
        supersedes = mine[-1]["_file"] if mine else None

        review = store.new_review(
            subject=subj,
            reviewer={"kind": "human", "id": reviewer_id},
            label=(payload.get("label") or "").strip() or None,
            confidence=payload.get("confidence"),
            comment=payload.get("comment"),
            shown=app.shown_block(subj),
            supersedes=supersedes,
        )
        try:
            path = store.write_review(review, reviews_dir=app.reviews_dir,
                                      known_pl_ids=app.known_pl_ids)
        except ValueError as e:
            return self._err(422, str(e))
        except FileExistsError:
            return self._err(409, "identical review already written")

        review["_file"] = path.name
        return self._json({
            "ok": True,
            "file": str(path.relative_to(ROOT) if path.is_relative_to(ROOT)
                        else path),
            "review": review,
            "others": others,  # revealed now that yours is on record
        })


# ---------------------------------------------------------------------------
# The page (inline: no build step, no static assets)
# ---------------------------------------------------------------------------

PAGE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PL sample review</title>
<style>
:root { --bg:#11151a; --panel:#1a2027; --line:#2a323c; --fg:#d7dde4;
        --muted:#8a949f; --acc:#4ea1ff; --ok:#3fb96d; --warn:#e0a93f; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
       font:14px/1.45 system-ui, sans-serif; }
header { display:flex; gap:10px; align-items:center; flex-wrap:wrap;
         padding:8px 14px; background:var(--panel);
         border-bottom:1px solid var(--line); position:sticky; top:0; z-index:5; }
header b { color:var(--acc); }
input, select, textarea, button {
  background:#222a33; color:var(--fg); border:1px solid var(--line);
  border-radius:6px; padding:5px 8px; font:inherit; }
button { cursor:pointer; }
button.primary { background:var(--acc); color:#06121f; font-weight:600; }
button.sugg { margin:2px 4px 2px 0; }
button.sugg.predicted { border-color:var(--warn); }
button.sugg.active { background:var(--acc); color:#06121f; }
.muted { color:var(--muted); }
.pill { border:1px solid var(--line); border-radius:10px; padding:0 7px;
        font-size:12px; color:var(--muted); }
main { display:flex; gap:12px; padding:12px; align-items:flex-start; }
#codecol { flex:3; min-width:0; }
#sidecol { flex:2; min-width:330px; max-width:560px; position:sticky; top:54px; }
.panel { background:var(--panel); border:1px solid var(--line);
         border-radius:8px; padding:12px; margin-bottom:12px; }
pre { margin:0; padding:12px; overflow:auto; max-height:78vh;
      font:12.5px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
      white-space:pre; tab-size:4; }
.fhead { display:flex; gap:10px; align-items:baseline; flex-wrap:wrap;
         padding:10px 12px; border-bottom:1px solid var(--line); }
.fhead code { word-break:break-all; }
a { color:var(--acc); }
#label-now { font-family:ui-monospace, monospace; padding:6px 8px;
             border:1px dashed var(--line);
             border-radius:6px; min-height:1.5em; }
#label-now.set { border-color:var(--ok); color:var(--ok); }
.row { margin:8px 0; }
.results div { padding:3px 6px; cursor:pointer; border-radius:4px; }
.results div:hover { background:#222a33; }
textarea { width:100%; min-height:60px; resize:vertical; }
.revealed { border-left:3px solid var(--warn); padding-left:8px; margin:6px 0; }
.revealed.mine { border-left-color:var(--ok); }
.revealed.old { opacity:.5; }
#toast { position:fixed; bottom:14px; left:50%; transform:translateX(-50%);
         background:#222a33; border:1px solid var(--line); padding:8px 14px;
         border-radius:8px; display:none; z-index:10; }
#browse { display:none; margin:12px; }
#btable { width:100%; border-collapse:collapse; font-size:13px; }
#btable th { text-align:left; color:var(--muted); font-weight:500;
             border-bottom:1px solid var(--line); padding:4px 8px;
             position:sticky; top:46px; background:var(--panel); }
#btable td { padding:3px 8px; border-bottom:1px solid #20262e; }
#btable tr[data-sha] { cursor:pointer; }
#btable tr[data-sha]:hover { background:#222a33; }
#btable tr.done td { opacity:.55; }
kbd { background:#222a33; border:1px solid var(--line); border-radius:4px;
      padding:0 5px; font-size:11px; }
</style></head>
<body>
<header>
  <b>PL sample review</b>
  <label class="muted">reviewer <input id="reviewer" size="14"></label>
  <label class="muted">queue <select id="strategy"></select></label>
  <label class="muted">ext <input id="extfilter" size="6" list="extlist" placeholder="all">
  <datalist id="extlist"></datalist></label>
  <button id="reload">reload queue</button>
  <button id="browsebtn">browse (b)</button>
  <span id="pos" class="pill"></span>
  <span id="session" class="pill">session: 0</span>
  <span id="rev" class="pill" title="git revision the server was started from"></span>
  <span class="muted" style="margin-left:auto">
    <kbd>1</kbd>–<kbd>9</kbd> pick · <kbd>⌃⏎</kbd> submit · <kbd>s</kbd> skip · <kbd>b</kbd> browse</span>
</header>
<div id="browse" class="panel">
  <div style="display:flex; gap:10px; align-items:center; margin-bottom:8px; flex-wrap:wrap">
    <input id="bfilter" placeholder="filter (filename, ext, slot, predicted)…" style="flex:1; min-width:200px">
    <select id="bstatus">
      <option value="all">all</option>
      <option value="unreviewed">no human review yet</option>
      <option value="not-mine">not reviewed by me</option>
      <option value="mine">reviewed by me</option>
    </select>
    <span id="bcount" class="pill"></span>
  </div>
  <table id="btable"></table>
</div>
<main>
  <div id="codecol">
    <div class="panel" style="padding:0">
      <div class="fhead" id="fhead"></div>
      <pre id="code"></pre>
    </div>
  </div>
  <div id="sidecol">
    <div class="panel" id="suggpanel">
      <div class="muted" style="margin-bottom:6px">Suggestions</div>
      <div id="suggs"></div>
    </div>
    <div class="panel">
      <div class="row"><div class="muted">Verdict</div>
        <div id="label-now">— no label —</div></div>
      <div class="row">
        <input id="plsearch" placeholder="search PL (name or id)…" style="width:100%">
        <div class="results" id="plresults"></div>
      </div>
      <div class="row">
        <select id="fixedlabel" style="width:100%">
          <option value="">not a PL / other label…</option>
        </select>
      </div>
      <div class="row" style="display:flex; gap:6px">
        <input id="newpl" placeholder="new PL slug" style="flex:1">
        <button onclick="setFromNewPl()">pl/new:</button>
      </div>
      <div class="row" style="display:flex; gap:6px">
        <input id="rawlabel" placeholder="advanced: raw label (pl/dialect:… pl/family:…)" style="flex:1">
        <button onclick="setFromRaw()">set</button>
      </div>
      <div class="row">confidence:
        <label><input type="radio" name="conf" value="high"> high</label>
        <label><input type="radio" name="conf" value="medium" checked> medium</label>
        <label><input type="radio" name="conf" value="low"> low</label>
      </div>
      <div class="row"><textarea id="comment"
        placeholder="comment (optional — required if no label)"></textarea></div>
      <div class="row" style="display:flex; gap:8px">
        <button class="primary" onclick="submitReview()">Submit ⌃⏎</button>
        <button onclick="clearLabel()">clear label</button>
        <button onclick="nextSample()">skip (s)</button>
      </div>
      <div id="othersnote" class="muted"></div>
      <div id="reveal"></div>
    </div>
  </div>
</main>
<div id="toast"></div>
<script>
const $ = id => document.getElementById(id);
let state = { queue: [], idx: 0, cur: null, label: null, session: 0,
              standalone: null, browseRows: [] };

function toast(msg, ms=2600) {
  $('toast').textContent = msg; $('toast').style.display = 'block';
  clearTimeout(toast._t); toast._t = setTimeout(() => $('toast').style.display='none', ms);
}
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

async function init() {
  const st = await (await fetch('api/state')).json();
  $('rev').textContent = 'rev ' + (st.rev || '?');
  $('reviewer').value = localStorage.reviewer || st.default_reviewer;
  for (const s of st.strategies) {
    const o = document.createElement('option'); o.value = o.textContent = s;
    $('strategy').appendChild(o);
  }
  $('strategy').value = localStorage.strategy || 'unreviewed-by-me';
  $('extfilter').value = localStorage.extfilter || '';
  for (const [ext, n] of st.exts) {
    const o = document.createElement('option'); o.value = ext;
    o.label = `${ext} (${n})`; $('extlist').appendChild(o);
  }
  for (const l of st.fixed_labels) {
    const o = document.createElement('option'); o.value = o.textContent = l;
    $('fixedlabel').appendChild(o);
  }
  await loadQueue();
}

async function loadQueue() {
  localStorage.reviewer = $('reviewer').value;
  localStorage.strategy = $('strategy').value;
  localStorage.extfilter = $('extfilter').value;
  const p = new URLSearchParams({ strategy: $('strategy').value,
    ext: $('extfilter').value, reviewer: $('reviewer').value });
  const r = await (await fetch('api/queue?' + p)).json();
  state.queue = r.queue; state.idx = 0; state.standalone = null;
  if (!state.queue.length) {
    $('pos').textContent = 'queue empty 🎉';
    $('fhead').innerHTML = '<span class="muted">Nothing matches this queue — change strategy/ext.</span>';
    $('code').textContent = ''; $('suggs').innerHTML = ''; state.cur = null;
    return;
  }
  await loadSample();
}

async function loadSample(shaOverride) {
  const sha = shaOverride || state.queue[state.idx];
  if (!sha) { toast('queue empty — try browse (b) or other filters'); return; }
  state.standalone = shaOverride || null;
  $('pos').textContent = shaOverride
    ? 'browse pick' : `${state.idx + 1} / ${state.queue.length}`;
  const p = new URLSearchParams({ sha, reviewer: $('reviewer').value });
  const r = await (await fetch('api/sample?' + p)).json();
  state.cur = r; clearLabel(); $('comment').value = '';
  $('reveal').innerHTML = '';
  document.querySelector('input[name=conf][value=medium]').checked = true;

  const s = r.subject;
  $('fhead').innerHTML =
    `<strong>${esc(s.filename)}</strong> <span class="pill">${esc(s.ext)}</span>` +
    `<span class="muted">${s.length} B · ${esc(s.slots.join(', '))}</span>` +
    `<a href="https://archive.softwareheritage.org/${esc(s.swhid)}/" target="_blank">SWH ↗</a>`;
  $('code').textContent = r.code + (r.truncated ? '\n…(truncated)…' : '');

  const sug = r.suggestions; let html = '';
  if (sug.predicted_pl_id)
    html += `<button class="sugg predicted" data-label="${esc(sug.predicted_pl_id)}">` +
            `★ ${esc(sug.predicted_pl_id)} <span class="muted">(predicted via ${esc(sug.predicted_via)})</span></button><br>`;
  sug.claimants.forEach((c, i) =>
    html += `<button class="sugg" data-label="${esc(c.pl_id)}">` +
      `${i + 1 <= 9 ? `<kbd>${i + 1}</kbd> ` : ''}${esc(c.name)} ` +
      `<span class="muted">${esc(c.strength)}·${esc(c.source)}</span></button>`);
  $('suggs').innerHTML = html ||
    '<span class="muted">no prediction, no claimants — virgin territory</span>';
  document.querySelectorAll('#suggs .sugg').forEach(b =>
    b.addEventListener('click', () => setLabel(b.dataset.label)));

  const mineNote = r.mine.length ? ` · you already reviewed this (new submit supersedes)` : '';
  $('othersnote').textContent = (r.others_count && !r.others)
    ? `${r.others_count} other review(s) — hidden until you submit${mineNote}`
    : (r.mine.length && !r.others_count ? `no other reviews${mineNote}` : '');
  renderHistory(r.mine, r.others);
}

function setLabel(l) {
  state.label = l;
  $('label-now').textContent = l; $('label-now').classList.add('set');
  document.querySelectorAll('#suggs .sugg').forEach(b =>
    b.classList.toggle('active', b.dataset.label === l));
}
function clearLabel() {
  state.label = null;
  $('label-now').textContent = '— no label —';
  $('label-now').classList.remove('set');
  $('fixedlabel').value = ''; $('newpl').value = ''; $('rawlabel').value = '';
  $('plsearch').value = ''; $('plresults').innerHTML = '';
  document.querySelectorAll('#suggs .sugg').forEach(b => b.classList.remove('active'));
}
function setFromNewPl() {
  const v = $('newpl').value.trim().toLowerCase().replace(/[^a-z0-9+._-]+/g, '-');
  if (v) setLabel('pl/new:' + v);
}
function setFromRaw() { const v = $('rawlabel').value.trim(); if (v) setLabel(v); }
$('fixedlabel').addEventListener('change', e => { if (e.target.value) setLabel(e.target.value); });

let _searchT;
$('plsearch').addEventListener('input', () => {
  clearTimeout(_searchT);
  _searchT = setTimeout(async () => {
    const q = $('plsearch').value.trim();
    if (!q) { $('plresults').innerHTML = ''; return; }
    const r = await (await fetch('api/pls?q=' + encodeURIComponent(q))).json();
    $('plresults').innerHTML = r.results.map(x =>
      `<div data-label="${esc(x.pl_id)}"><code>${esc(x.pl_id)}</code> ${esc(x.name)}</div>`).join('');
    document.querySelectorAll('#plresults div').forEach(d =>
      d.addEventListener('click', () => { setLabel(d.dataset.label); $('plresults').innerHTML=''; }));
  }, 150);
});

function renderHistory(mine, others) {
  const superseded = new Set();
  [...(mine || []), ...(others || [])].forEach(r => {
    const s = (r.verdict || {}).supersedes; if (s) superseded.add(s);
  });
  const item = (o, cls) => {
    const rv = o.reviewer, v = o.verdict || {};
    const old = superseded.has(o._file);
    return `<div class="revealed ${cls}${old ? ' old' : ''}"><b>${esc(rv.id)}</b> ` +
      `<span class="pill">${esc(rv.kind)}${rv.version ? ' ' + esc(rv.version) : ''}</span> ` +
      `<span class="muted">${esc((o.created_at || '').slice(0, 16).replace('T', ' '))}</span> ` +
      (old ? '<span class="pill">superseded</span> ' : '') +
      `${v.label ? `<code>${esc(v.label)}</code> (${esc(v.confidence || '')})` : '<i>comment only</i>'}` +
      `${o.comment ? `<div class="muted">${esc(o.comment)}</div>` : ''}</div>`;
  };
  let html = '';
  if (mine && mine.length)
    html += '<div class="muted" style="margin-top:8px">Your reviews</div>' +
            mine.map(o => item(o, 'mine')).join('');
  if (others && others.length)
    html += '<div class="muted" style="margin-top:8px">Other reviews</div>' +
            others.map(o => item(o, '')).join('');
  $('reveal').innerHTML = html;
}

async function submitReview() {
  if (!state.cur) return;
  const body = {
    sha: state.cur.subject.sha1_git,
    reviewer: $('reviewer').value,
    label: state.label,
    confidence: document.querySelector('input[name=conf]:checked').value,
    comment: $('comment').value,
  };
  const resp = await fetch('api/review', { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const r = await resp.json();
  if (!resp.ok) { toast('✗ ' + r.error, 5000); return; }
  state.session++; $('session').textContent = 'session: ' + state.session;
  toast('✓ saved ' + r.file.split('/').pop());
  state.cur.mine.push(r.review);
  if (r.others && r.others.length) { renderHistory(state.cur.mine, r.others); }
  else nextSample();
}

function nextSample() {
  if (state.standalone) {           // came from browse → back to the queue
    state.standalone = null;
    if (state.queue.length) loadSample(); else toggleBrowse(true);
    return;
  }
  if (state.idx + 1 < state.queue.length) { state.idx++; loadSample(); }
  else { toast('end of queue — reload to refresh'); }
}

async function toggleBrowse(force) {
  const b = $('browse');
  const show = force !== undefined ? force : b.style.display !== 'block';
  b.style.display = show ? 'block' : 'none';
  document.querySelector('main').style.display = show ? 'none' : 'flex';
  if (show) {
    const r = await (await fetch('api/samples?reviewer=' +
      encodeURIComponent($('reviewer').value))).json();
    state.browseRows = r.rows; renderBrowse();
    $('bfilter').focus();
  }
}

function renderBrowse() {
  const f = $('bfilter').value.toLowerCase();
  const st = $('bstatus').value;
  const rows = state.browseRows.filter(r =>
    (!f || r.filename.toLowerCase().includes(f) || r.ext.includes(f) ||
     r.slots.join(',').toLowerCase().includes(f) ||
     (r.predicted_pl_id || '').includes(f)) &&
    (st === 'all' ? true :
     st === 'unreviewed' ? r.n_human === 0 :
     st === 'mine' ? r.reviewed_by_me : !r.reviewed_by_me));
  $('bcount').textContent = `${rows.length} / ${state.browseRows.length}`;
  $('btable').innerHTML =
    '<tr><th>file</th><th>ext</th><th>bytes</th><th>slot</th>' +
    '<th>predicted</th><th>👤</th><th>🤖</th><th>my label</th></tr>' +
    rows.map(r =>
      `<tr data-sha="${r.sha1_git}" class="${r.reviewed_by_me ? 'done' : ''}">` +
      `<td><code>${esc(r.filename)}</code></td><td>${esc(r.ext)}</td>` +
      `<td>${r.length}</td><td class="muted">${esc(r.slots.join(', '))}</td>` +
      `<td>${esc(r.predicted_pl_id || '—')}</td>` +
      `<td>${r.n_human || ''}</td><td>${r.n_machine || ''}</td>` +
      `<td>${r.my_label ? '<code>' + esc(r.my_label) + '</code>' : ''}</td></tr>`
    ).join('');
  document.querySelectorAll('#btable tr[data-sha]').forEach(tr =>
    tr.addEventListener('click', () => { toggleBrowse(false); loadSample(tr.dataset.sha); }));
}
$('browsebtn').addEventListener('click', () => toggleBrowse());
$('bfilter').addEventListener('input', renderBrowse);
$('bstatus').addEventListener('change', renderBrowse);

document.addEventListener('keydown', e => {
  const typing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName);
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { submitReview(); return; }
  if (typing) return;
  if (e.key >= '1' && e.key <= '9') {
    const b = document.querySelectorAll('#suggs .sugg:not(.predicted)')[+e.key - 1];
    if (b) setLabel(b.dataset.label);
  }
  if (e.key === 's') nextSample();
  if (e.key === 'b') toggleBrowse();
});
$('reload').addEventListener('click', loadQueue);
init();
</script>
</body></html>
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def autocommit(reviews_dir: Path) -> None:
    rel = str(reviews_dir.relative_to(ROOT)) if reviews_dir.is_relative_to(ROOT) else None
    if rel is None:
        print("(autocommit skipped: reviews dir outside the repo)")
        return
    status = subprocess.run(["git", "status", "--porcelain", rel],
                            capture_output=True, text=True, cwd=ROOT).stdout
    n = sum(1 for line in status.splitlines() if line.strip())
    if not n:
        print("(autocommit: nothing new under reviews/)")
        return
    digest = hashlib.sha256((ROOT / "data" / "pl_list.txt").read_bytes()).hexdigest()[:8]
    subprocess.run(["git", "add", rel], cwd=ROOT, check=True)
    msg = (f"reviews: session of {n} file(s) via review_server\n\n"
           f"List-Digest: {digest}")
    subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)
    print(f"committed {n} review file(s).")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default="127.0.0.1",
                   help="bind address (0.0.0.0 for LAN sessions; no auth!)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--as", dest="reviewer", default=None,
                   help="default reviewer id (default: git config user.name)")
    p.add_argument("--samples-dir", default=str(store.SAMPLES_DIR))
    p.add_argument("--reviews-dir", default=str(store.REVIEWS_DIR))
    p.add_argument("--autocommit", action="store_true",
                   help="git-commit new review files on exit (Ctrl-C)")
    p.add_argument("--open", action="store_true", help="open a browser tab")
    args = p.parse_args()

    app = App(samples_dir=Path(args.samples_dir),
              reviews_dir=Path(args.reviews_dir),
              default_reviewer=store.slugify(args.reviewer)
              if args.reviewer else store.default_reviewer_id())
    Handler.app = app

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/"
    print(f"{len(app.samples)} samples · {len(app.pl_index)} PLs in taxonomy")
    print(f"reviewer: {app.default_reviewer} · reviews → {app.reviews_dir}")
    print(f"serving {url}  (Ctrl-C to stop)")
    if args.open:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye.")
        if args.autocommit:
            autocommit(Path(args.reviews_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
