#!/usr/bin/env python3
# tools/claude/orchestrator.py
"""
Parallel orchestrator for Claude Code agents.

Spawns multiple agents on separate branches, waits for completion,
then merges successful branches into main.
"""

import argparse
import json
import os
import subprocess
import sys
import time
# Note: Agents run sequentially since git operations don't parallelize in same worktree
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs"
LOCK = ROOT / ".orchestrator.lock"

# Ensure logs directory exists
LOGS.mkdir(exist_ok=True)


@dataclass
class BatchResult:
    """Result of a batch of parallel agents."""
    branches: list[str]
    successes: int
    failures: int
    merged: int
    skipped: int
    duration_s: float


def log_event(event: dict):
    """Log an event to JSONL file."""
    now = datetime.now(UTC)
    log_path = LOGS / f"claude-{now:%Y%m%d}.jsonl"
    entry = {"ts": now.isoformat(), **event}
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def acquire_lock() -> int | None:
    """
    Acquire advisory lock for single instance.

    Returns:
        File descriptor if acquired, None if already locked
    """
    try:
        lock_fd = os.open(str(LOCK), os.O_CREAT | os.O_RDWR, 0o644)
        try:
            import fcntl
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_fd
        except (BlockingIOError, OSError):
            os.close(lock_fd)
            return None
    except Exception:
        return None


def release_lock(lock_fd: int):
    """Release the advisory lock."""
    try:
        os.close(lock_fd)
        LOCK.unlink(missing_ok=True)
    except Exception:
        pass


def run_agent_subprocess(
    branch: str,
    model: str,
    web_search: bool,
    timeout: int,
) -> dict:
    """
    Run a single agent as a subprocess.

    This is used with ThreadPoolExecutor to run agents in parallel.

    Returns:
        Dict with result information
    """
    from .turn import run_agent, AgentResult

    result = run_agent(
        branch=branch,
        model=model,
        web_search=web_search,
        timeout=timeout,
    )

    return {
        "branch": result.branch,
        "success": result.success,
        "language": result.language,
        "error": result.error,
        "duration_s": result.duration_s,
        "model": result.model,
        "web_search": result.web_search,
    }


def run_parallel_batch(
    n_agents: int,
    models: list[str],
    web_search: bool,
    timeout: int,
    batch_id: int,
) -> BatchResult:
    """
    Run a batch of parallel agents.

    Args:
        n_agents: Number of agents to spawn
        models: List of models to rotate through
        web_search: Whether to enable web search
        timeout: Timeout per agent in seconds
        batch_id: Batch identifier for branch naming

    Returns:
        BatchResult with aggregate statistics
    """
    from .merge import merge_branches, checkout_main, log_merge_results

    t0 = time.time()
    timestamp = int(time.time())

    # Ensure we start from main
    checkout_main()

    # Prepare agent configurations
    agent_configs = []
    for i in range(n_agents):
        branch = f"agent-{batch_id}-{i}-{timestamp}"
        model = models[i % len(models)]
        agent_configs.append((branch, model))

    print(f"[orchestrator] Starting batch {batch_id} with {n_agents} agents")
    for branch, model in agent_configs:
        print(f"  - {branch} ({model})")

    # Run agents sequentially (git operations don't parallelize well in same worktree)
    successful_branches = []
    failures = 0

    for branch, model in agent_configs:
        print(f"[orchestrator] Running agent {branch} ({model})...")
        try:
            result = run_agent_subprocess(
                branch=branch,
                model=model,
                web_search=web_search,
                timeout=timeout,
            )
            if result["success"]:
                print(f"[orchestrator] Agent {branch} SUCCESS: {result['language']}")
                successful_branches.append(branch)
            else:
                print(f"[orchestrator] Agent {branch} FAILED: {result['error']}")
                failures += 1

            # Log individual result
            log_event({
                "kind": "agent.complete",
                "batch_id": batch_id,
                **result,
            })

        except Exception as e:
            print(f"[orchestrator] Agent {branch} EXCEPTION: {e}")
            failures += 1
            log_event({
                "kind": "agent.exception",
                "batch_id": batch_id,
                "branch": branch,
                "error": str(e),
            })

    # Merge successful branches
    merged = 0
    skipped = 0

    if successful_branches:
        print(f"[orchestrator] Merging {len(successful_branches)} successful branches...")
        checkout_main()
        merge_results = merge_branches(successful_branches, cleanup=True)
        log_merge_results(merge_results)

        for result in merge_results:
            if result.merged:
                merged += 1
                print(f"  - MERGED: {result.language}")
            else:
                skipped += 1
                print(f"  - SKIPPED: {result.language} ({result.reason})")

    duration = time.time() - t0

    batch_result = BatchResult(
        branches=[b for b, _ in agent_configs],
        successes=len(successful_branches),
        failures=failures,
        merged=merged,
        skipped=skipped,
        duration_s=round(duration, 2),
    )

    log_event({
        "kind": "batch.complete",
        "batch_id": batch_id,
        "agents": n_agents,
        "successes": batch_result.successes,
        "failures": batch_result.failures,
        "merged": batch_result.merged,
        "skipped": batch_result.skipped,
        "duration_s": batch_result.duration_s,
    })

    return batch_result


