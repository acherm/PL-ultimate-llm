#!/usr/bin/env python3
# tools/claude/turn.py
"""
Execute one turn using a Claude Code agent on a dedicated branch.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs"
DATA = ROOT / "data"

# Ensure logs directory exists
LOGS.mkdir(exist_ok=True)


@dataclass
class AgentResult:
    """Result of a single agent turn."""
    branch: str
    model: str
    web_search: bool
    success: bool
    head_before: str
    head_after: str
    duration_s: float
    exit_code: int
    language: str | None = None
    error: str | None = None


def get_head_sha() -> str:
    """Get current git HEAD short SHA."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def get_list_digest() -> str:
    """Get SHA256 digest of pl_list.txt (first 8 chars)."""
    import hashlib
    pl_path = DATA / "pl_list.txt"
    content = pl_path.read_bytes() if pl_path.exists() else b""
    return hashlib.sha256(content).hexdigest()[:8]


def create_branch(branch_name: str) -> bool:
    """Create and checkout a new branch from main."""
    try:
        # Ensure we're on main first
        subprocess.run(
            ["git", "checkout", "main"],
            capture_output=True,
            cwd=ROOT,
            check=True,
        )
        # Create new branch
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            capture_output=True,
            cwd=ROOT,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[turn] Failed to create branch {branch_name}: {e}", file=sys.stderr)
        return False


def delete_branch(branch_name: str):
    """Delete a branch (cleanup)."""
    try:
        # Switch to main first
        subprocess.run(
            ["git", "checkout", "main"],
            capture_output=True,
            cwd=ROOT,
        )
        # Delete the branch
        subprocess.run(
            ["git", "branch", "-D", branch_name],
            capture_output=True,
            cwd=ROOT,
        )
    except subprocess.CalledProcessError:
        pass  # Best effort cleanup


def get_current_branch() -> str:
    """Get the current branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def extract_language_from_commit() -> str | None:
    """Extract language name from the last commit message."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
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


def validate_commit() -> tuple[bool, str | None]:
    """
    Validate the last commit.

    Returns:
        (is_valid, error_message)
    """
    try:
        # Get commit message
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        msg = result.stdout

        # Check format
        if not msg.startswith("turn: add "):
            return False, "Commit message must start with 'turn: add '"

        if "List-Digest:" not in msg:
            return False, "Missing List-Digest trailer"

        if "Agent:" not in msg:
            return False, "Missing Agent trailer"

        if "WebSearch:" not in msg:
            return False, "Missing WebSearch trailer"

        # Extract language name
        lang = extract_language_from_commit()
        if not lang:
            return False, "Could not extract language name from commit"

        # Check language directory exists
        lang_dir = ROOT / "languages" / lang
        if not lang_dir.exists():
            return False, f"Language directory not found: {lang_dir}"

        meta_path = lang_dir / "meta.json"
        if not meta_path.exists():
            return False, f"meta.json not found: {meta_path}"

        # Check programs directory has content
        programs_dir = lang_dir / "programs"
        if not programs_dir.exists() or not any(programs_dir.iterdir()):
            return False, f"No programs found in {programs_dir}"

        return True, None

    except subprocess.CalledProcessError as e:
        return False, f"Git error: {e}"


