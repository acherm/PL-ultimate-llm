"""Review app for the .fsf study — mirrors tools/cobol/review_app.py.

One pane over each sampled content: the source, mechanical indicators, the
LLM-judge verdict (content_type / format / expressed_in / related_languages /
ecosystem / domain / FEAT detail), the deterministic reclassifier label, the
origin (from the graph CSV, carried in the report), and a human-review form.

Run:  python3 -m tools.fsf.review_app          # http://127.0.0.1:8767
Reviews append to reviews_fsf/<sha>/ (cobol-review-style JSON).
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
from urllib.parse import parse_qs, urlparse

from tools.fsf import taxonomy as tax

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "fsf_study"
REPORTS = STUDY / "reports"
CACHE = ROOT / ".cache" / "cobol"          # shared byte cache
REVIEWS = ROOT / "reviews_fsf"
RULES_FILE = REVIEWS / "_rules.jsonl"
RULE_LABELS = ["not-fsl-feat", "fsl-feat", "config-other", "data",
               "docs", "noise", "not-fsf:other"]
SWH = "https://archive.softwareheritage.org"
SCHEMA = "fsf-review/1"


# --------------------------------------------------------------------------- #
def load_reports() -> dict[str, dict]:
    out = {}
    if REPORTS.is_dir():
        for p in REPORTS.glob("*.json"):
            try:
                out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
    return out


def read_code(sha: str) -> str:
    p = CACHE / f"{sha}.bin"
    if not p.exists():
        return "(bytes not cached)"
    return p.read_bytes()[:60000].decode("latin-1", "replace")


def reviews_for(sha: str) -> list[dict]:
    d = REVIEWS / sha
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return out


def save_review(rec: dict) -> Path:
    sha = rec["subject"]["sha1_git"]
    d = REVIEWS / sha
    d.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time()))
    h8 = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:8]
    path = d / f"{stamp}--{rec['reviewer']['id']}--{h8}.json"
    path.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def verdict(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def load_rules() -> list[dict]:
    out = []
    if RULES_FILE.exists():
        for line in RULES_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def save_rule(rule: dict) -> None:
    RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RULES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rule) + "\n")


def rule_for(r: dict, rules: list[dict]):
    """First rule whose origin/filename matches this content, else None."""
    name, origin = r.get("name", ""), r.get("origin")
    for rule in rules:
        if rule.get("scope") == "origin" and origin and rule.get("value") == origin:
            return rule
        if rule.get("scope") == "filename" and rule.get("value"):
            try:
                if re.search(rule["value"], name):
                    return rule
            except re.error:
                pass
    return None


# --------------------------------------------------------------------------- #
CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a}
header{background:#3d2f6b;color:#fff;padding:10px 18px;position:sticky;top:0;z-index:5}
header a{color:#d9cdff;text-decoration:none;margin-right:14px}
main{padding:16px 18px;max-width:1240px}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #e6e6e6;padding:5px 8px;text-align:left;font-size:13px}
tr:hover{background:#f7f5fc}
a{color:#5b3ea8}
.tag{display:inline-block;background:#efeaf8;border-radius:3px;padding:1px 6px;font-size:12px;margin:1px}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0}
.card{background:#faf9fc;border:1px solid #e3e3e3;border-radius:8px;padding:12px 14px;min-width:150px}
.card b{font-size:22px;display:block}
.bar{height:14px;background:#5b3ea8;border-radius:2px;display:inline-block;vertical-align:middle}
.grid{display:grid;grid-template-columns:1fr 420px;gap:18px}
pre.code{background:#0d1117;color:#d6dee8;padding:12px;border-radius:6px;overflow:auto;
  max-height:66vh;font:12px/1.45 SFMono-Regular,Consolas,monospace;white-space:pre}
.panel{background:#faf9fc;border:1px solid #e3e3e3;border-radius:6px;padding:12px;margin-bottom:14px}
.panel h3{margin:0 0 8px;font-size:12px;text-transform:uppercase;color:#555;letter-spacing:.04em}
.jbox{border-left:3px solid #5b3ea8;padding-left:10px}
.kv{display:grid;grid-template-columns:130px 1fr;gap:2px 8px;font-size:13px}
.kv div:nth-child(odd){color:#666}
label{display:block;margin:8px 0 2px;font-size:12px;color:#444;font-weight:600}
select,input[type=text],textarea{width:100%;padding:5px;border:1px solid #ccc;border-radius:4px;font:inherit;box-sizing:border-box}
button{background:#3d2f6b;color:#fff;border:0;border-radius:5px;padding:9px 16px;cursor:pointer;margin-top:12px}
.muted{color:#888;font-size:12px}
"""


