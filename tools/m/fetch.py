"""Fetch the `.m` worklist bytes from SWH into the shared cache (.cache/cobol/).

Decoupled from judging: fetching is the *rate-limited* stage (anonymous 120
req/h; a token lifts it ~10×), judging is the *paid* stage. The loop re-reads
`.swh_token` every 25 fetches, validates it, and switches to it on the fly — so
refreshing an expired token speeds up a running job without a restart. An
expired/invalid token falls back to anonymous instead of failing.

    python3 -m tools.m.fetch                 # whole worklist, worklist order
    python3 -m tools.m.fetch --limit 200
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.common import CACHE_DIR, fetch_content  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKLIST = ROOT / "data" / "derived" / "m_study" / "worklist_all.csv"
TOKEN_FILE = ROOT / ".swh_token"
PROBE = "https://archive.softwareheritage.org/api/1/content/sha1_git:e69de29bb2d1d6434b8b29ae775ad8c2e48c5391/"


def _token_from_file() -> str | None:
    if not TOKEN_FILE.exists():
        return None
    for line in TOKEN_FILE.read_text().splitlines():
        line = line.strip()
        if "SWH_TOKEN=" in line:
            return line.split("SWH_TOKEN=", 1)[1].strip().strip("'\"") or None
    return None


def _token_ok(tok: str) -> bool:
    req = urllib.request.Request(PROBE, headers={"Authorization": f"Bearer {tok}",
                                                 "User-Agent": "PL-ultimate-llm/m-study"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except urllib.error.HTTPError:
        return False
    except Exception:
        return False


_last_tok = {"value": None, "ok": False}


def refresh_token(verbose=True) -> bool:
    """Adopt `.swh_token` if it changed and works; else run anonymously."""
    tok = _token_from_file()
    if tok == _last_tok["value"]:
        return _last_tok["ok"]
    ok = bool(tok) and _token_ok(tok)
    _last_tok.update(value=tok, ok=ok)
    if ok:
        os.environ["SWH_TOKEN"] = tok
    else:
        os.environ.pop("SWH_TOKEN", None)
    if verbose:
        print(f"[token] {'authenticated' if ok else 'ANONYMOUS (token missing/expired)'}", flush=True)
    return ok


def cached(sha: str) -> bool:
    return (CACHE_DIR / f"{sha}.bin").exists() and (CACHE_DIR / f"{sha}.meta.json").exists()


def _priority(r: dict):
    """Judge targets (rank ≤ 1000 in U or R) first, then frame T, then the rest."""
    ranks = [int(r[k]) for k in ("u_rank", "d_rank") if r.get(k)]
    m = min(ranks) if ranks else 10**9
    if m <= 1000:
        return (0, m)
    if r.get("t_rank"):
        return (1, int(r["t_rank"]))
    return (2, m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    from tools.m.study import worklist
    rows = worklist()
    if a.limit:
        rows = rows[: a.limit]
    todo = sorted((r for r in rows if not cached(r["sha1_git"])), key=_priority)
    print(f"worklist {len(rows)} | cached {len(rows) - len(todo)} | to fetch {len(todo)}", flush=True)
    refresh_token()
    t0, done = time.time(), 0
    for i, r in enumerate(todo, 1):
        if i % 25 == 0:
            refresh_token(verbose=False)
        try:
            fetch_content(r["swhid"], filename=r["name"])
            done += 1
        except Exception as e:
            msg = str(e)
            if "403" in msg or "401" in msg:
                _last_tok.update(value=None)
                refresh_token()
            print(f"[{i}/{len(todo)}] {r['sha1_git'][:10]} ERROR {msg[:160]}", file=sys.stderr, flush=True)
            continue
        if i % 20 == 0:
            rate = done / max(time.time() - t0, 1) * 3600
            print(f"[{i}/{len(todo)}] fetched {done} ({rate:.0f}/h, "
                  f"{'tok' if os.environ.get('SWH_TOKEN') else 'anon'})", flush=True)
    print(f"fetch complete: {done} new", flush=True)


if __name__ == "__main__":
    main()
