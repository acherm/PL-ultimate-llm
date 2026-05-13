#!/usr/bin/env python3
"""Generate a ranked review queue of unattributed file extensions.

Input:
  - data/derived/swh_extensions_popularity.csv  (SWH-MSR-ARV, aggregated;
                                                  see docs/citations.md)
  - data/derived/pl_taxonomy/ext_summary.csv    (what we currently claim)

Output:
  - data/derived/extension_review_queue.csv

Each row carries: extension, SWH occurrence counts, current PL claimants
(if any), an auto-suggested heuristic label (just a guess), and a priority
score. Higher priority = "more present in SWH and least claimed by us" — these
are the extensions reviewers should look at first.

The auto-suggested label is a hint, not a decision. The point is to *rank* the
work, not to do the labelling.

Vocabulary lives in `docs/extension_labels.md`. Reviewers pick from there.
"""

from __future__ import annotations
import argparse
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SWH_POP_CSV = ROOT / "data" / "derived" / "swh_extensions_popularity.csv"
EXT_SUMMARY_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "ext_summary.csv"
OUT_CSV = ROOT / "data" / "derived" / "extension_review_queue.csv"

# Heuristic categorisations — every label here MUST appear in
# docs/extension_labels.md too. These are *suggestions* the queue uses to seed
# the reviewer's choice; the reviewer is free to override.
HINT_LABELS = {
    "binary:image":    {"png","jpg","jpeg","gif","svg","webp","tga","bmp","ico","tif","tiff","psd","ai","heic","avif"},
    "binary:audio":    {"mp3","wav","ogg","aac","m4a","flac","wma","opus","mid","midi"},
    "binary:video":    {"mp4","avi","mov","flv","swf","wmv","mkv","webm","mpg","mpeg"},
    "binary:font":     {"ttf","otf","woff","woff2","eot"},
    "binary:archive":  {"zip","tar","gz","bz2","xz","7z","rar","tgz","tbz2","zst","lz","lzma"},
    "binary:executable": {"exe","dll","so","dylib","msi","app","apk","ipa","com","bin","o","class","pyc","pyo","jar","wasm","dex"},
    "binary:db":       {"db","sqlite","sqlite3","mdb","accdb","fdb","rdb"},
    "binary:other":    {"pdf","doc","docx","xls","xlsx","ppt","pptx","odt","ods","odp"},
    "data:json-like":  {"json","jsonl","ndjson","jsonc","geojson","topojson"},
    "data:xml-like":   {"xml","xsd","xsl","xslt","rdf","wsdl","xhtml","plist","gml","sgml"},
    "data:yaml":       {"yaml","yml"},
    "data:csv-tsv":    {"csv","tsv","psv"},
    "data:config":     {"ini","conf","cfg","toml","properties","env"},
    "docs":            {"md","markdown","rst","adoc","asciidoc","org","tex","rtf","epub","html","htm"},
    "lock/cache":      {"lock","lockfile","cache","tmp","bak","swp","old","orig","tmpconfig"},
    "build-artifact":  {"o","obj","out","log","map","pdb","info","tlog","cache","pack","idx","manifest"},
    "model/data":      {"npy","npz","pkl","pickle","h5","hdf5","onnx","pb","tflite","ckpt"},
    "license/manifest": {"license","readme","copying","authors","contributors"},
}

# Reverse index: ext_no_dot -> label
_LABEL_LOOKUP: dict[str, str] = {}
for label, exts in HINT_LABELS.items():
    for e in exts:
        # First label wins on conflict — order in HINT_LABELS is the priority.
        _LABEL_LOOKUP.setdefault(e.lower(), label)


def suggest_label(ext: str) -> str:
    e = ext.lstrip(".").lower()
    if e in _LABEL_LOOKUP:
        return _LABEL_LOOKUP[e]
    # Numeric-only extensions are usually section / version numbers.
    if e.isdigit():
        return "numeric-suffix"
    # SHA-like extensions (32+ hex chars) are content-addressable filenames.
    if len(e) >= 32 and all(c in "0123456789abcdef" for c in e):
        return "sha-filename"
    return "unknown"


