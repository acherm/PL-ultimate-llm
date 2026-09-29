"""Ingest the `.m` population (SWH-m-files.zip → Parquet) and describe it.

The maintainer's export is 6 headerless CSV shards (14 GB, ~55 M rows) of
``swh:1:cnt:<sha1_git>,<SWH browse URL>``; the browse URL carries
``branch``, ``origin_url``, ``path`` and ``timestamp``. It was produced by the
Rust ``swh-provenance`` tool on CINES, and three defects must be handled:

  1. **no-origin rows** — ``[... ERROR provenance::graph_utils] Swhid … has no
     predecessors in this graph``: the content is in the archive but the graph
     walk found no origin. Kept, with ``status='no_origin'``.
  2. **multi-line paths** — a file name containing a newline splits one record
     over several physical lines. The first line is kept (sha, origin, branch
     and the path prefix are intact) with ``status='multiline'``; the
     continuation lines are dropped.
  3. **the CINES job report** appended at the end of each shard — dropped (it
     does not start with ``swh:1:cnt:``).

    unzip SWH-m-files.zip -d .cache/m/csv        # stored zip: ~45 s
    .venv/bin/python -m tools.m.ingest            # → .cache/m/m_rows.parquet
    .venv/bin/python -m tools.m.ingest --stats    # → data/derived/m_study/population.json
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_GLOB = str(ROOT / ".cache" / "m" / "csv" / "m-*.csv")
PARQUET = ROOT / ".cache" / "m" / "m_rows.parquet"
STUDY = ROOT / "data" / "derived" / "m_study"
POP_JSON = STUDY / "population.json"

_READ = (f"read_csv('{CSV_GLOB}', columns={{'line':'VARCHAR'}}, delim='\\x01', "
         "quote='', escape='', header=false, filename=true, parallel=true, "
         "strict_mode=false, new_line='\\n', ignore_errors=true)")


def build(con):
    t0 = time.time()
    con.execute(f"""
    COPY (
      WITH raw AS (
        SELECT line, regexp_extract(filename, '(m-[0-9]+)\\.csv', 1) AS shard
        FROM {_READ}
        WHERE starts_with(line, 'swh:1:cnt:') AND substr(line, 51, 1) = ','
      ), p AS (
        SELECT shard, substr(line, 11, 40) AS sha, substr(line, 52) AS rest FROM raw
      ), q AS (
        SELECT shard, sha,
          CASE
            WHEN starts_with(rest, 'https://archive.softwareheritage.org/browse/origin/')
              THEN CASE WHEN regexp_matches(rest, '&timestamp=[^&]*$') THEN 'ok' ELSE 'multiline' END
            WHEN position('no predecessors' IN rest) > 0 THEN 'no_origin'
            ELSE 'other'
          END AS status,
          rest
        FROM p
      )
      SELECT shard, sha, status,
        nullif(regexp_extract(rest, '[?&]branch=(.*?)&origin_url=', 1), '') AS branch,
        nullif(regexp_extract(rest, '[?&]origin_url=(.*?)&path=', 1), '') AS origin,
        CASE WHEN status = 'ok' THEN regexp_extract(rest, '&path=(.*)&timestamp=[^&]*$', 1)
             WHEN status = 'multiline' THEN regexp_extract(rest, '&path=(.*)$', 1) END AS path,
        nullif(regexp_extract(rest, '&timestamp=([^&]*)$', 1), '') AS ts
      FROM q
    ) TO '{PARQUET}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 1000000)
    """)
    print(f"wrote {PARQUET} in {time.time() - t0:.0f}s")


def _view(con):
    con.execute(f"""
    CREATE OR REPLACE VIEW m AS
    SELECT *,
      regexp_extract(coalesce(path, ''), '([^/]*)$', 1) AS fname,
      regexp_extract(regexp_extract(coalesce(path, ''), '([^/]*)$', 1), '(\\.[^.]*)$', 1) AS ext,
      regexp_extract(coalesce(origin, ''), '^[A-Za-z+]+://([^/]+)', 1) AS forge,
      try_cast(substr(ts, 1, 4) AS INTEGER) AS year
    FROM read_parquet('{PARQUET}')
    """)


def stats(con):
    _view(con)
    one = lambda sql: con.execute(sql).fetchone()  # noqa: E731
    rows, shas = one("SELECT count(*), count(DISTINCT sha) FROM m")
    status = dict(con.execute("SELECT status, count(*) FROM m GROUP BY 1 ORDER BY 2 DESC").fetchall())
    # one row per content (sha): take the first provenance context if several
    con.execute("""CREATE OR REPLACE TEMP TABLE c AS
                   SELECT sha, any_value(origin) origin, any_value(path) path,
                          any_value(fname) fname, any_value(ext) ext,
                          any_value(forge) forge, any_value(year) AS year,
                          count(*) n_rows
                   FROM m WHERE status IN ('ok','multiline') GROUP BY sha""")
    with_origin = one("SELECT count(*) FROM c")[0]
    dup_rows = one("SELECT count(*) FILTER (WHERE n_rows>1), max(n_rows) FROM c")
    con.execute("CREATE OR REPLACE TEMP TABLE r AS SELECT origin, count(*) n FROM c GROUP BY 1")
    n_repos, med, mean, mx, p90, singles = one(
        "SELECT count(*), median(n), round(avg(n),1), max(n), quantile_cont(n, 0.9), "
        "count(*) FILTER (WHERE n=1) FROM r")
    top = con.execute("SELECT origin, n, round(100.0*n/sum(n) OVER (),2) FROM r ORDER BY n DESC LIMIT 25").fetchall()
    r80 = one("""SELECT min(k) FROM (SELECT row_number() OVER (ORDER BY n DESC) k,
                 sum(n) OVER (ORDER BY n DESC ROWS UNBOUNDED PRECEDING) cum,
                 sum(n) OVER () tot FROM r) WHERE cum >= 0.8*tot""")[0]
    top10 = one("SELECT round(100.0*sum(n)/(SELECT sum(n) FROM r),1) FROM (SELECT n FROM r ORDER BY n DESC LIMIT 10)")[0]
    top100 = one("SELECT round(100.0*sum(n)/(SELECT sum(n) FROM r),1) FROM (SELECT n FROM r ORDER BY n DESC LIMIT 100)")[0]
    forges_c = con.execute("SELECT forge, count(*) FROM c GROUP BY 1 ORDER BY 2 DESC LIMIT 12").fetchall()
    forges_r = con.execute("SELECT regexp_extract(origin,'^[A-Za-z+]+://([^/]+)',1) f, count(*) FROM r GROUP BY 1 ORDER BY 2 DESC LIMIT 12").fetchall()
    exts = con.execute("SELECT ext, count(*) FROM c GROUP BY 1 ORDER BY 2 DESC LIMIT 10").fetchall()
    fnames = con.execute("SELECT fname, count(*) FROM c GROUP BY 1 ORDER BY 2 DESC LIMIT 40").fetchall()
    years = con.execute("SELECT year, count(*) FROM c WHERE year IS NOT NULL GROUP BY 1 ORDER BY 1").fetchall()
    # version inflation: distinct (origin, path) vs contents
    files = one("SELECT count(*) FROM (SELECT DISTINCT origin, path FROM c)")[0]
    top_paths = con.execute("SELECT origin, path, count(*) n FROM c GROUP BY 1,2 ORDER BY n DESC LIMIT 10").fetchall()

    pop = {
        "csv_rows_parsed": rows, "row_status": status,
        "unique_contents": shas,
        "contents_with_origin": with_origin,
        "contents_listed_more_than_once": dup_rows[0], "max_rows_per_content": dup_rows[1],
        "unique_origins": n_repos,
        "distinct_origin_path_files": files,
        "version_inflation_pct": round(100 * (1 - files / with_origin), 1),
        "contents_per_repo": {"median": med, "mean": mean, "max": mx, "p90": p90,
                              "repos_with_1": singles},
        "concentration": {"top1_pct": top[0][2], "top10_pct": top10, "top100_pct": top100,
                          "repos_for_80pct": r80,
                          "repos_for_80pct_share": round(100 * r80 / n_repos, 2)},
        "top_repos": [{"origin": o, "contents": n, "pct": p} for o, n, p in top],
        "top_paths": [{"origin": o, "path": p, "versions": n} for o, p, n in top_paths],
        "forges_by_content": dict(forges_c), "forges_by_repo": dict(forges_r),
        "ext_case": dict(exts),
        "top_filenames": [{"name": k, "n": v} for k, v in fnames],
        "year_hist": {str(y): n for y, n in years},
    }
    STUDY.mkdir(parents=True, exist_ok=True)
    POP_JSON.write_text(json.dumps(pop, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in pop.items() if k not in ("top_filenames", "year_hist", "top_repos")}, indent=2))
    print(f"wrote {POP_JSON}")


def main():
    import duckdb
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="describe the population (needs the Parquet)")
    ap.add_argument("--threads", type=int, default=14)
    a = ap.parse_args()
    con = duckdb.connect()
    con.execute(f"SET threads={a.threads}")
    con.execute("SET preserve_insertion_order=false")
    con.execute(f"SET temp_directory='{ROOT / '.cache' / 'm' / 'duckdb_tmp'}'")
    if a.stats:
        stats(con)
    else:
        PARQUET.parent.mkdir(parents=True, exist_ok=True)
        build(con)


if __name__ == "__main__":
    main()
