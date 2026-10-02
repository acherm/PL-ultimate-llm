#!/usr/bin/env python3
"""Build the Synid benchmark cases from the extension studies (README.md).

Writes `cases.csv` (one row per archived file, with the answers that count as
right) and `files.tar.xz` (the files' bytes, named by sha1_git, each verified
against it). Re-run only to release a new benchmark version: cases are frozen
so that results stay comparable across Synid versions.

    python3 benchmarks/synid/build_cases.py

Tiers
  gold    a human reviewed the file (blind audit of the .m study); the two LLM
          judges agree with the human on all of them
  silver  both LLM judges agree on the language (by-file and by-repository
          samples of the study, ranks ≤ 1000), no human review
"""

from __future__ import annotations

import csv
import io
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from tools import study_export as SE  # noqa: E402
from tools.m import audit as A  # noqa: E402
from tools.m.data import J1, J2, load  # noqa: E402
from tools.m.synid_assess import NO_REF, fam  # noqa: E402

VERSION = "synid-bench/1"
CASES = HERE / "cases.csv"
FILES = HERE / "files.tar.xz"
FIELDS = ["case_id", "tier", "ext", "sha1_git", "filename", "qualified_swhid", "expected", "expected_detail",
          "accept", "reference", "frame", "stratum", "weight", "tags"]

# Synid answers that count as right, per language-level label. Names Synid does
# not (yet) offer for `.m` are listed too, so that a future version gets credit.
ACCEPT = {
    "matlab-family": ["MATLAB"], "objective-c": ["Objective-C"], "mathematica-wolfram": ["Wolfram Language"],
    "mercury": ["Mercury"], "mumps-m": ["M"], "limbo": ["Limbo"], "muf": ["MUF"], "mason": ["Mason"],
    "magma": ["Magma"], "c-or-cpp": ["C", "C++"], "not-code": ["Text"], "other": [],
}
# Synid's candidates for `.m` (from Linguist), as of 9bc1c32
M_CANDIDATES = {"objective-c", "matlab-family", "mercury", "mumps-m", "mathematica-wolfram", "limbo", "muf", "mason"}


def tags(expected: str, raw: bytes) -> list[str]:
    t = []
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        t.append("non-utf8")
        text = raw.decode("utf-8", "replace")
    if expected == "matlab-family" and not re.search(r"(?m)^\s*%|^function|^!\w+", text):
        t.append("comment-free-matlab")          # nothing for Synid's MATLAB heuristics to see
    if expected == "objective-c" and re.search(r'@"[^"\n]*%', text):
        t.append("objc-format-string")           # `%` in @"…": the comment strategy took it for MATLAB
    if expected not in M_CANDIDATES and expected != "not-code":
        t.append("out-of-candidates")             # not among Synid's candidates for `.m`
    if text.count("\n") < 3:
        t.append("tiny")
    return t


def main() -> int:
    recs = load()
    queue = {d["sha1_git"]: d for d in A.queue()}
    gold = [r for r in recs.values() if r.sha in queue and r.human_latest() and r.lang("judge") and r.lang("judge2")
            and r.human()["language"] not in NO_REF]
    n_h = {}
    for r in gold:
        n_h[queue[r.sha]["stratum"]] = n_h.get(queue[r.sha]["stratum"], 0) + 1
    gold_shas = {r.sha for r in gold}
    silver = [r for r in recs.values() if (r.in_frame("U", 1000) or r.in_frame("R", 1000)) and r.sha not in gold_shas
              and r.lang("judge") and r.lang("judge2") and fam(r.lang("judge")) == fam(r.lang("judge2"))
              and fam(r.lang("judge")) != "none"]

    rows, buf = [], io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:xz") as tar:
        for tier, recs_t in (("gold", gold), ("silver", silver)):
            for r in sorted(recs_t, key=lambda r: r.sha):
                raw = SE.content_bytes("m", r.sha)
                if raw is None:
                    print(f"skip {r.sha[:12]}: bytes unavailable")
                    continue
                label = r.human()["language"] if tier == "gold" else r.lang("judge")
                exp = fam(label)
                frame = "+".join(f for f in ("U", "R") if r.in_frame(f, 1000)) or "audit"
                d = queue.get(r.sha)
                rows.append({
                    "case_id": f"m:{r.sha[:12]}", "tier": tier, "ext": ".m", "sha1_git": r.sha,
                    "filename": r.row.get("name", ""),
                    "qualified_swhid": SE.qualified_swhid(r.sha, r.row.get("origin"), r.row.get("path")),
                    "expected": exp, "expected_detail": label, "accept": ";".join(ACCEPT.get(exp, [])),
                    "reference": ("human:" + "+".join(r.human_reviewers()) if tier == "gold"
                                  else f"judges:{J1}+{J2}".replace("__", "/")),
                    "frame": frame, "stratum": d["stratum"] if (tier == "gold" and d) else "",
                    "weight": round(int(d["stratum_N"]) / n_h[d["stratum"]], 4) if (tier == "gold" and d) else "",
                    "tags": ";".join(tags(exp, raw)),
                })
                info = tarfile.TarInfo(r.sha)
                info.size = len(raw)
                tar.addfile(info, io.BytesIO(raw))
    with CASES.open("w", encoding="utf-8", newline="") as f:
        f.write(f"# {VERSION} — generated by benchmarks/synid/build_cases.py; see README.md\n")
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    FILES.write_bytes(buf.getvalue())
    by = {}
    for r in rows:
        by[r["tier"]] = by.get(r["tier"], 0) + 1
    print(f"{VERSION}: {len(rows)} cases {by} → {CASES.relative_to(ROOT)}, "
          f"{FILES.relative_to(ROOT)} ({len(buf.getvalue()) / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
