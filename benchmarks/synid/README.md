# Synid benchmark (non-regression suite)

A frozen, reusable benchmark to assess [SWH Synid](https://gitlab.softwareheritage.org/teams/codecommons/swh-syntax-identification)
— Software Heritage's syntax identifier — on real archived files, version after
version. It answers: *is this Synid version better or worse than the last one,
on which files, and on which known failure triggers?*

It comes from the `.m` extension study (`docs/m_swh_study.md`), where `.m` is
shared by Objective-C, MATLAB/Octave, Wolfram, Mercury, MUMPS, Magma, … — a
hard, realistic case for any identifier. The assessment behind it:
`docs/m_synid_assessment.md`.

## Contents

| file | what |
|---|---|
| `cases.csv` | the cases (`synid-bench/1`): one archived file each — sha1_git, file name, qualified SWHID, expected language, the Synid answers that count as right (`accept`), tier, tags |
| `files.tar.xz` | the files' bytes (2.9 MB), named by sha1_git — no Software Heritage access needed |
| `run.py` | runs a Synid binary over the cases → `results/<label>.jsonl` |
| `score.py` | scores a run; compares it with a baseline (fixed / regressed / changed); exit 1 on regression |
| `baselines/` | stored runs of known Synid versions — the reference for non-regression |
| `HISTORY.md` | every baseline side by side (`history.py`) |
| `build_cases.py` | how the cases were built from the study (only to release a new version) |

**Tiers.** `gold` (54): a human reviewed the file in the study's blind audit;
both LLM judges agree with the human on all of them. `silver` (1,938): both LLM
judges agree on the language (the study's by-file and by-repository samples).
Gold is the reference; silver gives statistical power and covers far more
cases of each failure trigger.

**Scoring.** A case is right when Synid gives exactly one syntax and it is in
`accept` (MATLAB for MATLAB and Octave files, `Text` only for files that are not
code; names Synid cannot produce yet — Magma, C — are accepted so that a future
version gets credit). Several syntaxes = undecided. Gold also has population
weights (the audit over-samples hard files), giving a weighted estimate.

**Tags** mark the failure triggers found in the assessment, so each one is
tracked on its own:

| tag | trigger |
|---|---|
| `objc-format-string` | Objective-C with `%` inside `@"…"` — the comment strategy took it for MATLAB |
| `comment-free-matlab` | MATLAB/Octave with no line starting with `%`, `!` or `function` — nothing for the MATLAB heuristics; the Pygments strategy then answers `Text` |
| `non-utf8` | bytes that are not UTF-8 — `synid file` skips every content strategy |
| `out-of-candidates` | a language that is not among Synid's candidates for `.m` (Magma, C) |
| `tiny` | fewer than three lines |

## Use

```bash
# build Synid (any version)
git clone https://gitlab.softwareheritage.org/teams/codecommons/swh-syntax-identification
cd swh-syntax-identification && cargo build --release --bin synid && cd -

# run and score against the latest baseline
python3 benchmarks/synid/run.py --synid swh-syntax-identification/target/release/synid --label mytest
python3 benchmarks/synid/score.py benchmarks/synid/results/mytest.jsonl \
    --baseline benchmarks/synid/baselines/48c3c45-default.jsonl --report benchmarks/synid/results/mytest.md
```

`run.py` generates the configuration with the binary itself (`synid info
generate-config`), so it follows Synid's options across versions; it disables
the networked `linguist-api` strategy (the benchmark measures what Synid infers
from a file's name and bytes). `--disable <strategy>` runs an ablation.

**New Synid version accepted?** Copy its run into `baselines/` and re-run
`history.py`. `.github/workflows/synid_bench.yml` builds Synid's `main` weekly
(and on demand), scores it against the latest baseline, and fails — opening an
issue — when a gold case regresses.

**Adding cases** (other extensions: the COBOL, `.fsf`, `.rpgle` studies) means a
new benchmark version (`synid-bench/2`): cases are frozen within a version so
that results stay comparable.
