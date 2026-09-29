## Appendix B — Reproducing

```bash
# 0. population: 14 GB zip → Parquet (DuckDB lives in .venv)
unzip SWH-m-files.zip -d .cache/m/csv
.venv/bin/python -m tools.m.ingest            # → .cache/m/m_rows.parquet (2.8 GB)
.venv/bin/python -m tools.m.ingest --stats    # → population.json
.venv/bin/python -m tools.m.name_pop          # → name_popularity.json, population_signals.json

# 1. samples (seed 17; md5 ranks, every prefix is an SRS)
.venv/bin/python -m tools.m.sample --n-uniform 10000 --n-repo 3000 --seed 17
.venv/bin/python -m tools.m.sample --top-repos 25 --per-repo 4      # frame T

# 2. fetch (rate-limited; picks up a refreshed .swh_token on the fly)
python3 -m tools.m.fetch

# 3. free labellers: indicators, ours v1+v2, Linguist, Pygments; then SWH Synid
python3 -m tools.m.study --label
(cd swh-syntax-identification && cargo build --release)
python3 -m tools.m.run_synid

# 4. paid labellers (source .openrouter_key)
python3 -m tools.m.study --judge --n 1000                                   # Sonnet 4.6, blind
python3 -m tools.m.study --judge --n 1000 --model google/gemini-3.8-flash   # second vendor
python3 -m tools.m.study --judge --n 300 --frames U --with-indicators        # E5 anchoring
python3 -m tools.m.study --judge --n 4 --frames T                           # frame T
python3 -m tools.m.study --judge --n 4 --frames T --model google/gemini-3.8-flash

# 5. analysis, tables, figures, audit
python3 -m tools.m.analysis                   # → analysis.json (every number in this report)
python3 -m tools.m.report_tables              # the report's tables, from analysis.json
.venv/bin/python -m tools.m.make_figures      # → docs/assets/m/*.png
python3 -m tools.m.audit --build              # → audit_queue.csv (stratified, weighted)
python3 -m tools.m.review_app                 # http://127.0.0.1:8769
python3 -m tools.m.audit --score              # once the audit has reviews
```

Artifacts in `data/derived/m_study/`: `PREREGISTRATION.md`, `population.json`,
`population_signals.json`, `name_popularity.json`, `worklist_all.csv`,
`worklist_top.csv`, `labels/<sha>.json` (free labels, regenerable),
`synid.jsonl`, `judge/<model>/<sha>.json` (paid, append-only; usage and cost
inside), `analysis.json`, `audit_queue.csv`, `mapping_pygments_ext_fallback.json`.

## Appendix C — A Synid failure mode, ready to report upstream

**Tool.** `swh-syntax-identification` (Synid), commit `9bc1c32` (2026-06-15),
`synid file`, default strategy set minus the network-bound `linguistapi`.

**Symptom.** On `.m` files the judge (and Linguist's own rules) call
Objective-C, Synid answers `Text` for about one in ten.

**Minimal reproduction.** Any `.m` file with Objective-C `@interface` /
`@implementation`, no `//` or `/* */` comments, and a format string such as
`@"%@"`, e.g. the React-Native template `…AppTests.m`
(`swh:1:cnt:bbbcb890d40628ee37cff8c5f3d1a9791212ea63`).

**Mechanism.** The strategies run in sequence: *extension* yields the eight `.m`
candidates; the **comment** strategy (`src/strategies/comment_strategy/mod.rs`)
then scores every candidate by the number of lines that *contain* its comment
symbol — `line.contains(c)`, anywhere in the line, string literals included —
and keeps only the maximum. `%` inside `@"%@"` scores for MATLAB and Mercury;
Objective-C's `//` scores zero; Objective-C is removed from the candidate set.
The Linguist heuristic (`^\s*(@(interface|…|implementation)\b|#import …)`),
which would have decided Objective-C, runs next — on a set that no longer
contains the answer. The remaining strategies cannot recover, and the pipeline
returns `Text`.

**Evidence.** Removing only the `comment` strategy recovers Objective-C on the
large majority of these files (§5.1); the failure is specific to that step.

**Suggested fixes** (any one would do): count a comment symbol only at the
start of a line (after whitespace) or outside string literals; run
`hyplyheuristics` *before* `comment` for extensions that have a Linguist
disambiguation block; or let `comment` down-weight rather than eliminate
candidates.

**A second, independent failure — in `file` mode and the SquashFS host.**
In our judged sample, every text file for which Synid returned the full
eight-way candidate set (36 of 36) is not valid UTF-8 — typically MATLAB with
Latin-1 accented comments — and every file it resolved (1,958 of 1,958) is.
The cause is in `src/content.rs`: the local `FileFetcher` and the SquashFS
content host read with `std::fs::read_to_string`, which fails on invalid UTF-8;
the content strategies then return early and the extension's full candidate
list passes through unchanged. The AWS S3 host (`String::from_utf8_lossy`) and
the Web API host (`reqwest` `text()`) decode lossily and are **not** affected,
so the impact on archive-wide runs depends on the content host used. Reading
bytes and decoding with the same lossy fallback everywhere would fix it:
Linguist's `^\s*%` rule alone would then resolve 33 of the 35 MATLAB files.
