#!/usr/bin/env python3
"""Ingest manual extension labels from GitHub issues.

Looks for issues with label `ext-review` in the repo, parses the structured
YAML block in each body, and writes/updates
`data/derived/extension_labels.csv`.

Expected issue body format (built by the /review/extensions/ page):

    ```yaml
    ext: ".pbf"
    proposed_label: "binary:other"
    evidence: |
      OpenStreetMap protocol buffers binary. Spec at https://...
    ```

Schema of `data/derived/extension_labels.csv` (written here):

    ext, label, annotator, submitted_at, evidence, issue_url, issue_state, curator_status

`curator_status` is one of:
    - 'new'         — just imported from an issue
    - 'accepted'    — maintainer reviewed and accepted
    - 'rejected'    — maintainer reviewed and rejected (kept for audit)
    - 'needs-info'  — maintainer requested more evidence

Run:
    python3 tools/process_extension_labels.py [--limit N] [--dry-run]

Requires `gh auth login`. Reads, never writes to GitHub.
"""

from __future__ import annotations
import argparse
import csv
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "data" / "derived" / "extension_labels.csv"
SCHEMA = [
    "ext", "label", "friendly_name", "reference_url", "annotator",
    "submitted_at", "evidence", "issue_url",
    "issue_state", "issue_number", "curator_status",
]


def gh_owner_repo() -> str | None:
    """Best-effort: resolve the repo's owner/name via `gh repo view`."""
    try:
        r = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            check=True, text=True, capture_output=True,
        )
        data = json.loads(r.stdout)
        return f"{data['owner']['login']}/{data['name']}"
    except Exception:
        return None


def fetch_issues(*, owner_repo: str, label: str = "ext-review", limit: int = 500) -> list[dict]:
    """Return open + closed issues with the given label."""
    cmd = [
        "gh", "api",
        f"repos/{owner_repo}/issues?labels={label}&state=all&per_page=100",
        "--paginate",
    ]
    r = subprocess.run(cmd, check=True, text=True, capture_output=True)
    items: list[dict] = []
    # gh api with --paginate concatenates JSON arrays; can be a single big array
    # or multiple. Try to robustly parse both.
    txt = r.stdout.strip()
    if not txt:
        return []
    try:
        parsed = json.loads(txt)
        if isinstance(parsed, list):
            items = parsed
    except json.JSONDecodeError:
        # Multiple arrays concatenated — split and merge.
        depth = 0
        start = 0
        for i, c in enumerate(txt):
            if c == "[":
                if depth == 0:
                    start = i
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    chunk = txt[start:i+1]
                    items.extend(json.loads(chunk))
    items = items[:limit]
    return items


_YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
_EXT_RE      = re.compile(r'^ext:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
# Accept both `label:` (new schema) and `proposed_label:` (legacy, pre-form).
_LBL_RE      = re.compile(r'^(?:label|proposed_label):\s*[\"\']?([^\"\'\n#]+?)[\"\']?\s*(?:#.*)?$', re.MULTILINE)
_FRIENDLY_RE = re.compile(r'^friendly_name:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
_REFURL_RE   = re.compile(r'^reference_url:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
_EVD_RE      = re.compile(r'^evidence:\s*\|\s*\n((?:^[ \t]+.*\n?)+)', re.MULTILINE)


def parse_issue_body(body: str) -> dict | None:
    """Extract structured fields from the YAML block in an issue body.

    Required: ext + label. Optional: friendly_name, reference_url, evidence.
    Returns None if required fields are missing or the placeholder text wasn't
    edited by the reviewer.
    """
    if not body:
        return None
    m = _YAML_BLOCK.search(body)
    if not m:
        return None
    block = m.group(1)
    ext_m = _EXT_RE.search(block)
    lbl_m = _LBL_RE.search(block)
    if not (ext_m and lbl_m):
        return None
    ext = ext_m.group(1).strip()
    label = lbl_m.group(1).strip()
    # Reject obvious placeholders.
    if label in ("<change to a label from docs/extension_labels.md>", "", "<unset>"):
        return None
    if label.startswith("<") and label.endswith(">"):
        return None
    friendly = (_FRIENDLY_RE.search(block) or [None, ""])[1].strip() if _FRIENDLY_RE.search(block) else ""
    ref_url  = (_REFURL_RE.search(block)   or [None, ""])[1].strip() if _REFURL_RE.search(block)   else ""
    evd_m = _EVD_RE.search(block)
    evidence = ""
    if evd_m:
        lines = evd_m.group(1).splitlines()
        if lines:
            indent = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
            evidence = "\n".join(l[indent:] for l in lines).strip()
    return {
        "ext": ext, "label": label, "evidence": evidence,
        "friendly_name": friendly, "reference_url": ref_url,
    }


def load_existing() -> list[dict]:
    if not OUT_CSV.exists():
        return []
    with OUT_CSV.open() as f:
        return list(csv.DictReader(f))


def write_csv(rows: list[dict]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in SCHEMA})


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--limit", type=int, default=500,
                   help="Max issues to fetch (default: %(default)s).")
    p.add_argument("--owner-repo", default=None,
                   help="owner/repo (default: auto-detected via `gh repo view`).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be written; don't update the CSV.")
    args = p.parse_args()

    repo = args.owner_repo or gh_owner_repo()
    if not repo:
        sys.exit("ERROR: couldn't determine owner/repo. Pass --owner-repo or run `gh repo view`.")

    print(f"Fetching ext-review issues from {repo}…")
    try:
        issues = fetch_issues(owner_repo=repo, limit=args.limit)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: gh api failed: {e.stderr}")
    print(f"  fetched: {len(issues)}")

    existing = load_existing()
    # Key by (issue_url, label) so multi-PL submissions (one issue, comma-
    # separated `label:`) produce one CSV row per label without colliding.
    by_key: dict[tuple[str, str], dict] = {
        (r.get("issue_url", ""), r.get("label", "")): r for r in existing
    }

    parsed = 0
    skipped = 0
    multi_label_rows = 0
    new_rows = list(existing)  # carry-over previously-curated rows
    # Track the set of labels each successfully-parsed issue currently asserts.
    # After the loop we use this to RECONCILE: drop any pre-existing row whose
    # issue we just reprocessed but whose label is no longer in the body
    # (e.g. an annotator edited their submission from `pl/pl/c, pl/cpp,
    # pl/objective-c` to `pl/c, pl/cpp, pl/objective-c` — the stale `pl/pl/c`
    # row shouldn't survive). Maintainer-confirmed statuses are preserved.
    current_labels_by_url: dict[str, set[str]] = {}
    for it in issues:
        url = it.get("html_url")
        if not url:
            continue
        parsed_data = parse_issue_body(it.get("body") or "")
        if not parsed_data:
            skipped += 1
            continue
        annotator = (it.get("user") or {}).get("login", "")
        submitted_at = it.get("created_at", "")

        # Split comma-separated labels — `.h` style multi-PL submissions
        # expand into N rows (one per pl_id), all sharing the same issue.
        raw_label = parsed_data["label"] or ""
        labels = [l.strip() for l in raw_label.split(",") if l.strip()]
        if not labels:
            skipped += 1
            continue
        if len(labels) > 1:
            multi_label_rows += 1
        current_labels_by_url[url] = set(labels)

        for label_value in labels:
            common_fields = {
                "ext": parsed_data["ext"],
                "label": label_value,
                "friendly_name": parsed_data.get("friendly_name", ""),
                "reference_url": parsed_data.get("reference_url", ""),
                "annotator": annotator,
                "submitted_at": submitted_at,
                "evidence": parsed_data.get("evidence", ""),
                "issue_url": url,
                "issue_state": it.get("state", ""),
                "issue_number": it.get("number", ""),
            }
            key = (url, label_value)
            existing_row = by_key.get(key)
            if existing_row:
                # Preserve curator_status (and any other manually-set fields)
                # across re-imports.
                row = existing_row.copy()
                row.update(common_fields)
                for i, r in enumerate(new_rows):
                    if (r.get("issue_url"), r.get("label")) == key:
                        new_rows[i] = row
                        break
            else:
                row = dict(common_fields)
                # Accepted by default: this project is small enough that
                # blocking on a manual curator-flip created more friction
                # than it removed. The maintainer can still flip to
                # `rejected` / `needs-info` later by editing the CSV;
                # preservation logic above keeps any maintainer-set
                # status across re-imports.
                row["curator_status"] = "accepted"
                new_rows.append(row)
        parsed += 1

    # Reconcile per-issue: drop rows whose issue we just reprocessed but whose
    # label is no longer in the current body. Maintainer-confirmed rows
    # (curator_status in {accepted, needs-info}) are preserved as a safety
    # net — the maintainer's call sticks even if the annotator later edits
    # away the label.
    PRESERVED = {"accepted", "needs-info"}
    before = len(new_rows)
    dropped_rows: list[dict] = []
    kept_rows: list[dict] = []
    for r in new_rows:
        url = r.get("issue_url", "")
        label = r.get("label", "")
        status = r.get("curator_status", "")
        if url in current_labels_by_url and label not in current_labels_by_url[url] and status not in PRESERVED:
            dropped_rows.append(r)
        else:
            kept_rows.append(r)
    new_rows = kept_rows
    print(f"  parsed: {parsed}, skipped (no structured block): {skipped}, "
          f"multi-label issues: {multi_label_rows}")
    if dropped_rows:
        print(f"  reconciled: dropped {len(dropped_rows)} stale row(s) "
              f"whose label is no longer in the issue body")
        for r in dropped_rows:
            print(f"    drop: {r.get('ext','')}  label={r.get('label','')}  "
                  f"issue={r.get('issue_url','')}  status={r.get('curator_status','')}")
    print(f"  total rows in output: {len(new_rows)} (was {before})")

    if args.dry_run:
        print("(dry-run; CSV NOT updated)")
        for r in new_rows[-5:]:
            print(" ", {k: r[k] for k in ("ext","label","annotator","curator_status")})
        return 0
    write_csv(new_rows)
    print(f"Wrote {OUT_CSV}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