def run_agent(
    branch: str,
    model: str,
    web_search: bool,
    timeout: int = 300,
    max_budget: float = 1.0,
    rejected_languages: list[str] | None = None,
) -> AgentResult:
    """
    Run a Claude Code agent on the specified branch.

    Args:
        branch: Branch name to work on
        model: Claude model to use (sonnet, opus)
        web_search: Whether to enable web search
        timeout: Max seconds for agent execution
        max_budget: Max USD budget for the agent
        rejected_languages: Languages to exclude from proposal

    Returns:
        AgentResult with outcome details
    """
    from .prompt import build_prompt, build_system_prompt

    head_before = get_head_sha()
    t0 = time.time()

    # Create and checkout branch
    if not create_branch(branch):
        return AgentResult(
            branch=branch,
            model=model,
            web_search=web_search,
            success=False,
            head_before=head_before,
            head_after=head_before,
            duration_s=0,
            exit_code=-1,
            error="Failed to create branch",
        )

    # Build prompt
    prompt = build_prompt(
        web_search=web_search,
        model=model,
        rejected_languages=rejected_languages,
    )

    # Build command
    cmd = [
        "claude",
        "--print",
        "--model", model,
        "--dangerously-skip-permissions",
        "--max-turns", "50",
    ]

    # Note: --max-budget-usd may not be available in all versions
    # Uncomment if supported:
    # cmd.extend(["--max-budget-usd", str(max_budget)])

    # Add prompt as the final argument
    cmd.append(prompt)

    # Run the agent
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=ROOT,
        )
        exit_code = result.returncode

        if result.stderr:
            print(f"[turn] Agent stderr: {result.stderr[:500]}", file=sys.stderr)

    except subprocess.TimeoutExpired:
        duration = time.time() - t0
        delete_branch(branch)
        return AgentResult(
            branch=branch,
            model=model,
            web_search=web_search,
            success=False,
            head_before=head_before,
            head_after=head_before,
            duration_s=round(duration, 2),
            exit_code=-1,
            error="Timeout",
        )
    except Exception as e:
        duration = time.time() - t0
        delete_branch(branch)
        return AgentResult(
            branch=branch,
            model=model,
            web_search=web_search,
            success=False,
            head_before=head_before,
            head_after=head_before,
            duration_s=round(duration, 2),
            exit_code=-1,
            error=str(e),
        )

    duration = time.time() - t0
    head_after = get_head_sha()

    # Check if a new commit was created
    if head_after == head_before:
        return AgentResult(
            branch=branch,
            model=model,
            web_search=web_search,
            success=False,
            head_before=head_before,
            head_after=head_after,
            duration_s=round(duration, 2),
            exit_code=exit_code,
            error="No commit created",
        )

    # Validate the commit
    is_valid, error = validate_commit()
    if not is_valid:
        return AgentResult(
            branch=branch,
            model=model,
            web_search=web_search,
            success=False,
            head_before=head_before,
            head_after=head_after,
            duration_s=round(duration, 2),
            exit_code=exit_code,
            error=f"Invalid commit: {error}",
        )

    # Success!
    language = extract_language_from_commit()
    return AgentResult(
        branch=branch,
        model=model,
        web_search=web_search,
        success=True,
        head_before=head_before,
        head_after=head_after,
        duration_s=round(duration, 2),
        exit_code=exit_code,
        language=language,
    )


def log_result(result: AgentResult):
    """Log the agent result to JSONL file."""
    now = datetime.now(UTC)
    log_path = LOGS / f"claude-{now:%Y%m%d}.jsonl"

    entry = {
        "ts": now.isoformat(),
        "kind": "agent.turn",
        **asdict(result),
    }

    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run a single Claude Code agent turn"
    )
    parser.add_argument(
        "--model",
        default="sonnet",
        choices=["sonnet", "opus", "haiku"],
        help="Claude model to use",
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        default=True,
        help="Enable web search (default)",
    )
    parser.add_argument(
        "--no-web-search",
        action="store_true",
        help="Disable web search",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout in seconds",
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="Branch name (auto-generated if not provided)",
    )
    parser.add_argument(
        "--keep-branch",
        action="store_true",
        help="Keep branch after completion (for debugging)",
    )
    args = parser.parse_args()

    # Determine web search setting
    web_search = not args.no_web_search

    # Generate branch name if not provided
    branch = args.branch or f"agent-{int(time.time())}"

    print(f"[turn] Starting agent on branch '{branch}'")
    print(f"[turn] Model: {args.model}, WebSearch: {web_search}")

    # Run the agent
    result = run_agent(
        branch=branch,
        model=args.model,
        web_search=web_search,
        timeout=args.timeout,
    )

    # Log result
    log_result(result)

    # Print outcome
    if result.success:
        print(f"[turn] SUCCESS: Added '{result.language}'")
        print(f"[turn] Commit: {result.head_after}")
        print(f"[turn] Duration: {result.duration_s}s")

        if not args.keep_branch:
            # Note: Don't delete branch here - orchestrator will merge it
            print(f"[turn] Branch '{branch}' ready for merge")
    else:
        print(f"[turn] FAILED: {result.error}", file=sys.stderr)
        print(f"[turn] Duration: {result.duration_s}s", file=sys.stderr)

        if not args.keep_branch:
            delete_branch(branch)
            print(f"[turn] Branch '{branch}' deleted")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
