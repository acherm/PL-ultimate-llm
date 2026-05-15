#!/usr/bin/env python3
"""Verify that every sample under `samples/` has a SWHID that SWH knows about.

This is the weak existence check documented in
`docs/SOURCES_AND_SWH_EVIDENCE.md` §8: for each sample's
`qualified_swhid`, ask SWH "do you have a content with this sha1_git?"
via the bulk `POST /api/1/known/` endpoint.

What this CAN tell us:
- whether the bytes on disk correspond to *some* content SWH archives;
  if `known=false`, the GitHub→SWH chain broke for this sample and the
  metadata.json is misleading.

What this CANNOT tell us:
- whether those bytes are the same blob the parquet row was indexing
  (the popularity score `occurrences_in_swh` was about). That strict
  match needs the nodes parquet to resolve content_id → sha1_git.

Output: `data/derived/swh_sample_verification.csv` with one row per
sample, columns: pl_id, sha1_git, sample_path, qualified_swhid,
swh_known (yes/no), checked_at.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
OUT_CSV = ROOT / "data" / "derived" / "swh_sample_verification.csv"

KNOWN_ENDPOINT = "https://archive.softwareheritage.org/api/1/known/"
USER_AGENT = "PL-ultimate-llm/verify_swh_samples"
BATCH_SIZE = 100


def collect_samples() -> list[dict]:
    """Walk samples/ and return one dict per metadata.json found."""
    out: list[dict] = []
    for meta_path in SAMPLES_DIR.rglob("metadata.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        qualified = meta.get("qualified_swhid") or ""
        # The bare content SWHID is the part before any `;` qualifier.
        bare = qualified.split(";", 1)[0]
        if not bare.startswith("swh:1:cnt:"):
            continue
        # samples/<pl_id>/<sha1>/<file> → pl_id is parents[1].relative_to(SAMPLES_DIR)
        try:
            rel = meta_path.parent.relative_to(SAMPLES_DIR)
            pl_id = "/".join(rel.parts[:-1])
        except ValueError:
            pl_id = ""
        out.append({
            "pl_id": pl_id,
            "sha1_git": meta.get("sha1_git", ""),
            "sample_path": str(meta_path.relative_to(ROOT)),
            "qualified_swhid": qualified,
            "bare_swhid": bare,
        })
    return out


def post_known(swhids: list[str]) -> dict[str, bool]:
    """POST a batch to /api/1/known/. Returns {swhid: known_bool}."""
    payload = json.dumps(swhids).encode("utf-8")
    req = urllib.request.Request(
        KNOWN_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
        remaining = r.headers.get("X-Ratelimit-Remaining")
        if remaining is not None:
            print(f"  X-Ratelimit-Remaining: {remaining}")
    return {s: bool(v.get("known", False)) for s, v in data.items()}


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--out-csv", default=str(OUT_CSV),
                   help="Output CSV path (default: %(default)s).")
    p.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                   help="SWHIDs per /api/1/known/ POST (default: %(default)d).")
    p.add_argument("--dry-run", action="store_true",
                   help="List samples that would be checked; make no requests.")
    args = p.parse_args()

    samples = collect_samples()
    if not samples:
        print(f"No samples found under {SAMPLES_DIR}.")
        return 0
    print(f"Found {len(samples)} samples with content SWHIDs under {SAMPLES_DIR}.")

    if args.dry_run:
        for s in samples[:5]:
            print(f"  {s['pl_id']:30s}  {s['bare_swhid']}")
        if len(samples) > 5:
            print(f"  ... ({len(samples) - 5} more)")
        return 0

    # Deduplicate by bare SWHID — the same blob can appear under multiple pl_ids
    # (unclassified fan-out). We only need to ask SWH once per blob.
    unique_swhids = sorted({s["bare_swhid"] for s in samples})
    print(f"Unique content SWHIDs to verify: {len(unique_swhids)}")
    n_batches = (len(unique_swhids) + args.batch_size - 1) // args.batch_size
    print(f"Will issue {n_batches} POST(s) of up to {args.batch_size} SWHIDs each.")

    known_map: dict[str, bool] = {}
    checked_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for i in range(0, len(unique_swhids), args.batch_size):
        batch = unique_swhids[i : i + args.batch_size]
        print(f"Batch {i // args.batch_size + 1}/{n_batches}: {len(batch)} SWHIDs ...")
        try:
            result = post_known(batch)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.reason}; giving up on this batch.")
            for s in batch:
                known_map[s] = None  # marker for "check failed"
            continue
        known_map.update(result)

    # Write CSV.
    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n_yes = n_no = n_err = 0
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "pl_id", "sha1_git", "sample_path",
            "qualified_swhid", "bare_swhid",
            "swh_known", "checked_at",
        ])
        for s in samples:
            k = known_map.get(s["bare_swhid"])
            if k is True:
                tag, n_yes = "yes", n_yes + 1
            elif k is False:
                tag, n_no = "no", n_no + 1
            else:
                tag, n_err = "error", n_err + 1
            w.writerow([
                s["pl_id"], s["sha1_git"], s["sample_path"],
                s["qualified_swhid"], s["bare_swhid"],
                tag, checked_at,
            ])

    print(f"\nWrote {out_path}")
    print(f"Summary: known={n_yes}  unknown={n_no}  errored={n_err}  total={len(samples)}")
    if n_no:
        print(f"\nSamples NOT in SWH ({n_no}):")
        with out_path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["swh_known"] == "no":
                    print(f"  {row['pl_id']:30s}  {row['sha1_git'][:12]}  {row['sample_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
