"""Draw the `.m` study samples from the Parquet population (deterministic).

Two frames, both reproducible from a seed with no RNG state (rank = md5 of
``seed || key``), so the first k items of either frame are themselves a
simple random sample of that frame — the fetch/judge loop can stop anywhere
and still hold a valid sample.

  U  by-file  : uniform over all 51.4 M contents (incl. the 0.1 % no-origin)
  R  by-repo  : uniform over the 2.08 M origins, then one content uniformly
                within the origin (two-stage: "the typical repository")

Every sampled row also carries its population weights so post-stratified
frames cost nothing later:
  repo_n        contents in its origin          (by-repo weight   = 1/repo_n)
  path_versions contents sharing (origin, path) (by-path weight   = 1/path_versions)

    .venv/bin/python -m tools.m.sample --n-uniform 2000 --n-repo 1000 --seed 17
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from tools.m.ingest import PARQUET, STUDY

WORKLIST = STUDY / "worklist_all.csv"
COLS = ["swhid", "sha1_git", "name", "path", "origin", "forge", "branch", "ts",
        "in_uniform", "in_diverse", "u_rank", "d_rank", "repo_n", "path_versions"]


def main():
    import duckdb
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-uniform", type=int, default=2000)
    ap.add_argument("--n-repo", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=17)
    a = ap.parse_args()
    s = str(a.seed)
    con = duckdb.connect()
    con.execute("SET threads=14")
    con.execute(f"""CREATE TEMP TABLE m AS SELECT sha, status, origin, path, branch, ts,
        regexp_extract(coalesce(path,''), '([^/]*)$', 1) AS name,
        regexp_extract(coalesce(origin,''), '^[A-Za-z+]+://([^/]+)', 1) AS forge
        FROM read_parquet('{PARQUET}')""")
    con.execute("CREATE TEMP TABLE rn AS SELECT origin, count(*) repo_n FROM m WHERE origin IS NOT NULL GROUP BY 1")
    con.execute("CREATE TEMP TABLE pv AS SELECT origin, path, count(*) path_versions FROM m WHERE origin IS NOT NULL GROUP BY 1,2")
    # U: uniform by content
    con.execute(f"""CREATE TEMP TABLE u AS
        SELECT sha, row_number() OVER (ORDER BY md5(sha || '|U|{s}')) u_rank
        FROM m QUALIFY u_rank <= {a.n_uniform}""")
    # R: uniform origin, then uniform content within it
    con.execute(f"""CREATE TEMP TABLE pick AS
        SELECT origin, arg_min(sha, md5(sha || '|W|{s}')) sha
        FROM m WHERE origin IS NOT NULL GROUP BY origin""")
    con.execute(f"""CREATE TEMP TABLE d AS
        SELECT sha, row_number() OVER (ORDER BY md5(origin || '|R|{s}')) d_rank
        FROM pick QUALIFY d_rank <= {a.n_repo}""")
    rows = con.execute("""
        SELECT 'swh:1:cnt:' || m.sha, m.sha, m.name, m.path, m.origin, m.forge, m.branch, m.ts,
               (u.sha IS NOT NULL)::INT, (d.sha IS NOT NULL)::INT, u.u_rank, d.d_rank,
               rn.repo_n, pv.path_versions
        FROM m
        LEFT JOIN u USING (sha) LEFT JOIN d USING (sha)
        LEFT JOIN rn ON rn.origin = m.origin
        LEFT JOIN pv ON pv.origin = m.origin AND pv.path = m.path
        WHERE u.sha IS NOT NULL OR d.sha IS NOT NULL
        ORDER BY least(coalesce(u.u_rank, 1e9), coalesce(d.d_rank, 1e9)), m.sha
    """).fetchall()
    STUDY.mkdir(parents=True, exist_ok=True)
    with WORKLIST.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    nu = sum(r[8] for r in rows)
    nd = sum(r[9] for r in rows)
    print(f"uniform={nu}  by-repo={nd}  union={len(rows)}  overlap={nu + nd - len(rows)}")
    print(f"wrote {WORKLIST}")


if __name__ == "__main__":
    main()
