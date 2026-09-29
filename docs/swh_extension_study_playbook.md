# A playbook for "what is *actually* in file-extension X on Software Heritage?"

*Generalised from the COBOL case study (`docs/cobol_swh_study.md`,
`tools/cobol/`). Applies to any extension — programming language, DSL,
config format, or data — for which you can obtain an
`<ext>_files+origin.csv`.*

## The question

An extension is a *claim*, not a fact. `.CBL` claims COBOL; ~40 % of it was a
synthetic test fixture. `.cbl` also claims COBOL; it collides with Calibre
comic-book lists. `.fsf` claims nothing in Linguist, yet it is a coherent
neuroimaging config format. This playbook answers, for any extension:

1. **Is it what the extension says** (a programming language / the expected
   format), and how much of it is *not*?
2. **What is it, precisely** — dialect / format / sub-type / domain / maturity?
3. **Where does it come from**, and how concentrated is it across projects?
4. Doing (1)–(3) also **stress-tests the extension→PL mapping** itself.

## Inputs

- **`<ext>_files+origin.csv`** — `SWHID, name, <SWH browse URL>`. The browse
  URL is graph-derived and carries `origin_url` + `path` + visit `timestamp` +
  `branch`. (Content→origin is *not* in the SWH REST API; it needs the SWH
  graph. The maintainer builds this CSV once per extension.)
- **The bytes** — fetched from SWH by `sha1_git` (self-verifying), one request
  per content, cached.

## The pipeline (7 stages)

| Stage | What | Key point | COBOL tool |
|---|---|---|---|
| 1. **Sample** | dedup by content sha; pick N | two frames: *uniform-random* (population) **and** *origin-diverse* (≤1/repo — project population) | `sample.py`, `sample_diverse.py` |
| 2. **Fetch** | raw bytes by sha1_git, cached | 1 req/content; anon 120/h, self-pace on `X-RateLimit-*`; token → ~25× | `common.py` |
| 3. **Indicators** | cheap deterministic metrics | size, format, marker counts; feed the judge *and* catch noise | `indicators.py` |
| 4. **LLM-judge** | enum-constrained verdict | structured outputs (`json_schema`); free-text `*_detail` for nuance; a cost **gate** skips obvious non-target | `judge.py`, `taxonomy.py` |
| 5. **Reclassifier** | zero-API content classifier | bootstrapped from judge labels; **validated** against the LLM (P/R/F1); scales archive-wide | `reclassify.py`, `eval_reclassify.py` |
| 6. **Origins** | parse the CSV (+ optional GitHub match) | enables by-repo sampling, provenance, concentration/fork analysis | `origins.py`, `recover_origins.py` |
| 7. **Review** | one web pane over every label | judge/reclassifier/oracle/gate/human/origin, disagreements surfaced → human ground truth | `review_app.py` |

Everything is **resumable** and **cached**: re-runs and re-judging cost zero
SWH quota. Aggregates are enum-normalised so free-text and schema changes don't
require re-judging.

## What is fixed vs what you swap per extension

**Fixed (reuse as-is):** fetch + cache + rate-limiting (`common.py`), the
sampler and origin-diverse sampler, the origins layer, the run/aggregate
orchestrator (`run_study.py`), the review app, the figure generator, the
corpus-estimate sweep, the cost gate mechanism.

**Swap (per extension):**
- **`taxonomy.py`** — the enum vocabulary the judge must pick from (dialects/
  formats/domains/maturities relevant to *this* extension).
- **`judge.py` schema + prompt** — the questions and the JSON shape.
- **`indicators.py`** — the structural markers (COBOL divisions ↔ FEAT
  `set fmri(...)` directives, etc.).
- **`reclassify.py`** — the content-rule categories for the non-target tail.
- **the gate** — the cheap "is this plausibly the target?" predicate.

In practice ~70 % of `tools/cobol/` is extension-agnostic; a new study is
mostly a new taxonomy + indicators + reclassifier.

