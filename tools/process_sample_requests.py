#!/usr/bin/env python3
"""Process open `sample-request` GitHub issues.

Workflow:
  1. List open issues labelled `sample-request` via `gh api`.
  2. Parse each issue body's YAML block to extract the target extension.
  3. Build a target file (one ext per line) and invoke
     `tools/swh_extension_mining.py --mine-extensions <file> --execute`.
  4. Run `tools/fetch_samples.py` to materialize any newly-qualified bytes
     to `samples/unclassified/<sha>/`.
  5. For each issue, count how many sample files now exist for its extension
     (under `samples/`) and comment on the issue. Close the issue if any
     samples were materialized; otherwise leave it open with a "no samples
     found" comment so a maintainer can retry later.

Typical usage:
    python3 tools/process_sample_requests.py            # do the run
    python3 tools/process_sample_requests.py --dry-run  # just show plan

Use `--no-close` to comment without closing (e.g. when the run is
exploratory and you want maintainer review before resolution).

The script is idempotent on the bytes side (mining + fetch only ADD files,
never delete). Comments are appended; closed issues are skipped on re-run.
"""

from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
TARGETS_FILE = ROOT / "data" / "derived" / "sample_request_targets.txt"
MINING_OUT_CSV = ROOT / "data" / "derived" / "swh_extension_samples_requests.csv"

_YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
_EXT_RE = re.compile(r'^ext:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_NOTES_RE = re.compile(r'^notes:\s*\|\s*\n((?:^[ \t]+.*\n?)+)', re.MULTILINE)

# Require at least one alpha char in the extension. Otherwise we end up
# scanning the archive for `.0`, `.1`, … which mostly match PyPI version
# suffixes (`aiographite-0.2.0`) and similar packaging detritus rather than
# anything that could plausibly be a PL. Power-users who really want to mine
# a numeric extension can still bypass this by calling
# `swh_extension_mining.py --mine-extensions` directly.
_EXT_VALID = re.compile(r"^\.[A-Za-z][A-Za-z0-9_+\-]{0,7}$")


def gh_owner_repo() -> str | None:
    try:
        r = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            check=True, text=True, capture_output=True,
        )
        data = json.loads(r.stdout)
        return f"{data['owner']['login']}/{data['name']}"
    except Exception:
        return None


def fetch_open_requests(owner_repo: str) -> list[dict]:
    cmd = [
        "gh", "api",
        f"repos/{owner_repo}/issues?labels=sample-request&state=open&per_page=100",
        "--paginate",
    ]
    r = subprocess.run(cmd, check=True, text=True, capture_output=True)
    txt = r.stdout.strip()
    if not txt:
        return []
    try:
        parsed = json.loads(txt)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        items, depth, start = [], 0, 0
        for i, c in enumerate(txt):
            if c == "[":
                if depth == 0:
                    start = i
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    items.extend(json.loads(txt[start:i + 1]))
        return items
    return []


def parse_request_body(body: str) -> dict | None:
    if not body:
        return None
    m = _YAML_BLOCK.search(body)
    if not m:
        return None
    block = m.group(1)
    ext_m = _EXT_RE.search(block)
    if not ext_m:
        return None
    ext = ext_m.group(1).strip()
    if not ext.startswith("."):
        ext = "." + ext
    notes = ""
    nm = _NOTES_RE.search(block)
    if nm:
        lines = nm.group(1).splitlines()
        if lines:
            indent = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
            notes = "\n".join(l[indent:] for l in lines).strip()
    return {"ext": ext, "notes": notes}


def count_samples_for_ext(ext: str) -> int:
    """Walk samples/ for files whose suffix matches `ext` (case-insensitive)."""
    if not SAMPLES_DIR.exists():
        return 0
    target = ext.lower()
    n = 0
    for p in SAMPLES_DIR.rglob("*"):
        if not p.is_file():
            continue
        if p.name == "metadata.json":
            continue
        if p.suffix.lower() == target:
            n += 1
    return n