def priority_score(total_occ: int, last_year: int | None, current_claimant_count: int) -> float:
    """Rank: high SWH popularity + low current claim coverage = high priority.

    Score is log10(total_occ) minus 1.0 per claimant (so an ext with even one
    claim drops one rank-tier), plus a small recency bonus.
    """
    base = math.log10(max(total_occ, 1))
    base -= 1.0 * current_claimant_count
    if last_year is not None and last_year >= 2020:
        base += 0.3
    return base


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--min-occurrences", type=int, default=10_000,
                   help="Only include extensions with at least this many SWH occurrences (default: %(default)s).")
    p.add_argument("--max-rows", type=int, default=5000,
                   help="Top N rows to write (default: %(default)s).")
    args = p.parse_args()

    if not SWH_POP_CSV.exists():
        raise SystemExit(f"ERROR: {SWH_POP_CSV} missing. Run the popularity derivation first.")

    # Load taxonomy claimants per ext + flag whether the ext is "well-attributed"
    # (≥1 primary claim from an authoritative upstream source — Linguist or Pygments).
    # These don't need review.
    claimants_per_ext: dict[str, list[str]] = {}
    if EXT_SUMMARY_CSV.exists():
        for r in csv.DictReader(open(EXT_SUMMARY_CSV)):
            names = (r.get("primary_claimants") or "").split(";")
            names = [n.strip() for n in names if n.strip()]
            claimants_per_ext[r["ext"]] = names

    EXT_CLAIM_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "ext_claim.csv"
    well_attributed_exts: set[str] = set()
    if EXT_CLAIM_CSV.exists():
        AUTH = {"linguist", "pygments"}
        for c in csv.DictReader(open(EXT_CLAIM_CSV)):
            if c.get("strength") == "primary" and c.get("source") in AUTH:
                well_attributed_exts.add(c["ext"])

    # Build queue rows. Skip extensions that are already well-attributed by an
    # authoritative upstream source — they don't need manual review.
    queue: list[dict] = []
    skipped_well_attributed = 0
    with SWH_POP_CSV.open() as f:
        for r in csv.DictReader(f):
            ext = r["extension"]
            if not ext.startswith("."):
                continue
            total = int(r["total_occ"] or 0)
            if total < args.min_occurrences:
                continue
            ext_lc = ext.lower()
            if ext_lc in well_attributed_exts:
                skipped_well_attributed += 1
                continue
            recent = int(r["recent_occ"] or 0)
            fy = int(r["first_year"]) if r["first_year"] else None
            ly = int(r["last_year"]) if r["last_year"] else None
            claimants = claimants_per_ext.get(ext_lc) or claimants_per_ext.get(ext) or []
            queue.append({
                "ext_canonical": ext_lc,
                "ext_raw": ext,
                "total_occ": total,
                "recent_occ": recent,
                "first_year": fy or "",
                "last_year": ly or "",
                "n_current_claimants": len(claimants),
                "current_claimants": "; ".join(claimants),
                "review_status": "pending",
                "suggested_label": suggest_label(ext),
                "priority_score": priority_score(total, ly, len(claimants)),
            })

    # Case-aggregate one more time (across rows with same lowercase ext)
    by_ext: dict[str, dict] = {}
    for q in queue:
        k = q["ext_canonical"]
        prev = by_ext.get(k)
        if prev is None:
            by_ext[k] = q
        else:
            prev["total_occ"] += q["total_occ"]
            prev["recent_occ"] += q["recent_occ"]
            # Track that this was an aggregation
            prev["ext_raw"] = f"{prev['ext_raw']},{q['ext_raw']}"
            # Recompute score
            prev["priority_score"] = priority_score(
                prev["total_occ"],
                int(prev["last_year"]) if prev["last_year"] else None,
                prev["n_current_claimants"],
            )

    rows = sorted(by_ext.values(), key=lambda x: -x["priority_score"])[: args.max_rows]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "ext_canonical","ext_raw","total_occ","recent_occ",
            "first_year","last_year",
            "n_current_claimants","current_claimants",
            "review_status","suggested_label","priority_score",
        ])
        w.writeheader()
        for r in rows:
            r["priority_score"] = f"{r['priority_score']:.2f}"
            w.writerow(r)

    print(f"Wrote {OUT_CSV}: {len(rows):,} extensions (min_occurrences={args.min_occurrences:,}, max_rows={args.max_rows:,}).")
    print(f"Skipped {skipped_well_attributed} extension(s) already well-attributed (≥1 primary claim from Linguist or Pygments).")
    # Quick distribution summary
    from collections import Counter
    label_counts = Counter(r["suggested_label"] for r in rows)
    print("\nSuggested-label distribution (top 10):")
    for lab, n in label_counts.most_common(10):
        print(f"  {lab:25s} {n:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
