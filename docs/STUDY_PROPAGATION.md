# From extension studies to the encyclopedia

An extension study (`docs/cobol_swh_study.md`, `docs/fsf_swh_study.md`,
`docs/rpgle_swh_study.md`, `docs/m_swh_study.md`) reads what Software Heritage
actually holds under one file extension. What it learns is not only a report: it
improves the encyclopedia in four concrete ways.

| Channel | What a study contributes | Where it lands |
|---|---|---|
| **Mapping** | languages *observed* under the extension (with shares), languages *missing* from the mapping, claims that are *never observed*, claims that are *wrong* | `data/derived/pl_taxonomy/ext_claim.csv` (rows with `source = swh_study:<study>`; disputed rows) |
| **Evidence** | share of each language/format per sampling frame, with interval and method | `data/derived/pl_taxonomy/ext_evidence.csv` → the extension page's *Observed in Software Heritage* panel |
| **Identifiers** | measured precision/abstention of Linguist rules, Pygments, SWH Synid, the study's own rules | `data/derived/pl_taxonomy/heuristic_eval.csv` → *Measured on SWH* column and *How identifiers fare* table |
| **Samples & ground truth** | verified files with provenance (origin + path), the judges' and humans' verdicts | `samples/pl/<id>/<sha1_git>/` and the review store `reviews/<sha1_git>/` |

Two more outputs are proposals, not data: **new languages** (rare — a study
finds a notation that is not in `pl_list.txt`) and **extension labels** for
non-PL extensions (e.g. `.fsf` → `data:domain`). Both go to the maintainer's
existing issue workflows (`study_label_proposals.csv` lists the labels).

## The export format (`tools/study_export.py`)

Every study writes the same files to `data/derived/study_exports/<study>/`:

| File | One row per | Key columns |
|---|---|---|
| `study.json` | study | title, extensions, report, population, frames, judges, spend, date |
| `ext_evidence.csv` | (extension, language/format, frame) | `share_pct`, `ci_lo_pct`, `ci_hi_pct`, `n_class`, `n_frame`, `method`, `display` |
| `claims.csv` | proposed mapping change | `action` ∈ observe / add / unobserved / dispute / label, `strength`, shares, `evidence`, `rationale`, `status` |
| `samples.csv` | verified sample | `sha1_git`, `qualified_swhid`, origin, path, `verified_by` |
| `heuristic_eval.csv` | (identifier, metric) | `heuristic_id` or `tool`, `metric`, `value`, `n`, `reference` |

Rules that keep it honest:

- **The frame is part of the fact.** A share is of *files*, of *repositories*,
  of `(repository, path)` files…, never "of the extension" in general.
- **Claims only for conventional extensions.** Magma's `.m` is a claim; C code
  saved as `main.m` is evidence, not a claim that C uses `.m`.
- **Case is kept in evidence, folded in claims.** `ext_claim.csv` is
  case-folded, so a `.CBL` observation is evidence on `.CBL` and a claim on `.cbl`.
- **Sources are never rewritten.** A dispute downgrades the named source's row
  to `strength = disputed` and appends the study's evidence; the row stays, so
  the encyclopedia still records what the source said.
- **The export is the reviewed artifact.** Each claim carries `status`; set it to
  `rejected` in the export to keep a claim out of the taxonomy.

## Workflow

```bash
python3 -m tools.<study>.export                       # write the export
python3 tools/propagate_study.py --study <study>      # plan: what would change
python3 tools/propagate_study.py --study <study> --apply
#   → samples + reviews materialised, taxonomy rebuilt (it reads the exports
#     directly, so the CI taxonomy rebuild keeps them), label proposals listed
python3 web/build_site.py                             # extension pages show the evidence
```

`--apply` is idempotent: samples are rewritten in place, reviews have
deterministic file names (original timestamps), taxonomy rows are recomputed.

## What the four studies contributed (as of 2026-10)