def esc(s):
    return html.escape(str(s if s is not None else ""))


def opts(values, cur=""):
    return "".join([f'<option value="">—</option>'] +
                   [f'<option{" selected" if v == cur else ""}>{esc(v)}</option>' for v in values])


def page(title, body):
    return (f"<!doctype html><meta charset=utf-8><title>{esc(title)}</title><style>{CSS}</style>"
            f"<header><a href='/'>◇ .fsf labels</a><a href='/list'>browse</a>"
            f"<a href='/list?flag=nonfeat'>non-FEAT</a>"
            f"<a href='/list?flag=unreviewed'>unreviewed</a>"
            f"<a href='/list?flag=ruled'>rule-labelled</a>"
            f"<span class=muted style='color:#d9cdff'>{esc(title)}</span></header>"
            f"<main>{body}</main>").encode("utf-8")


class App:
    def __init__(self):
        self.reps = load_reports()
        print(f"loaded {len(self.reps)} fsf reports")

    def dashboard(self):
        reps = list(self.reps.values())
        judged = [r for r in reps if verdict(r)]
        reviewed = sum(1 for sha in self.reps if reviews_for(sha))
        rules = load_rules()
        ruled = sum(1 for r in reps if rule_for(r, rules))
        cards = "".join(f"<div class=card><b>{v}</b><span class=muted>{k}</span></div>"
                        for k, v in [("contents", len(reps)), ("judged", len(judged)),
                                     ("reviewed", reviewed), ("rule-labelled", ruled)])
        rule_html = ("<div class=panel><h3>group rules</h3>" + "".join(
            f"<div class=muted><span class=tag>{esc(rl['label'])}</span> "
            f"{esc(rl['scope'])} = {esc(rl['value'])} "
            f"(<a href='/list?flag=ruled'>{sum(1 for r in reps if rule_for(r,[rl]))} contents</a>)</div>"
            for rl in rules) + "</div>") if rules else ""

        def dist(getter):
            c = Counter(getter(verdict(r)) for r in judged)
            n = sum(c.values()) or 1
            return c, n

        def rellangs():
            c = Counter()
            for r in judged:
                for l in (verdict(r).get("related_languages") or []):
                    c[l.strip()] += 1
            return c

        def panel(title, counter, n, link=None):
            mx = max(counter.values()) if counter else 1
            rows = "".join(
                f"<tr><td>{('<a href=\"/list?'+link+'='+esc(k)+'\">'+esc(k)+'</a>') if link else esc(k)}</td>"
                f"<td>{v}</td><td>{round(100*v/n)}%</td>"
                f"<td><span class=bar style='width:{int(150*v/mx)}px'></span></td></tr>"
                for k, v in counter.most_common(12))
            return f"<div class=panel><h3>{title}</h3><table>{rows}</table></div>"

        ct, nct = dist(lambda v: v.get("content_type", ""))
        dm, ndm = dist(lambda v: v.get("domain", ""))
        rl = rellangs()
        fg = Counter(r.get("forge", "") for r in reps)
        return page("dashboard",
                    f"<div class=cards>{cards}</div>{rule_html}"
                    + panel("content_type", ct, nct, "content_type")
                    + panel("related_languages (what .fsf relates to)", rl, len(judged) or 1)
                    + panel("domain", dm, ndm)
                    + panel("forge", fg, len(reps) or 1))

    def listing(self, f):
        rows = []
        for sha, r in sorted(self.reps.items(), key=lambda kv: kv[1].get("name", "")):
            v = verdict(r) or {}
            if f.get("content_type") and v.get("content_type") != f["content_type"]:
                continue
            if f.get("q") and f["q"].lower() not in r.get("name", "").lower():
                continue
            if f.get("flag") == "nonfeat" and r["reclass"]["label"] == "fsl-feat":
                continue
            if f.get("flag") == "unreviewed" and reviews_for(sha):
                continue
            if f.get("flag") == "ruled" and not rule_for(r, load_rules()):
                continue
            rl = ", ".join(v.get("related_languages") or [])
            rows.append(
                f"<tr><td>{'✓' if reviews_for(sha) else ''}</td>"
                f"<td><a href='/file/{sha}'>{esc(r.get('name',''))[:38]}</a></td>"
                f"<td>{esc(v.get('content_type',''))}</td>"
                f"<td>{esc(rl)[:24]}</td><td>{esc(v.get('domain',''))}</td>"
                f"<td>{esc(r['reclass']['label'])}</td>"
                f"<td class=muted>{esc(r.get('forge',''))}</td></tr>")
        head = (f"<p class=muted>{len(rows)} shown</p>"
                f"<form class=muted><input name=q value='{esc(f.get('q',''))}' placeholder=filename>"
                f"<input type=hidden name=flag value='{esc(f.get('flag',''))}'><button>search</button></form>")
        return page("browse", head + "<table><tr><th>rev</th><th>file</th><th>content_type</th>"
                    "<th>related</th><th>domain</th><th>reclass</th><th>forge</th></tr>"
                    + "".join(rows[:600]) + "</table>")

    def detail(self, sha):
        r = self.reps.get(sha)
        if not r:
            return page("404", "unknown content")
        v = verdict(r) or {}
        ind = r["indicators"]
        hr = reviews_for(sha)
        prev = hr[-1]["human"] if hr else {}
        code = read_code(sha)
        jb = (f"<div class=kv>"
              f"<div>content_type</div><div><b>{esc(v.get('content_type',''))}</b></div>"
              f"<div>format</div><div>{esc(v.get('format',''))}</div>"
              f"<div>expressed_in</div><div>{esc(v.get('expressed_in',''))}</div>"
              f"<div>related_languages</div><div><b>{esc(', '.join(v.get('related_languages') or []))}</b></div>"
              f"<div>ecosystem/tool</div><div>{esc(v.get('ecosystem_tool',''))}</div>"
              f"<div>domain</div><div>{esc(v.get('domain',''))}</div>"
              f"<div>is PL?</div><div>{esc(v.get('is_programming_language'))}</div>"
              f"<div>FEAT level</div><div>{esc(v.get('feat_level',''))} · {esc(v.get('analysis_type',''))} · {esc(v.get('generated',''))}</div>"
              f"</div><p class=muted>{esc(v.get('purpose',''))}</p>") if v else "<p class=muted>not judged yet</p>"
        indrows = "".join(f"<div>{esc(k)}</div><div>{esc(val)}</div>" for k, val in [
            ("lines", ind["total_lines"]), ("comment ratio", ind["comment_ratio"]),
            ("set fmri(...)", ind["n_set_fmri"]), ("has_feat", ind["has_feat"]),
            ("level / inmelodic", f"{ind['feat_level']} / {ind['inmelodic']}"),
            ("EVs / timepoints", f"{ind['n_evs']} / {ind['n_timepoints']}"),
            ("FEAT version", ind["feat_version"]), ("reclass", r["reclass"]["label"])])
        origin, forge = r.get("origin", ""), r.get("forge", "")
        prov = (f"<div class=panel jbox><h3>origin</h3>"
                f"<a target=_blank href='{esc(origin)}'>{esc(origin)}</a> <span class=tag>{esc(forge)}</span></div>") if origin else ""
        form = f"""
        <div class=panel><h3>your review</h3><form id=f>
        <input type=hidden name=sha1_git value="{esc(sha)}"><input type=hidden name=filename value="{esc(r.get('name',''))}">
        <label>content_type</label><select name=content_type>{opts(tax.CONTENT_TYPES, prev.get('content_type',''))}</select>
        <label>related languages (comma-sep)</label><input name=related_languages value="{esc(prev.get('related_languages',''))}" placeholder="Tcl">
        <label>Is it FSL FEAT?</label><select name=is_feat>{opts(['yes','no','unsure'], prev.get('is_feat',''))}</select>
        <label>Agreement with judge</label><select name=agreement>{opts(['agree','partial','disagree'], prev.get('agreement',''))}</select>
        <label>Notes</label><textarea name=notes rows=3>{esc(prev.get('notes',''))}</textarea>
        <button type=button onclick=save()>Save</button> <span id=msg class=muted></span></form></div>
        <script>async function save(){{const fd=new FormData(document.getElementById('f'));
        const res=await fetch('/api/review',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(fd.entries()))}});
        document.getElementById('msg').textContent=res.ok?' saved ✓':' error';}}</script>"""
        cur = rule_for(r, load_rules())
        pat = re.sub(r"\d+", r"\\d+", re.escape(r.get("name", "")))
        cur_html = (f"<p class=muted>already covered: <span class=tag>{esc(cur['label'])}</span> "
                    f"{esc(cur['scope'])}={esc(cur['value'])}</p>") if cur else ""
        assert_html = f"""
        <div class=panel><h3>assert for a group</h3>{cur_html}
        <p class=muted>One statement labels every matching content (e.g. all files from a non-FEAT repo).</p>
        <form id=rf><input type=hidden name=example_sha value="{esc(sha)}">
        <label>Scope</label><select name=scope onchange="rscope(this.value)">
        <option value=origin>this origin</option><option value=filename>filename pattern (regex)</option></select>
        <label>Value</label><input name=value id=rval value="{esc(origin)}">
        <label>Label</label><select name=label>{opts(RULE_LABELS, 'not-fsl-feat')}</select>
        <label>Rationale</label><input name=rationale placeholder="not FSL FEAT">
        <button type=button onclick=saverule()>Assert rule</button> <span id=rmsg class=muted></span></form></div>
        <script>const _o={json.dumps(origin)},_p={json.dumps(pat)};
        function rscope(v){{document.getElementById('rval').value=(v=='origin')?_o:_p;}}
        async function saverule(){{const fd=new FormData(document.getElementById('rf'));
        const r=await fetch('/api/rule',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(Object.fromEntries(fd.entries()))}});
        const j=await r.json();document.getElementById('rmsg').textContent=r.ok?(' asserted ✓ ('+j.matched+')'):(' err');}}</script>"""
        left = (f"<h2 style='margin:4px 0'>{esc(r.get('name',''))}</h2>"
                f"<p class=muted>swh:1:cnt:{esc(sha)} · {esc(r.get('length'))} bytes · "
                f"<a target=_blank href='{SWH}/swh:1:cnt:{esc(sha)}/'>SWH↗</a></p>"
                f"<pre class=code>{esc(code)}</pre>")
        right = f"{prov}<div class=panel jbox><h3>LLM judge</h3>{jb}</div><div class=panel><h3>indicators</h3><div class=kv>{indrows}</div></div>{assert_html}{form}"
        return page(r.get("name", sha), f"<div class=grid><div>{left}</div><div>{right}</div></div>")


