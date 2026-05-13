#!/usr/bin/env python3
"""Download bytes for rows in `swh_extension_samples.csv` so you can browse
real programs on disk, organized by predicted PL.

For each row that has been successfully qualified (i.e. `qualify_status='ok'`),
this fetches the file content from GitHub raw at the pinned commit (fast, CDN),
verifies the length + sha1_git match what the qualified SWHID asserts, then
writes:

    samples/<pl_id>/<sha1_git>/<filename>
    samples/<pl_id>/<sha1_git>/metadata.json

The metadata.json carries the full provenance chain (qualified SWHID, heuristic
id that fired, origin URL, commit, path, language attribution) so you can cite
or re-fetch later without the CSV.

Usage
-----
    # Everything in the CSV (subject to filters), default targets samples/
    python tools/fetch_samples.py

    # Just Lua programs, only those where the classifier agrees with the claim
    python tools/fetch_samples.py --pl-id pl/lua --matches-claim yes

    # Browse by language name (case-insensitive)
    python tools/fetch_samples.py --lang Perl

    # Confidence floor
    python tools/fetch_samples.py --confidence high

    # Limit per PL (useful for "show me 5 examples each")
    python tools/fetch_samples.py --per-pl-limit 5
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "derived" / "swh_extension_samples.csv"
DEFAULT_OUT = ROOT / "samples"


def sha1_git(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode() + b"\0")
    h.update(data)
    return h.hexdigest()


def _strip_owner_repo(origin_url: str) -> str | None:
    """Turn https://github.com/owner/repo into owner/repo."""
    if not origin_url.startswith("https://github.com/"):
        return None
    return origin_url[len("https://github.com/"):].rstrip("/")


def fetch_bytes(*, origin: str, commit_sha: str, path: str,
                content_sha1git: str, expected_length: int) -> tuple[bytes, str]:
    """Try GitHub raw at the pinned commit, then SWH /raw/ as fallback.

    Returns (bytes, source) where source is 'github' or 'swh'.
    """
    repo = _strip_owner_repo(origin)
    if repo:
        url = f"https://raw.githubusercontent.com/{repo}/{commit_sha}/{urllib.parse.quote(path.lstrip('/'))}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
            if len(data) == expected_length and sha1_git(data) == content_sha1git:
                return data, "github"
            # Length/hash mismatch — drop through to SWH.
        except urllib.error.HTTPError:
            pass
        except Exception:
            pass

    # SWH /raw/ — authoritative byte-source, no CDN.
    swh_url = (
        f"https://archive.softwareheritage.org/api/1/content/"
        f"sha1_git:{content_sha1git}/raw/"
    )
    with urllib.request.urlopen(swh_url, timeout=30) as r:
        data = r.read()
    return data, "swh"


def _content_sha1git_from_swhid(content_swhid: str) -> str | None:
    """Extract the sha1_git from a bare-or-qualified content SWHID."""
    if not content_swhid:
        return None
    body = content_swhid.split(";", 1)[0]
    if not body.startswith("swh:1:cnt:"):
        return None
    h = body[len("swh:1:cnt:"):]
    if len(h) != 40 or not all(c in "0123456789abcdef" for c in h.lower()):
        return None
    return h.lower()


def _commit_from_anchor(anchor: str) -> str | None:
    if not anchor or not anchor.startswith("swh:1:rev:"):
        return None
    return anchor[len("swh:1:rev:"):]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--csv", default=str(DEFAULT_CSV),
                   help="Path to the mining CSV (default: %(default)s).")
    p.add_argument("--out-dir", default=str(DEFAULT_OUT),
                   help="Where to write samples (default: %(default)s).")
    p.add_argument("--pl-id", default=None,
                   help="Restrict to a single predicted pl_id (e.g. pl/lua).")
    p.add_argument("--lang", default=None,
                   help="Restrict by claimed language (case-insensitive).")
    p.add_argument("--matches-claim", choices=["yes", "no", "any"], default="any",
                   help="Filter on predicted_matches_claim (default: any).")
    p.add_argument("--confidence", choices=["high", "medium", "low", "any"], default="any",
                   help="Minimum prediction confidence (default: any).")
    p.add_argument("--per-pl-limit", type=int, default=0,
                   help="Cap samples per pl_id (0 = no cap, default).")
    p.add_argument("--overwrite", action="store_true",
                   help="Re-download even if the sample file already exists.")
    p.add_argument("--dry-run", action="store_true",
                   help="List what would be fetched; do not write any file.")
    return p.parse_args()


