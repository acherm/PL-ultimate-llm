"""Prototype: a case-aware extension→PL claim for COBOL.

The production taxonomy folds extension case (`_norm_ext` lower-cases), so
`.CBL` and `.cbl` collapse to a single `pl/cobol` claim keyed on `.cbl`. The
study shows the two casings index *different populations*, so folding drops a
real signal (cf. the documented `.R` vs `.r` coverage fix in
`docs/SWH_EXTENSIONS_DECISIONS.md`).

This prototype does NOT modify the production pipeline. It:
  1. reads the case-preserving SWH extension counts + the current lowercase
     COBOL claims,
  2. emits a case-aware claim table (`.CBL` and `.cbl` as distinct rows, each
     → pl/cobol, with a `casing` column, SWH occurrence counts, and a
     study-derived `population_hint`),
  3. prints the before/after and the minimal `_norm_ext` change it implies.

Run:  python3 -m tools.cobol.case_aware_mapping
Out:  data/derived/cobol_study/ext_claim_case_aware_prototype.csv
"""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

from .common import ROOT, STUDY_DIR

POP_CSV = ROOT / "data" / "derived" / "swh_extensions_popularity.csv.gz"
EXT_CLAIM = ROOT / "data" / "derived" / "pl_taxonomy" / "ext_claim.csv"
OUT = STUDY_DIR / "ext_claim_case_aware_prototype.csv"

# Extensions whose casing is semantically significant (this study's finding).
# The general rule the pipeline should adopt: keep casing for members of this
# set instead of folding to lowercase.
CASE_SIGNIFICANT = {".cbl"}

# Population hints distilled from the study (§4.7 of docs/cobol_swh_study.md).
POPULATION_HINT = {
    ".CBL": "enterprise/mainframe-leaning (study: ~83% healthcare/ORCA, "
            "~96% production-like, ~90% GnuCOBOL)",
    ".cbl": "education/hobbyist-leaning (study: ~36% education-tutorial, "
            "~39% student-grade, diverse domains)",
}


def swh_counts_for(base_ext: str) -> dict[str, int]:
    """{exact-cased ext -> total_occ} for all casings of base_ext (e.g. .cbl)."""
    want = base_ext.lower()
    out: dict[str, int] = {}
    if not POP_CSV.exists():
        return out
    with gzip.open(POP_CSV, "rt", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ext = row["extension"]
            if ext.lower() == want:
                try:
                    out[ext] = int(row["total_occ"])
                except (ValueError, KeyError):
                    out[ext] = 0
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def current_cobol_claims() -> list[dict]:
    rows = []
    if EXT_CLAIM.exists():
        with EXT_CLAIM.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("pl_id") == "pl/cobol":
                    rows.append(r)
    return rows


def main() -> None:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    claims = current_cobol_claims()
    claim_exts = sorted({c["ext"] for c in claims})
    print(f"current pl/cobol claims (folded, lowercase): {claim_exts}")

    counts = swh_counts_for(".cbl")
    total = sum(counts.values())
    print(f"\nSWH occurrences by exact casing of .cbl ({total:,} total):")
    for ext, n in counts.items():
        share = 100 * n / total if total else 0
        print(f"  {ext:6} {n:>9,}  ({share:4.1f}%)   {'<- case-significant' if ext.lower() in CASE_SIGNIFICANT else ''}")

    # Build the case-aware prototype rows: one per casing variant with >0 occ.
    # Rare mixed-case (<0.1%) fold into the dominant lowercase claim.
    rows_out = []
    minor = 0
    for ext, n in counts.items():
        share = n / total if total else 0
        if ext in POPULATION_HINT and share >= 0.001:
            rows_out.append({
                "pl_id": "pl/cobol",
                "ext": ext,                  # case PRESERVED
                "casing": "as-seen",
                "swh_total_occ": n,
                "population_hint": POPULATION_HINT[ext],
                "source": "cobol-swh-study",
                "evidence": "docs/cobol_swh_study.md §4.7",
            })
        else:
            minor += n                       # rare mixed-case → fold

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pl_id", "ext", "casing",
                                          "swh_total_occ", "population_hint",
                                          "source", "evidence"])
        w.writeheader()
        w.writerows(rows_out)

    print(f"\nwrote {len(rows_out)} case-aware claim rows -> {OUT}"
          f"  ({minor:,} rare mixed-case occ folded into lowercase)")
    print("\nProposed minimal pipeline change (tools/build_pl_taxonomy.py::_norm_ext):")
    print("  # keep casing for members of a CASE_SIGNIFICANT allowlist")
    print("  return tok if tok in CASE_SIGNIFICANT else tok.lower()")
    print("Then match SWH's case-preserved extensions WITHOUT lower-casing for")
    print("those keys, so .CBL and .cbl carry distinct claims + population hints.")


if __name__ == "__main__":
    main()
