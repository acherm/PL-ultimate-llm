#!/usr/bin/env python3
# tools/claude/parallel.py
"""
Parallel orchestrator using git worktrees.

Each agent runs in its own worktree, enabling true parallel execution.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs"
DATA = ROOT / "data"
LOCK = ROOT / ".orchestrator.lock"

LOGS.mkdir(exist_ok=True)


@dataclass
class AgentResult:
    """Result from a parallel agent."""
    worktree: str
    model: str
    success: bool
    language: str | None
    duration_s: float
    error: str | None = None


def log_event(event: dict):
    """Log an event to JSONL file."""
    now = datetime.now(UTC)
    log_path = LOGS / f"claude-{now:%Y%m%d}.jsonl"
    entry = {"ts": now.isoformat(), **event}
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def acquire_lock() -> int | None:
    """Acquire advisory lock."""
    try:
        lock_fd = os.open(str(LOCK), os.O_CREAT | os.O_RDWR, 0o644)
        import fcntl
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except (BlockingIOError, OSError, Exception):
        return None


def release_lock(lock_fd: int):
    """Release advisory lock."""
    try:
        os.close(lock_fd)
        LOCK.unlink(missing_ok=True)
    except Exception:
        pass


def get_main_head() -> str:
    """Get current HEAD of main branch."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "main"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    return result.stdout.strip()