class Handler(BaseHTTPRequestHandler):
    app = None
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
        path = urlparse(self.path).path
        data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
        if path == "/api/rule":
            scope, value, label = (data.get("scope") or "").strip(), (data.get("value") or "").strip(), (data.get("label") or "").strip()
            if scope not in ("origin", "filename") or not value or not label:
                self._send(b'{"error":"scope/value/label required"}', 400, "application/json"); return
            if scope == "filename":
                try:
                    re.compile(value)
                except re.error as e:
                    self._send(json.dumps({"error": f"bad regex: {e}"}).encode(), 400, "application/json"); return
            rule = {"scope": scope, "value": value, "label": label,
                    "rationale": (data.get("rationale") or "").strip(),
                    "example_sha": data.get("example_sha", ""),
                    "reviewer": {"kind": "human", "id": self.reviewer_id},
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))}
            save_rule(rule)
            matched = sum(1 for r in self.app.reps.values() if rule_for(r, [rule]))
            self._send(json.dumps({"ok": True, "matched": matched}).encode(), 200, "application/json"); return
        if path != "/api/review":
            self._send(b'{"error":"?"}', 404, "application/json"); return
        sha = (data.get("sha1_git") or "").strip()
        if len(sha) != 40:
            self._send(b'{"error":"bad sha"}', 400, "application/json"); return
        rec = {"schema": SCHEMA,
               "subject": {"sha1_git": sha, "swhid": f"swh:1:cnt:{sha}", "filename": data.get("filename", "")},
               "reviewer": {"kind": "human", "id": self.reviewer_id},
               "human": {k: (data.get(k, "") or "").strip() for k in
                         ("content_type", "related_languages", "is_feat", "agreement", "notes")},
               "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))}
        p = save_review(rec)
        self._send(json.dumps({"ok": True, "path": p.name}).encode(), 200, "application/json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8767)
    ap.add_argument("--reviewer", default=None)
    a = ap.parse_args()
    Handler.reviewer_id = a.reviewer or getpass.getuser() or "anon"
    REVIEWS.mkdir(parents=True, exist_ok=True)
    Handler.app = App()
    print(f".fsf review app: http://{a.host}:{a.port}/  (reviewer={Handler.reviewer_id})")
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
