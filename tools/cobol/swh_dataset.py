"""Anonymous access to the Software Heritage public dataset (S3, ORC) — and
what it takes to recover origin for a bare content SWHID.

TESTED FACTS (2026-07, this repo)
---------------------------------
- The `softwareheritage` S3 bucket is **public-read over plain HTTPS** — no AWS
  account or credentials needed. Datasets: `graph/2018-09-25/` … `graph/2023-09-06/`.
- The relational export is **ORC** (not Parquet): tables `content`, `directory`,
  `directory_entry`, `revision`, `snapshot`, `snapshot_branch`, `origin`,
  `origin_visit`, `origin_visit_status`, `release`, … under `.../orc/<table>/`.
- Read it anonymously with pyarrow (DuckDB can't read ORC). One `origin` shard
  (~71 MB) holds ~2.0 M origins; the whole `origin` table is ~9.5 GB.

WHY content→origin is not a laptop query
----------------------------------------
The reverse lookup ("which origins contain this content") must scan
`directory_entry` to find directories holding the content, then walk
directory→directory→revision→snapshot→origin — recursively. `directory_entry`
is **~13 TB** and is sharded by random UUID (not by content hash), so there is
no way to touch only the relevant shard. This is a managed-scan (Athena) or a
graph (swh-graph) job, not an HTTPS-from-a-laptop job.

The three real routes (choose by what you have):
  1. **swh-graph** — the compressed property graph; a backward BFS from a
     `swh:1:cnt:` node to reachable origins. THE tool for reverse lookup.
     Hosted gRPC/HTTP API (researcher access) or self-hosted (multi-TB).
  2. **swh-provenance** — purpose-built index for "earliest revision/origin
     that introduced this content." Not on the anonymous REST API.
  3. **Athena / Spark over this ORC dataset** — great for FORWARD queries
     (origin → its files). For reverse, you pay to scan `directory_entry`
     (+ recursion), which is why the original `.cbl`/`.CBL` extraction likely
     dropped origin. If you re-run that extraction *starting from* revisions/
     snapshots, origin comes for free — keep it as a column.

Usage (needs pyarrow — not in this repo's interpreter):
    uv run --with pyarrow --python 3.12 python -m tools.cobol.swh_dataset
    uv run --with pyarrow --python 3.12 python -m tools.cobol.swh_dataset --grep cobol --shards 2
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
import urllib.request

S3 = "https://softwareheritage.s3.amazonaws.com/"
DATASET = "graph/2023-09-06"


def list_shards(table: str, dataset: str = DATASET, limit: int = 1000) -> list[str]:
    """Anonymous S3 listing of ORC shard URLs for a table (stdlib only)."""
    prefix = f"{dataset}/orc/{table}/"
    url = f"{S3}?list-type=2&prefix={prefix}&max-keys={limit}"
    with urllib.request.urlopen(url, timeout=60) as r:
        xml = r.read().decode("utf-8")
    keys = re.findall(r"<Key>([^<]+\.orc)</Key>", xml)
    return [S3 + k for k in keys]


def read_orc_url(url: str):
    """Download one ORC shard and return a pyarrow Table."""
    import pyarrow.orc as orc  # imported lazily; run under `uv run --with pyarrow`
    with tempfile.NamedTemporaryFile(suffix=".orc") as tmp:
        with urllib.request.urlopen(url, timeout=300) as r:
            tmp.write(r.read())
        tmp.flush()
        return orc.ORCFile(tmp.name).read()


def grep_origins(pattern: str, shards: int = 1) -> list[str]:
    """Scan the first N `origin` shards for URLs matching a substring.

    NOTE: this matches origin *URLs*, not content membership — it cannot prove
    a given content lives in an origin (that needs swh-graph). Useful only to
    surface candidate origins by name.
    """
    pat = pattern.lower()
    hits: list[str] = []
    for url in list_shards("origin")[:shards]:
        t = read_orc_url(url)
        hits += [u for u in t.column("url").to_pylist() if pat in u.lower()]
    return hits


def main() -> None:
    ap = argparse.ArgumentParser(description="Anonymous SWH ORC dataset access demo.")
    ap.add_argument("--table", default="origin")
    ap.add_argument("--grep", default=None, help="substring to match in origin URLs")
    ap.add_argument("--shards", type=int, default=1)
    args = ap.parse_args()

    shards = list_shards(args.table)
    print(f"{args.table}: {len(shards)} ORC shards under {DATASET} (anonymous HTTPS)")
    if not shards:
        return
    try:
        import pyarrow  # noqa: F401
    except ModuleNotFoundError:
        print("pyarrow not available — run under: "
              "uv run --with pyarrow --python 3.12 python -m tools.cobol.swh_dataset",
              file=sys.stderr)
        return

    if args.grep is not None:
        hits = grep_origins(args.grep, args.shards)
        print(f"origins matching '{args.grep}' in first {args.shards} shard(s): {len(hits)}")
        for u in hits[:20]:
            print("  ", u)
        return

    t = read_orc_url(shards[0])
    print(f"shard[0] columns={t.column_names} rows={t.num_rows:,}")
    if "url" in t.column_names:
        for u in t.column("url").to_pylist()[:5]:
            print("  ", u)


if __name__ == "__main__":
    main()
