#!/usr/bin/env python3
"""Materialize a `pl-add` GitHub issue into language files + a branch.

Reads ONE issue (by number, via `--issue NN`), parses its structured YAML
block, and writes:

  - `languages/<Name>/meta.json`
  - `languages/<Name>/programs/<sha256>/code.<ext>`  (if program provided)
  - `languages/<Name>/programs/<sha256>/manifest.json`  (idem)
  - appends the canonical name to `data/pl_list.txt` (kept sorted,
    case-insensitive)

Run from the `.github/workflows/pl-add-pr.yml` workflow on a clean
worktree. The workflow is responsible for committing on a feature branch
and opening the pull request — this script only produces the file diff.

Exit codes:
  0  → success, files written, ready to commit
  2  → validation failure (name already in pl_list, malformed body, etc.).
       The workflow should comment the failure reason back on the issue.
  3  → no `pl-add` YAML block found (issue has the label but body is
       missing the structured block).
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
_NAME_RE = re.compile(r'^name:\s*[\"\']?([^\"\'\n]+)[\"\']?\s*$', re.MULTILINE)
_EVID_RE = re.compile(r'^evidence_url:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
_ALIASES_RE = re.compile(r'^aliases:\s*\[(.*?)\]\s*$', re.MULTILINE)
_PROGRAM_KEYS = {"title", "ext", "origin_url", "license_guess"}


def _gh_fetch_issue(owner_repo: str, number: int) -> dict:
    r = subprocess.run(
        ["gh", "api", f"repos/{owner_repo}/issues/{number}"],
        check=True, text=True, capture_output=True,
    )
    return json.loads(r.stdout)


def _parse_program_block(yaml_body: str) -> dict | None:
    """Extract the `program:` sub-block from the YAML scalar.

    Two valid shapes:
      program: null
      program:
        title: "..."
        ext: "..."
        origin_url: "..."
        license_guess: "..."
        code: |
          (lines)
    """
    m = re.search(r'^program:\s*(.*)$', yaml_body, re.MULTILINE)
    if not m:
        return None
    inline = m.group(1).strip()
    if inline in ("null", "~", ""):
        return None
    # Multi-line program block. Capture everything until a top-level key
    # (notes:) or end-of-block.
    prog_start = m.end() + 1  # after the newline
    rest = yaml_body[prog_start:]
    # Find next top-level key (a non-indented line starting with a known key).
    top_re = re.compile(r'^(notes|name|aliases|evidence_url):\s', re.MULTILINE)
    next_top = top_re.search(rest)
    block = rest[: next_top.start()] if next_top else rest
    result: dict = {}
    for k in _PROGRAM_KEYS:
        kre = re.compile(rf'^\s+{k}:\s*[\"\']?([^\"\'\n]*)[\"\']?\s*$', re.MULTILINE)
        km = kre.search(block)
        if km:
            result[k] = km.group(1).strip()
    # `code: |` followed by indented body
    code_m = re.search(r'^\s+code:\s*\|\s*\n((?:^[ \t]+.*\n?)+)', block, re.MULTILINE)
    if code_m:
        lines = code_m.group(1).splitlines()
        if lines:
            indent = min((len(l) - len(l.lstrip())) for l in lines if l.strip())
            result["code"] = "\n".join(l[indent:] for l in lines).rstrip("\n")
    return result


def _parse_issue_body(body: str) -> dict | None:
    if not body:
        return None
    bm = _YAML_BLOCK.search(body)
    if not bm:
        return None
    yaml_body = bm.group(1)
    name_m = _NAME_RE.search(yaml_body)
    evid_m = _EVID_RE.search(yaml_body)
    if not name_m or not evid_m:
        return None
    name = name_m.group(1).strip()
    evidence_url = evid_m.group(1).strip()
    aliases: list[str] = []
    am = _ALIASES_RE.search(yaml_body)
    if am:
        raw = am.group(1).strip()
        if raw:
            aliases = [
                a.strip().strip('"').strip("'")
                for a in re.split(r",\s*", raw) if a.strip()
            ]
    return {
        "name": name,
        "aliases": aliases,
        "evidence_url": evidence_url,
        "program": _parse_program_block(yaml_body),
    }


def _code_sha256(code: str) -> str:
    normalized = "\n".join(line.rstrip() for line in code.splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _safe_dir_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("_") or "Unnamed"


def _already_in_pl_list(name: str) -> bool:
    if not PL_LIST.exists():
        return False
    existing = {line.strip().lower() for line in PL_LIST.read_text(encoding="utf-8").splitlines() if line.strip()}
    return name.lower() in existing


def _insert_sorted(name: str) -> None:
    existing = PL_LIST.read_text(encoding="utf-8").splitlines() if PL_LIST.exists() else []
    existing = [line for line in existing if line.strip()]
    existing.append(name)
    existing.sort(key=str.lower)
    PL_LIST.write_text("\n".join(existing) + "\n", encoding="utf-8")


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
    if "pl-add" not in labels:
        sys.exit(f"ERROR: issue #{args.issue} is missing the `pl-add` label (has: {labels})")

    parsed = _parse_issue_body(issue.get("body") or "")
    if not parsed:
        print("ERROR: could not parse structured YAML block.")
        return 3

    print("Parsed:")
    print(json.dumps({k: v for k, v in parsed.items() if k != "program"}, indent=2))
    if parsed["program"]:
        prog_summary = {k: v for k, v in parsed["program"].items() if k != "code"}
        prog_summary["code_lines"] = len(parsed["program"].get("code", "").splitlines())
        print(f"program: {json.dumps(prog_summary, indent=2)}")
    else:
        print("program: (skeleton proposal — no example)")

    name = parsed["name"]
    if _already_in_pl_list(name):
        print(f"ERROR: '{name}' already exists in pl_list.txt — refusing to duplicate.")
        return 2

    if args.dry_run:
        print("\n--- DRY RUN — exiting before file writes ---")
        return 0

    # Materialize files.
    dir_name = _safe_dir_name(name)
    lang_dir = LANGUAGES_DIR / dir_name
    lang_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {
        "name": name,
        "aliases": parsed["aliases"],
        "evidence_url": parsed["evidence_url"],
        "added_at": now,
    }
    (lang_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {lang_dir / 'meta.json'}")

    prog = parsed["program"]
    if prog and prog.get("code"):
        ext = (prog.get("ext") or "").lstrip(".")
        if not ext:
            print("WARNING: program has code but no ext — saving as code.txt")
            ext = "txt"
        sha = _code_sha256(prog["code"])
        prog_dir = lang_dir / "programs" / sha
        prog_dir.mkdir(parents=True, exist_ok=True)
        normalized = "\n".join(line.rstrip() for line in prog["code"].splitlines())
        (prog_dir / f"code.{ext}").write_text(normalized + "\n", encoding="utf-8")
        manifest = {
            "title": prog.get("title") or "Example",
            "origin_url": prog.get("origin_url") or "",
            "license_guess": prog.get("license_guess") or None,
            "code_sha256": sha,
            "added_at": now,
        }
        (prog_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"WROTE {prog_dir / f'code.{ext}'}")
        print(f"WROTE {prog_dir / 'manifest.json'}")

    _insert_sorted(name)
    print(f"WROTE {PL_LIST} (appended '{name}', kept sorted).")

    # Emit a small machine-readable summary so the workflow can pipe it into
    # the PR body without re-parsing files.
    summary_path = ROOT / ".tmp" / f"pl_add_summary_{args.issue}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps({
        "name": name,
        "aliases": parsed["aliases"],
        "evidence_url": parsed["evidence_url"],
        "dir_name": dir_name,
        "has_program": bool(prog and prog.get("code")),
        "issue": args.issue,
    }, indent=2), encoding="utf-8")
    print(f"WROTE {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
