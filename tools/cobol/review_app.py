"""Unified review app over ALL the labelled COBOL-in-SWH data.

One pane over every label a content has received:
  - **judge**        — the LLM verdict (cobol-judge/2): is-COBOL + dialect/
                       domain/standard/format/maturity  (from `reports/`)
  - **reclassifier** — the deterministic content label (`reclassify.py`;
                       from the 1K sweep / eval, or computed from cache)
  - **oracle**       — the LLM is-COBOL used to validate the reclassifier
                       (`reclassify_oracle_cache.json`)
  - **division-gate**— the cheap `n_divisions >= 2` baseline
  - **human**        — your own reviews (`reviews_cobol/`, shared with
                       `review_server.py`)

It surfaces where the labels disagree (the interesting cases to review) and
lets you record human ground truth. Stdlib only, read from the local cache.

Run:  python3 -m tools.cobol.review_app          # http://127.0.0.1:8766
"""

from __future__ import annotations

import argparse
import getpass
import html
import json
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import origins as orig_mod
from . import reclassify as rc
from . import taxonomy as tax
from .common import CACHE_DIR, STUDY_DIR
from .reclassify import COBOL_LABELS
from .review_server import REVIEWS_DIR, SCHEMA, reviews_for, save_review
from .run_study import canonical_view

REPORTS = STUDY_DIR / "reports"
WORKLIST_DATASET = {
    "worklist.csv": "pilot", "worklist_scaled.csv": "main",
    "worklist_lc.csv": "lc", "worklist_1k.csv": "1k",
}
LABEL_SOURCES = ["judge", "reclassifier", "oracle", "division-gate", "human"]


# --------------------------------------------------------------------------- #
# Build the unified label index (once, at startup)
# --------------------------------------------------------------------------- #
def _read_jsonl(p: Path):
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield json.loads(line)