See each study's `claims.csv`. Highlights for `.m`: Objective-C and MATLAB
observed as primary (53.6 % / 41.7 % of files; 71.2 % / 25.8 % of
repositories); **Magma added** (claimed by no source, 0.62 % of files); Limbo
observed once in 10 000 files; MUF and A+ never observed; **M4, Monkey C and
Win32 Message File disputed** (they inherited `.m` from Pygments' Mason lexer
through an extension-overlap join in `master_inventory.match_pygments_name`,
which affects 114 of 588 Pygments identities —
`data/derived/m_study/mapping_pygments_ext_fallback.json`).

Backfilled from the three earlier studies:

- **`.cbl` / `.CBL` (COBOL)** — COBOL observed as primary: 54.4 % of files but
  92.7 % of repositories, because 40.8 % of files (58.9 % of `.CBL`) are one
  GitLab test fixture of synthetic placeholders; Calibre comic-book lists are
  1.7 %. Exact-case rows (`.CBL` only) are kept in the evidence.
- **`.fsf`** — no language claim; a **label proposal** `.fsf → data:domain`
  (FSL FEAT fMRI design files, 80.6 % of files, configuration in Tcl syntax),
  which contradicts the `pl/new:fsl` example in `docs/extension_labels.md`.
  GLSL fragment shaders appear (0.1 % of files, 0.66 % of repositories) but
  `.fsf` is not a conventional GLSL extension: evidence only.
- **`.rpgle`** — RPG IV observed as primary (99.5 % of files); dialect shares
  per frame (fixed-format 40.7 % of files vs 21.8 % of repositories) and the
  copy-member share (≈19 %, frame-invariant) as qualifier rows.

**SWH Synid, measured on four extensions** (`heuristic_eval.csv`): on `.m` it
answers `Text` for 9.9 % of Objective-C (comment strategy) and never
content-identifies non-UTF-8 files in file mode; on `.cbl`/`.CBL` it answers
COBOL for every file — including the synthetic fixtures, comic-book lists and
binaries (precision 0.544 by file); on `.fsf` it calls 97.8 % of FEAT design
files *Algol 68* and misses all GLSL shaders; on `.rpgle` it is right for
98.9 % (it never catches the non-RPG tail). Extension-first identification is
only as good as the extension.

## Site linking fixed while propagating (2026-10-01)

The site attached taxonomy records to in-repo pages by first name hit, so on
`/ext/m/` `pl/matlab` linked to *GNU Octave* and `pl/m` (MUMPS) to *CML*
(through a Wikidata alias "CML" on the MUMPS record). `web/build_site.py` now:

- **chooses the page of a record** (`pl_pages`) when several in-repo languages
  attach to it: own name is one of the record's names *and* its evidence is the
  record's Wikipedia article › own name is the record's canonical name › own
  name is one of the record's names › site order. 69 records change page, e.g.
  `pl/m` → MUMPS, `pl/matlab` → MATLAB, `pl/ocaml` → OCaml, `pl/raku` → Raku;
- **attaches a language to a better record** in two narrow cases: its own name
  is the *canonical* name of another record that shares the key (`Octave`,
  `TypeScript`, `SBASIC`, `S`, `PASM`), unless its Wikipedia evidence confirms
  the first hit; or the first hit came only through an alias and its Wikipedia
  article contradicts the language's evidence while another candidate matches
  it (`CML`, `Small Basic`). 7 languages change record; no page disappears.

Record Wikipedia URLs are not trusted alone (the Wikidata overlay over-assigns
them, `docs/PL_IDENTITY.md` §5), hence the name requirements. Still open:
`languages/M` is Power Query M but its name is `pl/m`'s canonical name, so its
page shows MUMPS facts — a `cannot_link` decision for the identity layer.

Samples: files a human reviewer confirmed (blind, agreeing with both judges)
are always exported; judge-only exemplars stay capped per language.
