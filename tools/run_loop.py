#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timedelta, UTC  # add UTC

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
LOCK = ROOT / ".orchestrator.lock"
TURN = ROOT / "tools" / "turn.py"
LOGS.mkdir(exist_ok=True)


def log_event(ev: dict, suffix="loop"):
    now = datetime.now(UTC)
    p = LOGS / f"{suffix}-{now:%Y%m%d}.jsonl"
    ev = {"ts": now.isoformat(), **ev}  # already timezone-aware
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def git_head_short() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        return "none"


def run_turn() -> int:
    # returns process rc
    return subprocess.call([sys.executable, str(TURN)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--max-turns",
        type=int,
        default=0,
        help="Stop after N successful turns (0 = infinite).",
    )
    ap.add_argument(
        "--max-minutes",
        type=int,
        default=0,
        help="Stop after N minutes (0 = infinite).",
    )
    ap.add_argument(
        "--pause",
        type=float,
        default=5.0,
        help="Seconds to sleep after a successful turn.",
    )
    ap.add_argument(
        "--fail-backoff",
        type=float,
        default=10.0,
        help="Initial backoff after a failure (seconds).",
    )
    ap.add_argument(
        "--fail-multiplier",
        type=float,
        default=1.5,
        help="Exponent multiplier for backoff.",
    )
    ap.add_argument(
        "--max-fail-backoff", type=float, default=120.0, help="Max backoff seconds."
    )
    ap.add_argument(
        "--max-consecutive-fails",
        type=int,
        default=8,
        help="Circuit-breaker threshold.",
    )
    args = ap.parse_args()

    # single instance lock
    try:
        lock_fd = os.open(str(LOCK), os.O_CREAT | os.O_RDWR, 0o644)
        # advisory lock (best-effort on POSIX)
        try:
            import fcntl

            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except Exception:
            print("[loop] another instance is running", file=sys.stderr)
            log_event({"kind": "loop.error", "msg": "lock-unavailable"})
            sys.exit(1)
    except Exception as e:
        print(f"[loop] lock error: {e}", file=sys.stderr)
        sys.exit(1)

    start = datetime.now(UTC)
    deadline = (
        start + timedelta(minutes=args.max_minutes) if args.max_minutes > 0 else None
    )

    successes = 0
    consecutive_fails = 0
    backoff = args.fail_backoff

    log_event({"kind": "loop.start", "args": vars(args)})

    try:
        while True:
            if deadline and datetime.utcnow() >= deadline:
                log_event(
                    {
                        "kind": "loop.stop",
                        "reason": "time_budget",
                        "successes": successes,
                    }
                )
                break
            if args.max_turns > 0 and successes >= args.max_turns:
                log_event(
                    {
                        "kind": "loop.stop",
                        "reason": "turn_budget",
                        "successes": successes,
                    }
                )
                break

            head_before = git_head_short()
            t0 = time.time()
            rc = run_turn()
            dt = round(time.time() - t0, 3)
            head_after = git_head_short()

            if rc == 0 and head_after != head_before:
                # success
                log_event(
                    {
                        "kind": "turn.ok",
                        "rc": rc,
                        "duration_s": dt,
                        "head_before": head_before,
                        "head_after": head_after,
                    }
                )
                successes += 1
                consecutive_fails = 0
                backoff = args.fail_backoff  # reset
                time.sleep(args.pause)
            else:
                # failure or no new commit
                reason = "no_commit" if rc == 0 else "rc_nonzero"
                log_event(
                    {
                        "kind": "turn.fail",
                        "rc": rc,
                        "duration_s": dt,
                        "head_before": head_before,
                        "head_after": head_after,
                        "reason": reason,
                    }
                )
                consecutive_fails += 1
                if consecutive_fails >= args.max_consecutive_fails:
                    log_event(
                        {
                            "kind": "loop.stop",
                            "reason": "circuit_breaker",
                            "consecutive_fails": consecutive_fails,
                        }
                    )
                    break
                time.sleep(backoff)
                backoff = min(args.max_fail_backoff, backoff * args.fail_multiplier)

    finally:
        try:
            os.close(lock_fd)
            LOCK.unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
