#!/usr/bin/env python3
"""Rebuild an `nb_extensions_alphanum.csv`-shaped table from a SWH export.

The SWH-MSR-ARV file (`nb_extensions_alphanum.csv`, see `docs/citations.md`)
stops at a 2023 archive snapshot. This tool recomputes the same shape —
one row per file extension, one column per year — from the public
"Aggregated Contents" derived dataset of a newer graph export:

    s3://softwareheritage/derived_datasets/<DATE>/contents/*.parquet
    (https://datasets.softwareheritage.org/datasets/<DATE>-contents/)

One parquet row = one distinct content (blob), with its most popular
filename (`filename_last_extension`) and the timestamp of the oldest
revision/release containing it (`first_occurrence_timestamp`). We count
rows per (extension, year of first occurrence).

This is NOT the MSR 2025 methodology re-run: that file leaves ~44% of
occurrences undated (`-1`), while this dataset dates ~99.8% of contents,
and each content counts once, under its most popular name. Cite it as the
SWH dataset + this derivation, not as SWH-MSR-ARV.

Phases
------
1. Per-shard aggregation (cached, resumable): reads only
   `filename_last_extension` + `first_occurrence_timestamp` (~380 MB/shard,
   ~36 GB total for 2026-06-04) into `<out-dir>/shards/<i>.parquet`.
2. Merge into `<out-dir>/swh_contents_ext_year_<DATE>.parquet` — long format
   (ext BLOB, year, n, occ), ALL extensions, unfiltered.
3. Pivot into `<out-dir>/nb_extensions_alphanum_<DATE>.csv` using the same
   conventions as the original file:
   - header `extension,-1,1950,…,<export year>`
   - a `no extension` row (NULL `filename_last_extension`)
   - other rows kept iff the extension is `str.isalnum()` (Unicode-aware,
     no length limit — matches the original file, which has `.001西西57P289M`)
   - `-1` = no usable date: NULL timestamp, or year outside 1950..<export year>
   Plus a `.manifest.json` recording counts and provenance.

Usage
-----
    python3 tools/build_swh_ext_year_table.py                 # all phases
    python3 tools/build_swh_ext_year_table.py --shards 0,47   # phase 1 subset only
    python3 tools/build_swh_ext_popularity.py                 # then: -> data/derived/*.csv.gz
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
DEFAULT_OUT_ROOT = Path("/Users/mathieuacher/SANDBOX/PL-swh-contents")
FIRST_YEAR = 1950
NO_EXT_LABEL = "no extension"
BAD_YEAR = -2  # timestamp outside what to_timestamp() can represent


def connect(threads: int, memory_limit: str):
    try:
        import duckdb  # type: ignore
    except ImportError:
        raise SystemExit("duckdb required: pip install duckdb")
    con = duckdb.connect()
    con.execute(f"SET threads={threads}; SET memory_limit='{memory_limit}';")
    con.execute("INSTALL httpfs; LOAD httpfs;")
    # Anonymous S3 reads of multi-GB files stall or drop now and then:
    # retry harder than DuckDB's default (3 tries, 100 ms apart).
    con.execute("SET http_retries=10; SET http_retry_wait_ms=1000; SET http_retry_backoff=2; SET http_timeout=120;")
    # Public bucket (region us-east-1): anonymous access.
    con.execute("CREATE SECRET (TYPE s3, PROVIDER config, REGION 'us-east-1', KEY_ID '', SECRET '')")
    return con


def list_shards(con, base: str) -> list[str]:
    files = [r[0] for r in con.execute(f"SELECT file FROM glob('{base}*.parquet')").fetchall()]
    return sorted((Path(f).stem for f in files), key=lambda s: int(s) if s.isdigit() else s)


def phase1(con, base: str, shard_dir: Path, shards: list[str]) -> None:
    shard_dir.mkdir(parents=True, exist_ok=True)
    todo = [s for s in shards if not (shard_dir / f"{s}.parquet").exists()]
    print(f"[phase 1] {len(shards) - len(todo)}/{len(shards)} shards cached; {len(todo)} to go", flush=True)
    t0 = time.time()
    for k, s in enumerate(todo, 1):
        t = time.time()
        for attempt in range(1, 6):
            try:
                aggregate_shard(con, base, s, shard_dir)
                break
            except Exception as e:  # duckdb.IOException/HTTPException on flaky S3
                if attempt == 5:
                    raise
                print(f"[phase 1] shard {s} attempt {attempt} failed: {str(e)[:200]}; retrying", flush=True)
                time.sleep(30 * attempt)
        el = time.time() - t0
        print(f"[phase 1] shard {s} done in {time.time() - t:.0f}s "
              f"({k}/{len(todo)}, eta {el / k * (len(todo) - k) / 60:.0f} min)", flush=True)


def aggregate_shard(con, base: str, s: str, shard_dir: Path) -> None:
    tmp = shard_dir / f"{s}.parquet.tmp"
    con.execute(f"""
