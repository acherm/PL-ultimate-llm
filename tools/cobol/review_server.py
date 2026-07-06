"""Local web tool to review/annotate COBOL-in-SWH samples.

Shows, per sampled content: the source bytes (from the local cache), the
mechanical indicators, and the LLM-judge verdict — then captures a human
annotation that can confirm or correct the judge (a ground-truth /
cross-check layer). Reviews are append-only JSON, one file per review,
under ``reviews_cobol/<sha1_git>/`` — same git-as-sync model as the PL
reviewstore, but with the COBOL vocabulary from ``taxonomy.py``.

Run:
    python3 -m tools.cobol.review_server          # http://127.0.0.1:8765
    python3 -m tools.cobol.review_server --port 9000 --reviewer me

No external deps (stdlib http.server), no network: code is read from
``.cache/cobol/<sha>.bin`` (populated by run_study). Origin is not
recoverable from a bare cnt SWHID, so the form has a free-text
``origin_url`` for a human to paste the forge URL when they find one.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import html
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import taxonomy as tax
from .common import CACHE_DIR, STUDY_DIR, SWH_BASE
from .run_study import canonical_view

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = STUDY_DIR / "reports"
REVIEWS_DIR = ROOT / "reviews_cobol"
SCHEMA = "cobol-review/1"

IS_COBOL_CHOICES = ["yes", "no", "unsure"]
AGREEMENT_CHOICES = ["agree", "partial", "disagree", "n/a"]


# --------------------------------------------------------------------------- #
# Data access
# --------------------------------------------------------------------------- #
def load_report(sha: str) -> dict | None:
    p = REPORTS_DIR / f"{sha}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def iter_reports():
    for p in sorted(REPORTS_DIR.glob("*.json")):
        try:
            yield json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue


def read_code(sha: str) -> str | None:
    p = CACHE_DIR / f"{sha}.bin"
    if not p.exists():
        return None
    raw = p.read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def reviews_for(sha: str) -> list[dict]:
    d = REVIEWS_DIR / sha
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def reviewed_shas() -> set[str]:
    if not REVIEWS_DIR.is_dir():
        return set()
    return {d.name for d in REVIEWS_DIR.iterdir() if d.is_dir() and any(d.glob("*.json"))}


def save_review(record: dict) -> Path:
    sha = record["subject"]["sha1_git"]
    d = REVIEWS_DIR / sha
    d.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time()))
    blob = json.dumps(record, sort_keys=True).encode("utf-8")
    h8 = hashlib.sha256(blob).hexdigest()[:8]
    path = d / f"{stamp}--{record['reviewer']['id']}--{h8}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# HTML rendering
# --------------------------------------------------------------------------- #
CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a}
header{background:#0b3d61;color:#fff;padding:10px 18px;position:sticky;top:0;z-index:5}
header a{color:#cde4ff;text-decoration:none;margin-right:14px}
main{padding:16px 18px;max-width:1180px}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #e3e3e3;padding:5px 8px;text-align:left;font-size:13px}
tr:hover{background:#f6f9fc}
.tag{display:inline-block;background:#eef3f8;border-radius:3px;padding:1px 6px;font-size:12px}
.done{color:#127a2e;font-weight:600}
.todo{color:#9a6700}
.grid{display:grid;grid-template-columns:1fr 380px;gap:18px}
pre.code{background:#0d1117;color:#d6dee8;padding:12px;border-radius:6px;overflow:auto;
  max-height:72vh;font:12px/1.45 SFMono-Regular,Consolas,monospace;white-space:pre}
.panel{background:#fafbfc;border:1px solid #e3e3e3;border-radius:6px;padding:12px;margin-bottom:14px}
.panel h3{margin:0 0 8px;font-size:13px;text-transform:uppercase;color:#555;letter-spacing:.04em}
.kv{display:grid;grid-template-columns:130px 1fr;gap:2px 8px;font-size:13px}
.kv div:nth-child(odd){color:#666}
label{display:block;margin:8px 0 2px;font-size:12px;color:#444;font-weight:600}
select,input[type=text],textarea{width:100%;padding:5px;border:1px solid #ccc;border-radius:4px;font:inherit;box-sizing:border-box}
button{background:#0b3d61;color:#fff;border:0;border-radius:5px;padding:9px 16px;font-size:14px;cursor:pointer;margin-top:12px}
.muted{color:#888;font-size:12px}
.evidence li{font-size:12px;color:#555}
.judgebox{border-left:3px solid #0b3d61;padding-left:10px}
"""


