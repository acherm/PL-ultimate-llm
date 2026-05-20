#!/usr/bin/env python3
"""Materialize a `pl-program-add` GitHub issue into a program for an
existing PL.

Reads ONE issue (by number, via `--issue NN`), parses its structured YAML
block, validates that the target PL already exists in the catalog, and
writes:

  - `languages/<folder>/programs/<sha256>/code.<ext>`
  - `languages/<folder>/programs/<sha256>/manifest.json`

The `manifest.json` carries `created_via_issue: <N>` so the per-PL page
can render the submission's provenance link.

Run from the `.github/workflows/pl_program_add_pr.yml` workflow on a
clean worktree. The workflow is responsible for committing on a feature
branch and opening the pull request — this script only produces the file
diff.

Exit codes:
  0  → success, files written, ready to commit
  2  → validation failure (PL not in catalog, missing required fields,
       duplicate sha already on disk, etc.)
  3  → no `pl-program-add` YAML block found in the issue body
"""

from __future__ import annotations
import argparse
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

_YAML_BLOCK = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
_PL_NAME_RE = re.compile(r'^pl_name:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_PL_FOLDER_RE = re.compile(r'^pl_folder:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_PROGRAM_KEYS = {"title", "ext", "origin_url", "license_guess"}


def _gh_fetch_issue(owner_repo: str, number: int) -> dict:
    r = subprocess.run(
        ["gh", "api", f"repos/{owner_repo}/issues/{number}"],
        check=True, text=True, capture_output=True,
    )
    return json.loads(r.stdout)


def _parse_program_block(yaml_body: str) -> dict | None:
    """Extract the `program:` sub-block. Mirrors the parser in
    tools/process_pl_addition.py for schema parity."""
    # `[ \t]*` (not `\s*`) so we don't eat the newline + first indented
    # child key — otherwise `(.*)` ends up matching `title: "..."` and the
    # title silently disappears. Same root cause as the bug noted in
    # tools/process_pl_addition.py (kept there to avoid scope creep — the
    # existing pl-add flow has only ever shipped skeleton proposals so it
    # never tripped).
    m = re.search(r'^program:[ \t]*(.*)$', yaml_body, re.MULTILINE)
    if not m:
        return None
    inline = m.group(1).strip()
    # Explicit null inline scalar → skeleton submission. Empty inline is
    # the normal "multi-line block follows" case; don't bail there.
    if inline in ("null", "~"):
        return None
    prog_start = m.end() + 1
    rest = yaml_body[prog_start:]
    # Stop at the next top-level key in OUR schema.
    top_re = re.compile(r'^(notes|pl_name|pl_folder):\s', re.MULTILINE)
    next_top = top_re.search(rest)
    block = rest[: next_top.start()] if next_top else rest
    result: dict = {}
    for k in _PROGRAM_KEYS:
        kre = re.compile(rf'^\s+{k}:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
        km = kre.search(block)
        if km:
            result[k] = km.group(1).strip()
    # Match `code: |` body: indented lines OR blank lines (so pasted code
    # with blank lines between blocks survives the parse). Stops at the
    # next less-indented line — which is guaranteed because `block` was
    # already trimmed at the next top-level key.
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
    return result


def _parse_issue_body(body: str) -> dict | None:
    if not body:
        return None
    bm = _YAML_BLOCK.search(body)
    if not bm:
        return None
    yaml_body = bm.group(1)
    name_m = _PL_NAME_RE.search(yaml_body)
    folder_m = _PL_FOLDER_RE.search(yaml_body)
    if not name_m:
        return None
    return {
        "pl_name": name_m.group(1).strip(),
        "pl_folder": folder_m.group(1).strip() if folder_m else "",
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
    """Find the language directory. Prefer the explicit pl_folder hint;
    fall back to the safe-name derivation from pl_name."""
    candidates: list[str] = []
    if pl_folder:
        candidates.append(pl_folder)
    candidates.append(_safe_dir_name(pl_name))
    for c in candidates:
        # Reject path traversal — folder must be a single segment under languages/.
        if "/" in c or ".." in c or c.startswith("."):
            continue
        d = LANGUAGES_DIR / c
        if (d / "meta.json").exists():
            return d
    return None


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
    if "pl-program-add" not in labels:
        sys.exit(f"ERROR: issue #{args.issue} is missing the `pl-program-add` label (has: {labels})")

    parsed = _parse_issue_body(issue.get("body") or "")
    if not parsed:
        print("ERROR: could not parse structured YAML block.")
        return 3

    pl_name = parsed["pl_name"]
    pl_folder_hint = parsed["pl_folder"]
    prog = parsed["program"]

    print("Parsed:")
    print(json.dumps({"pl_name": pl_name, "pl_folder": pl_folder_hint}, indent=2))
    if prog:
        prog_summary = {k: v for k, v in prog.items() if k != "code"}
        prog_summary["code_lines"] = len(prog.get("code", "").splitlines())
        print(f"program: {json.dumps(prog_summary, indent=2)}")
    else:
        print("program: (none — refusing)")
        return 2

    if not prog.get("code"):
        print("ERROR: program block has no `code:` body.")
        return 2
    if not prog.get("origin_url"):
        print("ERROR: program block has no `origin_url`.")
        return 2

    if not _pl_list_contains(pl_name):
        print(f"ERROR: '{pl_name}' is not in pl_list.txt — use /contribute/add-pl/ to add the language first.")
        return 2

    lang_dir = _resolve_language_dir(pl_name, pl_folder_hint)
    if lang_dir is None:
        print(f"ERROR: cannot locate languages/<folder>/meta.json for pl_name='{pl_name}' (hint: '{pl_folder_hint}').")
        return 2
    print(f"Target dir: {lang_dir.relative_to(ROOT)}")

    if args.dry_run:
        print("\n--- DRY RUN — exiting before file writes ---")
        return 0

    ext = (prog.get("ext") or "").lstrip(".")
    if not ext:
        print("WARNING: program has no ext — saving as code.txt")
        ext = "txt"
    sha = _code_sha256(prog["code"])
    prog_dir = lang_dir / "programs" / sha
    if prog_dir.exists():
        print(f"ERROR: program with sha256 {sha} already exists at {prog_dir.relative_to(ROOT)} — refusing to duplicate.")
        return 2
    prog_dir.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(line.rstrip() for line in prog["code"].splitlines())
    (prog_dir / f"code.{ext}").write_text(normalized + "\n", encoding="utf-8")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "title": prog.get("title") or "Example",
        "origin_url": prog.get("origin_url") or "",
        "license_guess": prog.get("license_guess") or None,
        "code_sha256": sha,
        "added_at": now,
        "created_via_issue": args.issue,
    }
    (prog_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {prog_dir / f'code.{ext}'}")
    print(f"WROTE {prog_dir / 'manifest.json'}")

    summary_path = ROOT / ".tmp" / f"pl_program_add_summary_{args.issue}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps({
        "pl_name": pl_name,
        "pl_folder": lang_dir.name,
        "program_title": manifest["title"],
        "program_ext": "." + ext,
        "program_sha256": sha,
        "origin_url": manifest["origin_url"],
        "issue": args.issue,
    }, indent=2), encoding="utf-8")
    print(f"WROTE {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