COPY (
    SELECT filename_last_extension AS ext,
           CASE WHEN first_occurrence_timestamp IS NULL THEN -1
                WHEN first_occurrence_timestamp NOT BETWEEN -62135596800 AND 253402300799 THEN {BAD_YEAR}
                ELSE year(to_timestamp(first_occurrence_timestamp)) END::INTEGER AS year,
           count(*)::BIGINT AS n,
           sum(filename_occurrences)::HUGEINT AS occ
    FROM read_parquet('{base}{s}.parquet')
    GROUP BY 1, 2
) TO '{tmp.as_posix()}' (FORMAT parquet)""")
    os.replace(tmp, shard_dir / f"{s}.parquet")


def phase2(con, shard_dir: Path, long_out: Path) -> None:
    print(f"[phase 2] merging shards -> {long_out}", flush=True)
    tmp = long_out.with_suffix(".parquet.tmp")
    con.execute(f"""
COPY (
    SELECT ext, year, sum(n)::BIGINT AS n, sum(occ)::HUGEINT AS occ
    FROM read_parquet('{shard_dir.as_posix()}/*.parquet')
    GROUP BY 1, 2
    ORDER BY 1 NULLS FIRST, 2
) TO '{tmp.as_posix()}' (FORMAT parquet)""")
    os.replace(tmp, long_out)


def phase3(con, long_out: Path, wide_out: Path, date: str, meta: dict) -> None:
    last_year = int(date[:4])
    years = list(range(FIRST_YEAR, last_year + 1))
    col = {y: i + 1 for i, y in enumerate(years)}  # index 0 = the -1 column
    print(f"[phase 3] pivoting -> {wide_out}", flush=True)

    stats = {"rows_total": 0, "rows_kept": 0, "rows_no_extension": 0,
             "rows_non_alnum_dropped": 0, "rows_non_utf8_dropped": 0,
             "rows_undated": 0, "rows_year_out_of_range": 0,
             "extensions_kept": 0}

    def label(ext: bytes | None) -> str | None:
        if ext is None:
            return NO_EXT_LABEL
        try:
            s = bytes(ext).decode("utf-8")
        except UnicodeDecodeError:
            return None
        return "." + s if s.isalnum() else ""

    cur = con.execute(f"SELECT ext, year, n FROM read_parquet('{long_out.as_posix()}') ORDER BY ext NULLS FIRST, year")
    rows: list[tuple[str, list[int]]] = []
    cur_ext, cur_lab, vec = object(), None, None

    def flush():
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
                vec[0] += n
                stats["rows_undated" if year == -1 else "rows_year_out_of_range"] += n
    flush()

    # Same order as the original: `no extension` first, then by extension string.
    rows.sort(key=lambda r: (r[0] != NO_EXT_LABEL, r[0]))
    stats["extensions_kept"] = len(rows) - (1 if rows and rows[0][0] == NO_EXT_LABEL else 0)
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
    if args.shards:
        return 0
    missing = [s for s in all_shards if not (shard_dir / f"{s}.parquet").exists()]
    if missing:
        raise SystemExit(f"shards still missing: {missing}")

    kv = dict(con.execute(
        f"SELECT decode(key), decode(value) FROM parquet_kv_metadata('{base}{all_shards[0]}.parquet')"
    ).fetchall())
    meta = {
        "source": base,
        "source_page": f"https://datasets.softwareheritage.org/datasets/{args.date}-contents/",
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
