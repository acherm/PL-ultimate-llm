"""Review app for the `.m` study — every labeller side by side, plus a blind audit.

What is new compared with the cobol/fsf/rpgle review apps:
  * **all labellers in one table** — the two LLM judges, our reclassifier,
    Linguist's heuristics, Pygments, and SWH Synid (two configurations) — with
    each answer marked against the others, so disagreements are visible at a
    glance rather than only "judge vs our rule";
  * **a blind audit queue** (`/audit`): a stratified random sample with
    inverse-probability weights (`tools/m/audit.py`). In blind mode the
    machine labels stay hidden until the reviewer has saved their own — the
    human equivalent of the judge-anchoring ablation. `audit --score` then
    turns the reviews into weighted accuracies for every labeller;
  * provenance at a glance: forge link at the archived branch, the qualified
    SWHID, the SWH browse context, and three population signals — contents in
    the repo, versions of this path, and how many repos carry this filename;
  * group rules over an origin, a filename regex or a path regex.

Run:  python3 -m tools.m.review_app            # http://127.0.0.1:8769
Reviews → reviews_m/<sha>/<UTC>--<reviewer>--<h8>.json ; rules → reviews_m/_rules.jsonl
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import html
import json
import re
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

from tools.cobol.common import CACHE_DIR
from tools.m import audit as audit_mod
from tools.m import taxonomy as tax
from tools.m.analysis import ABSTAIN, COARSE, coarse
from tools.m.data import (LABELLERS, REVIEWS, RULES_FILE, STUDY, load, load_rules,
                          reviews_for, rule_for)

SWH = "https://archive.softwareheritage.org"
SCHEMA = "m-review/1"
RULE_LABELS = tax.LANGUAGES
SHOWN = ["judge", "judge2", "ours", "linguist", "pygments", "synid", "synid_nc"]
FLAGS = {
    "j1_ne_j2": "the two LLM judges disagree",
    "j1_ne_ours": "judge ≠ our reclassifier",
    "pyg_wrong": "Pygments ≠ judge",
    "synid_text": "Synid answers Text / unresolved",
    "ling_abstain": "Linguist heuristics abstain",
    "octave": "Octave: judge vs lexical markers disagree",
    "tail": "neither Objective-C nor MATLAB (judge)",
    "not_hand": "not hand-written (judge)",
    "reviewed": "human-reviewed", "unreviewed": "not yet reviewed", "ruled": "covered by a group rule",
}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def read_code(sha, limit=80000):
    p = CACHE_DIR / f"{sha}.bin"
    if not p.exists():
        return "(bytes not cached)"
    b = p.read_bytes()
    t = b[:limit].decode("utf-8", "replace")
    return t + (f"\n… [{len(b) - limit} more bytes]" if len(b) > limit else "")


def octave_lexical(r):
    i = r.ind
    return (i.get("oct_block_ends", 0) + i.get("oct_hash_comments", 0) + i.get("oct_printf", 0)
            + i.get("oct_ne", 0) + int(bool(i.get("oct_script_marker")))) > 0


def flag_ok(r, flag) -> bool:
    j, j2 = r.lang("judge"), r.lang("judge2")
    if flag == "j1_ne_j2":
        return bool(j and j2) and coarse(j) != coarse(j2)
    if flag == "j1_ne_ours":
        return bool(j) and r.labels is not None and coarse(j) != coarse(r.lang("ours"))
    if flag == "pyg_wrong":
        return bool(j) and r.labels is not None and coarse(j) != coarse(r.lang("pygments"))
    if flag == "synid_text":
        return r.lang("synid") in ("unknown", "unresolved")
    if flag == "ling_abstain":
        return r.labels is not None and r.lang("linguist") in ABSTAIN
    if flag == "octave":
        return j in ("matlab", "octave") and (j == "octave") != octave_lexical(r)
    if flag == "tail":
        return bool(j) and coarse(j) not in ("objective-c", "matlab-family")
    if flag == "not_hand":
        return bool(r.v("judge")) and r.v("judge").get("provenance_kind") != "hand-written"
    if flag == "reviewed":
        return bool(r.reviews)
    if flag == "unreviewed":
        return not r.reviews
    if flag == "ruled":
        return r.rule is not None
    return True


def forge_link(row):
    o, br, p = row.get("origin") or "", row.get("branch") or "", (row.get("path") or "").lstrip("/")
    b = br.replace("refs/heads/", "").replace("refs/tags/", "")
    if not (o and b and p):
        return o
    if "github.com" in o:
        return f"{o}/blob/{quote(b)}/{quote(p)}"
    if "gitlab" in o:
        return f"{o.removesuffix('.git')}/-/blob/{quote(b)}/{quote(p)}"
    if "bitbucket.org" in o:
        return f"{o}/src/{quote(b)}/{quote(p)}"
    return o


def swh_links(row):
    sha = row["sha1_git"]
    q = {k: v for k, v in (("branch", row.get("branch")), ("origin_url", row.get("origin")),
                           ("path", row.get("path")), ("timestamp", row.get("ts"))) if v}
    browse = f"{SWH}/browse/origin/directory/?{urlencode(q)}" if row.get("origin") else ""
    swhid = f"swh:1:cnt:{sha}" + (f";origin={row['origin']};path={row.get('path', '')}" if row.get("origin") else "")
    return browse, f"{SWH}/{swhid}/", swhid


CSS = """
:root{--ink:#16181d;--mut:#6b7280;--line:#e5e7eb;--bg:#fff;--soft:#f7f7fb;--acc:#3730a3;--acc2:#e0e7ff;
--ok:#15803d;--bad:#b91c1c;--warn:#b45309}
*{box-sizing:border-box}
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:var(--ink);background:var(--bg)}
header{background:var(--acc);color:#fff;padding:9px 18px;position:sticky;top:0;z-index:5;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header a{color:#e0e7ff;text-decoration:none} header b{margin-right:8px}
main{padding:16px 18px;max-width:1500px}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid var(--line);padding:4px 7px;text-align:left;font-size:13px;vertical-align:top}
th{font-weight:600;color:#374151;background:var(--soft)}
tr:hover td{background:#fafaff}
a{color:var(--acc)}
.tag{display:inline-block;background:var(--acc2);border-radius:3px;padding:0 6px;font-size:12px;margin:1px;white-space:nowrap}
.tag.bad{background:#fee2e2;color:var(--bad)} .tag.ok{background:#dcfce7;color:var(--ok)} .tag.warn{background:#fef3c7;color:var(--warn)}
.cards{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 14px}
.card{background:var(--soft);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:130px}
.card b{font-size:22px;display:block}
.bar{height:12px;background:var(--acc);border-radius:2px;display:inline-block;vertical-align:middle}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 470px;gap:16px}
@media (max-width:1100px){.grid{grid-template-columns:1fr}}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:900px){.two{grid-template-columns:1fr}}
pre.code{background:#0f1117;color:#d6dee8;padding:10px 0;border-radius:6px;overflow:auto;max-height:78vh;
  font:12px/1.45 SFMono-Regular,Menlo,Consolas,monospace;margin:0}
pre.code span.ln{display:inline-block;width:46px;color:#5b6475;text-align:right;padding-right:10px;user-select:none}
.panel{background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin-bottom:12px}
.panel h3{margin:0 0 6px;font-size:11px;text-transform:uppercase;color:var(--mut);letter-spacing:.05em}
.kv{display:grid;grid-template-columns:150px 1fr;gap:1px 8px;font-size:13px}
.kv div:nth-child(odd){color:var(--mut)}
.kv div{overflow-wrap:anywhere;min-width:0}
td{overflow-wrap:anywhere}
label{display:block;margin:7px 0 2px;font-size:12px;color:#374151;font-weight:600}
select,input[type=text],textarea{width:100%;padding:5px;border:1px solid #cbd5e1;border-radius:4px;font:inherit}
button{background:var(--acc);color:#fff;border:0;border-radius:5px;padding:8px 14px;cursor:pointer;margin-top:10px}
button.sec{background:#fff;color:var(--acc);border:1px solid var(--acc)}
.muted{color:var(--mut);font-size:12px}
.hidden{display:none}
.filters a{margin-right:8px;font-size:12px}
.prog{height:10px;background:var(--line);border-radius:5px;overflow:hidden}
.prog>div{height:10px;background:var(--ok)}
"""


def page(title, body):
    nav = ("<b>.m labels</b><a href='/'>dashboard</a><a href='/list'>browse</a>"
           "<a href='/audit'>audit queue</a><a href='/audit/next'>▶ next audit item</a>"
           "<a href='/list?flag=j1_ne_j2'>judges disagree</a><a href='/list?flag=tail'>tail</a>"
           "<a href='/rules'>rules</a>")
    return (f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{esc(title)} · .m review</title><style>{CSS}</style>"
            f"<header>{nav}</header><main>{body}</main>").encode("utf-8")


def opts(values, cur=""):
    return "".join(['<option value="">—</option>'] +
                   [f'<option{" selected" if v == cur else ""}>{esc(v)}</option>' for v in values])


class App:
    def __init__(self):
        self.reload()

    def reload(self):
        self.recs = load()
        self.queue = audit_mod.queue()
        self.qset = {d["sha1_git"]: d for d in self.queue}
        try:
            self.npop = json.loads((STUDY / "name_popularity.json").read_text())
        except Exception:
            self.npop = {}
        print(f"loaded {len(self.recs)} contents; {sum(1 for r in self.recs.values() if r.v('judge'))} judged; "
              f"audit queue {len(self.queue)}")

    def refresh_one(self, sha):
        r = self.recs.get(sha)
        if r:
            r.reviews = reviews_for(sha)

    def refresh_rules(self):
        rules = load_rules()
        for r in self.recs.values():
            r.rule = rule_for(r.row, rules)

    # ------------------------------------------------------------------ dashboard
    def dashboard(self):
        recs = list(self.recs.values())
        judged = [r for r in recs if r.v("judge")]
        reviewed = sum(1 for r in recs if r.reviews)
        ruled = sum(1 for r in recs if r.rule)
        q_done = sum(1 for d in self.queue if self.recs[d["sha1_git"]].reviews)
        cards = "".join(f"<div class=card><b>{v}</b><span class=muted>{k}</span></div>" for k, v in [
            ("contents in sample", len(recs)), ("fetched + labelled", sum(1 for r in recs if r.labels)),
            ("LLM-judged", len(judged)), ("second judge", sum(1 for r in recs if r.v("judge2"))),
            ("human-reviewed", reviewed), ("rule-labelled", ruled),
            ("audit done", f"{q_done}/{len(self.queue)}")])

        def frame_panel(title, fr):
            c = Counter(coarse(r.lang("judge")) for r in fr)
            n = sum(c.values()) or 1
            mx = max(c.values()) if c else 1
            rows = "".join(f"<tr><td>{esc(k)}</td><td>{c[k]}</td><td>{100 * c[k] / n:.1f}%</td>"
                           f"<td><span class=bar style='width:{int(140 * c[k] / mx)}px'></span></td></tr>"
                           for k in COARSE if c.get(k))
            return f"<div class=panel><h3>{esc(title)} · n={sum(c.values())}</h3><table>{rows}</table></div>"

        U = [r for r in judged if r.in_frame("U")]
        R = [r for r in judged if r.in_frame("R")]
        T = [r for r in judged if r.in_frame("T")]
        # labeller agreement with the judge
        agree_rows = ""
        for lab in SHOWN[1:]:
            xs = [(coarse(r.lang("judge")), r.lang(lab)) for r in judged if r.lang(lab) is not None]
            if not xs:
                continue
            ab = sum(1 for _, y in xs if y in ABSTAIN)
            ok = sum(1 for g, y in xs if y not in ABSTAIN and coarse(y) == g)
            agree_rows += (f"<tr><td>{esc(lab)}</td><td class=muted>{esc(LABELLERS[lab][1])}</td>"
                           f"<td>{len(xs)}</td><td>{100 * ok / len(xs):.1f}%</td><td>{100 * ab / len(xs):.1f}%</td></tr>")
        agree = ("<div class=panel><h3>coarse agreement with the primary judge (all judged contents)</h3>"
                 "<table><tr><th>labeller</th><th></th><th>n</th><th>agree</th><th>abstain</th></tr>"
                 f"{agree_rows}</table><p class=muted>The judge is <i>not</i> ground truth — the audit queue is.</p></div>")
        flags = "".join(f"<a href='/list?flag={k}'>{esc(v)}</a> ({sum(1 for r in recs if r.labels and flag_ok(r, k))}) · "
                        for k, v in FLAGS.items())
        prov = Counter(r.v("judge").get("provenance_kind") for r in U)
        nprov = sum(prov.values()) or 1
        prov_html = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td><td>{100 * v / nprov:.1f}%</td></tr>" for k, v in prov.most_common())
        return page("dashboard",
                    f"<div class=cards>{cards}</div>"
                    f"<div class=two>{frame_panel('by-file frame (U)', U)}{frame_panel('by-repo frame (R)', R)}</div>"
                    f"<div class=two>{agree}<div class=panel><h3>provenance kind · by-file</h3><table>{prov_html}</table></div></div>"
                    f"{frame_panel('frame T — the 25 largest repositories', T) if T else ''}"
                    f"<div class=panel><h3>disagreement & work queues</h3><div class=filters>{flags}</div></div>")

    # ------------------------------------------------------------------ listing
    def listing(self, f):
        frame, lang, flag, q = f.get("frame", ""), f.get("lang", ""), f.get("flag", ""), f.get("q", "").lower()
        rows = []
        for sha, r in self.recs.items():
            if not r.labels:
                continue
            if frame and not r.in_frame(frame):
                continue
            if lang and coarse(r.lang("judge")) != lang and r.lang("judge") != lang:
                continue
            if flag and not flag_ok(r, flag):
                continue
            if q and q not in (r.row.get("name", "") + " " + (r.row.get("origin") or "")).lower():
                continue
            rows.append(r)
        rows.sort(key=lambda r: (min(x for x in (r.u_rank, r.d_rank, r.t_rank and 10**6 + r.t_rank, 10**9) if x)))
        pg = int(f.get("page", "1") or 1)
        per = 200
        body = []
        for r in rows[(pg - 1) * per: pg * per]:
            j = r.lang("judge")
            cells = []
            for lab in SHOWN:
                y = r.lang(lab)
                cls = "" if y is None else ("warn" if y in ABSTAIN else ("ok" if j and coarse(y) == coarse(j) else "bad"))
                cells.append(f"<td><span class='tag {cls}'>{esc(y or '·')}</span></td>")
            fr = "".join(x for x, ok in (("U", r.u_rank), ("R", r.d_rank), ("T", r.t_rank)) if ok)
            rev = "✓" if r.reviews else ("⚑" if r.rule else "")
            body.append(f"<tr><td>{rev}</td><td>{fr}</td><td><a href='/file/{sha}'>{esc(r.row['name'][:40])}</a>"
                        f"<div class=muted>{esc((r.row.get('origin') or '')[:60])}</div></td>{''.join(cells)}</tr>")
        pages = (len(rows) + per - 1) // per
        qs = {k: v for k, v in f.items() if k != "page"}
        nav = " ".join(f"<a href='/list?{urlencode({**qs, 'page': p})}'>{p}</a>" if p != pg else f"<b>{p}</b>"
                       for p in range(1, pages + 1)) if pages > 1 else ""
        form = (f"<form class=muted style='display:flex;gap:8px;align-items:end'>"
                f"<div><label>frame</label><select name=frame>{opts(['U', 'R', 'T'], frame)}</select></div>"
                f"<div><label>judge language</label><select name=lang>{opts(COARSE + tax.LANGUAGES, lang)}</select></div>"
                f"<div><label>flag</label><select name=flag>{opts(list(FLAGS), flag)}</select></div>"
                f"<div style='flex:1'><label>name / origin</label><input type=text name=q value='{esc(f.get('q', ''))}'></div>"
                f"<button>filter</button></form>")
        head = "".join(f"<th>{esc(l)}</th>" for l in SHOWN)
        return page("browse", f"{form}<p class=muted>{len(rows)} contents · {esc(FLAGS.get(flag, ''))} {nav}</p>"
                              f"<table><tr><th></th><th>frame</th><th>file</th>{head}</tr>{''.join(body)}</table>"
                              f"<p>{nav}</p>")

    # ------------------------------------------------------------------ audit
    def audit(self):
        if not self.queue:
            return page("audit", "<p>No audit queue yet — run <code>python3 -m tools.m.audit --build</code>.</p>")
        done = [d for d in self.queue if self.recs[d["sha1_git"]].reviews]
        pct = 100 * len(done) / len(self.queue)
        rows = "".join(
            f"<tr><td>{d['order']}</td><td>{'✓' if self.recs[d['sha1_git']].reviews else ''}</td>"
            f"<td><span class=tag>{esc(d['stratum'])}</span></td><td>{esc(d['weight'])}</td>"
            f"<td><a href='/file/{d['sha1_git']}?blind=1&audit=1'>{esc(d['name'][:50])}</a></td></tr>"
            for d in self.queue)
        sc = audit_mod.score(verbose=False)
        score_rows = "".join(f"<tr><td>{esc(k)}</td><td>{v['accuracy']:.3f}</td><td>[{v['ci'][0]:.3f}, {v['ci'][1]:.3f}]</td>"
                             f"<td>{v['n']}</td></tr>" for k, v in sc.get("labellers", {}).items())
        return page("audit", f"""
        <h2 style='margin:4px 0'>Blind audit queue</h2>
        <p class=muted>A stratified random sample of the judged by-file frame. Disagreements are over-sampled;
        each item carries the weight N<sub>h</sub>/n<sub>h</sub> of its stratum, so the scores below estimate accuracy
        over the whole by-file population. Items open in <b>blind mode</b>: machine labels stay hidden until you save.</p>
        <div class=prog><div style='width:{pct:.1f}%'></div></div><p class=muted>{len(done)} / {len(self.queue)} reviewed ·
        <a href='/audit/next'>continue ▶</a></p>
        <div class=two><div class=panel><h3>weighted accuracy vs human (coarse language)</h3>
        <table><tr><th>labeller</th><th>acc.</th><th>95% CI</th><th>n</th></tr>{score_rows or '<tr><td colspan=4 class=muted>no reviews yet</td></tr>'}</table></div>
        <div class=panel><h3>queue</h3><div style='max-height:50vh;overflow:auto'><table>
        <tr><th>#</th><th></th><th>stratum</th><th>w</th><th>file</th></tr>{rows}</table></div></div></div>""")

    def next_audit(self):
        for d in self.queue:
            if not self.recs[d["sha1_git"]].reviews:
                return f"/file/{d['sha1_git']}?blind=1&audit=1"
        return "/audit"

    # ------------------------------------------------------------------ rules
    def rules(self):
        rules = load_rules()
        rows = "".join(
            f"<tr><td><span class=tag>{esc(rl['label'])}</span></td><td>{esc(rl['scope'])}</td><td><code>{esc(rl['value'])}</code></td>"
            f"<td>{sum(1 for r in self.recs.values() if rule_for(r.row, [rl]))}</td><td class=muted>{esc(rl.get('rationale', ''))}</td>"
            f"<td class=muted>{esc(rl.get('reviewer', {}).get('id', ''))} {esc(rl.get('created_at', ''))}</td></tr>"
            for rl in rules)
        return page("rules", "<h2>Group rules</h2><p class=muted>One assertion labels every sampled content in an "
                    "origin, or whose filename / path matches a regex. Later rules win.</p>"
                    f"<table><tr><th>label</th><th>scope</th><th>value</th><th>matches</th><th>rationale</th><th>by</th></tr>{rows}</table>")

    # ------------------------------------------------------------------ detail
    def detail(self, sha, q):
        r = self.recs.get(sha)
        if not r:
            return page("404", "unknown content")
        blind = q.get("blind") == "1" and not r.reviews
        in_audit = q.get("audit") == "1" or sha in self.qset
        row = r.row
        j = r.lang("judge")
        # labeller table
        lt = []
        for lab in SHOWN:
            y = r.lang(lab)
            raw = ""
            if lab in ("ours",) and r.labels:
                raw = r.labels["ours"].get("reason", "")
            elif lab in ("linguist", "pygments") and r.labels:
                raw = r.labels[lab].get("raw") or "(abstain)"
            elif lab.startswith("synid") and r.synid:
                raw = ", ".join(r.synid.get("default" if lab == "synid" else "nocomment") or [])
            elif lab in ("judge", "judge2") and r.v(lab):
                raw = r.v(lab).get("language_detail", "")
            cls = "" if y is None else ("warn" if y in ABSTAIN else ("ok" if j and coarse(y) == coarse(j) else "bad"))
            lt.append(f"<tr><td>{esc(lab)}<div class=muted>{esc(LABELLERS[lab][1])}</div></td>"
                      f"<td><span class='tag {cls}'>{esc(y or '—')}</span></td><td class=muted>{esc(raw)[:120]}</td></tr>")
        h = r.human()
        if h:
            lt.insert(0, f"<tr><td><b>human</b>{' (rule)' if h.get('_rule') else ''}</td>"
                         f"<td><span class='tag ok'>{esc(h.get('language'))}</span></td><td class=muted>{esc(h.get('notes', ''))[:120]}</td></tr>")
        lab_panel = f"<div class=panel><h3>all labellers — language</h3><table>{''.join(lt)}</table></div>"
        # judge verdicts side by side
        fields = ["language", "language_detail", "content_type", "is_programming_language", "provenance_kind",
                  "provenance_detail", "unit_kind", "matlab_dialect", "related_languages", "domain", "maturity",
                  "confidence", "purpose"]
        v1, v2 = r.v("judge") or {}, r.v("judge2") or {}
        jrows = "".join(
            f"<tr><td class=muted>{f}</td><td>{esc(', '.join(v1.get(f)) if isinstance(v1.get(f), list) else v1.get(f, ''))}</td>"
            f"<td {'style=background:#fff7ed' if v2 and str(v1.get(f)) != str(v2.get(f)) and f not in ('purpose', 'language_detail', 'provenance_detail') else ''}>"
            f"{esc(', '.join(v2.get(f)) if isinstance(v2.get(f), list) else v2.get(f, ''))}</td></tr>" for f in fields)
        judge_panel = (f"<div class=panel><h3>LLM judges (differences shaded)</h3><table><tr><th></th>"
                       f"<th>sonnet-4.6</th><th>gemini-3.8-flash</th></tr>{jrows}</table></div>")
        ind = {k: v for k, v in r.ind.items() if v not in (0, False, 0.0, None, "")}
        ind_panel = ("<div class=panel><h3>mechanical indicators (non-zero)</h3><div class=kv>"
                     + "".join(f"<div>{esc(k)}</div><div>{esc(v)}</div>" for k, v in ind.items()) + "</div></div>")
        # provenance
        browse, swh_cnt, swhid = swh_links({**row, "sha1_git": sha})
        np_ = self.npop.get(row.get("name", ""), {})
        prov = (f"<div class=panel><h3>provenance</h3><div class=kv>"
                f"<div>origin</div><div><a target=_blank href='{esc(row.get('origin'))}'>{esc(row.get('origin'))}</a></div>"
                f"<div>at branch</div><div><a target=_blank href='{esc(forge_link(row))}'>{esc(row.get('branch'))}</a></div>"
                f"<div>path</div><div>{esc(row.get('path'))}</div>"
                f"<div>visit timestamp</div><div>{esc(row.get('ts'))}</div>"
                f"<div>SWH</div><div><a target=_blank href='{esc(browse)}'>browse in context</a> · "
                f"<a target=_blank href='{esc(swh_cnt)}'>qualified SWHID</a></div>"
                f"<div>contents in repo</div><div>{esc(row.get('repo_n'))}</div>"
                f"<div>versions of this path</div><div>{esc(row.get('path_versions'))}</div>"
                f"<div>repos with this filename</div><div>{esc(np_.get('repos', '?'))} "
                f"<span class=muted>({esc(np_.get('contents', '?'))} contents, whole population)</span></div>"
                f"<div>frames</div><div>{' '.join(f'{k} #{v}' for k, v in (('U', r.u_rank), ('R', r.d_rank), ('T', r.t_rank)) if v)}"
                f"{' · audit ' + esc(self.qset[sha]['stratum']) + ' w=' + esc(self.qset[sha]['weight']) if sha in self.qset else ''}</div>"
                f"</div></div>")
        prev = h if h and not h.get("_rule") else {}
        form = f"""
        <div class=panel style='border-color:var(--acc)'><h3>your review {'(blind — machine labels hidden until you save)' if blind else ''}</h3><form id=f>
        <input type=hidden name=sha1_git value="{esc(sha)}"><input type=hidden name=filename value="{esc(row.get('name'))}">
        <input type=hidden name=blind value="{'1' if blind else '0'}">
        <label>Language</label><select name=language>{opts(tax.LANGUAGES + ['unsure'], prev.get('language', ''))}</select>
        <div class=muted>Same rule as the judges: <b>matlab</b> = MATLAB-family code MATLAB accepts (portable code too);
        <b>octave</b> only if the file uses syntax MATLAB rejects (<code>#</code> comments, <code>endfunction</code>/<code>endif</code>,
        <code>printf</code>, <code>++</code>, <code>!=</code>). Record portability in the MATLAB-dialect field.</div>
        <label>Content type</label><select name=content_type>{opts(tax.CONTENT_TYPES, prev.get('content_type', ''))}</select>
        <label>Provenance kind</label><select name=provenance_kind>{opts(tax.PROVENANCE_KINDS, prev.get('provenance_kind', ''))}</select>
        <label>MATLAB dialect (if MATLAB-family)</label><select name=matlab_dialect>{opts(tax.MATLAB_DIALECTS, prev.get('matlab_dialect', ''))}</select>
        <label>Your confidence</label><select name=confidence>{opts(tax.CONFIDENCES, prev.get('confidence', ''))}</select>
        <label>Notes</label><textarea name=notes rows=2>{esc(prev.get('notes', ''))}</textarea>
        <button type=button onclick="save(false)">Save</button>
        {'<button type=button onclick="save(true)">Save &amp; next audit item ▶</button>' if in_audit else ''}
        <span id=msg class=muted></span></form></div>
        <script>
        async function save(next){{const fd=new FormData(document.getElementById('f'));
          const res=await fetch('/api/review',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(fd.entries()))}});
          if(!res.ok){{document.getElementById('msg').textContent=' error';return;}}
          if(next){{location.href='/audit/next';return;}}
          document.getElementById('msg').textContent=' saved ✓';
          document.querySelectorAll('.machine').forEach(e=>e.classList.remove('hidden'));}}
        function reveal(){{document.querySelectorAll('.machine').forEach(e=>e.classList.remove('hidden'));}}
        document.addEventListener('keydown',e=>{{if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT')return;
          if(e.key==='n')location.href='/audit/next';}});
        </script>"""
        pat = re.sub(r"\d+", r"\\d+", re.escape(row.get("name", "")))
        rule_form = f"""
        <div class='panel machine {'hidden' if blind else ''}'><h3>assert a group rule</h3>
        {'<p class=muted>covered by: <span class=tag>' + esc(r.rule['label']) + '</span> ' + esc(r.rule['scope']) + '=' + esc(r.rule['value']) + '</p>' if r.rule else ''}
        <form id=rf><input type=hidden name=example_sha value="{esc(sha)}">
        <label>Scope</label><select name=scope id=rscope onchange="rs(this.value)">
        <option value=origin>this origin</option><option value=filename>filename regex</option><option value=path>path regex</option></select>
        <label>Value</label><input type=text name=value id=rval value="{esc(row.get('origin'))}">
        <label>Language label</label><select name=label>{opts(RULE_LABELS, j or '')}</select>
        <label>Rationale</label><input type=text name=rationale placeholder="e.g. iOS firmware class-dump">
        <button type=button class=sec onclick=saverule()>Assert rule</button> <span id=rmsg class=muted></span></form></div>
        <script>const _o={json.dumps(row.get('origin') or '')},_p={json.dumps(pat)},_d={json.dumps(re.escape(str(Path(row.get('path') or '').parent)))};
        function rs(v){{document.getElementById('rval').value=v=='origin'?_o:(v=='filename'?_p:_d);}}
        async function saverule(){{const fd=new FormData(document.getElementById('rf'));
          const r=await fetch('/api/rule',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(fd.entries()))}});
          const j=await r.json();document.getElementById('rmsg').textContent=r.ok?(' asserted ✓ ('+j.matched+' sampled contents)'):(' '+(j.error||'error'));}}</script>"""
        code = read_code(sha)
        numbered = "\n".join(f"<span class=ln>{i}</span>{esc(line)}" for i, line in enumerate(code.split("\n"), 1))
        left = (f"<h2 style='margin:2px 0'>{esc(row.get('name'))}</h2>"
                f"<p class=muted>{esc(swhid.split(';')[0])} · {esc(r.labels and r.labels.get('length'))} bytes · "
                f"{esc(r.ind.get('total_lines'))} lines</p><pre class=code>{numbered}</pre>")
        machine = (f"<div class='machine {'hidden' if blind else ''}'>{lab_panel}{judge_panel}{ind_panel}</div>"
                   + (f"<p><button class=sec type=button onclick=reveal()>reveal machine labels</button></p>" if blind else ""))
        right = form + prov + machine + rule_form
        return page(row.get("name", sha), f"<div class=grid><div>{left}</div><div>{right}</div></div>")


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

    def _redirect(self, loc):
        self.send_response(302)
        self.send_header("Location", loc)
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == "/":
            self._send(self.app.dashboard())
        elif u.path == "/list":
            self._send(self.app.listing(q))
        elif u.path == "/audit":
            self._send(self.app.audit())
        elif u.path == "/audit/next":
            self._redirect(self.app.next_audit())
        elif u.path == "/rules":
            self._send(self.app.rules())
        elif u.path.startswith("/file/"):
            self._send(self.app.detail(u.path.split("/file/", 1)[1], q))
        elif u.path == "/api/export":
            out = {sha: {"reviews": r.reviews, "rule": r.rule} for sha, r in self.app.recs.items() if r.reviews or r.rule}
            self._send(json.dumps(out, indent=1).encode(), 200, "application/json")
        else:
            self._send(page("404", "not found"), 404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
        except Exception:
            self._send(b'{"error":"bad json"}', 400, "application/json")
            return
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if path == "/api/rule":
            scope, value, label = ((data.get(k, "") or "").strip() for k in ("scope", "value", "label"))
            if scope not in ("origin", "filename", "path") or not value or label not in RULE_LABELS:
                self._send(b'{"error":"scope/value/label required"}', 400, "application/json")
                return
            if scope != "origin":
                try:
                    re.compile(value)
                except re.error as e:
                    self._send(json.dumps({"error": str(e)}).encode(), 400, "application/json")
                    return
            rule = {"scope": scope, "value": value, "label": label,
                    "rationale": (data.get("rationale") or "").strip(), "example_sha": data.get("example_sha", ""),
                    "reviewer": {"kind": "human", "id": self.reviewer_id}, "created_at": now}
            RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
            with RULES_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rule) + "\n")
            self.app.refresh_rules()
            matched = sum(1 for r in self.app.recs.values() if rule_for(r.row, [rule]))
            self._send(json.dumps({"ok": True, "matched": matched}).encode(), 200, "application/json")
            return
        if path != "/api/review":
            self._send(b'{"error":"?"}', 404, "application/json")
            return
        sha = (data.get("sha1_git") or "").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha not in self.app.recs:
            self._send(b'{"error":"bad sha"}', 400, "application/json")
            return
        human = {k: (data.get(k, "") or "").strip() for k in
                 ("language", "content_type", "provenance_kind", "matlab_dialect", "confidence", "notes")}
        if not human["language"]:
            self._send(b'{"error":"language required"}', 400, "application/json")
            return
        rec = {"schema": SCHEMA,
               "subject": {"sha1_git": sha, "swhid": f"swh:1:cnt:{sha}", "filename": data.get("filename", "")},
               "reviewer": {"kind": "human", "id": self.reviewer_id},
               "blind": data.get("blind") == "1",
               "audit": sha in self.app.qset,
               "human": human, "created_at": now}
        d = REVIEWS / sha
        d.mkdir(parents=True, exist_ok=True)
        h8 = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:8]
        p = d / f"{now.replace('-', '').replace(':', '')}--{self.reviewer_id}--{h8}.json"
        p.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
        self.app.refresh_one(sha)
        self._send(json.dumps({"ok": True, "path": p.name}).encode(), 200, "application/json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8769)
    ap.add_argument("--reviewer", default=None)
    a = ap.parse_args()
    Handler.reviewer_id = re.sub(r"[^\w.-]", "_", a.reviewer or getpass.getuser() or "anon")
    REVIEWS.mkdir(parents=True, exist_ok=True)
    Handler.app = App()
    print(f".m review app: http://{a.host}:{a.port}/  (reviewer={Handler.reviewer_id})")
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
