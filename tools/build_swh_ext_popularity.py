#!/usr/bin/env python3
"""Derive `data/derived/swh_extensions_popularity.csv.gz` from a per-extension × year table.

Input: a wide `nb_extensions_alphanum*.csv` table — one row per file
extension, columns `-1` (undated) and one per year — in either of:

  - the 2026-06-04 rebuild (current default), produced by
    `tools/build_swh_ext_year_table.py` from the SWH "Aggregated Contents"
    dataset of the 2026-06-04 graph export (distinct files per extension,
    dated by first appearance; see docs/SWH_EXTENSIONS_DECISIONS.md §14);
  - the original SWH-MSR-ARV file published with
        Adèle Desmazières, Roberto Di Cosmo, Valentin Lorentz.
        "50 Years of Programming Language Evolution through the Software
         Heritage looking glass." MSR 2025: 372-383.
    (2023 snapshot; pass `--src .../PL-roberto/nb_extensions_alphanum.csv`).

See `docs/citations.md`.

Output:
  A narrow per-extension aggregate at
  `data/derived/swh_extensions_popularity.csv.gz`:

      extension, total_occ, recent_occ, undated_occ, first_year, last_year, median_year

  - `total_occ`   = sum across all years + the `-1` column
  - `recent_occ`  = sum over the last `--recent-years` (5) full years; the
                    last year column is a partial year (the export is taken
                    mid-year), so for a table ending in 2026 this is 2021–2025
  - `undated_occ` = the `-1` column + the artefact years (below)
  - `first_year`  = earliest dated year with a positive count (empty if undated only)
  - `last_year`   = latest dated year with a positive count
  - `median_year` = year by which half of the dated files had appeared

Artefact years (`--artifact-years`, default 1970,1980) are counted as
undated: they are the Unix and MS-DOS epochs, where broken commit dates
land (2026-06-04: 18.0 M files in 1970 vs 28 K in 1971; 1.5 M in 1980 vs
~100 K in 1979/1981). Stray wrong dates remain in other years (e.g. `.go`
files in 1973), so `first_year` is NOT a reliable start date — the site
shows `median_year` instead.

A sidecar `swh_extensions_popularity.meta.json` records the recent window
and artefact years, for labels. The CSV is committed (gzipped: ~22 MB vs
118 MB raw, under GitHub's 100 MB file limit) so the CI Pages deploy has it
without a fetch step.

Usage
-----
    python3 tools/build_swh_ext_popularity.py [--src PATH] [--out PATH]
"""

from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path("/Users/mathieuacher/SANDBOX/PL-swh-contents/2026-06-04/nb_extensions_alphanum_2026-06-04.csv")
OUT_CSV = ROOT / "data" / "derived" / "swh_extensions_popularity.csv.gz"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--src", default=str(DEFAULT_SRC),
                        help="Path to a nb_extensions_alphanum*.csv table (default: %(default)s)")
    parser.add_argument("--out", default=str(OUT_CSV),
                        help="Output path (default: %(default)s)")
    parser.add_argument("--recent-years", type=int, default=5,
                        help="Length of the recent window, in full years (default: %(default)s)")
    parser.add_argument("--artifact-years", default="1970,1980",
                        help="Years counted as undated (default: %(default)s)")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--memory-limit", default="6GB")
    args = parser.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    if not src.exists():
        raise SystemExit(
            f"ERROR: source CSV not found at {src}.\n"
            "Rebuild it with `tools/build_swh_ext_year_table.py` (SWH 2026-06-04 "
            "export), or pass --src to the original SWH-MSR-ARV "
            "`nb_extensions_alphanum.csv` (Desmazières/Di Cosmo/Lorentz, MSR 2025)."
        )

    try:
        import duckdb  # type: ignore
    except ImportError:
        raise SystemExit("duckdb required: pip install duckdb")

    out.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{args.memory_limit}'; SET threads={args.threads};")

    print(f"Reading {src} ({src.stat().st_size/1024/1024:.0f} MB)…")
    # Schema: extension, -1, 1950, 1951, …, <last year>. The last year depends
    # on the snapshot (2023 for SWH-MSR-ARV; later for files rebuilt by
    # `tools/build_swh_ext_year_table.py`), so read it from the header.
    with open(src, encoding="utf-8") as f:
        header = f.readline().rstrip("\r\n").split(",")
    year_cols = [c for c in header[1:] if c.lstrip("-").isdigit()]
    print(f"Year columns: {year_cols[0]}, {year_cols[1]} … {year_cols[-1]}")
    cols_sql = ", ".join(f'"{y}"' for y in year_cols)
    # The last column is the export year, i.e. a partial year.
    recent_to = max(int(y) for y in year_cols) - 1
    recent_from = recent_to - args.recent_years + 1
    artifact_years = sorted(int(y) for y in args.artifact_years.split(",") if y.strip())
    artifacts_sql = ", ".join(str(y) for y in artifact_years) or "NULL"
    print(f"Recent window: {recent_from}–{recent_to}; artefact years counted as undated: {artifact_years}")

    con.execute(f"""
COPY (
    WITH src AS (
        SELECT *
        FROM read_csv_auto('{src.as_posix()}',
                           header=true, ignore_errors=true, sample_size=20000)
    ),
    unpivoted AS (
        SELECT extension,
               CASE WHEN year::INTEGER IN ({artifacts_sql}) THEN -1
                    ELSE year::INTEGER END AS year,
               occ::BIGINT AS occ
        FROM src
        UNPIVOT (occ FOR year IN ({cols_sql}))
        WHERE occ IS NOT NULL AND occ > 0
    ),
    by_ext AS (
        SELECT
            extension,
            sum(occ) AS total_occ,
            sum(CASE WHEN year BETWEEN {recent_from} AND {recent_to} THEN occ ELSE 0 END) AS recent_occ,
            sum(CASE WHEN year < 0 THEN occ ELSE 0 END) AS undated_occ,
            min(CASE WHEN year >= 0 THEN year END) AS first_year,
            max(CASE WHEN year >= 0 THEN year END) AS last_year
        FROM unpivoted
        GROUP BY extension
    ),
    cumul AS (
        SELECT extension, year,
               sum(occ) OVER (PARTITION BY extension ORDER BY year
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS c,
               sum(occ) OVER (PARTITION BY extension) AS t
        FROM unpivoted
        WHERE year >= 0
    ),
    median AS (
        SELECT extension, min(year) AS median_year
        FROM cumul WHERE 2 * c >= t
        GROUP BY extension
    )
    SELECT b.extension, total_occ, recent_occ, undated_occ, first_year, last_year, median_year
    FROM by_ext b LEFT JOIN median m USING (extension)
    ORDER BY total_occ DESC, b.extension
)
TO '{out.as_posix()}'
WITH (HEADER, DELIMITER ',')
""")
    n = con.execute(
        f"SELECT count(*) FROM read_csv_auto('{out.as_posix()}', header=true)"
    ).fetchone()[0]
    print(f"Wrote {out} ({out.stat().st_size/1024/1024:.0f} MB, {n:,} rows).")

    meta_path = out.parent / (out.name.split(".")[0] + ".meta.json")
    meta_path.write_text(json.dumps({
        "source": src.name,
        "year_columns": [year_cols[0], year_cols[-1]],
        "recent_from": recent_from,
        "recent_to": recent_to,
        "artifact_years_as_undated": artifact_years,
        "rows": n,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "tools/build_swh_ext_popularity.py",
    }, indent=2) + "\n")
    print(f"Wrote {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
