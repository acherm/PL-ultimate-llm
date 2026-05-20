#!/usr/bin/env python3
"""Materialize a `pl-contribute` GitHub issue into:
  - a row in `data/derived/extension_labels.csv` claiming `ext → pl/<id>`
    (with `curator_status="accepted"`, because the PR merge IS the
    maintainer's approval), and
  - optionally, program files under
    `languages/<folder>/programs/<sha256>/{code.<ext>,manifest.json}`
    when the submitter pasted code.

Reads ONE issue (by `--issue NN`), parses its structured YAML block,
validates the target PL, and writes the file diff. The workflow
`.github/workflows/pl_contribute_pr.yml` commits + PRs the result.

Expected issue body (built by the "Propose a file extension" form on
/l/<slug>/):

    ```yaml
    pl_name: "Oaklisp"
    pl_folder: "Oaklisp"
    pl_id: "pl/oaklisp"
    ext: ".oak"
    reference_url: "https://github.com/barak/oaklisp/blob/master/src/world/math.oak"
    friendly_name: ""                    # optional
    notes: |                              # optional
      (free text)
    program: null                         # or a block:
    program:
      title: "Math utilities"             # optional
      license_guess: "GPL-2.0"            # optional
      code: |                             # optional — if present, becomes a program
        (verbatim bytes)
    ```

Required fields: `pl_name`, `pl_id`, `ext`, `reference_url`. The
program block is fully optional; if `code:` is set, `title` defaults
to "Example".

Exit codes:
  0  → success
  2  → validation failure
  3  → no `pl-contribute` YAML block found
"""

from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PL_LIST = ROOT / "data" / "pl_list.txt"
LANGUAGES_DIR = ROOT / "languages"
LABELS_CSV = ROOT / "data" / "derived" / "extension_labels.csv"
LABELS_SCHEMA = [
    "ext", "label", "friendly_name", "reference_url", "annotator",
    "submitted_at", "evidence", "issue_url",
    "issue_state", "issue_number", "curator_status",
]

_YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
_PL_NAME_RE = re.compile(r'^pl_name:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_PL_FOLDER_RE = re.compile(r'^pl_folder:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
_PL_ID_RE = re.compile(r'^pl_id:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_EXT_RE = re.compile(r'^ext:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_REF_URL_RE = re.compile(r'^reference_url:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_FRIENDLY_RE = re.compile(r'^friendly_name:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
_NOTES_RE = re.compile(r'^notes:\s*\|\s*\n((?:^[ \t]+.*\n?|^\n)+)', re.MULTILINE)
_PROGRAM_KEYS = {"title", "license_guess"}


def _gh_fetch_issue(owner_repo: str, number: int) -> dict:
    r = subprocess.run(
        ["gh", "api", f"repos/{owner_repo}/issues/{number}"],
        check=True, text=True, capture_output=True,
    )
    return json.loads(r.stdout)


def _parse_program_block(yaml_body: str) -> dict | None:
    """Extract the optional `program:` sub-block."""
    # `[ \t]*` (not `\s*`) so we don't eat the newline + indented child key.
    m = re.search(r'^program:[ \t]*(.*)$', yaml_body, re.MULTILINE)
    if not m:
        return None
    inline = m.group(1).strip()
    # Explicit null inline → skeleton submission.
    if inline in ("null", "~"):
        return None
    prog_start = m.end() + 1
    rest = yaml_body[prog_start:]
    # Stop at the next top-level key in our schema.
    top_re = re.compile(
        r'^(notes|pl_name|pl_folder|pl_id|ext|reference_url|friendly_name):\s',
        re.MULTILINE,
    )
    next_top = top_re.search(rest)
    block = rest[: next_top.start()] if next_top else rest
    # The YAML-fence capture strips the trailing newline; ensure every
    # captured line (including the last) is terminated so the code-body
    # regex can match it uniformly.
    if not block.endswith("\n"):
        block += "\n"
    result: dict = {}
    for k in _PROGRAM_KEYS:
        kre = re.compile(rf'^\s+{k}:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
        km = kre.search(block)
        if km:
            result[k] = km.group(1).strip()
    code_m = re.search(
        r'^\s+code:\s*\|\s*\n((?:^[ \t]+[^\n]*\n|^\n)+)',
        block,
        re.MULTILINE,
    )
    if code_m:
        lines = code_m.group(1).splitlines()
        if lines:
            indent = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
            result["code"] = "\n".join(l[indent:] if l.strip() else "" for l in lines).rstrip("\n")
    return result if (result.get("code") or result.get("title") or result.get("license_guess")) else None


def _parse_block_scalar(body: str, regex: re.Pattern) -> str:
    """Parse a `|`-style block scalar, returning the dedented body."""
    m = regex.search(body)
    if not m:
        return ""
    lines = m.group(1).splitlines()
    if not lines:
        return ""
    indent = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
    return "\n".join(l[indent:] if l.strip() else "" for l in lines).strip()


def _parse_issue_body(body: str) -> dict | None:
    if not body:
        return None
    bm = _YAML_BLOCK.search(body)
    if not bm:
        return None
    # The fence capture strips the trailing newline; restore it so every
    # block-scalar regex sees the last line uniformly terminated.
    yaml_body = bm.group(1)
    if not yaml_body.endswith("\n"):
        yaml_body += "\n"
    name_m = _PL_NAME_RE.search(yaml_body)
    id_m = _PL_ID_RE.search(yaml_body)
    ext_m = _EXT_RE.search(yaml_body)
    ref_m = _REF_URL_RE.search(yaml_body)
    if not (name_m and id_m and ext_m and ref_m):
        return None
    folder_m = _PL_FOLDER_RE.search(yaml_body)
    friendly_m = _FRIENDLY_RE.search(yaml_body)
    ext = ext_m.group(1).strip()
    if not ext.startswith("."):
        ext = "." + ext
    return {
        "pl_name": name_m.group(1).strip(),
        "pl_folder": folder_m.group(1).strip() if folder_m else "",
        "pl_id": id_m.group(1).strip(),
        "ext": ext,
        "reference_url": ref_m.group(1).strip(),
        "friendly_name": friendly_m.group(1).strip() if friendly_m else "",
        "notes": _parse_block_scalar(yaml_body, _NOTES_RE),
        "program": _parse_program_block(yaml_body),
    }


def _code_sha256(code: str) -> str:
    normalized = "\n".join(line.rstrip() for line in code.splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _safe_dir_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("_") or "Unnamed"


def _pl_list_contains(name: str) -> bool:
    if not PL_LIST.exists():
        return False
    existing = {line.strip().lower() for line in PL_LIST.read_text(encoding="utf-8").splitlines() if line.strip()}
    return name.lower() in existing


def _resolve_language_dir(pl_name: str, pl_folder: str) -> Path | None:
    candidates: list[str] = []
    if pl_folder:
        candidates.append(pl_folder)
    candidates.append(_safe_dir_name(pl_name))
    for c in candidates:
        if "/" in c or ".." in c or c.startswith("."):
            continue
        d = LANGUAGES_DIR / c
        if (d / "meta.json").exists():
            return d
    return None


def _upsert_label_row(*, ext: str, pl_id: str, friendly_name: str,
                      reference_url: str, annotator: str,
                      submitted_at: str, notes: str, issue_url: str,
                      issue_state: str, issue_number: int) -> None:
    """Append (or update) a row in extension_labels.csv keyed by
    (issue_url, label). Sets curator_status to `accepted` — the PR merge
    is the maintainer's approval."""
    rows: list[dict] = []
    if LABELS_CSV.exists():
        with LABELS_CSV.open() as f:
            rows = list(csv.DictReader(f))
    key = (issue_url, pl_id)
    new_row = {
        "ext": ext,
        "label": pl_id,
        "friendly_name": friendly_name,
        "reference_url": reference_url,
        "annotator": annotator,
        "submitted_at": submitted_at,
        "evidence": notes,
        "issue_url": issue_url,
        "issue_state": issue_state,
        "issue_number": str(issue_number),
        "curator_status": "accepted",
    }
    replaced = False
    for i, r in enumerate(rows):
        if (r.get("issue_url"), r.get("label")) == key:
            rows[i] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)
    LABELS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with LABELS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LABELS_SCHEMA)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in LABELS_SCHEMA})


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--issue", type=int, required=True, help="Issue number to process.")
    p.add_argument("--repo", default=None, help="owner/name (default: `gh repo view`).")
    p.add_argument("--dry-run", action="store_true", help="Show parsed payload; don't write files.")
    args = p.parse_args()

    repo = args.repo
    if not repo:
        r = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            check=True, text=True, capture_output=True,
        )
        rd = json.loads(r.stdout)
        repo = f"{rd['owner']['login']}/{rd['name']}"
    print(f"Repo: {repo}, issue: #{args.issue}")

    try:
        issue = _gh_fetch_issue(repo, args.issue)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: gh api failed: {e.stderr}")

    labels = [(l.get("name") if isinstance(l, dict) else l) for l in (issue.get("labels") or [])]
    if "pl-contribute" not in labels:
        sys.exit(f"ERROR: issue #{args.issue} is missing the `pl-contribute` label (has: {labels})")

    parsed = _parse_issue_body(issue.get("body") or "")
    if not parsed:
        print("ERROR: could not parse structured YAML block (need pl_name, pl_id, ext, reference_url).")
        return 3

    print("Parsed:")
    print(json.dumps({k: v for k, v in parsed.items() if k != "program"}, indent=2))
    prog = parsed["program"]
    if prog:
        prog_summary = {k: v for k, v in prog.items() if k != "code"}
        prog_summary["code_lines"] = len(prog.get("code", "").splitlines())
        print(f"program: {json.dumps(prog_summary, indent=2)}")
    else:
        print("program: (none — ext-only submission)")

    if not _pl_list_contains(parsed["pl_name"]):
        print(f"ERROR: '{parsed['pl_name']}' is not in pl_list.txt — use /contribute/add-pl/ first.")
        return 2
    lang_dir = _resolve_language_dir(parsed["pl_name"], parsed["pl_folder"])
    if lang_dir is None:
        print(f"ERROR: cannot locate languages/<folder>/meta.json for pl_name='{parsed['pl_name']}' (hint: '{parsed['pl_folder']}').")
        return 2
    print(f"Target dir: {lang_dir.relative_to(ROOT)}")

    annotator = (issue.get("user") or {}).get("login", "")
    submitted_at = issue.get("created_at", "")
    issue_url = issue.get("html_url", "")
    issue_state = issue.get("state", "")

    if args.dry_run:
        print("\n--- DRY RUN — exiting before file writes ---")
        return 0

    # 1. Extension label → extension_labels.csv (curator_status=accepted).
    _upsert_label_row(
        ext=parsed["ext"],
        pl_id=parsed["pl_id"],
        friendly_name=parsed["friendly_name"],
        reference_url=parsed["reference_url"],
        annotator=annotator,
        submitted_at=submitted_at,
        notes=parsed["notes"],
        issue_url=issue_url,
        issue_state=issue_state,
        issue_number=args.issue,
    )
    print(f"WROTE {LABELS_CSV.relative_to(ROOT)} (label '{parsed['pl_id']}' on '{parsed['ext']}' → accepted)")

    # 2. Optional program → languages/<folder>/programs/<sha>/...
    has_program = False
    program_sha = ""
    if prog and prog.get("code"):
        ext_no_dot = parsed["ext"].lstrip(".") or "txt"
        sha = _code_sha256(prog["code"])
        prog_dir = lang_dir / "programs" / sha
        if prog_dir.exists():
            print(f"WARNING: program with sha256 {sha} already exists at {prog_dir.relative_to(ROOT)} — skipping program write.")
        else:
            prog_dir.mkdir(parents=True, exist_ok=True)
            normalized = "\n".join(line.rstrip() for line in prog["code"].splitlines())
            (prog_dir / f"code.{ext_no_dot}").write_text(normalized + "\n", encoding="utf-8")
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            manifest = {
                "title": prog.get("title") or "Example",
                "origin_url": parsed["reference_url"],
                "license_guess": prog.get("license_guess") or None,
                "code_sha256": sha,
                "added_at": now,
                "created_via_issue": args.issue,
            }
            (prog_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"WROTE {(prog_dir / f'code.{ext_no_dot}').relative_to(ROOT)}")
            print(f"WROTE {(prog_dir / 'manifest.json').relative_to(ROOT)}")
            has_program = True
            program_sha = sha

    # 3. Workflow-readable summary.
    summary_path = ROOT / ".tmp" / f"pl_contribute_summary_{args.issue}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps({
        "pl_name": parsed["pl_name"],
        "pl_folder": lang_dir.name,
        "pl_id": parsed["pl_id"],
        "ext": parsed["ext"],
        "reference_url": parsed["reference_url"],
        "has_program": has_program,
        "program_sha256": program_sha,
        "issue": args.issue,
    }, indent=2), encoding="utf-8")
    print(f"WROTE {summary_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
