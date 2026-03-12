#!/bin/bash
# Campaign runner — launches parallel Claude agents to add programming languages.
# Runs inside screen(1) for resilience to disconnections.
#
# Usage:
#   ./tools/claude/runner.sh [options]
#
# Options:
#   -m, --minutes  MINUTES   Duration in minutes (default: 60)
#   -a, --agents   N         Number of parallel agents (default: 2)
#   -M, --models   MODELS    Comma-separated models (default: sonnet)
#   -w, --web-search         Enable web search (default: off)
#   -t, --timeout  SECONDS   Per-agent timeout (default: 600)
#   -p, --prompt-mode MODE   Prompt mode: default, batch, sibling, or prefix
#   -n, --n-candidates N     Candidates per agent for sibling/prefix (default: 10)
#
# Examples:
#   ./tools/claude/runner.sh                        # 60 min, 2 agents, sonnet
#   ./tools/claude/runner.sh -m 120                 # 2 hours
#   ./tools/claude/runner.sh -m 60 -a 3 -M opus    # 1 hour, 3 opus agents
#   ./tools/claude/runner.sh -m 60 -w               # 1 hour with web search
#   ./tools/claude/runner.sh -m 60 -p batch         # batch-recall-100 mode
#   ./tools/claude/runner.sh -m 60 -p sibling       # sibling exploration
#   ./tools/claude/runner.sh -m 60 -p prefix        # prefix exploration
#   ./tools/claude/runner.sh -p prefix -n 15        # prefix with 15 candidates
#
# Monitor:
#   screen -r plcampaign          # attach to live session
#   cat logs/runner-*.log         # high-level progress
#   tail -30 logs/parallel-*.log  # batch details
#
# Stop:
#   screen -S plcampaign -X quit && pkill -f "tools.claude.parallel"

set -euo pipefail

# ── Parse arguments ────────────────────────────────────────
MINUTES=60
AGENTS=2
MODELS=sonnet
WEB_SEARCH=false
TIMEOUT=600
PROMPT_MODE=default
BATCH_SIZE=100
N_CANDIDATES=10

while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--minutes)  MINUTES="$2"; shift 2 ;;
        -a|--agents)   AGENTS="$2";  shift 2 ;;
        -M|--models)   MODELS="$2";  shift 2 ;;
        -t|--timeout)  TIMEOUT="$2"; shift 2 ;;
        -p|--prompt-mode) PROMPT_MODE="$2"; shift 2 ;;
        -b|--batch-size) BATCH_SIZE="$2"; shift 2 ;;
        -n|--n-candidates) N_CANDIDATES="$2"; shift 2 ;;
        -w|--web-search) WEB_SEARCH=true; shift ;;
        -h|--help)
            sed -n '2,/^$/{ s/^# //; s/^#//; p }' "$0"
            exit 0 ;;
        *) echo "Unknown option: $1 (try --help)"; exit 1 ;;
    esac
done

if $WEB_SEARCH; then
    WS_FLAG="--web-search"
    WS_LABEL="on"
else
    WS_FLAG="--no-web-search"
    WS_LABEL="off"
fi

cd "$(dirname "$0")/../.."
ROOT=$(pwd)

# Prevent "nested session" error when launched from within Claude Code
unset CLAUDECODE
# Raise output token limit for --print mode (large pl_list.txt)
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000

# ── Preflight ──────────────────────────────────────────────
command -v claude >/dev/null || { echo "ERROR: claude CLI not found"; exit 1; }
command -v screen >/dev/null || { echo "ERROR: screen not found (brew install screen)"; exit 1; }

if screen -ls 2>/dev/null | grep -q plcampaign; then
    echo "ERROR: campaign already running (screen -r plcampaign to attach)"
    exit 1
fi

# Clean up stale state from previous runs
rm -f "$ROOT/.orchestrator.lock"
python3 -m tools.claude.worktree cleanup 2>/dev/null || true

BEFORE=$(wc -l < data/pl_list.txt | tr -d ' ')

echo "Launching campaign in screen session 'plcampaign'..."
echo "  Duration:    ${MINUTES} min"
echo "  Agents:      ${AGENTS}"
echo "  Models:      ${MODELS}"
echo "  Web search:  ${WS_LABEL}"
echo "  Timeout:     ${TIMEOUT}s"
echo "  Prompt mode: ${PROMPT_MODE}"
if [ "$PROMPT_MODE" = "batch" ]; then echo "  Batch size:  ${BATCH_SIZE}"; fi
if [ "$PROMPT_MODE" = "sibling" ] || [ "$PROMPT_MODE" = "prefix" ]; then echo "  Candidates:  ${N_CANDIDATES}"; fi
echo "  Collection:  ${BEFORE} languages"
echo ""

# ── Launch in detached screen ──────────────────────────────
screen -dmS plcampaign bash -c "
cd '$ROOT'
LOG=logs/runner-\$(date +%Y%m%d-%H%M%S).log
mkdir -p logs

echo '=== Campaign \$(date) | ${MINUTES}min | ${AGENTS} agents | ${MODELS} | ws=${WS_LABEL} ===' | tee \"\$LOG\"

END=\$((  \$(date +%s) + ${MINUTES} * 60 ))
N=0

while [ \$(date +%s) -lt \$END ]; do
    R=\$(( (END - \$(date +%s)) / 60 ))
    [ \$R -lt 5 ] && break

    N=\$((N + 1))
    BEFORE=\$(wc -l < data/pl_list.txt | tr -d ' ')

    echo \"[B\$N] start \${R}min \$(date +%H:%M:%S)\" | tee -a \"\$LOG\"

    rm -f .orchestrator.lock

    # Support mixed prompt mode: cycle through strategies
    if [ '${PROMPT_MODE}' = 'mixed' ]; then
        MODES=(batch sibling prefix)
        MODE=\${MODES[\$(( (N - 1) % 3 ))]}
    else
        MODE='${PROMPT_MODE}'
    fi

    echo \"  mode=\$MODE\" | tee -a \"\$LOG\"

    python3 -u -m tools.claude.parallel  \
        --agents ${AGENTS}               \
        --models ${MODELS}               \
        ${WS_FLAG}                       \
        --prompt-mode \$MODE             \
        --batch-size ${BATCH_SIZE}       \
        --n-candidates ${N_CANDIDATES}   \
        --max-minutes \$R                \
        --pause 5                        \
        --timeout ${TIMEOUT}              \
        --single-batch                   \
        >> logs/parallel-\$(date +%Y%m%d).log 2>&1 || true

    AFTER=\$(wc -l < data/pl_list.txt | tr -d ' ')
    echo \"[B\$N] done +\$((AFTER - BEFORE)) langs (now \$AFTER)\" | tee -a \"\$LOG\"

    sleep 10
done

echo \"=== Done \$(date) | collection=\$(wc -l < data/pl_list.txt | tr -d ' ') ===\" | tee -a \"\$LOG\"
"

echo "Campaign running. Useful commands:"
echo "  screen -r plcampaign                  # attach"
echo "  cat logs/runner-*.log | tail -20      # progress"
echo "  screen -S plcampaign -X quit          # stop"