def build_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}

    def rec(sha: str) -> dict:
        return idx.setdefault(sha, {
            "sha": sha, "filenames": set(), "datasets": set(),
            "cached": (CACHE_DIR / f"{sha}.bin").exists(),
            "length": None, "n_divisions": None, "code_lines": None,
            "judge": None, "reclass": None, "oracle": None, "gate": None,
            "provenance": None,
        })

    # 1. study reports -> indicators + judge verdict
    for p in REPORTS.glob("*.json"):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        sha = r["sample"]["sha1_git"]
        d = rec(sha)
        if r["sample"].get("filename"):
            d["filenames"].add(r["sample"]["filename"])
        ind = r.get("indicators", {})
        d["length"] = r.get("content", {}).get("length", d["length"])
        d["n_divisions"] = ind.get("n_divisions", d["n_divisions"])
        d["code_lines"] = ind.get("code_lines", d["code_lines"])
        if d["n_divisions"] is not None:
            d["gate"] = d["n_divisions"] >= 2
        j = r.get("judge")
        if isinstance(j, dict) and j.get("verdict"):
            cv = canonical_view(j["verdict"])
            if cv:
                d["judge"] = {
                    "is_cobol": cv["cobol_confirmed"] == "true",
                    "family": cv["family"], "domain": cv["domain"],
                    "standard": cv["standard"], "source_format": cv["source_format"],
                    "maturity": cv["maturity"],
                    "summary": (j["verdict"].get("purpose") or {}).get("summary", ""),
                }

    # 2. reclassifier labels (1K sweep + eval), then compute for the gap
    stored_reclass: dict[str, dict] = {}
    for row in _read_jsonl(STUDY_DIR / "corpus_estimate.jsonl"):
        stored_reclass[row["sha1_git"]] = {"label": row["label"], "is_cobol": row["is_cobol"]}
        d = rec(row["sha1_git"]); d["filenames"].add(row.get("name", "")); d["datasets"].add("1k")
    evalf = STUDY_DIR / "reclassify_eval.json"
    if evalf.exists():
        for row in json.loads(evalf.read_text())["rows"]:
            sha = row["sha1_git"]; d = rec(sha)
            d["filenames"].add(row.get("filename", ""))
            d["datasets"].add(f"eval:{row['group']}")
            stored_reclass.setdefault(sha, {"label": row["heuristic_label"],
                                            "is_cobol": row["heuristic_is_cobol"]})
            d["oracle"] = {"is_cobol": row["oracle_is_cobol"],
                           "not_cobol_label": row.get("oracle_not_cobol_label", "")}
            if d["n_divisions"] is None:
                d["n_divisions"] = row.get("n_divisions")
                d["gate"] = row.get("gate_is_cobol")

    # 3. oracle cache (is-COBOL truth used in the eval)
    oc = STUDY_DIR / "reclassify_oracle_cache.json"
    if oc.exists():
        for sha, v in json.loads(oc.read_text()).items():
            d = rec(sha)
            if d["oracle"] is None:
                d["oracle"] = {"is_cobol": v.get("is_cobol"),
                               "not_cobol_label": v.get("not_cobol_label", "")}

    # 4. worklists -> dataset membership + filenames
    for wl, ds in WORKLIST_DATASET.items():
        p = STUDY_DIR / wl
        if not p.exists():
            continue
        import csv
        for row in csv.DictReader(p.open(encoding="utf-8")):
            d = rec(row["sha1_git"]); d["datasets"].add(ds)
            if row.get("name"):
                d["filenames"].add(row["name"])

    # 5. reclassifier label: stored where available, else compute from cache
    for sha, d in idx.items():
        if sha in stored_reclass:
            d["reclass"] = stored_reclass[sha]
        elif d["cached"]:
            raw = (CACHE_DIR / f"{sha}.bin").read_bytes()
            fn = next(iter(d["filenames"]), "")
            res = rc.classify(fn, raw)
            d["reclass"] = {"label": res["label"], "is_cobol": res["is_cobol"]}

    # 6. origins — graph CSV (cbl_file+origin.csv) + github-match, merged
    for sha, d in idx.items():
        prov = orig_mod.origin_for(sha)
        if prov:
            d["provenance"] = prov
    return idx


def rep_name(d: dict) -> str:
    for n in sorted(d["filenames"]):
        if n:
            return n
    return d["sha"][:14]


def votes(d: dict, human: dict | None) -> dict:
    """is-COBOL vote per available source."""
    v = {}
    if d.get("judge"):
        v["judge"] = d["judge"]["is_cobol"]
    if d.get("reclass"):
        v["reclassifier"] = d["reclass"]["is_cobol"]
    if d.get("oracle") and d["oracle"].get("is_cobol") is not None:
        v["oracle"] = d["oracle"]["is_cobol"]
    if d.get("gate") is not None:
        v["division-gate"] = d["gate"]
    if human and human.get("is_cobol") in ("yes", "no"):
        v["human"] = human["is_cobol"] == "yes"
    return v


