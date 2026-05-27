#!/usr/bin/env python3
"""Compare two `wikipedia_infobox.<date>[.suffix].jsonl` snapshots — typically
the legacy mwparserfromhell extraction vs. the structured-wikipedia
extraction — and report per-source recall against Wikidata P1195 plus
per-PL recall gains/losses.

Usage:
  python3 tools/diff_wikipedia_infobox_sources.py \\
      --legacy     data/raw/wikipedia_infobox.2026-05-15.jsonl \\
      --structured data/raw/wikipedia_infobox.2026-05-24.structured.jsonl
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with path.open() as f:
        for line in f:
            rec = json.loads(line)
            qid = rec.get("qid")
            if qid:
                out[qid] = rec
    return out


def recall_vs_wikidata(snapshot: dict[str, dict]) -> tuple[int, int, int]:
    """Return (recovered, total_wd_exts, items_with_any_recall)."""
    recovered = total = items_recovered = 0
    for r in snapshot.values():
        wd = set(r.get("wikidata_extensions") or [])
        wp = set(r.get("wikipedia_extensions") or [])
        total += len(wd)
        recovered += len(wd & wp)
        if wd & wp:
            items_recovered += 1
    return recovered, total, items_recovered


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--legacy", required=True, type=Path,
                   help="Legacy wikipedia_infobox.*.jsonl (mwparserfromhell)")
    p.add_argument("--structured", required=True, type=Path,
                   help="structured-wikipedia wikipedia_infobox.*.structured.jsonl")
    p.add_argument("--top", type=int, default=25,
                   help="Show top-N biggest recall gains / losses (default: 25)")
    p.add_argument("--show-all-losses", action="store_true",
                   help="Print every item where legacy beat structured "
                        "(useful before retiring the legacy parser)")
    args = p.parse_args()

    legacy = load(args.legacy)
    structured = load(args.structured)

    shared = set(legacy) & set(structured)
    only_legacy = set(legacy) - set(structured)
    only_structured = set(structured) - set(legacy)

    print("=== Coverage ===")
    print(f"  legacy entries:     {len(legacy):>6}")
    print(f"  structured entries: {len(structured):>6}")
    print(f"  shared QIDs:        {len(shared):>6}")
    print(f"  only in legacy:     {len(only_legacy):>6}")
    print(f"  only in structured: {len(only_structured):>6}")

    legacy_box = sum(1 for r in legacy.values() if r.get("infobox_hits"))
    struct_box = sum(1 for r in structured.values() if r.get("infobox_hits"))
    print()
    print("=== Items with non-empty infobox_hits ===")
    print(f"  legacy:     {legacy_box:>6} / {len(legacy)}  ({legacy_box / max(len(legacy), 1):.1%})")
    print(f"  structured: {struct_box:>6} / {len(structured)}  ({struct_box / max(len(structured), 1):.1%})")

    # Per-row parser tag breakdown (structured side only).
    parser_counts: dict[str, int] = defaultdict(int)
    for r in structured.values():
        parser_counts[r.get("parser", "?")] += 1
    print()
    print("=== Parser tag breakdown (structured snapshot) ===")
    for k, v in sorted(parser_counts.items(), key=lambda x: -x[1]):
        print(f"  {k:<24} {v}")

    # Recall vs Wikidata.
    lr, lt, li = recall_vs_wikidata(legacy)
    sr, st, si = recall_vs_wikidata(structured)
    print()
    print("=== Recall of Wikidata P1195 extensions inside each Wikipedia snapshot ===")
    print(f"  legacy:     {lr:>5}/{lt} extensions  ({lr / max(lt, 1):.1%})  "
          f"items with ≥1 recall: {li}/{len(legacy)}")
    print(f"  structured: {sr:>5}/{st} extensions  ({sr / max(st, 1):.1%})  "
          f"items with ≥1 recall: {si}/{len(structured)}")

    # Per-QID gains/losses on shared entries.
    gains = []
    losses = []
    for qid in shared:
        l = legacy[qid]
        s = structured[qid]
        l_ext = set(l.get("wikipedia_extensions") or [])
        s_ext = set(s.get("wikipedia_extensions") or [])
        gained = s_ext - l_ext
        lost = l_ext - s_ext
        if gained:
            gains.append((len(gained), qid, l.get("label"), sorted(gained)))
        if lost:
            losses.append((len(lost), qid, l.get("label"), sorted(lost)))

    print()
    print(f"=== Top {args.top} gains: structured > legacy ===")
    for n, qid, label, exts in sorted(gains, reverse=True)[: args.top]:
        print(f"  +{n:>2}  {qid:<10}  {label:<40}  {exts[:10]}")

    print()
    losses_sorted = sorted(losses, reverse=True)
    print(f"=== Top {args.top} losses: legacy > structured  "
          f"(total items with regressions: {len(losses)}) ===")
    show = losses_sorted if args.show_all_losses else losses_sorted[: args.top]
    for n, qid, label, exts in show:
        print(f"  -{n:>2}  {qid:<10}  {label:<40}  {exts[:10]}")

    # Headline numbers.
    n_qids_gained = len(gains)
    n_qids_lost = len(losses)
    print()
    print("=== Headline ===")
    print(f"  QIDs where structured RECOVERS extensions: {n_qids_gained}")
    print(f"  QIDs where structured REGRESSES:           {n_qids_lost}")
    print(f"  net recall delta (extensions):             "
          f"{sr - lr:+d}  ({sr - lr:+d} / {st})")


if __name__ == "__main__":
    main()
