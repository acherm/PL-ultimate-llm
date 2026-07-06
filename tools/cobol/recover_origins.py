"""Recover origin + anchor for real-COBOL samples via the repo's existing
GitHub matcher (`tools/swh_extension_mining.py::qualify_via_github`).

For each sampled content we search GitHub by filename, keep a byte-length
match, and — crucially — confirm the GitHub file's `sha1_git` equals OUR
target content sha (so the recovered origin is byte-identical, not just a
same-name/same-length coincidence). Emits a qualified SWHID
`swh:1:cnt:…;origin=…;anchor=swh:1:rev:…;path=…` the review UIs render.

Subset: judge-confirmed COBOL contents (from `reports/`), deduped by sha.
Resumable: appends to `data/derived/cobol_study/origins.jsonl`; already-done
shas are skipped. Rate-limited by GitHub code search (~10/min; the underlying
tool self-throttles), so a few hundred files take ~an hour.

    OPENROUTER unnecessary. Needs `gh auth` (a GitHub token).
    python3 -m tools.cobol.recover_origins --limit 150
    python3 -m tools.cobol.recover_origins --report
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/ on path
from swh_extension_mining import qualify_via_github, _gh_token  # noqa: E402

from .common import STUDY_DIR  # noqa: E402

REPORTS = STUDY_DIR / "reports"
OUT = STUDY_DIR / "origins.jsonl"


def subset() -> list[dict]:
    """Deduped (sha, filename, length) for judge-confirmed COBOL contents."""
    out: dict[str, dict] = {}
    for p in REPORTS.glob("*.json"):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        j = r.get("judge")
        v = j.get("verdict") if isinstance(j, dict) else None
        if not v or str(v.get("cobol_confirmed")).lower() != "true":
            continue
        sha = r["sample"]["sha1_git"]
        name = os.path.basename((r["sample"].get("filename") or "").lstrip("/"))
        length = r.get("content", {}).get("length")
        if sha and name and length:
            out.setdefault(sha, {"sha": sha, "filename": name, "length": int(length)})
    return sorted(out.values(), key=lambda d: d["filename"])


def done_shas() -> set[str]:
    s = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            try:
                s.add(json.loads(line)["sha"])
            except Exception:
                pass
    return s


def report() -> None:
    if not OUT.exists():
        print("no results yet."); return
    rows = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
    n = len(rows)
    conf = [r for r in rows if r.get("content_match")]
    anch = [r for r in conf if r.get("anchor")]
    from collections import Counter
    st = Counter(r["result"] for r in rows)
    print(f"=== origin recovery over {n} judged-COBOL contents ===")
    print(f"confirmed origin (byte-identical GitHub file): {len(conf)} = {100*len(conf)/n:.1f}%")
    print(f"  …of which with an anchor revision: {len(anch)}")
    print("outcomes:", dict(st.most_common()))
    print("\nsample recovered origins:")
    for r in conf[:15]:
        print(f"  {r['filename']:26} -> {r['origin']}"
              f"{' @'+r['anchor'][:20]+'…' if r.get('anchor') else ''}")


def run(limit: int | None) -> None:
    token = _gh_token()
    if not token:
        sys.exit("no GitHub token — run `gh auth login` first.")
    items = subset()
    done = done_shas()
    todo = [d for d in items if d["sha"] not in done]
    if limit:
        todo = todo[:limit]
    print(f"judged-COBOL contents: {len(items)} | done {len(done)} | this run {len(todo)}")
    conf = 0
    with OUT.open("a", encoding="utf-8") as out:
        for i, d in enumerate(todo, 1):
            sha, name, length = d["sha"], d["filename"], d["length"]
            rec = {"sha": sha, "filename": name, "length": length,
                   "result": "error", "content_match": False,
                   "origin": None, "anchor": None, "qualified": None, "notes": ""}
            try:
                res = qualify_via_github(name, length, token=token,
                                         max_candidates=5, verify_in_swh=False,
                                         file_ext=os.path.splitext(name)[1])
                rec["result"] = res.status
                rec["notes"] = res.notes[:120]
                # authoritative only if the GitHub file's sha == our target sha
                if res.content_swhid == f"swh:1:cnt:{sha}":
                    rec.update(content_match=True, origin=res.origin,
                               anchor=res.anchor, qualified=res.qualified)
                    conf += 1
                elif res.content_swhid:
                    rec["notes"] = f"length-matched but content differs ({res.content_swhid[:20]}…)"
            except Exception as e:
                rec["notes"] = f"{type(e).__name__}: {e}"[:120]
            out.write(json.dumps(rec) + "\n"); out.flush()
            if i % 10 == 0 or rec["content_match"]:
                flag = f" ✓ {rec['origin']}" if rec["content_match"] else ""
                print(f"[{i}/{len(todo)}] {name[:24]:26} {rec['result']}{flag}")
    print(f"\nthis run: {conf}/{len(todo)} confirmed origins")
    report()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    report() if args.report else run(args.limit)


if __name__ == "__main__":
    main()
