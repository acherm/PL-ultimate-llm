#!/usr/bin/env python3
# tools/claude/worktree.py
"""
Git worktree manager for parallel agent execution.

Each agent runs in its own worktree, enabling true parallelism.
"""

import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[2]
WORKTREES_DIR = ROOT / "worktrees"


@dataclass
class Worktree:
    """Represents a git worktree."""
    name: str
    path: Path
    branch: str


def setup_worktrees(n: int) -> list[Worktree]:
    """
    Create N git worktrees for parallel agent execution.

    Args:
        n: Number of worktrees to create

    Returns:
        List of Worktree objects
    """
    WORKTREES_DIR.mkdir(exist_ok=True)
    worktrees = []

    for i in range(n):
        name = f"agent-{i}"
        path = WORKTREES_DIR / name
        branch = f"worktree-{i}"

        # Remove existing worktree if present
        if path.exists():
            remove_worktree(name)

        # Create branch from main if it doesn't exist
        subprocess.run(
            ["git", "branch", "-D", branch],
            capture_output=True,
            cwd=ROOT,
        )
        subprocess.run(
            ["git", "branch", branch, "main"],
            capture_output=True,
            cwd=ROOT,
            check=True,
        )

        # Create worktree
        subprocess.run(
            ["git", "worktree", "add", str(path), branch],
            capture_output=True,
            cwd=ROOT,
            check=True,
        )

        worktrees.append(Worktree(name=name, path=path, branch=branch))

    return worktrees


def remove_worktree(name: str):
    """Remove a worktree by name."""
    path = WORKTREES_DIR / name

    # Remove from git
    subprocess.run(
        ["git", "worktree", "remove", "--force", str(path)],
        capture_output=True,
        cwd=ROOT,
    )

    # Clean up directory if still exists
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def cleanup_worktrees():
    """Remove all worktrees."""
    # List all worktrees
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    for line in result.stdout.splitlines():
        if line.startswith("worktree ") and "worktrees/agent-" in line:
            path = line.split("worktree ")[1]
            subprocess.run(
                ["git", "worktree", "remove", "--force", path],
                capture_output=True,
                cwd=ROOT,
            )

    # Clean up directory
    if WORKTREES_DIR.exists():
        shutil.rmtree(WORKTREES_DIR, ignore_errors=True)

    # Prune stale worktrees
    subprocess.run(
        ["git", "worktree", "prune"],
        capture_output=True,
        cwd=ROOT,
    )

    # Clean up worktree branches
    for i in range(10):
        subprocess.run(
            ["git", "branch", "-D", f"worktree-{i}"],
            capture_output=True,
            cwd=ROOT,
        )


def reset_worktree(worktree: Worktree):
    """Reset a worktree to main for reuse."""
    # Fetch latest main
    subprocess.run(
        ["git", "fetch", "origin", "main"],
        capture_output=True,
        cwd=worktree.path,
    )

    # Reset to main
    subprocess.run(
        ["git", "reset", "--hard", "main"],
        capture_output=True,
        cwd=worktree.path,
        check=True,
    )

    # Clean untracked files
    subprocess.run(
        ["git", "clean", "-fd"],
        capture_output=True,
        cwd=worktree.path,
    )


def sync_worktree_to_main(worktree: Worktree):
    """Sync a worktree to current main."""
    subprocess.run(
        ["git", "reset", "--hard", "main"],
        capture_output=True,
        cwd=worktree.path,
        check=True,
    )


def get_worktree_head(worktree: Worktree) -> str:
    """Get HEAD commit SHA of a worktree."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=worktree.path,
    )
    return result.stdout.strip()


def worktree_has_new_commit(worktree: Worktree, original_head: str) -> bool:
    """Check if worktree has a new commit since original_head."""
    current = get_worktree_head(worktree)
    return current != original_head


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        print("Cleaning up worktrees...")
        cleanup_worktrees()
        print("Done.")
    else:
        print("Creating 3 worktrees...")
        wts = setup_worktrees(3)
        for wt in wts:
            print(f"  {wt.name}: {wt.path} ({wt.branch})")
        print("\nTo cleanup: python -m tools.claude.worktree cleanup")