def _esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _opts(values, current="") -> str:
    out = ['<option value="">—</option>']
    for v in values:
        sel = " selected" if v == current else ""
        out.append(f'<option value="{_esc(v)}"{sel}>{_esc(v)}</option>')
    return "".join(out)


def page(title: str, body: str) -> bytes:
    return (f"<!doctype html><html><head><meta charset=utf-8>"
            f"<title>{_esc(title)}</title><style>{CSS}</style></head><body>"
            f"<header><a href='/'>COBOL review</a>"
            f"<span class=muted style='color:#cde4ff'>{_esc(title)}</span></header>"
            f"<main>{body}</main></body></html>").encode("utf-8")


def render_index(flt: str) -> bytes:
    done = reviewed_shas()
    rows = []
    n = nrev = 0
    for r in iter_reports():
        sha = r["sample"]["sha1_git"]
        fn = r["sample"].get("filename", "")
        cv = canonical_view((r.get("judge") or {}).get("verdict")) if isinstance(r.get("judge"), dict) else None
        cv = cv or {}
        hay = f"{fn} {cv.get('family','')} {cv.get('domain','')}".lower()
        if flt and flt.lower() not in hay:
            continue
        n += 1
        is_done = sha in done
        nrev += is_done
        loc = r["indicators"]["code_lines"]
        rows.append(
            f"<tr><td>{'<span class=done>✓</span>' if is_done else '<span class=todo>•</span>'}</td>"
            f"<td><a href='/review/{sha}'>{_esc(fn) or sha[:12]}</a></td>"
            f"<td class=muted>{loc}</td>"
            f"<td><span class=tag>{_esc(cv.get('family',''))}</span></td>"
            f"<td>{_esc(cv.get('domain',''))}</td>"
            f"<td>{_esc(cv.get('standard',''))}</td>"
            f"<td>{_esc(cv.get('cobol_confirmed',''))}</td></tr>")
    head = (f"<form><input type=text name=q value='{_esc(flt)}' "
            f"placeholder='filter by filename / family / domain' "
            f"style='max-width:420px'> <button>filter</button></form>"
            f"<p class=muted>{n} samples · {nrev} reviewed · "
            f"{n - nrev} to go</p>")
    table = ("<table><tr><th></th><th>file</th><th>LOC</th><th>family (judge)</th>"
             "<th>domain</th><th>std</th><th>cobol?</th></tr>"
             + "".join(rows) + "</table>")
    return page("samples", head + table)


_ORIGINS = None


def recovered_origin(sha: str) -> dict | None:
    """Byte-confirmed origin recovered by tools/cobol/recover_origins.py."""
    global _ORIGINS
    if _ORIGINS is None:
        _ORIGINS = {}
        p = STUDY_DIR / "origins.jsonl"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if o.get("content_match"):
                    _ORIGINS[o["sha"]] = o
    return _ORIGINS.get(sha)