def _passes_filter(row: dict, args) -> bool:
    if row.get("qualify_status") != "ok":
        return False
    if not row.get("qualified_swhid"):
        return False
    if args.pl_id and row.get("predicted_pl_id") != args.pl_id:
        return False
    if args.lang and (row.get("language") or "").lower() != args.lang.lower():
        return False
    if args.matches_claim != "any" and row.get("predicted_matches_claim") != args.matches_claim:
        return False
    if args.confidence != "any":
        order = {"high": 3, "medium": 2, "low": 1, "none": 0, "": 0}
        if order.get(row.get("predicted_confidence", ""), 0) < order[args.confidence]:
            return False
    return True


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found. Run swh_extension_mining.py --execute first.")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Deduplicate rows by (predicted_pl_id, content_sha1_git). The CSV explodes
    # one row per claimant for shared extensions; we only need the bytes once.
    rows_by_pl: dict[str, list[dict]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not _passes_filter(row, args):
                continue
            sha1 = _content_sha1git_from_swhid(row.get("qualified_swhid", ""))
            if not sha1:
                continue
            pl = row.get("predicted_pl_id") or "unclassified"
            key = (pl, sha1)
            if key in seen:
                continue
            seen.add(key)
            rows_by_pl[pl].append(dict(row, _sha1=sha1))

    total = sum(len(v) for v in rows_by_pl.values())
    if total == 0:
        print("No rows passed the filter. Check --pl-id / --lang / --confidence flags.")
        return 0

    print(f"Will fetch {total} unique sample(s) across {len(rows_by_pl)} pl_id(s).")
    if args.dry_run:
        for pl, rows in sorted(rows_by_pl.items()):
            print(f"  {pl}: {len(rows)}")
            for r in rows[:5]:
                print(f"    {r['_sha1'][:12]}  {r['filename']}  ({r['length']}B)  via={r['predicted_via']}")
        return 0

    ok = skipped = failed = 0
    for pl, rows in sorted(rows_by_pl.items()):
        if args.per_pl_limit:
            rows = rows[: args.per_pl_limit]
        pl_dir = out_dir / pl
        for r in rows:
            sha1 = r["_sha1"]
            sample_dir = pl_dir / sha1
            file_path = sample_dir / r["filename"]
            meta_path = sample_dir / "metadata.json"
            if file_path.exists() and not args.overwrite:
                skipped += 1
                continue

            try:
                data, source = fetch_bytes(
                    origin=r["qualify_origin"],
                    commit_sha=_commit_from_anchor(r["qualify_anchor"]) or "",
                    path=r["qualify_path"],
                    content_sha1git=sha1,
                    expected_length=int(r["length"]),
                )
            except Exception as e:
                print(f"  FAIL {pl}/{r['filename']}: {type(e).__name__}: {e}")
                failed += 1
                continue

            sample_dir.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(data)
            actual_sha = sha1_git(data)
            meta = {
                "language_claim": r["language"],
                "predicted_pl_id": r["predicted_pl_id"],
                "predicted_via": r["predicted_via"],
                "predicted_confidence": r["predicted_confidence"],
                "predicted_heuristic_id": r["predicted_heuristic_id"] or None,
                "predicted_matches_claim": r["predicted_matches_claim"],
                "filename": r["filename"],
                "length_bytes": len(data),
                "expected_length_bytes": int(r["length"]),
                "sha1_git": actual_sha,
                "sha1_git_matches": actual_sha == sha1,
                "qualified_swhid": r["qualified_swhid"],
                "swh_browser_url": f"https://archive.softwareheritage.org/{r['qualified_swhid']}/",
                "swh_raw_url": (
                    f"https://archive.softwareheritage.org/api/1/content/"
                    f"sha1_git:{sha1}/raw/"
                ),
                "github_raw_url": (
                    None if not r["qualify_origin"].startswith("https://github.com/")
                    else f"https://raw.githubusercontent.com/"
                         f"{_strip_owner_repo(r['qualify_origin'])}/"
                         f"{_commit_from_anchor(r['qualify_anchor'])}"
                         f"{r['qualify_path']}"
                ),
                "fetched_from": source,
                "ext": r["extension"],
                "occurrences_in_swh": int(r["occurrences"]),
            }
            meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
            ok += 1
            print(f"  OK   {pl}/{sha1[:12]}/{r['filename']} ({len(data)}B from {source})")

    print(f"\nDone. ok={ok}, skipped(existing)={skipped}, failed={failed}")
    print(f"Browse: {out_dir}/<pl_id>/<sha1_git>/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
