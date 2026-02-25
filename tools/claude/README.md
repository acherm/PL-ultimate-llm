# Claude Code Campaign System

Automated infrastructure for running parallel Claude Code agents that
each add one programming language to the collection per turn.

## Architecture

```
runner.sh                 # entry-point: launches campaign in a screen session
  └─ parallel.py          # orchestrator: manages batches of parallel agents
       ├─ worktree.py     # creates/syncs/cleans git worktrees
       └─ prompt.py       # builds the agent prompt with pre-computed digest
```

### How a campaign works

1. **`runner.sh`** starts a detached `screen` session and loops until time
   runs out. Each iteration invokes `parallel.py --single-batch`.

2. **`parallel.py`** creates N git worktrees (one per agent), syncs each to
   `main`, then launches N `claude --print` processes in parallel via a
   `ThreadPoolExecutor`.

3. Each **agent** (a Claude Code CLI process) runs in its own worktree with
   `--dangerously-skip-permissions`. It reads `CLAUDE.md`, picks an obscure
   language, creates the required files, and makes a single git commit.

4. After all agents finish (or time out), `parallel.py` **cherry-picks**
   successful commits from the worktrees back to `main`, skipping duplicates.

5. **`runner.sh`** logs batch results and starts the next batch.

```
main ──●──●──●──●──●──●──●──  (cherry-picks land here)
       │                    ▲
worktree-0 ──────[commit]───┘  (agent-0)
worktree-1 ──────[commit]───┘  (agent-1)
```

## Running a campaign

### Basic usage

```bash
tools/claude/runner.sh -m 60 -a 2 -M sonnet -t 600
```

This runs for 60 minutes with 2 parallel sonnet agents, each limited to
600 seconds.

### All options

```
Usage:
  ./tools/claude/runner.sh [options]

Options:
  -m, --minutes  MINUTES   Duration in minutes (default: 30)
  -a, --agents   N         Number of parallel agents (default: 3)
  -M, --models   MODELS    Comma-separated models (default: sonnet,opus)
  -w, --web-search         Enable web search (default: off)
  -t, --timeout  SECONDS   Per-agent timeout (default: 600)

Examples:
  ./tools/claude/runner.sh                         # 30 min, 3 agents
  ./tools/claude/runner.sh -m 60 -a 2 -M sonnet   # recommended config
  ./tools/claude/runner.sh -m 120 -w               # 2 hours, web search on
```

### Monitor and stop

```bash
screen -r plcampaign                   # attach to live session (Ctrl+A D to detach)
tail -20 logs/runner-*.log             # batch summaries
tail -60 logs/parallel-*.log           # per-agent details
screen -S plcampaign -X quit           # stop the campaign
```

### After a campaign

```bash
wc -l data/pl_list.txt                 # check collection size
git log --oneline -20                  # review recent additions
git push origin main                   # push to remote
```

## Files

| File | Role |
|------|------|
| `runner.sh` | Campaign entry-point; manages screen session and batch loop |
| `parallel.py` | Orchestrator; manages worktrees, launches agents, cherry-picks results |
| `prompt.py` | Builds the agent prompt; pre-computes list digest and language count |
| `worktree.py` | Git worktree lifecycle (create, sync, reset, cleanup) |
| `config.yaml` | Model configuration (not used by the campaign system) |

## Key design decisions

### Git worktrees for isolation

Each agent works in its own worktree (`worktrees/agent-N`). This provides
true filesystem isolation — agents can't interfere with each other's
uncommitted changes. Successful commits are cherry-picked to `main`.

### Watchdog-based timeout

Python's `proc.wait(timeout=N)` is unreliable inside `ThreadPoolExecutor`
threads (observed: 1900s elapsed on a 900s timeout). Instead, a dedicated
watchdog thread uses `threading.Event.wait(delay)` and kills the process
group via `os.killpg()`:

```python
cancel_watchdog = threading.Event()
was_killed = threading.Event()

def _kill_on_timeout(proc, delay):
    if cancel_watchdog.wait(delay):
        return                        # process exited naturally
    was_killed.set()
    os.killpg(proc.pid, signal.SIGKILL)

proc = Popen(cmd, start_new_session=True, ...)
watchdog = Thread(target=_kill_on_timeout, args=(proc, timeout), daemon=True)
watchdog.start()
proc.wait()                           # blocks until exit or kill
cancel_watchdog.set()                 # cancel watchdog if exited naturally
```

`start_new_session=True` gives the child its own process group so
`os.killpg` can kill it and all subprocesses.

### Stash-based cherry-pick

