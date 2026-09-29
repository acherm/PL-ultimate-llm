# `.m` study — pre-registration

Written **2026-09-29T19:46Z**, after drawing the samples and reading ~500 fetched
files, **before any LLM-judge verdict on the study sample** (4 calibration calls
on hand-picked oddities excepted: `pong.m`, `lnd92254_094.m`,
`MBasym_temp2order100part2283.m`, `test.lua`). Committed together with the frozen
v1 reclassifier so the git timestamp is the evidence.

## Frozen before judging

- Samples: `worklist_all.csv`, seed 17 — U (by-file, uniform over 51,414,668
  contents) 10,000; R (by-repo, uniform over 2,076,825 origins, one content each)
  3,000. Ranks are md5-derived, so every rank-prefix is itself a simple random sample.
- Judge targets: U rank ≤ 1000 and R rank ≤ 1000 (2,000 contents).
- Primary judge: `anthropic/claude-sonnet-4.6`, temperature 0, schema `m-judge/1`,
  **blind** (no mechanical indicators in the prompt). Second judge:
  `google/gemini-3.8-flash`, same prompt and schema.
- Our reclassifier: `m-reclass/1` (`tools/m/reclassify.py`), written before any
  judge label. **Tuning split**: U ranks 1–300 may be used to revise it (→ v2);
  everything else is held out. v1 is scored prospectively on all of it.
- Existing identifiers: Linguist `.m` heuristics (as vendored in Synid), Pygments
  2.19 `guess_lexer_for_filename`, Synid `9bc1c32` (`file` mode, two configs).

## Predictions

- **H1 (polysemy).** By file, Objective-C + MATLAB-family ≥ 95%. The remainder is
  ≤ 5% but spans ≥ 6 distinct languages/formats.
- **H2 (frame).** The Objective-C share differs by ≥ 10 points between the by-file
  and by-repo frames. (Direction not predicted with confidence; weak guess:
  higher by file.)
- **H3 (not hand-written).** By file, ≥ 15% of Objective-C `.m` files are templates,
  vendored third-party copies, generated or dumped — not hand-written.
- **H4 (existing tools).** Linguist's heuristics abstain on ≥ 5% of files; Pygments
  labels ≥ 5% of MATLAB-family files as Objective-C; Synid's default content
  pipeline returns `Text` or an unresolved candidate set on ≥ 10% of files.
  *Not a blind prediction:* these three tools are label-free and were already run on
  the first 489–776 fetched files during calibration (abstain 5.7%; Pygments
  MATLAB→Objective-C ~11%; Synid `Text`/unresolved 12%). H4 is recorded so the
  full-sample figures can be checked against the calibration glimpse, not as a test.
- **H5 (lexical definition).** The judge's `octave` label disagrees with the lexical
  definition (Octave-only tokens present) and the disagreement is **one-sided**, as
  with `**FREE` in the rpgle study.
- **H6 (anchoring).** Shown the indicators, the same judge agrees *more* with our
  reclassifier than it does blind.
- **H7 (inter-model).** Cohen's κ between the two judges ≥ 0.9 on `language`;
  < 0.7 on `provenance_kind` and `maturity`.
