"""Unified origin lookup for a content sha, from two provenance sources.

1. **graph** — `cbl_file+origin.csv` (repo root): origin URLs the maintainer
   built from the SWH graph. Each `origin` cell is an SWH *browse* URL with
   `origin_url=`, `path=`, `timestamp=`, `branch=`. Authoritative + broad
   (~99.7% of the lowercase `.cbl` corpus, all forges: GitHub, GitLab,
   Bitbucket, SourceForge SVN/CVS, Google Code, …). The browse URL itself may
   404 (hand-built), but the `origin_url` (the repo) is always extractable.

2. **github** — `data/derived/cobol_study/origins.jsonl` (from
   `recover_origins.py`): byte-confirmed GitHub matches with an anchor
   revision. Narrower; a content can live in many repos, so this may name a
   *different* repo than the graph source (both are valid — SWH dedups content
   globally).

Both apps (`review_app`, `review_server`) use `origin_for(sha)`.
"""

from __future__ import annotations

import csv
import json
from urllib.parse import parse_qs, urlparse

from .common import ROOT, STUDY_DIR

CSV_CANDIDATES = [ROOT / "cbl_file+origin.csv",
                  ROOT / "COBOL-SWH-extracted" / "cbl_file+origin.csv"]
GH_JSONL = STUDY_DIR / "origins.jsonl"

_graph: dict[str, dict] | None = None
_github: dict[str, dict] | None = None


def _parse_browse_url(u: str) -> dict | None:
    if not u or "origin_url=" not in u:
        return None
    q = parse_qs(urlparse(u).query)
    origin = (q.get("origin_url") or [None])[0]
    if not origin:
        return None
    branch = (q.get("branch") or [None])[0]
    return {
        "origin": origin,
        "path": (q.get("path") or [None])[0],
        "timestamp": (q.get("timestamp") or [None])[0],
        "branch": branch.replace("refs/heads/", "") if branch else None,
        "forge": urlparse(origin).netloc,
        "swh_browse_url": u,
        "source": "swh-graph",
    }


def graph_origins() -> dict[str, dict]:
    global _graph
    if _graph is None:
        _graph = {}
        path = next((p for p in CSV_CANDIDATES if p.exists()), None)
        if path:
            with path.open(encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)  # header
                for row in reader:
                    if len(row) < 3:
                        continue
                    sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
                    rec = _parse_browse_url(row[2])
                    if sha and rec:
                        _graph[sha] = rec
    return _graph


def github_origins() -> dict[str, dict]:
    global _github
    if _github is None:
        _github = {}
        if GH_JSONL.exists():
            for line in GH_JSONL.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if o.get("content_match"):
                    _github[o["sha"]] = {
                        "origin": o.get("origin"), "anchor": o.get("anchor"),
                        "qualified": o.get("qualified"), "source": "github-match"}
    return _github


def origin_for(sha: str) -> dict | None:
    """Merged view: {graph, github, agree} — None if no source has it."""
    g = graph_origins().get(sha)
    h = github_origins().get(sha)
    if not g and not h:
        return None
    agree = None
    if g and h and g.get("origin") and h.get("origin"):
        agree = g["origin"].rstrip("/") == h["origin"].rstrip("/")
    return {"graph": g, "github": h, "agree": agree,
            "primary": g or h}  # graph preferred (broader/upstream)


def has_origin(sha: str) -> bool:
    return sha in graph_origins() or sha in github_origins()


if __name__ == "__main__":
    g, h = graph_origins(), github_origins()
    print(f"graph origins: {len(g)} | github-match origins: {len(h)}")
    import collections
    forges = collections.Counter(v["forge"] for v in g.values())
    print("top forges:", dict(forges.most_common(8)))