The main worktree may have dirty tracked files (modified tool scripts,
etc.). Cherry-pick fails if these overlap with the commit being applied.
The solution: `git stash` before cherry-pick, `git stash pop` after.
`--include-untracked` is intentionally omitted to avoid stashing gitignored
files like logs.

### Optimized agent prompt

With 2500+ languages in the collection, a naive agent wastes many turns
checking well-known languages that are already listed. The prompt is
optimized to:

- **Not read `pl_list.txt`** — uses `grep -ix` to check membership
- **Batch-check** 3-5 candidates at once with `grep -ix -e "L1" -e "L2"`
- **Pre-compute** the List-Digest and language count, injected into the prompt
- **Skip overhead**: no TodoWrite, no memory file reads

### Strategy tracking

Each agent chooses its own **search strategy** — a short freeform label
describing how it decided which language to look for (e.g., by paradigm,
era, geography, domain, language family, a random letter, etc.). The
strategy is recorded as a `Strategy:` trailer in the git commit, making
it easy to analyze which approaches are most productive:

```bash
# See all strategies used
git log --format='%(trailers:key=Strategy,valueonly)' | sort | uniq -c | sort -rn

# Find commits by strategy
git log --all --grep='Strategy: concatenative'
```

No categories are hardcoded in the prompt — agents are free to invent
their own strategies, which avoids biasing the collection toward any
particular kind of language.

### Source-directed search (web search mode)

When web search is enabled, agents are directed to **fetch real lists of
programming languages** from curated sources rather than guessing from
training data. This dramatically improves hit rates at 2500+ languages.

High-value sources provided in the prompt:
- **Rosetta Code** — ~900 languages with code examples
- **Wikipedia lists** — alphabetical and by-type (~700 languages)
- **Esolangs wiki** — 2000+ esoteric languages
- **HOPL** — 8000+ historical languages
- **99 Bottles of Beer** — 1500+ languages with code samples

The agent picks a source, fetches it with `WebFetch`, extracts language
names, batch-checks them against `pl_list.txt`, and adds the first gap.

### File-based stdout/stderr

Using `subprocess.PIPE` with large Claude output can cause deadlocks.
Agent output is redirected to files (`worktree/.agent-stdout.log`,
`.agent-stderr.log`) instead.

### CLAUDECODE env var

Claude CLI v2.1.49+ sets a `CLAUDECODE` environment variable. Child
`claude` processes inherit it and refuse to run ("nested session" error).
Both `runner.sh` (`unset CLAUDECODE`) and `parallel.py` (filtered from
`env` dict) strip this variable.

## Recommended configuration

Based on extensive testing:

| Parameter | Recommended | Why |
|-----------|-------------|-----|
| Agents | **2** | 3+ triggers API rate limiting (0-byte agent output) |
| Model | **sonnet** | Best cost/speed/success ratio for this task |
| Timeout | **600s** | Agents typically finish in 180-310s; 600s catches stragglers |
| Max turns | **50** (hardcoded) | 30 is too few at 2500+ languages; agents need ~15-25 turns |

Typical yield: **3-7 languages per hour** with 2 sonnet agents.

## Troubleshooting

### No languages added in a batch

Check `logs/parallel-*.log` for per-agent errors. Common causes:
- **Timeout**: agent exceeded 600s. May need prompt tuning.
- **No commit created**: agent couldn't find an unlisted language in 50 turns.
- **0-byte stdout**: API rate limiting. Reduce parallel agents.
- **Cherry-pick failed**: usually a conflict on `pl_list.txt`. The commit
  becomes a dangling object recoverable via `git fsck`.

### Recovering dangling commits

If a cherry-pick fails or a worktree is cleaned up before merging:

```bash
# Find dangling commits
git fsck --no-reflogs --unreachable | grep commit

# Inspect a candidate
git log -1 --format="%H %s" <sha>

# Cherry-pick if clean
git cherry-pick <sha>
```

### Campaign already running

```
ERROR: campaign already running (screen -r plcampaign to attach)
```

Either attach to the existing session or stop it first:
```bash
screen -S plcampaign -X quit
rm -f .orchestrator.lock
```

### Stale lock file

If `parallel.py` was killed abruptly, the lock file may persist:
```bash
rm -f .orchestrator.lock
```

## Logs

| Path | Content |
|------|---------|
| `logs/runner-YYYYMMDD-HHMMSS.log` | Batch-level summaries from `runner.sh` |
| `logs/parallel-YYYYMMDD.log` | Detailed per-agent output from `parallel.py` |
| `logs/claude-YYYYMMDD.jsonl` | Structured JSONL events (agent start/stop/merge) |
