#!/usr/bin/env python3
"""Derive `data/derived/swh_extensions_popularity.csv` from the SWH-MSR-ARV dataset.

The **SWH-MSR-ARV dataset** is the per-extension SWH occurrence table
published with:

    Adèle Desmazières, Roberto Di Cosmo, Valentin Lorentz.
    "50 Years of Programming Language Evolution through the Software Heritage
     looking glass." MSR 2025: 372-383.

See `docs/citations.md`.

Input:
  `nb_extensions_alphanum.csv` (the SWH-MSR-ARV file) — a wide table where
  each row is one file extension and columns are year-by-year occurrence
  counts in the Software Heritage archive (plus a `-1` column for undated
  files).

Output:
  A narrow per-extension aggregate at
  `data/derived/swh_extensions_popularity.csv`:

      extension, total_occ, recent_occ, undated_occ, first_year, last_year

  - `total_occ`   = sum across all years + the `-1` column
  - `recent_occ`  = sum across years 2019–2023 (proxy for "still alive")
  - `undated_occ` = the `-1` column verbatim
  - `first_year`  = earliest year with a positive count (empty if undated only)
  - `last_year`   = latest year with a positive count

The output file is intentionally gitignored — it's 77 MB and trivially
regenerable from this script. Track the script, not the artefact.

Usage
-----
    python3 tools/build_swh_ext_popularity.py [--src PATH]

Defaults to `/Users/mathieuacher/SANDBOX/PL-roberto/nb_extensions_alphanum.csv`,
which is where the SWH-MSR-ARV file ships in the original development setup.
Override `--src` if you keep it elsewhere.
"""

from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path("/Users/mathieuacher/SANDBOX/PL-roberto/nb_extensions_alphanum.csv")
OUT_CSV = ROOT / "data" / "derived" / "swh_extensions_popularity.csv"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--src", default=str(DEFAULT_SRC),
                        help="Path to the SWH-MSR-ARV nb_extensions_alphanum.csv (default: %(default)s)")
    parser.add_argument("--out", default=str(OUT_CSV),
                        help="Output path (default: %(default)s)")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--memory-limit", default="6GB")
    args = parser.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    if not src.exists():
        raise SystemExit(
            f"ERROR: source CSV not found at {src}.\n"
            "The SWH-MSR-ARV dataset (Desmazières/Di Cosmo/Lorentz, MSR 2025) "
            "ships separately. Obtain `nb_extensions_alphanum.csv` from the "
            "authors and pass --src or place it at the default path."
        )

    try:
        import duckdb  # type: ignore
    except ImportError:
        raise SystemExit("duckdb required: pip install duckdb")

    out.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{args.memory_limit}'; SET threads={args.threads};")

    print(f"Reading {src} ({src.stat().st_size/1024/1024:.0f} MB)…")
    # The CSV has a fixed schema: extension, -1, 1950, 1951, …, 2023.
    year_cols = ["-1"] + [str(y) for y in range(1950, 2024)]
    cols_sql = ", ".join(f'"{y}"' for y in year_cols)

    con.execute(f"""
COPY (
    WITH src AS (
        SELECT *
        FROM read_csv_auto('{src.as_posix()}',
                           header=true, ignore_errors=true, sample_size=20000)
    ),
    unpivoted AS (
        SELECT extension, year::INTEGER AS year, occ::BIGINT AS occ
        FROM src
        UNPIVOT (occ FOR year IN ({cols_sql}))
        WHERE occ IS NOT NULL AND occ > 0
    ),
    by_ext AS (
        SELECT
            extension,
            sum(occ) AS total_occ,
            sum(CASE WHEN year >= 2019 AND year >= 0 THEN occ ELSE 0 END) AS recent_occ,
            sum(CASE WHEN year < 0 THEN occ ELSE 0 END) AS undated_occ,
            min(CASE WHEN year >= 0 AND occ > 0 THEN year END) AS first_year,
            max(CASE WHEN year >= 0 AND occ > 0 THEN year END) AS last_year
        FROM unpivoted
        GROUP BY extension
    )
    SELECT extension, total_occ, recent_occ, undated_occ, first_year, last_year
    FROM by_ext
    ORDER BY total_occ DESC
)
TO '{out.as_posix()}'
WITH (HEADER, DELIMITER ',')
""")
    n = con.execute(
        f"SELECT count(*) FROM read_csv_auto('{out.as_posix()}', header=true)"
    ).fetchone()[0]
    print(f"Wrote {out} ({out.stat().st_size/1024/1024:.0f} MB, {n:,} rows).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
