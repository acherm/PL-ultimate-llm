# COBOL-in-SWH exploratory study

A small pipeline to understand what "COBOL" actually means inside Software
Heritage, starting from the extracted content lists in
`COBOL-SWH-extracted/` (`CBL_files.csv`, `cbl_files_lowercase.csv`).

For each sampled content it: fetches the bytes from SWH (cached), computes
**structural indicators** (LOC, divisions, EXEC SQL/CICS, COMP-3, …), and —
optionally — runs an **LLM-as-judge** (via OpenRouter) that categorises the
program (is-it-COBOL, dialect/standard, source format, purpose, domain).

## Pipeline

| Step | Module | Needs key? | Cost |
|---|---|---|---|
| Sample unique contents | `tools.cobol.sample` | no | local only |
| Fetch + indicators + (judge) + aggregate | `tools.cobol.run_study` | judge only | SWH: 1 req/content (cached after) |
| Indicators for one SWHID | `tools.cobol.indicators <swhid>` | no | 1 req |
| Judge one SWHID | `tools.cobol.judge <swhid>` | yes | 1 req + 1 LLM call |

Run everything from the repo root as modules (`python3 -m tools.cobol.<x>`).

## Quick start (no API key)

```bash
# 1. Sample 100 distinct contents (dedup by sha1_git, reproducible seed).
python3 -m tools.cobol.sample --n 100 --seed 42

# 2. Fetch bytes + compute indicators for the whole worklist (no key).
python3 -m tools.cobol.run_study --no-judge
```

Outputs land in `data/derived/cobol_study/`:
- `worklist.csv` — the sampled contents
- `reports/<sha1_git>.json` — per-file: sample + content + indicators + judge
- `indicators.csv` — flat per-file metrics (open in any spreadsheet)
- `summary.json` / `summary.md` — aggregate stats + a per-sample table

Fetched bytes are cached under `.cache/cobol/` (gitignored), so re-runs and
the judge pass cost **zero** SWH requests.

## Adding the LLM-judge

```bash
export OPENROUTER_API_KEY=sk-or-...
# Judge only real-COBOL-looking files (>=2 divisions); noise is skipped
# mechanically with no API spend. Uses the cached bytes -> 0 SWH requests.
python3 -m tools.cobol.run_study --judge --judge-min-divisions 2 \
    --model anthropic/claude-sonnet-4.6
```

- Model is configurable via `--model` or `COBOL_JUDGE_MODEL` (any OpenRouter
  slug). Default: `anthropic/claude-sonnet-4.6`.
- `--force` re-judges files that already have a verdict.
- `--tag <name>` suffixes the aggregate outputs (`summary_<name>.md`,
  `indicators_<name>.csv`) so parallel studies don't clobber each other; the
  per-content `reports/<sha>.json` are shared (keyed by content, reusable).

### Schema v2 — constrained enums (`cobol-judge/2`)

The judge uses OpenRouter **structured outputs** (`response_format=json_schema`,
`strict`) so the categorical fields are drawn from a fixed vocabulary
(`tools/cobol/taxonomy.py`), with a free-text `*_detail` field for nuance:

- `dialect.family` ∈ {ibm-mainframe, gnucobol, micro-focus, acucobol,
  rm-cobol, fujitsu-nec, other-vendor, unknown} · `dialect.detail` free-text
- `dialect.standard` ∈ COBOL-68/74/85/2002/2014/unknown
- `source_format` ∈ fixed/free/tab/mixed/unknown
- `purpose.domain` ∈ {banking-finance, insurance, healthcare-medical,
  government-public, payroll-hr, accounting-erp, retail-commerce, telecom,
  manufacturing-logistics, education-tutorial, demo-example, test-suite,
  utility-tooling, other, unknown} · `purpose.domain_detail` free-text
- `program_type`, `maturity`, `not_cobol_label` — likewise enums.

If a model/provider rejects `json_schema`, the judge falls back to
`json_object`; parsing is tolerant of fences/extra prose either way.

**Aggregation normalizes both versions.** `run_study` canonicalizes every
verdict through `taxonomy.normalize_*`, so older free-text (`cobol-judge/1`)
verdicts collapse into the same clean enum distributions **without a
re-judge** — just re-run `run_study --no-judge` to regenerate the summary.