def main():
    parser = argparse.ArgumentParser(
        description="Run parallel Claude Code agents"
    )
    parser.add_argument(
        "--agents",
        type=int,
        default=3,
        help="Number of parallel agents per batch (default: 3)",
    )
    parser.add_argument(
        "--models",
        default="sonnet,opus",
        help="Comma-separated list of models to rotate (default: sonnet,opus)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=0,
        help="Stop after N successful merges (0 = infinite)",
    )
    parser.add_argument(
        "--max-minutes",
        type=int,
        default=0,
        help="Stop after N minutes (0 = infinite)",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=10.0,
        help="Seconds to pause between batches",
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
        default=True,
        help="Enable web search (default)",
    )
    parser.add_argument(
        "--no-web-search",
        action="store_true",
        help="Disable web search",
    )
    parser.add_argument(
        "--fail-backoff",
        type=float,
        default=30.0,
        help="Backoff seconds after batch failure",
    )
    parser.add_argument(
        "--max-consecutive-fails",
        type=int,
        default=5,
        help="Circuit breaker threshold",
    )
    parser.add_argument(
        "--single-batch",
        action="store_true",
        help="Run only one batch then exit",
    )
    args = parser.parse_args()

    # Parse models
    models = [m.strip() for m in args.models.split(",")]
    web_search = not args.no_web_search

    print(f"[orchestrator] Configuration:")
    print(f"  Agents per batch: {args.agents}")
    print(f"  Models: {models}")
    print(f"  Web search: {web_search}")
    print(f"  Timeout: {args.timeout}s")
    print(f"  Max turns: {args.max_turns or 'unlimited'}")
    print(f"  Max minutes: {args.max_minutes or 'unlimited'}")

    # Acquire lock
    lock_fd = acquire_lock()
    if lock_fd is None:
        print("[orchestrator] Another instance is running", file=sys.stderr)
        log_event({"kind": "orchestrator.error", "msg": "lock-unavailable"})
        return 1

    try:
        start = datetime.now(UTC)
        deadline = (
            start + timedelta(minutes=args.max_minutes)
            if args.max_minutes > 0
            else None
        )

        total_merged = 0
        batch_id = 0
        consecutive_fails = 0

        log_event({
            "kind": "orchestrator.start",
            "agents": args.agents,
            "models": models,
            "web_search": web_search,
            "max_turns": args.max_turns,
            "max_minutes": args.max_minutes,
        })

        while True:
            # Check time budget
            if deadline and datetime.now(UTC) >= deadline:
                print("[orchestrator] Time budget exceeded")
                log_event({
                    "kind": "orchestrator.stop",
                    "reason": "time_budget",
                    "total_merged": total_merged,
                })
                break

            # Check turn budget
            if args.max_turns > 0 and total_merged >= args.max_turns:
                print(f"[orchestrator] Turn budget reached: {total_merged}")
                log_event({
                    "kind": "orchestrator.stop",
                    "reason": "turn_budget",
                    "total_merged": total_merged,
                })
                break

            # Run batch
            batch_id += 1
            print(f"\n{'='*60}")
            print(f"[orchestrator] Batch {batch_id}")
            print(f"{'='*60}")

            result = run_parallel_batch(
                n_agents=args.agents,
                models=models,
                web_search=web_search,
                timeout=args.timeout,
                batch_id=batch_id,
            )

            print(f"\n[orchestrator] Batch {batch_id} complete:")
            print(f"  Successes: {result.successes}/{args.agents}")
            print(f"  Merged: {result.merged}")
            print(f"  Skipped: {result.skipped}")
            print(f"  Duration: {result.duration_s}s")

            total_merged += result.merged

            # Check for consecutive failures
            if result.merged == 0:
                consecutive_fails += 1
                if consecutive_fails >= args.max_consecutive_fails:
                    print(f"[orchestrator] Circuit breaker: {consecutive_fails} consecutive failures")
                    log_event({
                        "kind": "orchestrator.stop",
                        "reason": "circuit_breaker",
                        "consecutive_fails": consecutive_fails,
                        "total_merged": total_merged,
                    })
                    break

                print(f"[orchestrator] Backing off for {args.fail_backoff}s...")
                time.sleep(args.fail_backoff)
            else:
                consecutive_fails = 0
                if not args.single_batch:
                    print(f"[orchestrator] Pausing for {args.pause}s...")
                    time.sleep(args.pause)

            # Single batch mode
            if args.single_batch:
                log_event({
                    "kind": "orchestrator.stop",
                    "reason": "single_batch",
                    "total_merged": total_merged,
                })
                break

        print(f"\n[orchestrator] Total languages added: {total_merged}")
        return 0

    finally:
        release_lock(lock_fd)


if __name__ == "__main__":
    sys.exit(main())
