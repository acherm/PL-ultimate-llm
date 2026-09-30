#!/usr/bin/env python3
"""Rebuild an `nb_extensions_alphanum.csv`-shaped table from a SWH export.

Why this exists
---------------
The SWH-MSR-ARV file (`nb_extensions_alphanum.csv`, Desmazières / Di Cosmo /
Lorentz, MSR 2025 — see `docs/citations.md`) is a 2023 archive snapshot:
2022–2023 are under-counted and 43.8 % of its occurrences are undated (`-1`).
This tool recomputes a table of the same shape — one row per file extension,
one column per year — from the public "Aggregated Contents" derived dataset
of a newer Software Heritage graph export:

    s3://softwareheritage/derived_datasets/<DATE>/contents/*.parquet
    https://datasets.softwareheritage.org/datasets/<DATE>-contents/

What is counted
---------------
One parquet row = one distinct content (a blob, i.e. unique file bytes) with:
  - `filename_last_extension` (BLOB): last extension of the content's MOST
    POPULAR filename, without the dot (`py`; `attach.tar.gz` -> `gz`); NULL
    when that filename has no extension — including dotfiles such as
    `.gitignore` or `.bashrc`, which therefore count as "no extension";
  - `first_occurrence_timestamp` (seconds since the Unix epoch, UTC): date of
    the oldest revision/release containing the content; NULL when unknown.
We count rows per (extension, year of first occurrence). So the unit is
"distinct files, each counted once, under its most popular name, in the year
it first appeared". A content seen as both `a.h` and `a.hpp` counts once.

This is the MSR 2025 idea on a newer export, not a bit-for-bit re-run: that
file leaves 43.8 % of occurrences undated, this one only 0.8 % (2026-06-04).
Rankings agree (Spearman ~0.97 on its top 100/1K/10K); per-year curves do not.
Cite MSR 2025 for the approach plus the SWH export; do not label these
numbers "SWH-MSR-ARV". Details: `docs/SWH_EXTENSIONS_DECISIONS.md` §14.

Facts about the 2026-06-04 export (measured 2026-09-29)
-------------------------------------------------------
  - 96 parquet files, 0.46 TB, 29,286,730,716 rows, 9 columns; built by SWH
    with swh-graph 12.1.2. Earlier exports differ: 2026-03-02 has the
    extension columns only in a separate `contents_with_extensions/` folder
    (`--subdir`); its plain `contents/` lacks them.
  - The bucket is in us-east-1 and readable anonymously.
  - We read 2 of the 9 columns (+ `filename_occurrences`): ~380 MB per file,
    ~36 GB in total. At 60–150 s per file, a full run takes ~2.5 h.

Phases
------
1. Per-file aggregation, cached in `<out-dir>/shards/<i>.parquet`, so an
   interrupted run resumes where it stopped.
2. Merge the 96 small aggregates into `<out-dir>/swh_contents_ext_year_<DATE>.parquet`
   — long format (ext BLOB, year, n, occ), ALL extensions, unfiltered. Keep it:
   any other filter or bucketing can be derived from it without touching S3.
3. Pivot into `<out-dir>/nb_extensions_alphanum_<DATE>.csv` with the SAME
   conventions as the original file, so every tool that read it reads this:
   - header `extension,-1,1950,…,<export year>`;
   - a `no extension` row (NULL `filename_last_extension`);
   - other rows kept iff the extension is `str.isalnum()` — Unicode-aware and
     with NO length limit, as in the original (which holds `.001西西57P289M`
     and extensions up to 226 characters);
   - `-1` = no usable date: NULL timestamp, or a year outside 1950..<export year>.
   Plus `<...>.manifest.json`: provenance and row counts.

   Raw years are kept as they are. Known artefacts — 1970 (Unix epoch, 18.0 M
   files) and 1980 (MS-DOS epoch, 1.5 M) — are handled downstream by
   `tools/build_swh_ext_popularity.py`, not here.

Usage
-----
    python3 tools/build_swh_ext_year_table.py                 # all phases
    python3 tools/build_swh_ext_year_table.py --shards 0,47   # phase 1 subset only
    python3 tools/build_swh_ext_popularity.py                 # then: -> data/derived/*.csv.gz

Operational notes (learned the hard way)
----------------------------------------
  - Run ONE process. A first attempt with four parallel workers (and the
    wrong S3 region) stalled at 0 MB/s for 30 min; the sequential run with
    the settings in `connect` completed. Parallelism was not retried.
  - Anonymous S3 reads fail now and then ("Server returned nothing"): DuckDB
    retries each request (see `connect`), and each file is retried up to 5
    times (see `phase1`).
  - On a laptop, keep the machine awake (`caffeinate -i -w <pid>` on macOS):
    one file took 6 h, most likely across a sleep.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DATE = "2026-06-04"
DEFAULT_S3_PREFIX = "s3://softwareheritage/derived_datasets"
# Outputs are ~1 GB (CSV 712 MB + long parquet 252 MB + shard cache): they
# live outside the repo, next to where SWH-MSR-ARV lives (`../PL-roberto/`).
DEFAULT_OUT_ROOT = Path("/Users/mathieuacher/SANDBOX/PL-swh-contents")
# First year column of the original file; earlier dates go to `-1`.
FIRST_YEAR = 1950
# Label used by the original file for contents whose name has no extension.
NO_EXT_LABEL = "no extension"
# Sentinel for timestamps outside what `to_timestamp()` can represent (years
# 1..9999). It never matches a year column, so phase 3 sends it to `-1`, but
# it stays distinguishable from NULL (-1) in the long parquet and the stats.
BAD_YEAR = -2


def connect(threads: int, memory_limit: str):
    """DuckDB connection able to read the public SWH bucket anonymously."""
    try:
        import duckdb  # type: ignore
    except ImportError:
        raise SystemExit("duckdb required: pip install duckdb")
    con = duckdb.connect()
    # Threads mostly overlap HTTP range requests (the job is I/O-bound).
    con.execute(f"SET threads={threads}; SET memory_limit='{memory_limit}';")
    con.execute("INSTALL httpfs; LOAD httpfs;")
    # Anonymous S3 reads of multi-GB files stall or drop now and then.
    # DuckDB's defaults (3 retries, 100 ms apart, 30 s timeout) gave up on
    # the first "Server returned nothing"; retry longer, back off
    # exponentially (1 s, 2 s, 4 s, …), and abort a stalled read after 120 s
    # so it is retried instead of hanging forever.
    con.execute("SET http_retries=10; SET http_retry_wait_ms=1000; SET http_retry_backoff=2; SET http_timeout=120;")
    # The bucket is in us-east-1 (see the `x-amz-bucket-region` header).
    # Empty key/secret = unsigned requests, which the public bucket accepts.
    con.execute("CREATE SECRET (TYPE s3, PROVIDER config, REGION 'us-east-1', KEY_ID '', SECRET '')")
    return con


def list_shards(con, base: str) -> list[str]:
    """Shard ids ("0" … "95") under `base`, in numeric order."""
    files = [r[0] for r in con.execute(f"SELECT file FROM glob('{base}*.parquet')").fetchall()]
    # Numeric sort so progress logs read 0, 1, 2, … rather than 0, 1, 10, 11, …
    return sorted((Path(f).stem for f in files), key=lambda s: int(s) if s.isdigit() else s)


def phase1(con, base: str, shard_dir: Path, shards: list[str]) -> None:
    """Aggregate each remote parquet file into a small local one (cached)."""
    shard_dir.mkdir(parents=True, exist_ok=True)
    # A shard is done iff its final file exists: `aggregate_shard` writes to
    # a `.tmp` and renames at the end, so a crash never leaves a partial
    # `<i>.parquet` that would be mistaken for a finished one.
    todo = [s for s in shards if not (shard_dir / f"{s}.parquet").exists()]
    print(f"[phase 1] {len(shards) - len(todo)}/{len(shards)} shards cached; {len(todo)} to go", flush=True)
    t0 = time.time()
    for k, s in enumerate(todo, 1):
        t = time.time()
        # Second line of defence after DuckDB's per-request retries: if the
        # whole query still fails, wait (30 s, 60 s, 90 s, 120 s) and redo
        # the file from scratch. The 5th failure aborts the run; rerunning
        # resumes from the cache.
        for attempt in range(1, 6):
            try:
                aggregate_shard(con, base, s, shard_dir)
                break
            except Exception as e:  # duckdb.IOException/HTTPException on flaky S3
                if attempt == 5:
                    raise
                print(f"[phase 1] shard {s} attempt {attempt} failed: {str(e)[:200]}; retrying", flush=True)
                time.sleep(30 * attempt)
        # The ETA averages over all files so far, so one very slow file
        # (e.g. across a laptop sleep) inflates it for a while.
        el = time.time() - t0
        print(f"[phase 1] shard {s} done in {time.time() - t:.0f}s "
              f"({k}/{len(todo)}, eta {el / k * (len(todo) - k) / 60:.0f} min)", flush=True)


def aggregate_shard(con, base: str, s: str, shard_dir: Path) -> None:
    """Count one remote file's rows per (extension, year) into `<s>.parquet`.

    Only the columns named in the query are fetched (parquet projection):
    `filename_last_extension`, `first_occurrence_timestamp` and
    `filename_occurrences`, ~450 MB of a ~4.5 GB file. Each output has
    ~250 K rows (~3.5 MB).
    """
    tmp = shard_dir / f"{s}.parquet.tmp"
    con.execute(f"""