def comment_and_close(
    *, owner_repo: str, issue_number: int, body: str, close: bool,
) -> None:
    """Post a comment on the issue. Optionally close it."""
    subprocess.run(
        ["gh", "issue", "comment", str(issue_number),
         "--repo", owner_repo, "--body", body],
        check=True,
    )
    if close:
        subprocess.run(
            ["gh", "issue", "close", str(issue_number),
             "--repo", owner_repo,
             "--comment", "Closing — samples materialized; the next site build will surface them."],
            check=True,
        )


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would happen; don't mine, comment, or close.")
    p.add_argument("--no-close", action="store_true",
                   help="Comment on issues but don't close them.")
    p.add_argument("--limit", type=int, default=50,
                   help="Max requests to process per run.")
    p.add_argument("--repo", default=None,
                   help="owner/repo override; defaults to `gh repo view`.")
    p.add_argument("--qualify-max-candidates", type=int, default=5,
                   help="Passed through to swh_extension_mining.py.")
    args = p.parse_args()

    repo = args.repo or gh_owner_repo()
    if not repo:
        sys.exit("ERROR: could not resolve repo; pass --repo owner/name.")
    print(f"Repo: {repo}")

    try:
        issues = fetch_open_requests(repo)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: gh api failed: {e.stderr}")
    print(f"Open sample-request issues: {len(issues)}")
    if not issues:
        return 0
    issues = issues[: args.limit]

    # Parse + dedupe by extension.
    parsed: list[tuple[dict, dict]] = []  # (issue, request)
    rejected: list[tuple[dict, str]] = []  # (issue, ext) — invalid extension
    exts: dict[str, list[dict]] = {}  # ext -> list of issues asking for it
    for it in issues:
        if it.get("pull_request"):
            continue
        req = parse_request_body(it.get("body") or "")
        if not req:
            print(f"  skip #{it['number']}: unparseable body")
            continue
        if not _EXT_VALID.match(req["ext"]):
            print(f"  reject #{it['number']}: ext {req['ext']!r} fails validation")
            rejected.append((it, req["ext"]))
            continue
        parsed.append((it, req))
        exts.setdefault(req["ext"], []).append(it)

    if rejected and not args.dry_run:
        for it, ext in rejected:
            body = (
                f"Cannot mine `{ext}` — extension must contain at least one "
                f"letter (matches `^\\.[A-Za-z][A-Za-z0-9_+\\-]{{0,7}}$`). "
                f"Pure-numeric extensions like `.0`/`.1` overwhelmingly match "
                f"packaging version suffixes (`foo-1.2.0`) rather than program "
                f"files, so the scan would burn S3 traffic for noise.\n\n"
                f"If you genuinely need this, ask a maintainer to run "
                f"`tools/swh_extension_mining.py --mine-extensions` directly."
            )
            comment_and_close(
                owner_repo=repo,
                issue_number=it["number"],
                body=body,
                close=not args.no_close,
            )

    if not parsed:
        print("Nothing to do (no parseable requests).")
        return 0

    print(f"Distinct extensions to mine: {len(exts)}")
    for ext, issue_list in exts.items():
        nums = ", ".join(f"#{i['number']}" for i in issue_list)
        print(f"  {ext}  ← {nums}")

    if args.dry_run:
        print("\n--- DRY RUN — exiting before mining ---")
        return 0

    # Write target file (one ext per line, no leading dot).
    TARGETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TARGETS_FILE.open("w") as f:
        f.write("# Auto-generated by tools/process_sample_requests.py\n")
        for ext in sorted(exts.keys()):
            f.write(ext.lstrip(".") + "\n")
    print(f"\nWrote targets to {TARGETS_FILE}")

    # Run the mining.
    print("\n=== Running swh_extension_mining.py ===")
    mining_cmd = [
        sys.executable, "-u",
        str(ROOT / "tools" / "swh_extension_mining.py"),
        "--mine-extensions", str(TARGETS_FILE),
        "--out-csv", str(MINING_OUT_CSV),
        "--qualify-max-candidates", str(args.qualify_max_candidates),
        "--execute",
    ]
    print(" ".join(mining_cmd))
    r = subprocess.run(mining_cmd)
    if r.returncode != 0:
        print(f"WARNING: mining exited with code {r.returncode}")

    # Materialize bytes.
    print("\n=== Running fetch_samples.py ===")
    fetch_cmd = [sys.executable, str(ROOT / "tools" / "fetch_samples.py")]
    r = subprocess.run(fetch_cmd)
    if r.returncode != 0:
        print(f"WARNING: fetch_samples exited with code {r.returncode}")

    # Comment + close each issue.
    print("\n=== Updating issues ===")
    for issue, req in parsed:
        ext = req["ext"]
        n = count_samples_for_ext(ext)
        if n > 0:
            ext_slug = ext.lstrip(".")
            body = (
                f"Sample-mining run completed for `{ext}`.\n\n"
                f"- Samples now on disk: **{n}**\n"
                f"- Browse at `/ext/{ext_slug}/index.html#samples` once the next site "
                f"build deploys.\n\n"
                f"Closing this request; reopen if the samples don't help."
            )
            comment_and_close(
                owner_repo=repo,
                issue_number=issue["number"],
                body=body,
                close=not args.no_close,
            )
            print(f"  #{issue['number']} ({ext}): {n} samples → "
                  f"{'closed' if not args.no_close else 'commented (kept open)'}")
        else:
            body = (
                f"Sample-mining run completed for `{ext}` but **no archived bytes "
                f"matched** (the SWH parquet query returned 0 verbatim files for this "
                f"extension within the queried sample window).\n\n"
                f"Keeping this issue open. A maintainer can retry with a different "
                f"shard scope or wider candidate-per-ext limit."
            )
            comment_and_close(
                owner_repo=repo,
                issue_number=issue["number"],
                body=body,
                close=False,
            )
            print(f"  #{issue['number']} ({ext}): 0 samples → commented (kept open)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
