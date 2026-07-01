# What is "COBOL" in Software Heritage? An LLM-as-judge exploratory study

*Exploratory study, June 2026. Toolkit: `tools/cobol/`. Data: `data/derived/cobol_study/`.*

## Abstract

We characterise the contents that Software Heritage (SWH) indexes under the
COBOL file extensions `.CBL` / `.cbl`, starting from two extracted content
lists (`COBOL-SWH-extracted/`). For sampled contents we fetch the bytes from
SWH, compute deterministic structural indicators (lines of code, divisions,
embedded SQL/CICS, copybooks, …), and run an enum-constrained
**LLM-as-judge** (Claude Sonnet 4.6 via OpenRouter) that classifies each file
by dialect family, language standard, source format, program type, business
domain, and maturity. Across 653 judged files we find that the SWH COBOL
extension space is (a) **heavily contaminated** — ~40 % of the deduplicated
`.CBL` list is a single family of synthetic placeholder files, and the
lowercase `.cbl` space additionally collides with Calibre comic-book
libraries and editor artefacts; and (b) **strongly bimodal** — the uppercase
`.CBL` archive is dominated (83 % of a clean slice) by one open-source
enterprise system, the Japan Medical Association's **ORCA** medical-receipt
software (GnuCOBOL, COBOL-85, fixed-format, batch), whereas lowercase `.cbl`
is a diverse **education / hobbyist** population (36 % tutorials, 39 %
student-grade). We release the pipeline, the per-file reports, and a
human review tool for building ground truth.

## 1. Motivation & questions

"COBOL" is often treated as a monolith. Before doing anything quantitative
with an archive-scale COBOL sample, we wanted to know what is actually *in*
it. Concretely:

- **Q1 — Contamination.** What fraction of the COBOL-extension corpus is not
  COBOL at all (synthetic files, extension collisions, binaries)?
- **Q2 — Composition.** Of the genuine COBOL, what dialects, standards,
  source formats, program types, and business domains appear, and in what
  proportions?
- **Q3 — Sub-populations.** Do the uppercase `.CBL` and lowercase `.cbl`
  spaces differ, and how?
- **Q4 — Method.** Can a cheap deterministic layer + an LLM-judge produce a
  useful, reproducible characterisation, and how far can we trust it?

## 2. Data sources

| Input | Rows | Unique contents (`sha1_git`) |
|---|---:|---:|
| `COBOL-SWH-extracted/CBL_files.csv` (`.CBL`) | 196,416 | 196,228 |
| `COBOL-SWH-extracted/cbl_files_lowercase.csv` (`.cbl`) | 83,840 | 81,446 |
| Union | — | 276,831 (overlap: 843) |

Each row is `swh:1:cnt:<sha1_git>,/<filename>`: a **content** identifier plus
a bare filename. The `sha1_git` is the SWH content id (git blob hash); it is
self-verifying, so the raw bytes can be re-fetched anonymously without any
trust in the CSV beyond the hash. The lists carry **no origin or commit** —
recovering "which repository this came from" is out of scope (see §7).

## 3. Methodology

### 3.1 Pipeline

```
sample.py  →  common.fetch  →  indicators.py  →  judge.py  →  run_study aggregation
(dedup)       (SWH raw,        (deterministic    (LLM enum      (canonical distributions,
              1 req/sha,        metrics)          verdict)       CSV + Markdown)
              cached)
```

All steps are reproducible (`python3 -m tools.cobol.<module>`), resumable
(per-content reports keyed by `sha1_git`), and idempotent (fetched bytes are
cached under `.cache/cobol/`, so re-runs and re-judging cost zero SWH
requests).

### 3.2 Sampling

Contents are **deduplicated by `sha1_git`** (the same bytes appear under many
filenames) and sampled with a fixed RNG seed for reproducibility. We ran
three samples:

| Study | Seed | Source | Filter | N | Text | Judged | Gated |
|---|---|---|---|---:|---:|---:|---:|
| Pilot | 42 | both lists | none | 100 | 100 | 46 | — |
| **Main** | 7 | both lists | exclude `WBC_*_FOO` | 350 | 344 | 317 | 33 |
| **LC** | 11 | `.cbl` only | exclude `WBC_*_FOO` | 350 | 340 | 291 | 59 |

