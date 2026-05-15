#!/usr/bin/env python3
"""Merge the pinned Wikidata + Wikipedia infobox snapshots into a reverse
index by extension. Debug / exploration artifact — not part of the
production taxonomy build. For PL-scoped integration see
build_pl_taxonomy.py; for non-PL items see build_external_extension_index.py.

Input:
  data/raw/wikidata_p1195.<date>.jsonl
  data/raw/wikipedia_infobox.<date>.jsonl

Output:
  data/derived/wikidata_wikipedia_by_extension.<date>.jsonl
  data/derived/wikidata_wikipedia_by_extension.<date>.summary.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "derived"


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--wikidata", required=True, help="wikidata_p1195.<date>.jsonl")
    p.add_argument("--wikipedia", default=None, help="wikipedia_infobox.<date>.jsonl")
    p.add_argument("--out-date", default=dt.date.today().isoformat())
    args = p.parse_args()

    wd_path = Path(args.wikidata)
    wp_path = Path(args.wikipedia) if args.wikipedia else None

    wd_records = load_jsonl(wd_path)
    print(f"[load] wikidata items: {len(wd_records)}", flush=True)

    wp_records = []
    if wp_path and wp_path.exists():
        wp_records = load_jsonl(wp_path)
        print(f"[load] wikipedia enriched items: {len(wp_records)}", flush=True)

    # ext -> qid -> entry
    index: dict[str, dict[str, dict]] = defaultdict(dict)

    for r in wd_records:
        qid = r["qid"]
        label = r["label"]
        for e in r.get("extensions", []):
            ext = e["value"].lower()
            entry = index[ext].setdefault(qid, {
                "qid": qid,
                "label": label,
                "sources": [],
                "wikidata": None,
                "wikipedia": None,
            })
            entry["sources"].append("wikidata") if "wikidata" not in entry["sources"] else None
            entry["wikidata"] = {
                "rank": e.get("rank"),
                "qualifiers": e.get("qualifiers", []),
                "enwiki_title": r.get("enwiki_title"),
                "instance_of": r.get("instance_of", []),
            }

    for r in wp_records:
        qid = r["qid"]
        label = r["label"]
        # Build a per-page ext -> first-seen note map across all infobox hits.
        ext_to_note: dict[str, str | None] = {}
        ext_to_raw: dict[str, str] = {}
        for hit in r.get("infobox_hits", []):
            for parsed in hit.get("parsed", []):
                ext = parsed["value"].lower()
                if ext not in ext_to_note:
                    ext_to_note[ext] = parsed.get("note")
                    ext_to_raw[ext] = parsed.get("raw_line", "")

        for ext, note in ext_to_note.items():
            entry = index[ext].setdefault(qid, {
                "qid": qid,
                "label": label,
                "sources": [],
                "wikidata": None,
                "wikipedia": None,
            })
            if "wikipedia" not in entry["sources"]:
                entry["sources"].append("wikipedia")
            entry["wikipedia"] = {
                "note": note,
                "raw_line": ext_to_raw[ext],
                "enwiki_title": r.get("enwiki_title"),
            }

    # Emit JSONL keyed by extension, sorted; flatten qid map to list.
    out_jsonl = DATA_DIR / f"wikidata_wikipedia_by_extension.{args.out_date}.jsonl"
    n_ext = 0
    n_ambig = 0
    polysemy: list[tuple[int, str]] = []
    with out_jsonl.open("w") as f:
        for ext in sorted(index.keys()):
            items_list = [
                {
                    "qid": v["qid"],
                    "label": v["label"],
                    "sources": v["sources"],
                    "wikidata": v["wikidata"],
                    "wikipedia": v["wikipedia"],
                }
                for v in sorted(index[ext].values(), key=lambda x: x["qid"])
            ]
            f.write(json.dumps({"extension": ext, "items": items_list}, ensure_ascii=False) + "\n")
            n_ext += 1
            if len(items_list) > 1:
                n_ambig += 1
            polysemy.append((len(items_list), ext))

    polysemy.sort(reverse=True)

    summary = {
        "snapshot_date": args.out_date,
        "extensions_total": n_ext,
        "extensions_polysemous": n_ambig,
        "top_polysemy": [{"extension": e, "items": n} for n, e in polysemy[:25]],
        "source_breakdown": _source_breakdown(index),
        "inputs": {
            "wikidata": str(wd_path),
            "wikipedia": str(wp_path) if wp_path else None,
        },
    }
    (DATA_DIR / f"wikidata_wikipedia_by_extension.{args.out_date}.summary.json").write_text(
        json.dumps(summary, indent=2)
    )

    print(f"[done] wrote {out_jsonl}", flush=True)
    print(f"       distinct extensions:    {n_ext}", flush=True)
    print(f"       polysemous (>1 item):   {n_ambig}", flush=True)
    if polysemy:
        print(f"       most-claimed ext:       .{polysemy[0][1]} by {polysemy[0][0]} items", flush=True)


def _source_breakdown(index: dict) -> dict:
    only_wd = only_wp = both = 0
    for ext, items in index.items():
        for v in items.values():
            srcs = set(v["sources"])
            if srcs == {"wikidata"}:
                only_wd += 1
            elif srcs == {"wikipedia"}:
                only_wp += 1
            elif srcs >= {"wikidata", "wikipedia"}:
                both += 1
    return {
        "item_extension_pairs": {
            "wikidata_only": only_wd,
            "wikipedia_only": only_wp,
            "both": both,
        },
    }


if __name__ == "__main__":
    sys.exit(main())