COPY (
    SELECT
        -- Kept as raw bytes: decoding (and the isalnum filter) happens in
        -- phase 3, so the long parquet keeps every extension losslessly,
        -- including non-UTF-8 ones.
        filename_last_extension AS ext,
        -- Year of first appearance, in UTC.
        --   NULL timestamp          -> -1 (undated, like the original `-1` column)
        --   outside years 1..9999   -> {BAD_YEAR} (to_timestamp would fail on it;
        --                              the bounds are 0001-01-01 and 9999-12-31)
        -- Implausible but representable years (e.g. 2514) are kept as is;
        -- phase 3 sends them to `-1`.
        CASE WHEN first_occurrence_timestamp IS NULL THEN -1
             WHEN first_occurrence_timestamp NOT BETWEEN -62135596800 AND 253402300799 THEN {BAD_YEAR}
             ELSE year(to_timestamp(first_occurrence_timestamp)) END::INTEGER AS year,
        -- n: distinct contents. This is what every output table reports.
        count(*)::BIGINT AS n,
        -- occ: how often those contents appear under their most popular
        -- name. Not used by the CSV; kept in the long parquet for anyone who
        -- wants a usage-weighted variant later. HUGEINT: sums can exceed
        -- 2^63 in theory.
        sum(filename_occurrences)::HUGEINT AS occ
    FROM read_parquet('{base}{s}.parquet')
    GROUP BY 1, 2
) TO '{tmp.as_posix()}' (FORMAT parquet)""")
    # Atomic publish: the cached file appears only once complete.
    os.replace(tmp, shard_dir / f"{s}.parquet")


def phase2(con, shard_dir: Path, long_out: Path) -> None:
    """Sum the per-shard aggregates into one long table (all extensions)."""
    print(f"[phase 2] merging shards -> {long_out}", flush=True)
    tmp = long_out.with_suffix(".parquet.tmp")
    # The same (ext, year) pair appears in many shards: sum them. Sorted by
    # extension then year, so phase 3 can pivot in one streaming pass.
    # NULL (no extension) first, like the original file's first row.
    con.execute(f"""