def render_review(sha: str) -> bytes:
    r = load_report(sha)
    if not r:
        return page("not found", f"<p>No report for {_esc(sha)}.</p>")
    code = read_code(sha) or "(bytes not in cache — run fetch first)"
    ind = r["indicators"]
    judge = r.get("judge") or {}
    verdict = judge.get("verdict") if isinstance(judge, dict) else None
    cv = canonical_view(verdict) or {}
    existing = reviews_for(sha)
    prev = existing[-1]["human"] if existing else {}
    prov = recovered_origin(sha)
    origin_default = prev.get("origin_url") or (prov["origin"] if prov else "")

    # judge panel
    if verdict:
        dia = verdict.get("dialect", {}) if isinstance(verdict, dict) else {}
        pur = verdict.get("purpose", {}) if isinstance(verdict, dict) else {}
        ev = "".join(f"<li>{_esc(e)}</li>" for e in (dia.get("evidence") or [])[:8])
        jbody = (
            f"<div class=kv>"
            f"<div>is COBOL</div><div>{_esc(cv.get('cobol_confirmed',''))}</div>"
            f"<div>family</div><div>{_esc(cv.get('family',''))} "
            f"<span class=muted>{_esc(dia.get('detail',''))}</span></div>"
            f"<div>standard</div><div>{_esc(cv.get('standard',''))}</div>"
            f"<div>format</div><div>{_esc(cv.get('source_format',''))}</div>"
            f"<div>domain</div><div>{_esc(cv.get('domain',''))} "
            f"<span class=muted>{_esc(pur.get('domain_detail',''))}</span></div>"
            f"<div>type</div><div>{_esc(cv.get('program_type',''))}</div>"
            f"<div>maturity</div><div>{_esc(cv.get('maturity',''))}</div>"
            f"</div>"
            f"<p class=muted>{_esc(pur.get('summary',''))}</p>"
            f"<ul class=evidence>{ev}</ul>"
            f"<p class=muted>{_esc(judge.get('model',''))} · {_esc(judge.get('schema',''))}</p>")
    else:
        skip = judge.get("skipped") if isinstance(judge, dict) else None
        jbody = f"<p class=muted>not judged ({_esc(skip or 'n/a')})</p>"

    swhid = r["sample"].get("swhid", f"swh:1:cnt:{sha}")
    indrows = "".join(
        f"<div>{_esc(k)}</div><div>{_esc(v)}</div>" for k, v in [
            ("LOC (code)", ind["code_lines"]), ("total/blank/comment",
             f"{ind['total_lines']}/{ind['blank_lines']}/{ind['comment_lines']}"),
            ("format (heur.)", ind["source_format_guess"]),
            ("divisions", ind["n_divisions"]),
            ("EXEC SQL / CICS", f"{ind['has_exec_sql']} / {ind['has_exec_cics']}"),
            ("COPY / CALL", f"{ind['copy_count']} / {ind['call_count']}"),
            ("PERFORM / GOTO", f"{ind['perform_count']} / {ind['goto_count']}"),
            ("COMP-3", ind["comp3_count"]),
            ("PROGRAM-IDs", ", ".join(ind["program_ids"]) or "—"),
        ])

    form = f"""
    <div class=panel><h3>your review</h3>
    <form id=f>
      <input type=hidden name=sha1_git value="{_esc(sha)}">
      <input type=hidden name=filename value="{_esc(r['sample'].get('filename',''))}">
      <label>Is this COBOL?</label>
      <select name=is_cobol>{_opts(IS_COBOL_CHOICES, prev.get('is_cobol',''))}</select>
      <label>Agreement with judge</label>
      <select name=agreement>{_opts(AGREEMENT_CHOICES, prev.get('agreement',''))}</select>
      <label>Dialect family (correct/confirm)</label>
      <select name=dialect_family>{_opts(tax.DIALECT_FAMILIES, prev.get('dialect_family',''))}</select>
      <label>Domain (correct/confirm)</label>
      <select name=domain>{_opts(tax.DOMAINS, prev.get('domain',''))}</select>
      <label>Source format</label>
      <select name=source_format>{_opts(tax.SOURCE_FORMATS, prev.get('source_format',''))}</select>
      <label>Origin URL (paste forge link if found)</label>
      <input type=text name=origin_url value="{_esc(origin_default)}" placeholder="https://github.com/...">
      <label>Notes</label>
      <textarea name=notes rows=4>{_esc(prev.get('notes',''))}</textarea>
      <button type=button onclick=submitReview()>Save review</button>
      <span id=msg class=muted></span>
    </form></div>
    <p class=muted>{len(existing)} prior review(s).
      <a href="{SWH_BASE}/{_esc(swhid)}/" target=_blank>open in SWH ↗</a></p>
    <script>
    async function submitReview(){{
      const fd=new FormData(document.getElementById('f'));
      const body=Object.fromEntries(fd.entries());
      const res=await fetch('/api/review',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(body)}});
      const j=await res.json();
      document.getElementById('msg').textContent=res.ok?(' saved ✓ '+j.path):(' error: '+j.error);
    }}
    </script>"""

    left = (f"<h2 style='margin:4px 0'>{_esc(r['sample'].get('filename','') or sha[:16])}</h2>"
            f"<p class=muted>{_esc(swhid)} · {ind['bytes_len']} bytes</p>"
            f"<pre class=code>{_esc(code)}</pre>")
    prov_html = ""
    if prov:
        anc = (f" @ <code>{_esc(prov['anchor'])}</code>" if prov.get("anchor")
               else " <span class=muted>(no anchor)</span>")
        prov_html = (f"<div class=panel judgebox><h3>recovered origin</h3>"
                     f"<a target=_blank href='{_esc(prov['origin'])}'>{_esc(prov['origin'])}</a>{anc}"
                     f"<p class=muted style='word-break:break-all'>{_esc(prov.get('qualified',''))}</p></div>")
    right = (f"{prov_html}"
             f"<div class=panel judgebox><h3>LLM judge</h3>{jbody}</div>"
             f"<div class=panel><h3>indicators</h3><div class=kv>{indrows}</div></div>"
             f"{form}")
    return page(r['sample'].get('filename', sha),
                f"<div class=grid><div>{left}</div><div>{right}</div></div>")


