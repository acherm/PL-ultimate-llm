#!/usr/bin/env python3
# tools/claude/merge.py
"""
Merge coordinator for Claude Code agent branches.

Handles:
- Duplicate language detection across branches
- Merge ordering (first successful agent wins)
- Branch cleanup
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
LOGS = ROOT / "logs"


@dataclass
class MergeResult:
    """Result of merging a branch."""
    branch: str
    merged: bool
    language: str | None = None
    reason: str | None = None


def get_current_branch() -> str:
    """Get current branch name."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    return result.stdout.strip()


def checkout_main():
    """Checkout main branch."""
    subprocess.run(
        ["git", "checkout", "main"],
        capture_output=True,
        cwd=ROOT,
        check=True,
    )


def read_pl_list() -> set[str]:
    """Read current language list from main branch."""
    pl_path = DATA / "pl_list.txt"
    if not pl_path.exists():
        return set()
    with pl_path.open("r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def get_branch_language(branch: str) -> str | None:
    """
    Get the language added in a branch by examining the commit message.

    Args:
        branch: Branch name

    Returns:
        Language name or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "log", branch, "-1", "--format=%s"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        msg = result.stdout.strip()
        # Parse "turn: add <LanguageName> (+1 program)"
        if msg.startswith("turn: add "):
            return msg.split("turn: add ")[1].split(" (+1")[0].strip()
    except (subprocess.CalledProcessError, IndexError):
        pass
    return None


def is_duplicate(language: str, existing: set[str], merged_this_batch: set[str]) -> bool:
    """
    Check if a language is a duplicate.

    Args:
        language: Language name to check
        existing: Languages already in main branch
        merged_this_batch: Languages merged in current batch

    Returns:
        True if duplicate
    """
    lang_lower = language.lower()
    return lang_lower in existing or lang_lower in merged_this_batch


def get_list_digest() -> str:
    """Get SHA256 digest of pl_list.txt (first 8 chars)."""
    import hashlib
    pl_path = DATA / "pl_list.txt"
    content = pl_path.read_bytes() if pl_path.exists() else b""
    return hashlib.sha256(content).hexdigest()[:8]


def merge_branch(branch: str) -> tuple[bool, str | None]:
    """
    Merge a branch into main.

    Args:
        branch: Branch name to merge

    Returns:
        (success, error_message)
    """
    try:
        # Get List-Digest for commit-msg hook requirement
        digest = get_list_digest()
        merge_msg = f"Merge branch '{branch}'\n\nList-Digest: {digest}"

        # Merge with --no-ff to preserve branch history
        result = subprocess.run(
            ["git", "merge", "--no-ff", "-m", merge_msg, branch],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        if result.returncode != 0:
            # Merge failed - likely conflict
            # Abort the merge
            subprocess.run(
                ["git", "merge", "--abort"],
                capture_output=True,
                cwd=ROOT,
            )
            return False, f"Merge conflict: {result.stderr}"

        return True, None

    except subprocess.CalledProcessError as e:
        return False, str(e)


def delete_branch(branch: str):
    """Delete a branch."""
    try:
        subprocess.run(
            ["git", "branch", "-D", branch],
            capture_output=True,
            cwd=ROOT,
        )
    except subprocess.CalledProcessError:
        pass


def merge_branches(branches: list[str], cleanup: bool = True) -> list[MergeResult]:
    """
    Merge multiple branches into main, handling duplicates.

    Args:
        branches: List of branch names to merge
        cleanup: Whether to delete branches after processing

    Returns:
        List of MergeResult for each branch
    """
    results = []

    # Ensure we're on main
    checkout_main()

    # Get existing languages
    existing = read_pl_list()
    merged_this_batch: set[str] = set()

    for branch in branches:
        # Get language from branch
        language = get_branch_language(branch)

        if not language:
            results.append(MergeResult(
                branch=branch,
                merged=False,
                reason="Could not determine language from branch",
            ))
            if cleanup:
                delete_branch(branch)
            continue

        # Check for duplicate
        if is_duplicate(language, existing, merged_this_batch):
            results.append(MergeResult(
                branch=branch,
                merged=False,
                language=language,
                reason=f"Duplicate language: {language}",
            ))
            if cleanup:
                delete_branch(branch)
            continue

        # Try to merge
        success, error = merge_branch(branch)

        if success:
            merged_this_batch.add(language.lower())
            results.append(MergeResult(
                branch=branch,
                merged=True,
                language=language,
            ))
            # Update existing set for next iteration
            existing.add(language.lower())
        else:
            results.append(MergeResult(
                branch=branch,
                merged=False,
                language=language,
                reason=error,
            ))

        if cleanup:
            delete_branch(branch)

    return results


def log_merge_results(results: list[MergeResult]):
    """Log merge results to JSONL file."""
    now = datetime.now(UTC)
    log_path = LOGS / f"claude-{now:%Y%m%d}.jsonl"

    for result in results:
        entry = {
            "ts": now.isoformat(),
            "kind": "merge.result",
            "branch": result.branch,
            "merged": result.merged,
            "language": result.language,
            "reason": result.reason,
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    """CLI for manual merge operations."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge agent branches into main"
    )
    parser.add_argument(
        "branches",
        nargs="+",
        help="Branch names to merge",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Keep branches after merge attempt",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be merged without actually merging",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("[merge] Dry run - checking branches:")
        existing = read_pl_list()
        for branch in args.branches:
            language = get_branch_language(branch)
            if not language:
                print(f"  {branch}: ERROR - could not determine language")
            elif language.lower() in existing:
                print(f"  {branch}: SKIP - duplicate '{language}'")
            else:
                print(f"  {branch}: MERGE - '{language}'")
        return 0

    print(f"[merge] Processing {len(args.branches)} branches...")
    results = merge_branches(args.branches, cleanup=not args.no_cleanup)
    log_merge_results(results)

    merged = sum(1 for r in results if r.merged)
    skipped = len(results) - merged

    print(f"[merge] Results: {merged} merged, {skipped} skipped")
    for result in results:
        status = "MERGED" if result.merged else "SKIPPED"
        reason = f" ({result.reason})" if result.reason else ""
        print(f"  {result.branch}: {status} {result.language or ''}{reason}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