def run_agent_in_worktree(
    worktree_path: Path,
    model: str,
    web_search: bool,
    timeout: int,
) -> AgentResult:
    """
    Run a Claude agent in a specific worktree.

    Args:
        worktree_path: Path to the worktree
        model: Model to use
        web_search: Enable web search
        timeout: Timeout in seconds

    Returns:
        AgentResult
    """
    from .prompt import build_prompt

    worktree_name = worktree_path.name
    t0 = time.time()

    # Get HEAD before
    head_before = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    # Build prompt
    prompt = build_prompt(
        web_search=web_search,
        model=model,
    )

    # Run claude agent in the worktree directory
    cmd = [
        "claude",
        "--print",
        "--model", model,
        "--dangerously-skip-permissions",
        "--max-turns", "50",
        prompt,
    ]

    try:
        # Use Popen with process group so we can kill the entire tree on timeout
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=worktree_path,
            start_new_session=True,  # creates new process group
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Kill the entire process group (claude + all children)
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                proc.wait(timeout=10)
            except Exception:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except Exception:
                    pass
            return AgentResult(
                worktree=worktree_name,
                model=model,
                success=False,
                language=None,
                duration_s=round(time.time() - t0, 2),
                error="Timeout",
            )
        # Build a result-like object for compatibility
        result = subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
    except Exception as e:
        return AgentResult(
            worktree=worktree_name,
            model=model,
            success=False,
            language=None,
            duration_s=round(time.time() - t0, 2),
            error=str(e),
        )

    duration = time.time() - t0

    # Get HEAD after
    head_after = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    # Check if commit was made
    if head_after == head_before:
        return AgentResult(
            worktree=worktree_name,
            model=model,
            success=False,
            language=None,
            duration_s=round(duration, 2),
            error="No commit created",
        )

    # Extract language from commit message
    msg = subprocess.run(
        ["git", "log", "-1", "--format=%s"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    language = None
    if msg.startswith("turn: add "):
        try:
            language = msg.split("turn: add ")[1].split(" (+1")[0].strip()
        except IndexError:
            pass

    if not language:
        return AgentResult(
            worktree=worktree_name,
            model=model,
            success=False,
            language=None,
            duration_s=round(duration, 2),
            error="Invalid commit message",
        )

    return AgentResult(
        worktree=worktree_name,
        model=model,
        success=True,
        language=language,
        duration_s=round(duration, 2),
    )


def merge_worktree_to_main(worktree_path: Path, existing_languages: set[str]) -> tuple[bool, str | None, str | None]:
    """
    Merge a worktree's commit to main.

    Returns:
        (success, language, error)
    """
    import hashlib

    # Get the language from worktree's last commit
    msg = subprocess.run(
        ["git", "log", "-1", "--format=%s"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    language = None
    if msg.startswith("turn: add "):
        try:
            language = msg.split("turn: add ")[1].split(" (+1")[0].strip()
        except IndexError:
            return False, None, "Could not parse language from commit"

    if not language:
        return False, None, "No language in commit"

    # Check for duplicate
    if language.lower() in existing_languages:
        return False, language, f"Duplicate: {language}"

    # Get worktree branch name
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    # Cherry-pick the commit to main
    commit_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    ).stdout.strip()

    # Switch to main in the main repo
    subprocess.run(
        ["git", "checkout", "main"],
        capture_output=True,
        cwd=ROOT,
        check=True,
    )

    # Cherry-pick the commit
    result = subprocess.run(
        ["git", "cherry-pick", commit_sha],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    if result.returncode != 0:
        # Abort cherry-pick
        subprocess.run(
            ["git", "cherry-pick", "--abort"],
            capture_output=True,
            cwd=ROOT,
        )
        return False, language, f"Cherry-pick failed: {result.stderr}"

    return True, language, None


def run_parallel_batch(
    worktrees: list,
    models: list[str],
    web_search: bool,
    timeout: int,
    batch_id: int,
) -> tuple[int, int, list[str]]:
    """
    Run agents in parallel across worktrees.

    Returns:
        (merged_count, failed_count, languages_added)
    """
    from .worktree import sync_worktree_to_main, get_worktree_head

    n_agents = len(worktrees)

    print(f"\n{'='*60}")
    print(f"[parallel] Batch {batch_id} - {n_agents} agents in parallel")
    print(f"{'='*60}")

    # Sync all worktrees to main
    for wt in worktrees:
        sync_worktree_to_main(wt)
        print(f"  [{wt.name}] synced to main")

    # Run agents in parallel
    results = []
    with ThreadPoolExecutor(max_workers=n_agents) as executor:
        futures = {}
        for i, wt in enumerate(worktrees):
            model = models[i % len(models)]
            future = executor.submit(
                run_agent_in_worktree,
                worktree_path=wt.path,
                model=model,
                web_search=web_search,
                timeout=timeout,
            )
            futures[future] = wt
            print(f"  [{wt.name}] started ({model})")

        for future in as_completed(futures):
            wt = futures[future]
            try:
                result = future.result()
                results.append((wt, result))
                status = "SUCCESS" if result.success else "FAILED"
                lang = result.language or result.error
                print(f"  [{wt.name}] {status}: {lang} ({result.duration_s}s)")
            except Exception as e:
                print(f"  [{wt.name}] EXCEPTION: {e}")
                results.append((wt, AgentResult(
                    worktree=wt.name,
                    model="unknown",
                    success=False,
                    language=None,
                    duration_s=0,
                    error=str(e),
                )))

    # Merge successful results to main
    print(f"\n[parallel] Merging results...")

    # Get current languages
    pl_path = DATA / "pl_list.txt"
    existing = set()
    if pl_path.exists():
        existing = {line.strip().lower() for line in pl_path.read_text().splitlines() if line.strip()}

    merged = 0
    failed = 0
    languages_added = []

    for wt, result in results:
        if not result.success:
            failed += 1
            log_event({
                "kind": "parallel.agent_failed",
                "batch_id": batch_id,
                "worktree": wt.name,
                "error": result.error,
                "duration_s": result.duration_s,
            })
            continue

        success, language, error = merge_worktree_to_main(wt.path, existing)

        if success:
            merged += 1
            existing.add(language.lower())
            languages_added.append(language)
            print(f"  MERGED: {language}")
            log_event({
                "kind": "parallel.merged",
                "batch_id": batch_id,
                "worktree": wt.name,
                "language": language,
                "duration_s": result.duration_s,
            })
        else:
            failed += 1
            print(f"  SKIPPED: {language} ({error})")
            log_event({
                "kind": "parallel.skipped",
                "batch_id": batch_id,
                "worktree": wt.name,
                "language": language,
                "error": error,
            })

    return merged, failed, languages_added


def main():
    parser = argparse.ArgumentParser(
        description="Run parallel Claude agents using git worktrees"
    )
    parser.add_argument(
        "--agents",
        type=int,
        default=3,
        help="Number of parallel agents (default: 3)",
    )
    parser.add_argument(
        "--models",
        default="sonnet",
        help="Comma-separated models to rotate (default: sonnet)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=0,
        help="Stop after N languages added (0 = unlimited)",
    )
    parser.add_argument(
        "--max-minutes",
        type=int,
        default=0,
        help="Stop after N minutes (0 = unlimited)",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=10.0,
        help="Seconds between batches",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout per agent in seconds",
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        default=False,
        help="Enable web search",
    )
    parser.add_argument(
        "--no-web-search",
        action="store_true",
        help="Disable web search (default)",
    )
    parser.add_argument(
        "--single-batch",
        action="store_true",
        help="Run one batch then exit",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up worktrees and exit",
    )
    args = parser.parse_args()

    from .worktree import setup_worktrees, cleanup_worktrees

    if args.cleanup:
        print("[parallel] Cleaning up worktrees...")
        cleanup_worktrees()
        print("[parallel] Done.")
        return 0

    models = [m.strip() for m in args.models.split(",")]
    web_search = args.web_search and not args.no_web_search

    print(f"[parallel] Configuration:")
    print(f"  Agents: {args.agents} (truly parallel)")
    print(f"  Models: {models}")
    print(f"  Web search: {web_search}")
    print(f"  Timeout: {args.timeout}s")
    print(f"  Max turns: {args.max_turns or 'unlimited'}")

    # Acquire lock
    lock_fd = acquire_lock()
    if lock_fd is None:
        print("[parallel] Another instance is running", file=sys.stderr)
        return 1

    try:
        # Setup worktrees
        print(f"\n[parallel] Setting up {args.agents} worktrees...")
        worktrees = setup_worktrees(args.agents)
        for wt in worktrees:
            print(f"  {wt.name}: {wt.path}")

        start = datetime.now(UTC)
        deadline = (
            start + timedelta(minutes=args.max_minutes)
            if args.max_minutes > 0
            else None
        )

        total_merged = 0
        batch_id = 0

        log_event({
            "kind": "parallel.start",
            "agents": args.agents,
            "models": models,
            "web_search": web_search,
        })

        while True:
            # Check limits
            if deadline and datetime.now(UTC) >= deadline:
                print(f"\n[parallel] Time limit reached")
                break

            if args.max_turns > 0 and total_merged >= args.max_turns:
                print(f"\n[parallel] Target reached: {total_merged} languages")
                break

            batch_id += 1

            merged, failed, languages = run_parallel_batch(
                worktrees=worktrees,
                models=models,
                web_search=web_search,
                timeout=args.timeout,
                batch_id=batch_id,
            )

            total_merged += merged

            print(f"\n[parallel] Batch {batch_id} complete: {merged} merged, {failed} failed")
            print(f"[parallel] Total progress: {total_merged}/{args.max_turns or '∞'}")

            if args.single_batch:
                break

            if merged == 0:
                print(f"[parallel] No merges, backing off 30s...")
                time.sleep(30)
            else:
                print(f"[parallel] Pausing {args.pause}s...")
                time.sleep(args.pause)

        print(f"\n[parallel] Final total: {total_merged} languages added")

        log_event({
            "kind": "parallel.stop",
            "total_merged": total_merged,
            "batches": batch_id,
        })

        # Cleanup
        print("[parallel] Cleaning up worktrees...")
        cleanup_worktrees()

        return 0

    finally:
        release_lock(lock_fd)


if __name__ == "__main__":
    sys.exit(main())
