#!/usr/bin/env python3
"""Verify that every sample under `samples/` has SWHIDs SWH knows about.

This is the weak existence check documented in
`docs/SOURCES_AND_SWH_EVIDENCE.md` §8. A sample's `qualified_swhid`
makes three independent claims:

    swh:1:cnt:<sha1>                      ← the file bytes
    ;origin=<URL>                         ← derived: swh:1:ori:<sha1(URL)>
    ;anchor=swh:1:rev:<commit>            ← the pinned commit
    ;path=<filepath>                      ← structurally unverifiable

For each of cnt / rev / ori we ask SWH "do you have this?" via the
bulk `POST /api/1/known/` endpoint. All three types coexist in one
request, so the entire sweep stays at ~3 API calls regardless of how
many sample files there are.

What this CAN tell us:
- whether the bytes correspond to *some* content SWH archives;
- whether SWH archived the commit we cite as the anchor;
- whether SWH ever crawled the origin URL we cite.

What this CANNOT tell us:
- whether those bytes are the same blob the parquet row was indexing
  (strict match needs the cnt-nodes parquet);
- whether that specific path/commit/origin combination is the real
  story for *this* content (revisions are global; a commit known to
  SWH might come from a different origin than the one we claim).

Output: `data/derived/swh_sample_verification.csv` with one row per
sample, columns: pl_id, sha1_git, sample_path, qualified_swhid,
bare_swhid, rev_swhid, ori_swhid, cnt_known, rev_known, ori_known,
all_known, checked_at.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
OUT_CSV = ROOT / "data" / "derived" / "swh_sample_verification.csv"

SWH_BASE = "https://archive.softwareheritage.org"
KNOWN_ENDPOINT = f"{SWH_BASE}/api/1/known/"
ORIGIN_ENDPOINT = f"{SWH_BASE}/api/1/origin/{{url}}/get/"
USER_AGENT = "PL-ultimate-llm/verify_swh_samples"
BATCH_SIZE = 100

# qualified SWHID qualifiers we parse out of metadata.json.
_ANCHOR_RE = re.compile(r";anchor=(swh:1:rev:[0-9a-f]{40})")
_ORIGIN_RE = re.compile(r";origin=([^;]+)")


def origin_swhid(url: str) -> str:
    """SWH origin SWHID = swh:1:ori:<sha1(url-bytes)>.

    Note: the bulk `/api/1/known/` endpoint does NOT accept `ori` SWHIDs
    (rejects with "'ori' is not a valid ObjectType"). For origin
    existence we have to fall back to `GET /api/1/origin/<url>/get/`,
    one request per origin. Kept here so the qualified-SWHID-as-string
    stays parsable and round-trippable.
    """
    return "swh:1:ori:" + hashlib.sha1(url.encode("utf-8")).hexdigest()


def _auth_headers(token: str | None) -> dict[str, str]:
    h = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def collect_samples() -> list[dict]:
    """Walk samples/ and return one dict per metadata.json found.

    Each sample carries up to three SWHIDs we can verify against SWH:
      bare_swhid = swh:1:cnt:<sha1_git>     (always, when extractable)
      rev_swhid  = swh:1:rev:<commit_sha>   (from `;anchor=`, may be empty)
      ori_swhid  = swh:1:ori:<sha1(URL)>    (from `;origin=`, may be empty)
    """
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
        rev_m = _ANCHOR_RE.search(qualified)
        rev = rev_m.group(1) if rev_m else ""
        ori_m = _ORIGIN_RE.search(qualified)
        ori = origin_swhid(ori_m.group(1)) if ori_m else ""
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
            "rev_swhid": rev,
            "ori_swhid": ori,
        })
    return out


def post_known(swhids: list[str], *, token: str | None = None) -> dict[str, bool]:
    """POST a batch to /api/1/known/. Returns {swhid: known_bool}.

    Only cnt/dir/rev/rel/snp SWHIDs are accepted — `ori` is rejected
    server-side. The caller must pre-filter.
    """
    payload = json.dumps(swhids).encode("utf-8")
    headers = _auth_headers(token)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        KNOWN_ENDPOINT, data=payload, headers=headers, method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
        remaining = r.headers.get("X-Ratelimit-Remaining")
        if remaining is not None:
            print(f"  X-Ratelimit-Remaining: {remaining}")
    return {s: bool(v.get("known", False)) for s, v in data.items()}


def check_origin(url: str, *, token: str | None = None) -> tuple[bool | None, int]:
    """GET /api/1/origin/<url>/get/. Returns (known, remaining_quota).

    `known=None` if the check failed for a reason other than 404.
    """
    encoded = urllib.parse.quote(url, safe=":/")
    endpoint = ORIGIN_ENDPOINT.format(url=encoded)
    req = urllib.request.Request(endpoint, headers=_auth_headers(token))
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            remaining = int(r.headers.get("X-Ratelimit-Remaining", "-1"))
            return (r.status == 200, remaining)
    except urllib.error.HTTPError as e:
        remaining = int(e.headers.get("X-Ratelimit-Remaining", "-1"))
        if e.code == 404:
            return (False, remaining)
        return (None, remaining)


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--out-csv", default=str(OUT_CSV),
                   help="Output CSV path (default: %(default)s).")
    p.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                   help="SWHIDs per /api/1/known/ POST (default: %(default)d).")
    p.add_argument("--check-origins", action="store_true",
                   help="Also verify each origin URL via GET "
                        "/api/1/origin/<url>/get/. The /known/ endpoint "
                        "does not accept ori SWHIDs, so origin checks "
                        "are 1 request each — 120 req/h anonymous, much "
                        "higher with SWH_TOKEN. Off by default to keep "
                        "the cnt+rev sweep at ~3 calls / ~10 seconds.")
    p.add_argument("--origin-throttle", type=float, default=0.5,
                   help="Seconds between origin GETs when --check-origins "
                        "is set (default: %(default).1f). Adaptive sleep "
                        "kicks in if quota drops below 5.")
    p.add_argument("--dry-run", action="store_true",
                   help="List samples that would be checked; make no requests.")
    args = p.parse_args()
    token = os.environ.get("SWH_TOKEN") or None
    if token:
        print("Auth: using SWH_TOKEN from env.")
    else:
        print("Auth: anonymous (120 req/h cap). Set SWH_TOKEN env var for higher limits.")

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

    # Bulk /known/ accepts cnt/dir/rev/rel/snp — not ori. Collect only those.
    bulk_swhids: set[str] = set()
    origin_urls: set[str] = set()
    for s in samples:
        bulk_swhids.add(s["bare_swhid"])
        if s["rev_swhid"]:
            bulk_swhids.add(s["rev_swhid"])
        # Capture the raw origin URL — origin SWHIDs (`swh:1:ori:`) are
        # rejected by /known/, so we need the URL for the per-origin
        # GET fallback regardless.
        om = _ORIGIN_RE.search(s["qualified_swhid"])
        if om:
            origin_urls.add(om.group(1))

    swhids_sorted = sorted(bulk_swhids)
    print(f"Bulk-known SWHIDs (cnt + rev): {len(swhids_sorted)} across {len(samples)} samples")
    n_batches = (len(swhids_sorted) + args.batch_size - 1) // args.batch_size
    print(f"Will issue {n_batches} POST(s) of up to {args.batch_size} SWHIDs each.")

    known_map: dict[str, bool | None] = {}
    checked_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for i in range(0, len(swhids_sorted), args.batch_size):
        batch = swhids_sorted[i : i + args.batch_size]
        print(f"Batch {i // args.batch_size + 1}/{n_batches}: {len(batch)} SWHIDs ...")
        try:
            result = post_known(batch, token=token)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.reason}; giving up on this batch.")
            for s in batch:
                known_map[s] = None
            continue
        known_map.update(result)

    # Origin verification: per-URL GET, optional.
    origin_known: dict[str, bool | None] = {}
    if args.check_origins and origin_urls:
        urls_sorted = sorted(origin_urls)
        print(f"\nChecking {len(urls_sorted)} unique origin URL(s) via "
              f"/api/1/origin/.../get/ (throttle={args.origin_throttle}s) ...")
        for i, url in enumerate(urls_sorted, start=1):
            try:
                known, remaining = check_origin(url, token=token)
            except urllib.error.URLError as e:
                print(f"  [{i}/{len(urls_sorted)}] {url[:60]} URLError: {e}")
                origin_known[url] = None
                continue
            origin_known[url] = known
            tag = "yes" if known is True else "no" if known is False else "error"
            print(f"  [{i}/{len(urls_sorted)}] {tag:5s}  remain={remaining}  {url[:80]}")
            # Adaptive sleep: if quota gets tight, slow down.
            sleep = args.origin_throttle
            if 0 <= remaining < 5:
                sleep = max(sleep, 30.0)
                print(f"    quota tight ({remaining}); sleeping {sleep}s")
            time.sleep(sleep)
    elif origin_urls and not args.check_origins:
        print(f"\nOrigin verification skipped (--check-origins not set). "
              f"{len(origin_urls)} unique origin URL(s) would be checked.")

    # Write CSV with per-claim columns.
    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    counts = {
        "cnt": {"yes": 0, "no": 0, "error": 0, "absent": 0},
        "rev": {"yes": 0, "no": 0, "error": 0, "absent": 0},
        "ori": {"yes": 0, "no": 0, "error": 0, "absent": 0, "skipped": 0},
    }
    n_all_known = 0

    def tag_of(swhid: str) -> str:
        if not swhid:
            return "absent"
        k = known_map.get(swhid)
        if k is True:
            return "yes"
        if k is False:
            return "no"
        return "error"

    def tag_origin(url: str) -> str:
        if not url:
            return "absent"
        if not args.check_origins:
            return "skipped"
        k = origin_known.get(url)
        if k is True:
            return "yes"
        if k is False:
            return "no"
        return "error"

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "pl_id", "sha1_git", "sample_path",
            "qualified_swhid", "bare_swhid", "rev_swhid", "ori_swhid",
            "cnt_known", "rev_known", "ori_known",
            "all_known", "checked_at",
        ])
        for s in samples:
            c = tag_of(s["bare_swhid"])
            r = tag_of(s["rev_swhid"])
            ori_url_m = _ORIGIN_RE.search(s["qualified_swhid"])
            ori_url = ori_url_m.group(1) if ori_url_m else ""
            o = tag_origin(ori_url)
            counts["cnt"][c] += 1
            counts["rev"][r] += 1
            counts["ori"][o] += 1
            # all_known = every checked claim came back yes. `absent` and
            # `skipped` claims don't count against; only `no`/`error` do.
            checked = [t for t in (c, r, o) if t not in ("absent", "skipped")]
            all_yes = checked and all(t == "yes" for t in checked)
            if all_yes:
                n_all_known += 1
            w.writerow([
                s["pl_id"], s["sha1_git"], s["sample_path"],
                s["qualified_swhid"], s["bare_swhid"], s["rev_swhid"], s["ori_swhid"],
                c, r, o,
                "yes" if all_yes else "no",
                checked_at,
            ])

    print(f"\nWrote {out_path}")
    print(f"Per-claim known counts (yes / no / error / absent):")
    for k, v in counts.items():
        print(f"  {k}_known:  yes={v['yes']:>4d}  no={v['no']:>4d}  "
              f"error={v['error']:>4d}  absent={v['absent']:>4d}")
    print(f"All-three claims known: {n_all_known}/{len(samples)}")

    # Print a few examples of any non-yes claims, so failures are visible.
    failures = []
    with out_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            bad_cnt = row["cnt_known"] not in ("yes", "absent", "skipped")
            bad_rev = row["rev_swhid"] and row["rev_known"] not in ("yes", "absent", "skipped")
            bad_ori = row["ori_known"] not in ("yes", "absent", "skipped")
            if bad_cnt or bad_rev or bad_ori:
                failures.append(row)
    if failures:
        print(f"\n{len(failures)} sample(s) with at least one claim not 'yes':")
        for row in failures[:20]:
            print(f"  {row['pl_id']:30s}  cnt={row['cnt_known']} "
                  f"rev={row['rev_known']} ori={row['ori_known']}  "
                  f"{row['sample_path']}")
        if len(failures) > 20:
            print(f"  ... ({len(failures) - 20} more — see {out_path})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