## Lessons learned (from COBOL — the numbers are real)

1. **The extension is a weak signal; measure contamination first.** ~40 % of
   the deduplicated `.CBL` corpus was one synthetic test fixture
   (`WBC_*_FOO.CBL`, "This is cobol file number N"); lowercase `.cbl`
   additionally collided with Calibre comic-book lists, `.NET` designer files,
   and editor temp files. A 1,000-content sweep put **~46 % as non-COBOL**.
   *Always* classify from content, never trust the extension.

2. **Case matters.** `.CBL` (192k) and `.cbl` (57k) are *different populations*
   (enterprise/mainframe vs education/hobby), the raw SWH data preserves case,
   yet the mapping folds it (cf. the earlier `.R` vs `.r` fix). Keep casing;
   fold only as an explicit, reversible choice.

3. **The sampling frame decides the story.** *By-file* sampling over-weights
   large repos: it said 77 % production-like, 49 % healthcare — because one
   system (JMA ORCA) contributed hundreds of files. *By-repo* (origin-diverse,
   ≤1 file/repo) said 14 % production-like, 60 % student-exercise, median 48
   LOC. Report both and state which question each answers ("typical *file*" vs
   "typical *project*"). This is only possible once you have origins.

4. **LLM-judge: constrained enums + structured outputs + a cross-check.**
   Free-text dialect/domain fragmented into 30+ near-duplicate strings;
   enum-constrained `json_schema` output aggregates cleanly. Keep a free-text
   `*_detail` for nuance. Cross-validate against the mechanical indicators
   (COBOL: 95 % agreement judge-vs-heuristic on source format) — cheap,
   independent confirmation.

4b. **Ask "what IS this content, and what does it relate to" — not "is it
   language X".** An extension is *polysemous*, and a single file relates to
   *several* notations at once. `.fsf` is a neuroimaging **config/DSL** (FSL
   FEAT) but is *expressed in* **Tcl** `set`-syntax, so it relates to Tcl — a
   binary "is it a programming language?" throws that away. Give the judge a
   `content_type` axis (config-or-dsl / source-code / script / data / markup /
   …), a free-text `format`, an `expressed_in` (host notation), a
   **`related_languages`** array (what it is written in / embeds / relates to),
   and an `ecosystem_tool`. Aggregating `related_languages` across the corpus
   is what surfaces the polysemy and the true PL/DSL relationships — the real
   goal for an extension→PL mapping.

5. **Gate to control cost, but measure the gate.** A cheap predicate
   (`n_divisions ≥ 2`) skipped obvious non-COBOL before spending API calls —
   but as a classifier it had recall 0.55. Know your gate's error before
   trusting its skips.

