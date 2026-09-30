"""Tail census — size the rare `.m` notations with a two-phase stratified design.

The judged frames (U, R ranks ≤ 1 000) hold only ~35 files outside
Objective-C/MATLAB, too few to size Wolfram, MUMPS, Magma or Mercury. Every
*fetched* content, however, carries a free label from our reclassifier. So:

  phase 1  all fetched contents of a frame (U ranks ≤ 10 000, R ranks ≤ 3 000),
           stratified by our rules: MAIN (Objective-C or MATLAB-family) vs TAIL
           (anything else, abstentions included);
  phase 2  the TAIL stratum is judged in full (a census, both judges); the MAIN
           stratum keeps its random subsample of judged files (ranks ≤ 1 000).

`analysis.py` (section M) combines them: p̂(c) = Σ_h W_h · p̂_h(c), which is
unbiased whatever the quality of the stratifying rules — rules that miss tail
files only move them into the MAIN stratum, where the judged subsample catches
them at their true rate. Added after the pre-registration (disclosed there).

    python3 -m tools.m.study --label            # free labels on everything fetched
    python3 -m tools.m.tail --select            # → data/derived/m_study/tail_worklist.csv
    python3 -m tools.m.tail --judge             # both judges on the tail stratum
"""

from __future__ import annotations

import argparse
import csv
import os

from tools.m.analysis import N_JUDGED, coarse
from tools.m.data import STUDY, load
from tools.m.study import PRIMARY_MODEL, SECOND_MODEL, do_judge

WORKLIST = STUDY / "tail_worklist.csv"
MAX_RANK = {"U": 10000, "R": 3000}
MAIN = {"objective-c", "matlab-family"}


def stratum(rec) -> str:
    return "main" if coarse(rec.labels["ours"]["lang"]) in MAIN else "tail"


def phase1(recs, frame: str):
    """All fetched + labelled contents of a frame, with their rank."""
    out = []
    for r in recs.values():
        rank = r.u_rank if frame == "U" else r.d_rank
        if rank is not None and rank <= MAX_RANK[frame] and r.labels is not None:
            out.append((rank, r))
    return sorted(out, key=lambda x: x[0])


def select():
    recs = load(with_reviews=False)
    rows = []
    for frame in ("U", "R"):
        p1 = phase1(recs, frame)
        tail = [(k, r) for k, r in p1 if stratum(r) == "tail"]
        new = [(k, r) for k, r in tail if k > N_JUDGED]
        print(f"{frame}: phase-1 {len(p1)} fetched · tail stratum {len(tail)} "
              f"({100 * len(tail) / max(len(p1), 1):.1f} %) · to judge beyond rank {N_JUDGED}: {len(new)}")
        rows += [{**r.row, "tail_frame": frame, "tail_rank": k} for k, r in new]
    with WORKLIST.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["sha1_git"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {WORKLIST} ({len(rows)} contents)")


def judge(workers: int, retry_failed: bool = False):
    rows = list(csv.DictReader(WORKLIST.open(encoding="utf-8")))
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY not set (source .openrouter_key)")
    do_judge(0, PRIMARY_MODEL, workers, 45.0, targets=rows, retry_failed=retry_failed)
    do_judge(0, SECOND_MODEL, workers, 20.0, targets=rows, retry_failed=retry_failed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--select", action="store_true")
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args()
    if a.select:
        select()
    if a.judge:
        judge(a.workers, a.retry_failed)


if __name__ == "__main__":
    main()