The Main sample is a union sample (197 `.CBL` + 153 `.cbl`); §4.7 also reports
a clean extension-split view.

### 3.3 Content retrieval

Bytes are fetched from `GET /api/1/content/sha1_git:<sha>/raw/` — **one
request per content**. SWH's anonymous quota is ~120 requests/hour; the
fetcher reads the `X-RateLimit-*` headers and self-paces (sleeping until the
window resets) so a multi-hundred-file sweep survives the hourly caps
unattended. Bytes are decoded UTF-8 → Latin-1 → replacement; a NUL byte or a
high non-printable ratio marks a content as non-text (excluded from the
judge).

### 3.4 Structural indicators (deterministic, no LLM)

Computed from the bytes alone, modelling COBOL's column rules (fixed format:
cols 1–6 sequence area, col 7 indicator `*`/`/` = comment, cols 8–11 Area A,
12–72 Area B; free format uses `*>` comments):

- **Size:** total / blank / comment / code lines; max & mean line length.
- **Format guess:** fixed / free / tab / unknown (heuristic).
- **Divisions present:** identification, environment, data, procedure.
- **Features:** `EXEC SQL`, `EXEC CICS`, `COPY`, `CALL`, `PERFORM`, `GO TO`,
  `PIC(TURE)`, `COMP-3`; extracted `PROGRAM-ID`s; compiler directives.

These feed the report *and* the judge prompt (the judge sees the same facts a
human reviewer would). One bug found and fixed during the study: fixed-format
`COPY` sits in Area B (~col 12) and was missed by a too-tight regex,
under-reporting copybook usage as 0 % → corrected to ~69 % (Main).

### 3.5 LLM-as-judge

- **Model:** `anthropic/claude-sonnet-4.6` via OpenRouter (OpenAI-compatible),
  `temperature=0`, `max_tokens=2048`, source truncated to 16,000 chars.
- **Structured outputs:** the verdict is produced under a strict
  `response_format=json_schema` so every categorical field is drawn from a
  fixed enum (`tools/cobol/taxonomy.py`); free-text `*_detail` fields carry
  nuance. This is schema `cobol-judge/2`. Fields: `cobol_confirmed`,
  `not_cobol_label`, `dialect.{family,standard,detail,evidence,confidence}`,
  `source_format`, `purpose.{domain,domain_detail,summary,program_type}`,
  `notable_features`, `maturity`, `overall_confidence`.
- **Gating:** to avoid spending on obvious non-COBOL, files below a division
  threshold (and lacking a PROGRAM-ID + COBOL verbs) are skipped mechanically
  (`--judge-min-divisions 2`) — no API call.
- **Normalization:** aggregation canonicalises every verdict through the
  taxonomy, so an earlier free-text schema (`cobol-judge/1`) collapses into
  the same enums with no re-judge. (The pilot was first judged free-text; its
  30+ ad-hoc dialect strings normalised to 5 families.)

### 3.6 Validity checks

- **Parse integrity:** 0 unparseable verdicts across 653 files (the single
  `max_tokens` truncation was found and fixed).
- **Judge vs deterministic agreement (source format):** the LLM's
  `source_format` matched the mechanical heuristic on **94.6 %** of Main and
  **85.9 %** of LC judged files — an independent cross-check that the two
  layers largely corroborate each other.

## 4. Results

### 4.1 Contamination (Q1)

- **Synthetic placeholders dominate `.CBL`.** `WBC_*_FOO.CBL` files — literal
  contents "This is cobol file number N" — account for **109,999 / 276,831
  (~40 %)** of the deduplicated union. In the unfiltered pilot, 51 % of a
  random 100 were this noise.
- **Extension collisions differ by casing.** After excluding `WBC_*_FOO`, the
  mechanical gate still rejected **17 %** of lowercase `.cbl` vs **~6 %** of
  `.CBL`. Lowercase `.cbl` collides with **Calibre comic-book libraries**
  (`[DC Comics] DC Master Reading Order…`, `Avengers 004.cbl`, `Wonder Woman
  1 - Golden Age.cbl`), `.NET` designer files (`*.aspx.designer.cbl`), and
  editor temp files (`tempCodeRunnerFile.cbl`).