## Human review / annotation tools

### Unified label-review app (`review_app.py`) — recommended

One pane over **all** labels a content has received — the LLM **judge**
verdict, the deterministic **reclassifier** label, the LLM **oracle**, the
**division-gate** baseline, and your **human** reviews — keyed by content and
surfacing where they disagree (the interesting cases to review):

```bash
python3 -m tools.cobol.review_app             # http://127.0.0.1:8766
```

- **Dashboard**: counts, per-dataset membership, reclassifier label
  distribution, and is-COBOL agreement (e.g. judge vs reclassifier).
- **Browse / filter**: by dataset, reclassifier label, filename, or
  `flag=disagree` / `unreviewed` / `noncobol`.
- **Per file**: source + indicators beside a labels table (all sources, with
  disagreements highlighted) and a human-review form.
- Human reviews save to `reviews_cobol/<sha>/` (`cobol-review/1`), shared with
  `review_server.py`.

### Single-study review server (`review_server.py`)

A lighter tool scoped to just the study reports:

```bash
python3 -m tools.cobol.review_server          # http://127.0.0.1:8765
python3 -m tools.cobol.review_server --port 9000 --reviewer alice
```

- **Index** lists every report (filter by filename / family / domain) and
  marks which are reviewed.
- **Per sample** shows the source (from `.cache/cobol/`), the mechanical
  indicators, and the LLM-judge verdict (with its evidence), beside a form:
  is-it-COBOL, agreement-with-judge, corrected dialect-family / domain /
  source-format (dropdowns from `taxonomy.py`), a free-text **origin URL**
  (paste the forge link when you find one — origin isn't recoverable from a
  bare cnt SWHID), and notes.
- Reviews are append-only JSON, one file per review, under
  `reviews_cobol/<sha1_git>/<UTC>--<reviewer>--<hash8>.json` (`cobol-review/1`)
  — git is the sync layer, no DB, no merge conflicts. These are meant to be
  committed (ground truth), unlike the regenerable study outputs.

## Prototypes (see report §8)

```bash
# 8.1 Case-aware mapping: emit .CBL vs .cbl as distinct pl/cobol claims
python3 -m tools.cobol.case_aware_mapping

# 8.2 Content reclassifier for the non-COBOL tail + validation experiment
python3 -m tools.cobol.reclassify <swhid>                    # classify one file
OPENROUTER_API_KEY=… python3 -m tools.cobol.eval_reclassify --tail-all
```

- `reclassify.py` labels a `.cbl`/`.CBL` file from content: `cobol`,
  `cobol-generated`, `cobol-copybook`, `synthetic-placeholder`,
  `comic-book-list`, `binary-data`, `other`. Zero API cost.
- `eval_reclassify.py` scores it against the LLM judge (oracle) on
  is-COBOL: **P 1.00 / R 0.79 / F1 0.88**, beating the division-gate
  baseline (F1 0.71). Oracle verdicts are cached, so re-runs are free.

## Notes & caveats

- **SWH quota:** anonymous access is ~120 requests/hour. We make **1 request
  per content** (raw bytes by `sha1_git`, which is self-verifying). Set
  `SWH_TOKEN` for higher limits. Backoff honours `X-RateLimit-Reset`.
- **Corpus noise:** a large fraction of the `.CBL` corpus is synthetic
  placeholder files (e.g. `WBC_*_FOO.CBL` = "This is cobol file number N").
  The indicators flag these (0 divisions); `--judge-min-divisions` or
  `sample --exclude-name 'WBC_.*_FOO'` keep the LLM budget on real programs.
- **Source format** (`fixed`/`free`/`tab`) is a heuristic; the LLM verdict is
  the interpretive authority. Tab-indented GnuCOBOL often reads as `free`.
- **Origin** (which repo/commit a content came from) is *not* recoverable
  from a bare `swh:1:cnt:` SWHID via the public API — out of scope for v1.

## Schemas

- Report: `cobol-report/1` (see `reports/*.json`).
- Judge verdict: `cobol-judge/2` — enum-constrained (see `judge_json_schema()`
  in `judge.py` and the vocab in `taxonomy.py`). `cobol-judge/1` (free-text)
  verdicts are still readable; aggregation normalizes them to the same enums.