COPY (
    SELECT ext, year, sum(n)::BIGINT AS n, sum(occ)::HUGEINT AS occ
    FROM read_parquet('{shard_dir.as_posix()}/*.parquet')
    GROUP BY 1, 2
    ORDER BY 1 NULLS FIRST, 2
) TO '{tmp.as_posix()}' (FORMAT parquet)""")
    os.replace(tmp, long_out)


def phase3(con, long_out: Path, wide_out: Path, date: str, meta: dict) -> None:
    """Pivot the long table into the original wide CSV layout + manifest."""
    # The export year is the last column even though it is a partial year
    # (2026-06-04 -> Jan–early Jun 2026); consumers decide how to treat it.
    last_year = int(date[:4])
    years = list(range(FIRST_YEAR, last_year + 1))
    col = {y: i + 1 for i, y in enumerate(years)}  # index 0 = the -1 column
    print(f"[phase 3] pivoting -> {wide_out}", flush=True)

    # Every content lands in exactly one bucket, so the counts add up:
    #   rows_total = rows_kept + rows_non_alnum_dropped + rows_non_utf8_dropped
    # and rows_total must equal the manifest's `source_rows` (it does for
    # 2026-06-04: 29,286,730,716).
    stats = {"rows_total": 0, "rows_kept": 0, "rows_no_extension": 0,
             "rows_non_alnum_dropped": 0, "rows_non_utf8_dropped": 0,
             "rows_undated": 0, "rows_year_out_of_range": 0,
             "extensions_kept": 0}

    def label(ext: bytes | None) -> str | None:
        """Row label in the original's convention, or a drop marker.

        Returns `no extension` for NULL, `.<ext>` when kept, "" when the
        extension is not alphanumeric (dropped, e.g. `.tar-gz`, `.c++`),
        and None when it is not valid UTF-8 (dropped; 14,448 contents).
        `str.isalnum()` is Unicode-aware (letters and digits of any script)
        and has no length limit: that reproduces the original file, whose
        extension rows run up to 226 characters and include CJK.
        """
        if ext is None:
            return NO_EXT_LABEL
        try:
            s = bytes(ext).decode("utf-8")
        except UnicodeDecodeError:
            return None
        return "." + s if s.isalnum() else ""

    # Streaming group-by: rows arrive sorted by (ext, year), so one vector per
    # extension is filled, then flushed when the extension changes. Only the
    # kept rows (4.2 M × 78 ints) are held in memory, not the 30 M+ input rows.
    cur = con.execute(f"SELECT ext, year, n FROM read_parquet('{long_out.as_posix()}') ORDER BY ext NULLS FIRST, year")
    rows: list[tuple[str, list[int]]] = []
    # `object()` is a sentinel that never equals a real ext (not even None,
    # which is the legitimate "no extension" key).
    cur_ext, cur_lab, vec = object(), None, None

    def flush():
        # Dropped extensions have a falsy label ("" or None) and are skipped.
        if cur_lab:
            rows.append((cur_lab, vec))

    while batch := cur.fetchmany(200_000):
        for ext, year, n in batch:
            stats["rows_total"] += n
            if ext != cur_ext:
                flush()
                cur_ext, cur_lab, vec = ext, label(ext), [0] * (len(years) + 1)
            if cur_lab is None:
                stats["rows_non_utf8_dropped"] += n
                continue
            if cur_lab == "":
                stats["rows_non_alnum_dropped"] += n
                continue
            stats["rows_kept"] += n
            if cur_lab == NO_EXT_LABEL:
                stats["rows_no_extension"] += n
            if year in col:
                vec[col[year]] += n
            else:
                # -1 (NULL timestamp), BAD_YEAR, before 1950, or after the
                # export year (bogus future dates, e.g. 2514): all "no usable
                # date", as in the original's `-1` column.
                vec[0] += n
                stats["rows_undated" if year == -1 else "rows_year_out_of_range"] += n
    flush()

    # Same order as the original: `no extension` first, then by extension
    # string (Python's code-point order; case-sensitive, so `.CBL` < `.cbl`).
    rows.sort(key=lambda r: (r[0] != NO_EXT_LABEL, r[0]))
    stats["extensions_kept"] = len(rows) - (1 if rows and rows[0][0] == NO_EXT_LABEL else 0)
    # Write to .tmp and rename, so a half-written CSV never replaces a good one.
    tmp = wide_out.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["extension", "-1", *years])
        for lab, v in rows:
            w.writerow([lab, *v])
    os.replace(tmp, wide_out)

    meta["stats"] = stats
    manifest = wide_out.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"[phase 3] wrote {wide_out} ({wide_out.stat().st_size / 1e6:.0f} MB, "
          f"{len(rows):,} rows) + {manifest.name}", flush=True)
    print(json.dumps(stats, indent=2), flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=DEFAULT_DATE, help="SWH export date (default: %(default)s)")
    ap.add_argument("--s3-prefix", default=DEFAULT_S3_PREFIX)
    ap.add_argument("--subdir", default="contents",
                    help="Contents table under <prefix>/<date>/ (2026-03-02 used `contents_with_extensions`)")
    ap.add_argument("--out-dir", default=None, help="Default: %s/<date>" % DEFAULT_OUT_ROOT)
    ap.add_argument("--shards", default="", help="Comma-separated shard ids; runs phase 1 only for these")
    ap.add_argument("--threads", type=int, default=32)
    ap.add_argument("--memory-limit", default="12GB")
    args = ap.parse_args()

    base = f"{args.s3_prefix}/{args.date}/{args.subdir}/"
    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_ROOT / args.date
    shard_dir = out_dir / "shards"
    long_out = out_dir / f"swh_contents_ext_year_{args.date}.parquet"
    wide_out = out_dir / f"nb_extensions_alphanum_{args.date}.csv"

    con = connect(args.threads, args.memory_limit)
    all_shards = list_shards(con, base)
    if not all_shards:
        raise SystemExit(f"no parquet files under {base}")
    shards = [s.strip() for s in args.shards.split(",") if s.strip()] or all_shards

    phase1(con, base, shard_dir, shards)
    # `--shards` = aggregate a subset only (smoke tests, or filling gaps);
    # the merge needs every shard, so stop here.
    if args.shards:
        return 0
    missing = [s for s in all_shards if not (shard_dir / f"{s}.parquet").exists()]
    if missing:
        raise SystemExit(f"shards still missing: {missing}")

    # Provenance for the manifest. Every file carries SWH's build metadata
    # (swh_graph_version, the graph path, creation date) as parquet key/value
    # pairs; the first file is representative. Only footers are read here.
    kv = dict(con.execute(
        f"SELECT decode(key), decode(value) FROM parquet_kv_metadata('{base}{all_shards[0]}.parquet')"
    ).fetchall())
    meta = {
        "source": base,
        "source_page": f"https://datasets.softwareheritage.org/datasets/{args.date}-contents/",
        # Checked against stats.rows_total after phase 3: nothing lost.
        "source_rows": con.execute(f"SELECT sum(num_rows) FROM parquet_file_metadata('{base}*.parquet')").fetchone()[0],
        "source_shards": len(all_shards),
        "swh_graph_version": kv.get("swh_graph_version"),
        "swh_graph_aggregate_version": kv.get("swh_graph_aggregate_version"),
        "unit": "distinct content (blob), counted once under its most popular filename's last extension",
        "year": "year of first_occurrence_timestamp (oldest revision/release containing the content), UTC",
        "minus_one_column": f"NULL timestamp, or year outside {FIRST_YEAR}..{args.date[:4]}",
        "row_filter": f"'{NO_EXT_LABEL}' row + extensions where str.isalnum() (Unicode, any length)",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "tools/build_swh_ext_year_table.py",
    }
    phase2(con, shard_dir, long_out)
    phase3(con, long_out, wide_out, args.date, meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