- **Binaries:** 6/350 (Main) and 10/350 (LC) sampled contents are non-text.

### 4.2 Size

| | Main (n=344 text) | LC (n=340 text) |
|---|---|---|
| Code lines — median | 596 | 107 |
| Code lines — mean | 2,040 | 405 |
| Code lines — max | 27,378 | 15,350 |
| Total code lines | 701,654 | 137,525 |

Both are right-skewed (large enterprise programs + many small files);
lowercase files are ~5× smaller at the median.

### 4.3 Dialect family (Main, n=317)

GnuCOBOL **70 %** · IBM mainframe 11 % · unknown 10 % · Micro Focus 4 % ·
ACUCOBOL 3 % · Fujitsu/NEC & other <1 %.

### 4.4 Standard & source format (Main)

- **Standard:** COBOL-85 **98 %**, COBOL-2002/2014 the rest. The corpus is
  overwhelmingly the 1985 standard.
- **Source format:** fixed **92 %**, free 8 % (judge); the mechanical
  heuristic agrees 95 %.

### 4.5 Program type & maturity (Main)

- **Type:** batch **44 %** · subprogram 23 % · online-CICS 18 % · demo 11 % ·
  test 3 %.
- **Maturity:** production-like **77 %** · student-exercise 17 % · toy 3 % ·
  snippet 3 %.

### 4.6 Domain (Main, n=317)

healthcare-medical **49 %** · education-tutorial 14 % · accounting-erp 8 % ·
demo 7 % · retail 5 % · utility 4 % · insurance 3 % · banking 3 % · payroll /
manufacturing / government tail.

### 4.7 Uppercase vs lowercase (Q3) — clean extension-split

Restricting to a single extension (the `.CBL` rows of the Main sample vs the
`.cbl`-only LC sample) makes the two sub-populations starkly different:

| Dimension | `.CBL` upper (n=185 judged, 6 % gated) | `.cbl` lower (n=291 judged, 17 % gated) |
|---|---|---|
| **Domain** | healthcare-medical **83 %**; long tail <3 % each | education-tutorial **36 %**, demo 11 %, retail 10 %, banking 8 %, accounting 8 % |
| **Maturity** | production-like **96 %** | production-like 45 %, **student-exercise 39 %**, snippet 10 %, toy 6 % |
| **Dialect** | GnuCOBOL **90 %**, Micro Focus 5 % | GnuCOBOL 49 %, IBM 19 %, unknown 18 %, Micro Focus 10 % |

The uppercase `.CBL` archive is almost a monoculture: ~83 % of it is the
Japan Medical Association **ORCA** open-source medical-receipt system (`ORC*`
programs, GnuCOBOL, COBOL-85, fixed-format, batch/CICS) — a single project is
the largest source of archived COBOL under this extension. Lowercase `.cbl`
is where the teaching and hobby COBOL lives.

### 4.8 Feature prevalence

| Feature | Main | LC |
|---|---|---|
| COPY (copybooks) | 69 % | 36 % |
| CALL (subprograms) | 65 % | 30 % |
| EXEC SQL (embedded DB2) | 5 % | 8 % |
| EXEC CICS (online tx) | 6 % | 6 % |
| COMP-3 (packed decimal) | 5 % | 7 % |

## 5. Insights

1. **The extension is a weak signal for "COBOL".** ~40 % of `.CBL` is
   synthetic; lowercase `.cbl` collides with unrelated formats. Any
   archive-scale COBOL study must filter aggressively, and casing matters.
2. **Archived open-source COBOL is not representative of "enterprise COBOL".**
   It is dominated by (a) one large open-source system (ORCA) and (b)
   student/tutorial code. Mainframe idioms (CICS, DB2/`EXEC SQL`, COMP-3)
   appear in only single-digit percentages — the classic IBM z/OS COBOL that
   motivates "COBOL modernization" is largely *absent* from the public
   archive.
3. **Uppercase vs lowercase are different worlds** (§4.7): enterprise
   monoculture vs diverse learner corpus. Naïvely pooling them mixes two
   populations.
