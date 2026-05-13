# PL Loop (Simplified, Local, Git-commit based)

This is a minimal scaffold for an infinite loop where, at each turn, a randomly chosen LLM proposes:
1) a programming language (that exists in the real world),
2) a real program (code + origin URL) in that language,
3) and the language must be new to the current list.

## Project status (May 2026, branch `swh-evidence-v1`)

> Originally scoped to **LLM-curated PLs + example programs**. This branch
> prototypes a broader role: **cross-source PL taxonomy + Software Heritage
> evidence + crowdsourced extension labelling**, all rendered into the same
> per-PL pages on the static site. Prototype-quality; not aimed at production
> yet, but the prototype is documented in detail so the design can be
> reviewed / criticised / refined.

What landed beyond the original LLM-curation scope:

| Piece | Where | What it does |
|---|---|---|
| Cross-source PL taxonomy | `tools/build_pl_taxonomy.py` + `data/derived/pl_taxonomy/` | Merges PLDB + Linguist + Pygments + Wikipedia + Esolang + Hyperpolyglot + Rosetta Code into `pl`, `pl_alias`, `ext_claim` (with `source`+`strength` per claim), `ext_summary`, `heuristic` tables. |
| Content-based PL classifier | `tools/pl_classify.py` | Runs Linguist's `heuristics.yml` (377 rules across 148 ambiguous extensions) as a runnable predicate set. |
| SWH mining + sample fetcher | `tools/swh_extension_mining.py` + `tools/fetch_samples.py` | Mines the SWH popular-content-names parquet for real archived programs per extension; materializes bytes to `samples/<pl_id>/<sha1>/` with citation-grade qualified SWHIDs. |
| Roberto's SWH-ext popularity | `tools/build_swh_ext_popularity.py` → `data/derived/swh_extensions_popularity.csv` | Per-extension occurrence aggregate (1950–2023) for ~2.96M alphanumeric extensions across the SWH archive. |
| Extension review queue | `tools/build_extension_review_queue.py` → `data/derived/extension_review_queue.csv` | Ranked list of extensions that need a manual label (popular in SWH, no PL claim). |
| Crowdsource label loop | `/review/extensions/`, per-ext form on `/ext/<slug>/`, GitHub Actions in `.github/workflows/ingest_ext_labels.yml` | Form on the site → pre-filled GH issue → curator script → updates `extension_labels.csv` → promotes accepted labels into `ext_claim.csv`. |
| Site enrichment | `web/build_site.py` (extensively) | Adds cross-source pill row, ext-claim table, SWH samples section, per-ext pages (8,344), per-source pages, `/samples/` index, `/review/` views, stats additions. ~13,755 PL pages total. |

Design + decision logs (the place to start reading):

- `docs/SOURCES_AND_SWH_EVIDENCE.md` — the big-picture motivation.
- `docs/SWH_EXTENSIONS_DECISIONS.md` — what's kept from Roberto's CSV, what's cut, why; provenance contract for any ext↔PL mapping; PL ↔ ext asymmetry.
- `docs/labelling_persistence.md` — how a GH issue becomes a row on the site.
- `docs/extension_labels.md` — controlled vocabulary for manual labels.
- `docs/PHASE2_OVERNIGHT.md` — concrete status note for the integration.

The original LLM-curation scope (everything below) is untouched.

---

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

## Master inventory reproduction

To reproduce the upstream `PL-ultimate` idea inside this repo and compare it
against the local `pl_list`, use [`tools/master_inventory.py`](tools/master_inventory.py).

It builds a master inventory from:
- PLDB
- GitHub Linguist
- Wikipedia
- optional Esolang

Then it augments that inventory with:
- Hyperpolyglot coverage
- local Pygments lexer support
- Rosetta Code language support

### Build

```bash
git clone --depth 1 https://github.com/breck7/pldb /tmp/pldb
python3 tools/master_inventory.py build --pldb-dir /tmp/pldb --include-esolang
```

Outputs are written under `data/derived/`, including:
- `languages_master.csv`
- `languages_master_augmented.csv`
- `languages_master_augmented_pygments.csv`
- `languages_master_augmented_rosettacode.csv`
- `extensions_inventory.csv`

Raw fetched sources are cached under `data/raw/`.

### Compare with pl_list

```bash
python3 tools/master_inventory.py compare
```

Comparison artifacts are written under `reports/master_inventory/`, including:
- `summary.md`
- `summary.json`
- `pl_list_matches_master.csv`
- `pl_list_missing_from_master.csv`
- `master_missing_from_pl_list.csv`

To run both steps in one shot:

```bash
python3 tools/master_inventory.py all --pldb-dir /tmp/pldb --include-esolang
```
