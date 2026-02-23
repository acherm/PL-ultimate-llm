# PL Loop (Simplified, Local, Git-commit based)

This is a minimal scaffold for an infinite loop where, at each turn, a randomly chosen LLM proposes:
1) a programming language (that exists in the real world),
2) a real program (code + origin URL) in that language,
3) and the language must be new to the current list.

Rules enforced locally by Python:
- The proposed language name must not already be in the list (`data/pl_list.txt`).
- The proposal must include at least one evidence URL for the language (e.g., Wikipedia or official site).
- The program must include code (kept to a small size) and an origin_url (where the code came from).
- The tool commits changes to the local git repo after validation.

Quick start:

1) Initialize a new repo (once)
   git init
   git config core.hooksPath .githooks

2) (Optional) Seed the language list from your CSV
   python3 tools/seed_from_csv.py ../languages_master.csv

3) Configure OpenRouter (edit tools/config.yaml)
4) Run one turn
   python3 tools/turn.py

Structure:

pl-loop/
  data/
    pl_list.txt            # Current list of canonical PL names (source of truth for membership)
    catalog.csv            # Flat log of accepted contributions
  languages/
    <Canonical-PL-Name>/
      meta.json            # language metadata
      programs/<sha256>/{ code.<ext>, manifest.json }
  tools/
    turn.py                # orchestrates one "turn" (one commit)
    templates.py           # prompt template for the LLM
    schema.py              # JSON schema for the LLM response
    validate.py            # local validation rules
    contribute.py          # writes files and performs the git commit
    util.py                # helpers (slugify, hashing, etc.)
    config.yaml            # list of models + settings
    seed_from_csv.py       # optional seeding from your master CSV
  .githooks/
    pre-commit             # validates & regenerates catalog.csv
    commit-msg             # enforces a small trailer

## Static website (browse + stats)

To browse the collected languages/programs as a static website:

```bash
python3 web/build_site.py
python3 -m http.server --directory web/dist 8000
```

Then open `http://localhost:8000`.

The Stats page also summarizes **agents/models used** based on git commit trailers (`Model:`, `Agent:`, `Temperature:`, `WebSearch:`, `Strategy:`) in `turn: add …` commits.

For data-quality checks (duplicates, integrity checks, clustering hints), run:

```bash
python3 tools/audit_repo.py --out web/dist/data/audit.json
```

## Claude Code agentic campaigns

The `tools/claude/` directory contains an automated campaign system that launches
parallel [Claude Code](https://docs.anthropic.com/en/docs/claude-code) agents to grow the
collection. Each agent runs in its own git worktree, finds an obscure
language not yet in the list, creates the required files, and commits.
Successful commits are cherry-picked back to `main`.

### Quick start

```bash
# 1-hour campaign, 2 parallel agents, sonnet model
tools/claude/runner.sh -m 60 -a 2 -M sonnet -t 600
```

The script launches in a detached `screen` session (`plcampaign`).

| Flag | Description | Default |
|------|-------------|---------|
| `-m` | Campaign duration (minutes) | 60 |
| `-a` | Parallel agents per batch | 2 |
| `-M` | Model (`sonnet`, `opus`) | `sonnet` |
| `-t` | Per-agent timeout (seconds) | 600 |
| `-w` | Enable web search | off |

### Monitor / stop

```bash
screen -r plcampaign                   # attach to live session
tail -20 logs/runner-*.log             # high-level batch summaries
tail -60 logs/parallel-*.log           # per-agent details
screen -S plcampaign -X quit           # stop the campaign
```

After a campaign finishes, push results with `git push origin main`.

See [`tools/claude/README.md`](tools/claude/README.md) for full architecture
details and troubleshooting.