def is_disagreement(d: dict) -> bool:
    vs = list(votes(d, reviews_for(d["sha"])[-1]["human"] if reviews_for(d["sha"]) else None).values())
    return len(set(vs)) > 1


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #
CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a}
header{background:#0b3d61;color:#fff;padding:10px 18px;position:sticky;top:0;z-index:5}
header a{color:#cde4ff;text-decoration:none;margin-right:14px}
main{padding:16px 18px;max-width:1240px}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #e6e6e6;padding:5px 8px;text-align:left;font-size:13px}
tr:hover{background:#f6f9fc}
a{color:#0b5cad}
.tag{display:inline-block;background:#eef3f8;border-radius:3px;padding:1px 6px;font-size:12px;margin:1px}
.ds{background:#eae6f8}
.yes{color:#127a2e;font-weight:600}.no{color:#b3261e;font-weight:600}
.warn{background:#fff4e5}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0}
.card{background:#fafbfc;border:1px solid #e3e3e3;border-radius:8px;padding:12px 14px;min-width:150px}
.card b{font-size:22px;display:block}
.bar{height:14px;background:#0b3d61;border-radius:2px;display:inline-block;vertical-align:middle}
.bar.no{background:#d1731f}
.grid{display:grid;grid-template-columns:1fr 420px;gap:18px}
pre.code{background:#0d1117;color:#d6dee8;padding:12px;border-radius:6px;overflow:auto;
  max-height:66vh;font:12px/1.45 SFMono-Regular,Consolas,monospace;white-space:pre}
.panel{background:#fafbfc;border:1px solid #e3e3e3;border-radius:6px;padding:12px;margin-bottom:14px}
.panel h3{margin:0 0 8px;font-size:12px;text-transform:uppercase;color:#555;letter-spacing:.04em}
label{display:block;margin:8px 0 2px;font-size:12px;color:#444;font-weight:600}
select,input[type=text],textarea{width:100%;padding:5px;border:1px solid #ccc;border-radius:4px;font:inherit;box-sizing:border-box}
button{background:#0b3d61;color:#fff;border:0;border-radius:5px;padding:9px 16px;font-size:14px;cursor:pointer;margin-top:12px}
.muted{color:#888;font-size:12px}
"""


def esc(s):
    return html.escape(str(s if s is not None else ""))


def opts(values, cur=""):
    out = ['<option value="">—</option>']
    for v in values:
        out.append(f'<option{" selected" if v==cur else ""}>{esc(v)}</option>')
    return "".join(out)


def yn(b):
    if b is None:
        return '<span class=muted>—</span>'
    return '<span class=yes>COBOL</span>' if b else '<span class=no>non</span>'


def page(title, body):
    return (f"<!doctype html><meta charset=utf-8><title>{esc(title)}</title>"
            f"<style>{CSS}</style>"
            f"<header><a href='/'>◧ COBOL labels</a>"
            f"<a href='/list'>browse</a>"
            f"<a href='/list?flag=disagree'>disagreements</a>"
            f"<a href='/list?flag=unreviewed'>unreviewed</a>"
            f"<a href='/list?flag=hasorigin'>with origin</a>"
            f"<span class=muted style='color:#cde4ff'>{esc(title)}</span></header>"
            f"<main>{body}</main>").encode("utf-8")


class App:
    def __init__(self):
        print("building label index …")
        self.idx = build_index()
        print(f"  {len(self.idx)} unique labelled contents")

    # ---- pages ----
    def dashboard(self):
        idx = self.idx
        n = len(idx)
        cached = sum(d["cached"] for d in idx.values())
        reviewed = sum(1 for sha in idx if reviews_for(sha))
        ds = Counter()
        for d in idx.values():
            for x in d["datasets"]:
                ds[x] += 1
        rl = Counter(d["reclass"]["label"] for d in idx.values() if d["reclass"])
        # agreement judge vs reclassifier / reclassifier vs oracle (is-COBOL)
        def pair(a, b):
            ag = di = 0
            for d in idx.values():
                va = d.get(a); vb = d.get(b)
                if not va or not vb:
                    continue
                xa = va["is_cobol"]; xb = vb["is_cobol"]
                if xb is None:
                    continue
                ag += xa == xb; di += xa != xb
            return ag, di
        jr_a, jr_d = pair("judge", "reclass")
        ro_a, ro_d = pair("reclass", "oracle")

        prov = sum(1 for d in idx.values() if d.get("provenance"))
        cards = "".join(
            f"<div class=card><b>{v}</b><span class=muted>{k}</span></div>"
            for k, v in [("labelled contents", n), ("cached bytes", cached),
                         ("human-reviewed", reviewed),
                         ("recovered origins", prov)])
        dsrows = "".join(
            f"<a class='tag ds' href='/list?dataset={esc(k)}'>{esc(k)}: {v}</a> "
            for k, v in ds.most_common())
        maxrl = max(rl.values()) if rl else 1
        rlrows = "".join(
            f"<tr><td><a href='/list?label={esc(k)}'>{esc(k)}</a></td>"
            f"<td>{v}</td><td><span class='bar{' no' if k not in COBOL_LABELS else ''}' "
            f"style='width:{int(160*v/maxrl)}px'></span></td></tr>"
            for k, v in rl.most_common())
        agree = (
            f"<div class=panel><h3>is-COBOL agreement</h3>"
            f"<p>judge vs reclassifier: <b>{jr_a}</b> agree · "
            f"<a href='/list?flag=disagree'><b>{jr_d}</b> disagree</a></p>"
            f"<p>reclassifier vs LLM-oracle: <b>{ro_a}</b> agree · "
            f"<b>{ro_d}</b> disagree</p></div>")
        legend = ("<p class=muted style='margin:6px 0'><b>is-COBOL label sources</b> — "
                  "<b>judge</b>: the LLM verdict · "
                  "<b>reclassifier</b>: deterministic content rules (reclassify.py) · "
                  "<b>oracle</b>: LLM is-COBOL used to validate the reclassifier · "
                  "<b>division-gate</b>: cheap baseline = has ≥2 COBOL divisions · "
                  "<b>human</b>: your reviews. A file is ⚠ when its available "
                  "is-COBOL votes disagree.</p>")
        return page("dashboard",
            f"<div class=cards>{cards}</div>{legend}"
            f"<div class=panel><h3>datasets</h3>{dsrows}</div>"
            f"{agree}"
            f"<div class=panel><h3>reclassifier label distribution</h3>"
            f"<table>{rlrows}</table></div>")

    def _match(self, d, f):
        if f.get("dataset") and f["dataset"] not in d["datasets"]:
            return False
        if f.get("label") and (not d["reclass"] or d["reclass"]["label"] != f["label"]):
            return False
        if f.get("q") and f["q"].lower() not in rep_name(d).lower():
            return False
        flag = f.get("flag")
        if flag == "disagree" and not is_disagreement(d):
            return False
        if flag == "reviewed" and not reviews_for(d["sha"]):
            return False
        if flag == "unreviewed" and reviews_for(d["sha"]):
            return False
        if flag == "noncobol" and (d["reclass"] and d["reclass"]["is_cobol"]):
            return False
        if flag == "hasorigin" and not d.get("provenance"):
            return False
        return True

    def listing(self, f):
        rows = [d for d in self.idx.values() if self._match(d, f)]
        rows.sort(key=rep_name)
        shown = rows[:600]
        trs = []
        for d in shown:
            hr = reviews_for(d["sha"])
            human = hr[-1]["human"] if hr else None
            dis = is_disagreement(d)
            j = d.get("judge"); rcl = d.get("reclass"); orc = d.get("oracle")
            trs.append(
                f"<tr class='{'warn' if dis else ''}'>"
                f"<td>{'✓' if hr else ''}</td>"
                f"<td><a href='/file/{d['sha']}'>{esc(rep_name(d))[:40]}</a></td>"
                f"<td>{''.join(f'<span class=\"tag ds\">{esc(x)}</span>' for x in sorted(d['datasets']))}</td>"
                f"<td>{yn(j['is_cobol']) if j else '—'}"
                f"{(' '+esc(j['domain'])) if j and j.get('domain') else ''}</td>"
                f"<td>{esc(rcl['label']) if rcl else '—'}</td>"
                f"<td>{yn(orc['is_cobol']) if orc else '—'}</td>"
                f"<td>{yn(d['gate'])}</td>"
                f"<td>{'⚠' if dis else ''}</td></tr>")
        head = (f"<p class=muted>{len(rows)} match"
                f"{' (showing 600)' if len(rows) > 600 else ''} · "
                f"filters: {esc(json.dumps({k:v for k,v in f.items() if v}))}</p>"
                f"<form class=muted style='margin:6px 0'>"
                f"<input name=q value='{esc(f.get('q',''))}' placeholder='filename' style='max-width:260px'>"
                f"<input type=hidden name=flag value='{esc(f.get('flag',''))}'>"
                f"<button>search</button></form>")
        return page("browse", head +
            "<table><tr><th>rev</th><th>file</th><th>datasets</th><th>judge</th>"
            "<th>reclassifier</th><th>oracle</th><th>division-gate</th><th></th></tr>"
            + "".join(trs) + "</table>")

    def detail(self, sha):
        d = self.idx.get(sha)
        if not d:
            return page("404", "<p>unknown content</p>")
        code = "(bytes not cached)"
        if d["cached"]:
            raw = (CACHE_DIR / f"{sha}.bin").read_bytes()
            code = raw[:60000].decode("latin-1", "replace")
        hr = reviews_for(sha)
        human = hr[-1]["human"] if hr else {}
        vs = votes(d, human or None)
        maj = None
        if vs:
            c = Counter(vs.values()); maj = c.most_common(1)[0][0]

        def lrow(name, is_cobol, detail):
            cls = "warn" if (is_cobol is not None and maj is not None and is_cobol != maj) else ""
            return (f"<tr class='{cls}'><td>{esc(name)}</td><td>{yn(is_cobol)}</td>"
                    f"<td class=muted>{esc(detail)}</td></tr>")
        j = d.get("judge"); rcl = d.get("reclass"); orc = d.get("oracle")
        lbl_rows = ""
        if j:
            lbl_rows += lrow("judge (LLM)", j["is_cobol"],
                             f"{j['family']} · {j['domain']} · {j['standard']} · {j['maturity']}")
        if rcl:
            lbl_rows += lrow("reclassifier", rcl["is_cobol"], rcl["label"])
        if orc:
            lbl_rows += lrow("LLM oracle", orc["is_cobol"], orc.get("not_cobol_label", ""))
        lbl_rows += lrow("division-gate", d["gate"], f"n_divisions={d['n_divisions']}")
        if human:
            lbl_rows += lrow("human", human.get("is_cobol") == "yes"
                             if human.get("is_cobol") in ("yes", "no") else None,
                             f"{human.get('dialect_family','')} · {human.get('domain','')}")

        summ = f"<p class=muted>{esc(j['summary'])}</p>" if j and j.get("summary") else ""
        form = f"""
        <div class=panel><h3>your review</h3><form id=f>
          <input type=hidden name=sha1_git value="{esc(sha)}">
          <input type=hidden name=filename value="{esc(rep_name(d))}">
          <label>Is this COBOL?</label>
          <select name=is_cobol>{opts(['yes','no','unsure'], human.get('is_cobol',''))}</select>
          <label>Dialect family</label>
          <select name=dialect_family>{opts(tax.DIALECT_FAMILIES, human.get('dialect_family',''))}</select>
          <label>Domain</label>
          <select name=domain>{opts(tax.DOMAINS, human.get('domain',''))}</select>
          <label>Source format</label>
          <select name=source_format>{opts(tax.SOURCE_FORMATS, human.get('source_format',''))}</select>
          <label>Origin URL</label>
          <input name=origin_url value="{esc(human.get('origin_url',''))}" placeholder="https://…">
          <label>Notes</label><textarea name=notes rows=3>{esc(human.get('notes',''))}</textarea>
          <button type=button onclick=save()>Save review</button> <span id=msg class=muted></span>
        </form></div>
        <script>async function save(){{const fd=new FormData(document.getElementById('f'));
          const r=await fetch('/api/review',{{method:'POST',headers:{{'Content-Type':'application/json'}},
          body:JSON.stringify(Object.fromEntries(fd.entries()))}});const j=await r.json();
          document.getElementById('msg').textContent=r.ok?' saved ✓':(' err: '+j.error);}}</script>"""
        left = (f"<h2 style='margin:4px 0'>{esc(rep_name(d))}</h2>"
                f"<p class=muted>swh:1:cnt:{esc(sha)} · {esc(d['length'])} bytes · "
                f"{''.join(f'<span class=\"tag ds\">{esc(x)}</span>' for x in sorted(d['datasets']))} · "
                f"<a target=_blank href='https://archive.softwareheritage.org/swh:1:cnt:{esc(sha)}/'>SWH ↗</a></p>"
                f"<pre class=code>{esc(code)}</pre>")
        prov = d.get("provenance")
        prov_html = ""
        if prov:
            g, h = prov.get("graph"), prov.get("github")
            rows = ""
            if g:
                rows += (f"<div>graph</div><div>"
                         f"<a target=_blank href='{esc(g['origin'])}'>{esc(g['origin'])}</a> "
                         f"<span class=tag>{esc(g.get('forge',''))}</span><br>"
                         f"<span class=muted>{esc(g.get('path') or '')} · {esc(g.get('branch') or '')} · {esc(g.get('timestamp') or '')}</span> "
                         f"<a class=muted target=_blank href='{esc(g.get('swh_browse_url',''))}'>SWH↗</a></div>")
            if h:
                anc = f" @ <code>{esc(h['anchor'])}</code>" if h.get("anchor") else ""
                note = "" if prov.get("agree") is not False else " <span class=muted>(≠ graph — same bytes, another repo)</span>"
                rows += (f"<div>github</div><div>"
                         f"<a target=_blank href='{esc(h['origin'])}'>{esc(h['origin'])}</a>{anc}{note}</div>")
            prov_html = (f"<div class=panel judgebox><h3>origin</h3>"
                         f"<div class=kv>{rows}</div></div>")
        right = (f"{prov_html}"
                 f"<div class=panel><h3>labels ({len(vs)} is-COBOL votes"
                 f"{' · ⚠ disagree' if len(set(vs.values()))>1 else ' · unanimous'})</h3>"
                 f"<table>{lbl_rows}</table>{summ}</div>{form}")
        return page(rep_name(d), f"<div class=grid><div>{left}</div><div>{right}</div></div>")


class Handler(BaseHTTPRequestHandler):
    app: App = None
    reviewer_id = "anon"

    def log_message(self, *a):
        pass

    def _send(self, body, status=200, ctype="text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == "/":
            self._send(self.app.dashboard())
        elif u.path == "/list":
            self._send(self.app.listing(q))
        elif u.path.startswith("/file/"):
            self._send(self.app.detail(u.path.split("/file/", 1)[1]))
        else:
            self._send(page("404", "not found"), 404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/review":
            self._send(b'{"error":"unknown"}', 404, "application/json"); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as e:
            self._send(json.dumps({"error": str(e)}).encode(), 400, "application/json"); return
        sha = (data.get("sha1_git") or "").strip()
        if len(sha) != 40:
            self._send(b'{"error":"bad sha"}', 400, "application/json"); return
        record = {
            "schema": SCHEMA,
            "subject": {"sha1_git": sha, "swhid": f"swh:1:cnt:{sha}",
                        "filename": data.get("filename", "")},
            "reviewer": {"kind": "human", "id": self.reviewer_id},
            "human": {k: (data.get(k, "") or "").strip() if isinstance(data.get(k, ""), str)
                      else data.get(k, "")
                      for k in ("is_cobol", "dialect_family", "domain",
                                "source_format", "origin_url", "notes")},
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time())),
        }
        try:
            p = save_review(record)
        except Exception as e:
            self._send(json.dumps({"error": str(e)}).encode(), 500, "application/json"); return
        self._send(json.dumps({"ok": True, "path": str(p.name)}).encode(), 200, "application/json")


def main():
    ap = argparse.ArgumentParser(description="Unified COBOL label-review app.")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--reviewer", default=None)
    args = ap.parse_args()
    Handler.reviewer_id = args.reviewer or getpass.getuser() or "anon"
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    Handler.app = App()
    print(f"COBOL review app: http://{args.host}:{args.port}/  (reviewer={Handler.reviewer_id})")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