6. **Bootstrap a reclassifier from the LLM; validate it honestly.** The LLM is
   an expensive *oracle* for cheap deterministic rules that then run
   archive-wide for free. Ours reached **P 1.00 / R 0.79 / F1 0.88** vs the
   judge (beating the gate's 0.71), correctly recovering copybooks / OO /
   Japanese-comment / NUL-bearing COBOL. The ambiguous tail (weak copybooks)
   stays with the LLM — that's the intended division of labour.

7. **Origins come from the graph, not the REST API.** SWH REST has no
   content→origin. The graph does (`/api/1/graph/` — gated, 401 anonymously).
   The maintainer's `<ext>_files+origin.csv` is the authoritative, broad,
   multi-forge source (COBOL: 99.7 % coverage, GitHub/GitLab/Bitbucket/SF-SVN/
   Google-Code). A GitHub filename+byte-length match is a *narrow* heuristic
   complement (10 % recall). **Global dedup**: identical bytes live in many
   origins, so two sources can name different repos for the same content —
   both valid; the graph often finds the upstream.

8. **Provenance closes the loop.** Origins let you *name* the noise (the WBC
   40 % = one GitLab "repo-with-many-files-in-one-tree" test fixture), resolve
   the real system (ORCA → `github.com/izumiya/jma-receipt`), and — via
   by-repo sampling — measure the project population instead of the file
   population.

9. **Operational realities.** SWH anon quota ≈ 120 req/h → a token is worth
   ~25×; cache everything (re-runs free); make every job resumable;
   structured-output verdicts occasionally hit `max_tokens` mid-JSON (bump it,
   parse tolerantly). Judge cost ≈ $0.02/file; a 1,000-file judged study is
   ~$15–25.

## How to run a new extension (checklist)

1. Obtain `<ext>_files+origin.csv`; drop it at the repo root.
2. Fetch a handful of contents; **read them** — decide what the extension
   actually is and draft its taxonomy (enums).
3. Parameterise: `taxonomy`, `judge` schema/prompt, `indicators` markers,
   `reclassify` categories, the gate predicate.
4. Sample two frames (uniform-random for the population, origin-diverse for the
   project view); fetch + indicators (no key).
5. Judge (gate on); reclassify + validate against the judge; run the
   corpus-estimate sweep for a population contamination number.
6. Load origins; review disagreements; record human ground truth.
7. Write it up: contamination, sub-types, by-file vs by-repo, provenance.

See `docs/fsf_study_design.md` for a worked design on a **non-programming**
extension (`.fsf`, FSL FEAT neuroimaging config).

---

## Revision 2 — after `.rpgle` and `.m` (2026-09)

The `.m` study (`docs/m_swh_study.md`, Part I) re-read the first three studies
as a reviewer would. The pipeline above stands; the *evaluation* around it
changes. Seven rules, each answering a weakness that was actually present:

1. **No labeller is the oracle — not even the LLM.** Label every content with
   several *independent* labellers, including tools you did not write (Linguist
   heuristics, Pygments, SWH Synid) and a second LLM from another vendor. Report
   agreement, per-class recall and abstention for each; add a Dawid–Skene
   estimate (it needs no gold, but flag its independence assumption).
2. **Keep the judge blind to the features it will be scored against.** The
   cobol/fsf/rpgle judges saw the indicators, then were compared with
   classifiers built from those indicators. The primary judge sees bytes,
   filename, path and repository only; an ablation re-judges a subset *with*
   indicators to measure anchoring.
3. **Split the schema by decidability** (from rpgle): semantic fields to the
   LLM, lexical facts to code — and when they disagree, look at the *direction*
   of the disagreement before deciding who is wrong.
4. **Pre-register.** Before the first judgement on the study sample, commit the
   samples, models, prompts, frozen v1 rules, the tuning split, and written
   predictions. Score v1 prospectively; tune v2 on the tuning split only.
5. **Rank-based samples.** Rank each frame by `md5(seed‖key)`; every prefix is a
   simple random sample, so a rate-limited fetch or a cost cap can stop anywhere
   without biasing the frame.
6. **Cheap labels on many, expensive labels on few, joined by PPI.**
   Prediction-powered inference turns a validated cheap classifier on the whole
   fetched sample plus the judge on a subset into valid (and narrower)
   intervals. Post-stratified frames (by-path, by-repo) use weights computed
   exactly from the full population table, not estimated from the sample.
7. **Close the loop with a small, weighted, blind human audit.** Over-sample
   disagreements, keep inverse-probability weights, and hide machine labels
   until the reviewer has answered. The review app serves the queue; one
   command turns the reviews into weighted accuracies for every labeller.

Also: **audit the population file** before sampling (count rows in = rows
parsed; keep defective rows with a status rather than dropping them), and
**stress-test the mapping** against every language that claims the extension,
not just the one you expect.

### Checklist additions

- 2b. Write `PREREGISTRATION.md`; commit it with the frozen rules *before* judging.
- 4b. Store each labeller as its own layer (`labels/`, `synid.jsonl`,
  `judge/<model>/`) so cheap layers can be regenerated without touching paid ones.
- 5b. Run the second judge and the anchoring ablation; compute PPI estimates.
- 6b. `audit --build`, review the queue blind, `audit --score`.
