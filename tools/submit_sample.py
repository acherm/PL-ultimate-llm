#!/usr/bin/env python3
"""Submit ONE specific program file as a SWH sample (form-style CLI).

`process_sample_requests.py` mines SWH per *extension* and picks candidates
by occurrence rank — there is no way to make it land one particular file.
This tool is the complement: you bring the bytes (local path) and/or the
content SWHID, it verifies everything it can against the SWH API, and
materializes the established layout:

    samples/<pl_id|unclassified>/<sha1_git>/<filename>
    samples/<pl_id|unclassified>/<sha1_git>/metadata.json

The site builder (`web/build_site.py`) walks `samples/` directly, so the
sample surfaces on `/ext/<x>/index.html#samples` (and, when unclassified,
fans out to the extension's primary-claimant PL pages) on the next build.
No CSV row is needed.

This is the first use-case of the standalone "fill the site's forms from
the terminal" CLI sketched in `docs/cli_roadmap.md`.

Usage
-----
    # Local file; ext inferred from the filename; lands in samples/unclassified/
    python3 tools/submit_sample.py --file ~/Downloads/XSetModifierMapping.m

    # No local bytes: fetch them from SWH by content SWHID
    python3 tools/submit_sample.py \\
        --swhid swh:1:cnt:f851a314d7b2dfc8949028f3671dba8f268ac4ee \\
        --filename XSetModifierMapping.m

    # Full provenance -> qualified SWHID (strong citation)
    python3 tools/submit_sample.py --file XSetModifierMapping.m \\
        --origin https://gitlab.freedesktop.org/xorg/test/xts \\
        --anchor 497a0865d1fa51adbba53c5c1c930dd18beacc4e \\
        --path /xts5/tset/Xlib13/XSetModifierMapping/XSetModifierMapping.m

    # Classified straight to a taxonomy slot instead of unclassified/
    python3 tools/submit_sample.py --file euler.sf --pl-id pl/sidef

    # Interactive form (prompts field by field)
    python3 tools/submit_sample.py --form

Verification policy
-------------------
- `sha1_git` is always computed from the actual bytes; a provided --swhid
  must match it (hard error otherwise).
- Unless --no-verify, the content SWHID is checked against SWH
  `/api/1/known/`. Unknown content is refused unless --allow-unarchived:
  the collection's premise is SWH-archived evidence.
- `--origin` / `--anchor`, when given, are checked too; failures degrade
  to a WARNING (aspirational provenance, see
  `docs/samples_aspirational_provenance.md`) rather than an error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLES_DIR = ROOT / "samples"
PL_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "pl.csv"

SWH_BASE = "https://archive.softwareheritage.org"
USER_AGENT = "PL-ultimate-llm/submit_sample"

_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def sha1_git(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode() + b"\0")
    h.update(data)
    return h.hexdigest()


def _request(url: str, *, data: bytes | None = None, method: str = "GET"):
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
    )
    return urllib.request.urlopen(req, timeout=30)


def swh_known(swhids: list[str]) -> dict[str, bool]:
    """POST /api/1/known/ — {swhid: known?} for cnt/rev/dir/snp SWHIDs."""
    body = json.dumps(swhids).encode()
    with _request(f"{SWH_BASE}/api/1/known/", data=body, method="POST") as r:
        resp = json.load(r)
    return {k: bool(v.get("known")) for k, v in resp.items()}


def swh_origin_known(origin_url: str) -> bool:
    url = f"{SWH_BASE}/api/1/origin/{origin_url}/get/"
    try:
        with _request(url) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def swh_fetch_raw(content_sha1git: str) -> bytes:
    url = f"{SWH_BASE}/api/1/content/sha1_git:{content_sha1git}/raw/"
    with _request(url) as r:
        return r.read()


def _norm_cnt_swhid(s: str) -> str:
    """Accept `swh:1:cnt:<hex>` (bare or qualified) or a bare 40-hex sha."""
    s = s.strip()
    body = s.split(";", 1)[0]
    if body.startswith("swh:1:cnt:"):
        body = body[len("swh:1:cnt:"):]
    body = body.lower()
    if not _HEX40.match(body):
        sys.exit(f"ERROR: not a content SWHID or 40-hex sha1_git: {s!r}")
    return body


def _norm_anchor(s: str) -> str:
    s = s.strip()
    if s.startswith("swh:1:rev:"):
        s = s[len("swh:1:rev:"):]
    s = s.lower()
    if not _HEX40.match(s):
        sys.exit(f"ERROR: --anchor must be a revision SWHID or 40-hex commit sha, got {s!r}")
    return s


def _known_pl_ids() -> set[str]:
    try:
        import csv as _csv
        with PL_CSV.open(encoding="utf-8") as f:
            return {row.get("pl_id", "") for row in _csv.DictReader(f)}
    except Exception:
        return set()


def _prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    val = input(f"  {label}{hint}: ").strip()
    return val or default


def run_form(args: argparse.Namespace) -> None:
    """Fill the missing args interactively, like the web form would."""
    print("Submit a specific program file as a SWH sample. Empty = skip/default.\n")
    if not args.file and not args.swhid:
        args.file = _prompt("Local file path (empty to fetch by SWHID)") or None
        if not args.file:
            args.swhid = _prompt("Content SWHID (swh:1:cnt:... or 40-hex)") or None
    if not args.file and not args.swhid:
        sys.exit("ERROR: need a local file or a content SWHID.")
    default_name = Path(args.file).name if args.file else ""
    args.filename = args.filename or _prompt("Filename (sets the extension)", default_name)
    default_ext = Path(args.filename).suffix.lower() if args.filename else ""
    args.ext = args.ext or _prompt("Extension", default_ext)
    args.pl_id = args.pl_id or _prompt("pl_id (e.g. pl/sidef; empty = unclassified)") or None
    args.origin = args.origin or _prompt("Origin URL (provenance, optional)") or None
    if args.origin:
        args.anchor = args.anchor or _prompt("Anchor commit sha (optional)") or None
        args.path = args.path or _prompt("Path in that revision (optional)") or None
    args.notes = args.notes or _prompt("Notes (why this sample matters, optional)") or None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--file", default=None,
                   help="Local file with the exact bytes to submit.")
    p.add_argument("--swhid", default=None,
                   help="Content SWHID (swh:1:cnt:<sha1_git>, bare 40-hex ok). "
                        "With --file: must match the bytes. Without: bytes are "
                        "fetched from the SWH raw API.")
    p.add_argument("--filename", default=None,
                   help="Filename to store (default: basename of --file).")
    p.add_argument("--ext", default=None,
                   help="Extension incl. dot (default: suffix of the filename).")
    p.add_argument("--pl-id", default=None,
                   help="Taxonomy slot, e.g. pl/sidef (default: unclassified).")
    p.add_argument("--language", default=None,
                   help="language_claim for metadata (default: _review_queue "
                        "when unclassified, else the pl_id).")
    p.add_argument("--origin", default=None,
                   help="Origin URL for the qualified SWHID (provenance).")
    p.add_argument("--anchor", default=None,
                   help="Anchor revision (commit sha or swh:1:rev:...).")
    p.add_argument("--path", default=None,
                   help="File path within the anchor revision (leading / added).")
    p.add_argument("--notes", default=None,
                   help="Free-text note stored in metadata.json (provenance, "
                        "what the file is, why it was submitted).")
    p.add_argument("--occurrences", type=int, default=0,
                   help="occurrences_in_swh if known from mining (default 0).")
    p.add_argument("--samples-dir", default=str(DEFAULT_SAMPLES_DIR),
                   help="Target samples root (default: %(default)s).")
    p.add_argument("--form", action="store_true",
                   help="Prompt interactively for missing fields.")
    p.add_argument("--no-verify", action="store_true",
                   help="Skip all SWH API checks (offline).")
    p.add_argument("--allow-unarchived", action="store_true",
                   help="Proceed even if SWH does not know the content.")
    p.add_argument("--overwrite", action="store_true",
                   help="Replace an existing sample dir for this content.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the plan; write nothing.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.form:
        run_form(args)
    if not args.file and not args.swhid:
        sys.exit("ERROR: need --file and/or --swhid (or --form).")

    # --- Resolve bytes + sha1_git -----------------------------------------
    claimed_sha = _norm_cnt_swhid(args.swhid) if args.swhid else None
    if args.file:
        fpath = Path(args.file).expanduser()
        if not fpath.is_file():
            sys.exit(f"ERROR: {fpath} is not a file.")
        data = fpath.read_bytes()
        fetched_from = "local"
    else:
        print(f"Fetching bytes from SWH for {claimed_sha} …")
        data = swh_fetch_raw(claimed_sha)
        fetched_from = "swh"
    sha = sha1_git(data)
    if claimed_sha and claimed_sha != sha:
        sys.exit(f"ERROR: bytes hash to {sha}, but --swhid says {claimed_sha}.")
    print(f"sha1_git {sha} ({len(data)} bytes, source: {fetched_from})")

    # --- Names ------------------------------------------------------------
    filename = args.filename or (Path(args.file).name if args.file else None)
    if not filename:
        sys.exit("ERROR: --filename is required when submitting by --swhid alone.")
    ext = args.ext or Path(filename).suffix.lower()
    if not ext.startswith("."):
        ext = "." + ext
    if len(ext) < 2:
        sys.exit(f"ERROR: cannot determine an extension from {filename!r}; use --ext.")

    pl_id = (args.pl_id or "").strip() or None
    if pl_id:
        known = _known_pl_ids()
        if known and pl_id not in known:
            print(f"WARNING: {pl_id} not found in {PL_CSV.relative_to(ROOT)} — "
                  f"the sample will still be written there.")
    target_slot = pl_id or "unclassified"

    # --- Provenance -------------------------------------------------------
    anchor = _norm_anchor(args.anchor) if args.anchor else None
    path = None
    if args.path:
        path = args.path if args.path.startswith("/") else "/" + args.path
    qualifiers = []
    if args.origin:
        qualifiers.append(f"origin={args.origin}")
    if anchor:
        qualifiers.append(f"anchor=swh:1:rev:{anchor}")
    if path:
        qualifiers.append(f"path={path}")
    qualified_swhid = ";".join([f"swh:1:cnt:{sha}"] + qualifiers)

    # --- SWH verification ---------------------------------------------------
    cnt_known = rev_known = ori_known = None
    if not args.no_verify:
        ids = [f"swh:1:cnt:{sha}"]
        if anchor:
            ids.append(f"swh:1:rev:{anchor}")
        known = swh_known(ids)
        cnt_known = known.get(f"swh:1:cnt:{sha}")
        if anchor:
            rev_known = known.get(f"swh:1:rev:{anchor}")
        if args.origin:
            ori_known = swh_origin_known(args.origin)
        print(f"SWH: cnt_known={cnt_known}"
              + (f", rev_known={rev_known}" if anchor else "")
              + (f", ori_known={ori_known}" if args.origin else ""))
        if cnt_known is False and not args.allow_unarchived:
            sys.exit("ERROR: SWH does not know these bytes. The collection's "
                     "premise is SWH-archived evidence — double-check the file, "
                     "or pass --allow-unarchived to proceed anyway.")
        if rev_known is False or ori_known is False:
            print("WARNING: provenance qualifiers not (fully) verifiable in SWH — "
                  "this sample will show up in the aspirational-provenance audit "
                  "(docs/samples_aspirational_provenance.md). The bytes are still "
                  "citable by their bare content SWHID.")

    # --- Compose metadata ---------------------------------------------------
    github_raw_url = None
    if args.origin and args.origin.startswith("https://github.com/") and anchor and path:
        repo = args.origin[len("https://github.com/"):].rstrip("/")
        github_raw_url = (f"https://raw.githubusercontent.com/{repo}/{anchor}"
                          f"{urllib.parse.quote(path)}")
    meta = {
        "language_claim": args.language or (pl_id if pl_id else "_review_queue"),
        "predicted_pl_id": pl_id or "",
        "predicted_via": "manual-request",
        "predicted_confidence": "high" if pl_id else "none",
        "predicted_heuristic_id": None,
        "predicted_matches_claim": "",
        "filename": filename,
        "length_bytes": len(data),
        "expected_length_bytes": len(data),
        "sha1_git": sha,
        "sha1_git_matches": True,
        "qualified_swhid": qualified_swhid,
        "swh_browser_url": f"{SWH_BASE}/{qualified_swhid}/",
        "swh_raw_url": f"{SWH_BASE}/api/1/content/sha1_git:{sha}/raw/",
        "github_raw_url": github_raw_url,
        "fetched_from": fetched_from,
        "ext": ext,
        "occurrences_in_swh": args.occurrences,
    }
    if args.notes:
        meta["notes"] = args.notes

    # --- Write --------------------------------------------------------------
    sample_dir = Path(args.samples_dir) / target_slot / sha
    file_path = sample_dir / filename
    if sample_dir.exists() and not args.overwrite:
        sys.exit(f"ERROR: {sample_dir.relative_to(ROOT) if sample_dir.is_relative_to(ROOT) else sample_dir} "
                 f"already exists. Use --overwrite to replace it.")
    if args.dry_run:
        print(f"\n[dry-run] would write:\n  {file_path}\n  {sample_dir / 'metadata.json'}")
        print(json.dumps(meta, indent=2))
        return 0
    sample_dir.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(data)
    (sample_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nOK   {target_slot}/{sha[:12]}/{filename}")
    print(f"     {sample_dir / 'metadata.json'}")
    print("\nNext steps:")
    print(f"  - it will surface on /ext/{ext.lstrip('.')}/index.html#samples at the next site build")
    print("  - optionally run: python3 tools/verify_swh_samples.py   (refresh the audit CSV)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
