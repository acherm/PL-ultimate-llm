#!/usr/bin/env python3
"""Consensus over the review store: one row per reviewed content.

Facts stay in `reviews/<sha1_git>/*.json` (one immutable file per review,
docs/reviews.md); this derives `data/derived/review_consensus.csv` and can be
re-run under other rules without touching them. Each reviewer counts once
(their latest review, `reviewstore.latest_per_reviewer`).

Tiers
  gold          ≥ 2 humans, all giving the same label
  silver        exactly 1 human
  disputed      humans give different labels (kept: disagreement is data)
  machine-only  no human review, only LLM judges / tools

    python3 tools/build_review_consensus.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import reviewstore as RS  # noqa: E402

OUT = ROOT / "data" / "derived" / "review_consensus.csv"
FIELDS = ["sha1_git", "filename", "ext", "tier", "consensus_label", "n_human", "human", "n_llm", "llm",
          "llm_agree", "n_tool", "studies", "last_review_at"]


def row_for(sha: str, revs: list[dict]) -> dict:
    latest = [r for r in RS.latest_per_reviewer(revs) if (r.get("verdict") or {}).get("label")]
    by_kind = {k: [r for r in latest if (r.get("reviewer") or {}).get("kind") == k] for k in RS.REVIEWER_KINDS}
    human = {r["reviewer"]["id"]: r["verdict"]["label"] for r in by_kind["human"]}
    llm = {r["reviewer"]["id"]: r["verdict"]["label"] for r in by_kind["llm"]}
    labels = set(human.values())
    if not human:
        tier, label = "machine-only", ""
    elif len(labels) > 1:
        tier, label = "disputed", ""
    else:
        tier, label = ("gold" if len(human) >= 2 else "silver"), next(iter(labels))
    subj = next((r.get("subject") for r in revs if r.get("subject")), {}) or {}
    studies = sorted({(r.get("shown") or {}).get("study") for r in revs if (r.get("shown") or {}).get("study")})
    return {
        "sha1_git": sha, "filename": subj.get("filename", ""), "ext": subj.get("ext", ""), "tier": tier,
        "consensus_label": label, "n_human": len(human),
        "human": "; ".join(f"{k}={v}" for k, v in sorted(human.items())),
        "n_llm": len(llm), "llm": "; ".join(f"{k}={v}" for k, v in sorted(llm.items())),
        "llm_agree": (f"{sum(v == label for v in llm.values())}/{len(llm)}" if label and llm else ""),
        "n_tool": len(by_kind["tool"]), "studies": "; ".join(studies),
        "last_review_at": max((r.get("created_at") or "" for r in revs), default=""),
    }


def main() -> int:
    rows = [row_for(sha, revs) for sha, revs in sorted(RS.reviews_by_sha().items())]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    tiers = Counter(r["tier"] for r in rows)
    print(f"{len(rows)} reviewed contents → {OUT.relative_to(ROOT)}: "
          + ", ".join(f"{k} {tiers.get(k, 0)}" for k in ("gold", "silver", "disputed", "machine-only")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