4. **A two-layer method works and is cheap.** Deterministic indicators catch
   noise for free and cross-validate the judge (95 % format agreement);
   enum-constrained structured outputs give clean, aggregatable categories at
   ~$0.03/file. Post-hoc normalization means schema changes don't require
   re-judging.

## 6. Limitations

- **Judge trust.** No human ground truth yet, so judge accuracy is
  *unmeasured*. The 95 %/86 % format cross-check and 0 parse failures are
  encouraging but not a substitute; a review tool ships with this study
  (`tools/cobol/review_server.py`) precisely to build that ground truth.
- **`unknown` dialect (10–18 %).** The judge honestly abstains on family when
  evidence is thin; these are unresolved, not resolved-as-other.
- **Truncation.** Sources >16,000 chars are truncated for the judge; very
  large programs are classified from their head. Indicators use full bytes.
- **Encoding.** Many ORCA files carry EUC-JP/Shift-JIS Japanese comments
  rendered as replacement chars in UTF-8; the judge flags this but comment
  ratios and some text metrics are approximate on such files.
- **Sampling scale.** 350 + 350 (+100) contents out of 276k; distributions
  have sampling error (±~5 pts on mid-range proportions). The clean
  `.CBL`-only slice is only n=185.
- **De-dup granularity.** We dedup by content hash, so near-duplicate programs
  (copy-pasted student exercises, forks of ORCA) still count separately;
  "49 % healthcare" is a share of *distinct contents*, not of distinct
  projects.
- **Origin absent.** Without origin/commit we cannot attribute contents to
  repositories, measure project-level concentration, or de-duplicate forks.

## 7. Future work

- **Ground truth & judge eval.** Use the review tool to annotate a stratified
  ~100–200 file sample; report judge precision/recall per field, and inter-
  rater agreement. Add a second model (e.g. a different provider) for a judge-
  vs-judge comparison and majority/adversarial verification.
- **Origin recovery.** Reprocess from the SWH dataset (graph / provenance, or
  the parquet that produced these lists) to attach origin + anchor revision,
  enabling project-level concentration analysis (how much is *literally* the
  ORCA repo and its forks?) and fork de-duplication.
- **Scale & stratify.** With an `SWH_TOKEN` (higher quota), scale to a few
  thousand contents; stratify by size band and extension casing to reduce the
  ORCA-domination of naïve samples.
- **Sharper deterministic layer.** Distinguish copybooks from programs;
  detect free-vs-fixed more robustly (tab-expanded GnuCOBOL); count
  paragraphs/sections; flag EBCDIC/Japanese encodings explicitly.
- **Beyond casing.** Mine other COBOL extensions (`.cob`, `.cpy`, `.ccp`,
  `.cbl` copybooks) and compare; quantify the comic-book / non-COBOL
  collision rate corpus-wide, not just in samples.

## 8. Reproducibility & artefacts

**Commands**
```bash
python3 -m tools.cobol.sample --n 350 --seed 7 --exclude-name 'WBC_.*_FOO'
python3 -m tools.cobol.run_study --no-judge                    # indicators only (no key)
OPENROUTER_API_KEY=… python3 -m tools.cobol.run_study --judge --judge-min-divisions 2 --tag scaled
python3 -m tools.cobol.review_server                           # human annotation UI
```

**Artefacts** (`data/derived/cobol_study/`): `worklist*.csv`,
`reports/<sha1_git>.json` (653 per-content: sample + content + indicators +
verdict), `indicators*.csv`, `summary*.{md,json}`. Toolkit: `tools/cobol/`
(`sample`, `common`, `indicators`, `judge`, `taxonomy`, `run_study`,
`review_server`) + `README.md`.

**Cost & scale.** Current stored verdicts (653 files): 3.98 M prompt +
0.35 M completion tokens, ~$17.2 embedded. Cumulative OpenRouter spend
including the pilot, the v1→v2 re-judge of the Main set, and smoke tests:
**~$26.5**. SWH: ~800 anonymous requests (1/content, cached thereafter).

*Model: claude-sonnet-4.6 (judge) · study authored with Claude Code.*