# --------------------------------------------------------------------------- #
# HTTP handler
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    reviewer_id = "anon"

    def log_message(self, *a):  # quiet
        pass

    def _send(self, body: bytes, status=200, ctype="text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            q = parse_qs(u.query).get("q", [""])[0]
            self._send(render_index(q))
        elif u.path.startswith("/review/"):
            self._send(render_review(u.path.split("/review/", 1)[1]))
        else:
            self._send(page("404", "<p>not found</p>"), status=404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/review":
            self._send(b'{"error":"unknown"}', 404, "application/json")
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as e:
            self._send(json.dumps({"error": f"bad json: {e}"}).encode(), 400,
                       "application/json")
            return
        sha = (data.get("sha1_git") or "").strip()
        if len(sha) != 40:
            self._send(b'{"error":"bad sha1_git"}', 400, "application/json")
            return
        record = {
            "schema": SCHEMA,
            "subject": {"sha1_git": sha,
                        "swhid": f"swh:1:cnt:{sha}",
                        "filename": data.get("filename", "")},
            "reviewer": {"kind": "human", "id": self.reviewer_id},
            "human": {
                "is_cobol": data.get("is_cobol", ""),
                "agreement": data.get("agreement", ""),
                "dialect_family": data.get("dialect_family", ""),
                "domain": data.get("domain", ""),
                "source_format": data.get("source_format", ""),
                "origin_url": (data.get("origin_url", "") or "").strip(),
                "notes": data.get("notes", ""),
            },
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time())),
        }
        try:
            path = save_review(record)
        except Exception as e:
            self._send(json.dumps({"error": str(e)}).encode(), 500, "application/json")
            return
        self._send(json.dumps({"ok": True, "path": str(path.relative_to(ROOT))}).encode(),
                   200, "application/json")


def main() -> None:
    ap = argparse.ArgumentParser(description="COBOL sample review/annotation server.")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--reviewer", default=None, help="reviewer id (default: $USER)")
    args = ap.parse_args()

    Handler.reviewer_id = args.reviewer or getpass.getuser() or "anon"
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    n = sum(1 for _ in REPORTS_DIR.glob("*.json")) if REPORTS_DIR.is_dir() else 0
    print(f"COBOL review server: http://{args.host}:{args.port}/  "
          f"({n} reports, reviewer={Handler.reviewer_id})")
    print(f"reviews -> {REVIEWS_DIR.relative_to(ROOT)}/<sha>/")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
