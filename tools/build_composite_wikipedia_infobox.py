#!/usr/bin/env python3
"""Merge a primary `wikipedia_infobox` snapshot (typically the new
structured-wikipedia extraction) with a legacy fallback snapshot
(mwparserfromhell over the MediaWiki API). Per-QID, pick whichever
source recovered more dot-prefixed extension tokens; tiebreak to the
primary. Writes a single composite JSONL that downstream
`build_pl_taxonomy.py` will pick up via its `wikipedia_infobox.*.jsonl`
latest-snapshot glob.

Why this exists:
  - The HF structured dump does not include articles created/renamed
    after its freeze date; those QIDs come back as `parser=missing` and
    we need the legacy snapshot to cover them.
  - A small number of multi-`<br/>`-section infoboxes are flattened by
    the upstream Wikimedia parser into a single scalar; on those
    specific articles the legacy regex-over-wikitext does better. The
    selection rule below picks the legacy version *only when* it
    actually carries more dot-prefixed extensions, so we avoid swapping
    in a worse-on-noise legacy record for an article where structured
    is strictly cleaner.

Schema: composite rows are a superset of the legacy schema. We add:
  - `infobox_source`: "structured" | "legacy" | "neither"
  - `composite_decision`: short reason string
The original primary fields (`wikipedia_name`, `wikipedia_url`,
`page_id`, `revision_id`, `parser`) ride along when the chosen source
provides them; missing when it doesn't.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def load(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            qid = rec.get("qid")
            if qid:
                out[qid] = rec
    return out


def dot_exts(rec: dict | None) -> set[str]:
    """Set of dot-prefixed extension tokens this record actually carries.
    We use this — not `wikipedia_extensions` — for the selection rule,
    because both parsers can emit noise tokens (section-header words,
    prose like 'binary' or 'split'). Dot-prefixed-only is the apples-to-
    apples signal."""
    if not rec:
        return set()
    out: set[str] = set()
    for h in rec.get("infobox_hits") or []:
        for p in h.get("parsed") or []:
            if (p.get("raw_line") or "").lstrip().startswith("."):
                v = p.get("value")
                if v:
                    out.add(v)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--primary", required=True, type=Path,
                   help="Primary snapshot (typically structured-wikipedia)")
    p.add_argument("--fallback", required=True, type=Path,
                   help="Legacy snapshot used when primary has zero "
                        "extensions OR fewer extensions than fallback")
    p.add_argument("--out", required=True, type=Path,
                   help="Composite output path (e.g. "
                        "data/raw/wikipedia_infobox.YYYY-MM-DD.jsonl)")
    args = p.parse_args()

    primary = load(args.primary)
    fallback = load(args.fallback)

    all_qids = sorted(set(primary) | set(fallback))
    print(f"[load] primary  : {args.primary.name} → {len(primary)} entries",
          flush=True)
    print(f"[load] fallback : {args.fallback.name} → {len(fallback)} entries",
          flush=True)
    print(f"[merge] total QIDs in union: {len(all_qids)}", flush=True)

    counts = {"structured": 0, "legacy": 0, "neither": 0}
    decisions: dict[str, int] = {}
    examples_legacy_won: list[tuple[str, str, int, int]] = []
    examples_structured_won: list[tuple[str, str, int, int]] = []

    n_primary_with_exts = 0
    n_fallback_with_exts = 0

    with args.out.open("w", encoding="utf-8") as f:
        for qid in all_qids:
            p_rec = primary.get(qid)
            f_rec = fallback.get(qid)
            p_exts = dot_exts(p_rec)
            f_exts = dot_exts(f_rec)
            if p_exts:
                n_primary_with_exts += 1
            if f_exts:
                n_fallback_with_exts += 1

            # Selection rule. Tiebreak to primary so we prefer the cleaner
            # extraction when neither side has more signal.
            if len(p_exts) >= len(f_exts) and p_rec is not None:
                chosen = dict(p_rec)
                src = "structured" if p_exts else (
                    "structured" if f_rec is None else "neither"
                )
                if not p_exts and not f_exts:
                    src = "neither"
                reason = (f"primary≥fallback ({len(p_exts)} vs {len(f_exts)})"
                          if p_exts or f_exts else "both-empty")
            elif f_rec is not None:
                chosen = dict(f_rec)
                src = "legacy"
                reason = f"fallback>primary ({len(f_exts)} vs {len(p_exts)})"
                examples_legacy_won.append((qid, chosen.get("label") or "",
                                            len(p_exts), len(f_exts)))
            else:
                # Primary exists but is empty; no fallback.
                chosen = dict(p_rec) if p_rec is not None else {"qid": qid}
                src = "neither"
                reason = "no-data"

            if src == "structured" and p_exts and (not f_exts or len(p_exts) > len(f_exts)):
                examples_structured_won.append((qid, chosen.get("label") or "",
                                                len(p_exts), len(f_exts)))

            chosen["infobox_source"] = src
            chosen["composite_decision"] = reason
            counts[src] = counts.get(src, 0) + 1
            decisions[reason] = decisions.get(reason, 0) + 1

            f.write(json.dumps(chosen, ensure_ascii=False) + "\n")

    print()
    print(f"[done] wrote {args.out}", flush=True)
    print(f"  source breakdown:")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {k:<12} {v}")
    print(f"  per-QID coverage:")
    print(f"    primary  with ≥1 dot-ext: {n_primary_with_exts}")
    print(f"    fallback with ≥1 dot-ext: {n_fallback_with_exts}")
    print()
    print(f"  top 10 QIDs where legacy won (strictly more dot-prefixed exts):")
    for qid, label, np_, nf in sorted(examples_legacy_won,
                                       key=lambda x: -(x[3] - x[2]))[:10]:
        print(f"    {qid:<11} {label:<40} primary={np_} fallback={nf}")
    print()
    print(f"  top 10 QIDs where structured won outright:")
    for qid, label, np_, nf in sorted(examples_structured_won,
                                       key=lambda x: -(x[2] - x[3]))[:10]:
        print(f"    {qid:<11} {label:<40} primary={np_} fallback={nf}")


if __name__ == "__main__":
    main()
