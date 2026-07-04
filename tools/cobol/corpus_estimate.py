"""Archive-scale contamination estimate: run the content reclassifier over a
uniform random sample of the full COBOL extension corpus.

Unlike the study worklists (which excluded `WBC_*_FOO`), this samples the full
union WITH the synthetic noise, so the label distribution is an unbiased
estimate of what the `.cbl`/`.CBL` extension space actually contains.

Fetch (cached, rate-limit self-pacing) + classify (zero API). Resumable:
progress is appended to a JSONL, and already-classified contents are skipped.

    python3 -m tools.cobol.corpus_estimate --worklist worklist_1k.csv   # run
    python3 -m tools.cobol.corpus_estimate --report                     # aggregate anytime
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

from . import reclassify as rc
from .common import STUDY_DIR, fetch_content
from .reclassify import COBOL_LABELS

RESULTS = STUDY_DIR / "corpus_estimate.jsonl"


def done_shas() -> set[str]:
    out = set()
    if RESULTS.exists():
        for line in RESULTS.read_text(encoding="utf-8").splitlines():
            try:
                out.add(json.loads(line)["sha1_git"])
            except Exception:
                continue
    return out


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Point estimate + Wilson 95% CI for a proportion (as percentages)."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return 100 * p, 100 * max(0, centre - half), 100 * min(1, centre + half)


def report() -> None:
    rows = [json.loads(l) for l in RESULTS.read_text(encoding="utf-8").splitlines()] \
        if RESULTS.exists() else []
    n = len(rows)
    if not n:
        print("no results yet.")
        return
    labels = Counter(r["label"] for r in rows)
    n_cobol = sum(r["is_cobol"] for r in rows)
    n_noncobol = n - n_cobol
    print(f"=== corpus contamination estimate (n={n} classified) ===\n")
    p, lo, hi = wilson(n_noncobol, n)
    print(f"NON-COBOL (contamination): {n_noncobol}/{n} = {p:.1f}%  (95% CI {lo:.1f}–{hi:.1f}%)")
    pc, lc, hc = wilson(n_cobol, n)
    print(f"COBOL:                     {n_cobol}/{n} = {pc:.1f}%  (95% CI {lc:.1f}–{hc:.1f}%)\n")
    print("by label:")
    for lab, k in labels.most_common():
        pp, ll, hh = wilson(k, n)
        tag = "cobol" if lab in COBOL_LABELS else "NON-cobol"
        print(f"  {lab:22} {k:5}  {pp:5.1f}%  (CI {ll:4.1f}–{hh:4.1f}%)  [{tag}]")


def run(worklist: Path) -> None:
    rows = list(csv.DictReader(worklist.open(encoding="utf-8")))
    done = done_shas()
    todo = [r for r in rows if r["sha1_git"] not in done]
    print(f"worklist {len(rows)} | done {len(done)} | to do {len(todo)}")
    n_fetch = 0
    with RESULTS.open("a", encoding="utf-8") as out:
        for i, r in enumerate(todo, 1):
            sha, name = r["sha1_git"], r["name"]
            try:
                c = fetch_content(r["swhid"], filename=name, polite_delay=0.0)
                n_fetch += (0 if c.from_cache else 1)
                res = rc.classify(name, c.raw)
            except Exception as e:
                print(f"[{i}/{len(todo)}] {sha[:10]} ERROR: {e}")
                continue
            out.write(json.dumps({"sha1_git": sha, "name": name,
                                  "label": res["label"],
                                  "is_cobol": res["is_cobol"]}) + "\n")
            out.flush()
            if i % 25 == 0:
                print(f"[{i}/{len(todo)}] {sha[:10]} {name[:26]:28} -> {res['label']}"
                      f"  (fetched {n_fetch})")
    print(f"done: classified {len(todo)} more ({n_fetch} network fetches)")
    report()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worklist", default=str(STUDY_DIR / "worklist_1k.csv"))
    ap.add_argument("--report", action="store_true", help="aggregate only")
    args = ap.parse_args()
    if args.report:
        report()
    else:
        run(Path(args.worklist))


if __name__ == "__main__":
    main()
