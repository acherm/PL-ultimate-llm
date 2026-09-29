### 6. The pre-registration, scored

Seven predictions were committed before the first study judgement (`eb988475`).
Verdicts are computed by `analysis.py` (section K), not written by hand.

| | Prediction | Observed | Verdict |
|---|---|---|---|
| H1 | By file, Objective-C + MATLAB ≥ 95%; the rest ≤ 5% but spanning ≥ 6 languages/formats | ⟪H1⟫ | **held** |
| H2 | Objective-C share differs by ≥ 10 points between frames (weak guess: higher by file) | ⟪H2⟫ | **held** — direction guessed wrong |
| H3 | By file, ≥ 15% of Objective-C is not hand-written | ⟪H3⟫ | **held** |
| H4 | Linguist abstains ≥ 5%; Pygments MATLAB→Objective-C ≥ 5%; Synid `Text`/unresolved ≥ 10% | ⟪H4⟫ | consistent — *not a blind test* (these tools were run during calibration) |
| H5 | The judge's `octave` disagrees with the lexical definition, one-sidedly | ⟪H5⟫ | **failed as registered**; holds post hoc for Sonnet only, after fixing *our* lexical markers |
| H6 | Shown the indicators, the judge agrees more with our rules | ⟪H6⟫ | **failed** |
| H7 | κ ≥ 0.9 on `language`; < 0.7 on `provenance_kind` and `maturity` | ⟪H7⟫ | **half held** — provenance is more reliable than predicted |

Three held (H1–H3, H2 with the direction guessed wrong), H4 was not a blind
test, H7 held by half, and two failed as registered (H5, H6) — H5 holding post hoc
for one of the two models once we fixed our own markers. Writing them down first is what
makes the failures informative: without H6 on record, "the blind judge is as good
as the anchored one" would read as an unremarkable detail rather than as a
refuted expectation; without H5, the lexer bug in our own markers would have been
invisible — it was found *because* the registered test failed and we read why.

### 7. Lessons for the playbook

Four extensions, one method:

| | `.cbl` / `.CBL` | `.fsf` | `.rpgle` | `.m` |
|---|---|---|---|---|
| Is it what the extension claims? | No — 46% not COBOL | No — 99% not a PL | Yes — 99.5% RPG | *Which* claim? 2 majors + 7 minors |
| Dominant population artefact | one synthetic fixture = 40.8% | git-annex pointers | 3 parser repos = 21% | Xcode/CocoaPods templates, firmware dumps, codegen |
| Frame sensitivity | contamination 46% → 7% | (census) | fixed-format 41% → 22% | Objective-C 54% → 71% |
| Where the judge was wrong | — | — | a lexical field, one-sided (9.1%) | Octave by context (1 of 2 vendors); portability (models disagree) |
| Where existing tools fail | — | — | — | Pygments 12% of MATLAB; Linguist abstains 14% of MATLAB; Synid 10% of Objective-C, and non-UTF-8 files in file mode |
| Judge independent of rules? | no | no | no | **yes (blind) — and it made no difference here** |
| Human ground truth | 1 review | 0 | 0 | audit queue of 100, weighted, blind — pending |

Revision 2 of the playbook (`docs/swh_extension_study_playbook.md`) records the
rules; the short version:

> **Lesson A — Measure every labeller; privilege none.** The question "how
> accurate is the judge?" has no answer without a reference; "how do seven
> independent labellers agree, and where exactly does each one break?" does —
> and it produced three upstream bug reports (Synid ×2, our own inventory join).

> **Lesson B — Lexical facts need a lexer.** "Compute lexical facts in code"
> (rpgle) is necessary but not sufficient: a regex that cannot see strings and
> comments manufactured three of the four disagreements we first blamed on the
> judge.

> **Lesson C — The second model is the cheapest reliability measurement there
> is.** One third of the primary judge's cost bought a per-field κ, located the
> fields not worth aggregating (`maturity`, `matlab_dialect`), and showed that
> "the LLM over-applies context" is a property of *a* model, not of LLMs.

> **Lesson D — Write the predictions down.** Two of seven failed; both failures
> taught us more than the successes.

> **Lesson E — Duplication is a first-class population property.** `.m` has
> 46% version inflation, millions of personalised template copies that
> content-deduplication cannot merge, and bot-driven histories. Measure these on
> the full population table before sampling; they decide what "a file" means.

### 8. Limitations

- **The consensus is not ground truth.** Two LLMs agreeing on 99.7% of files is
  strong but correlated evidence (both saw the same path and bytes). The audit
  queue exists to replace it with human labels; until it is reviewed, every
  accuracy is agreement.
- **The tail is thin.** 3.5% of 1,000 files is 35 files over seven notations;
  proportions below 1% have wide intervals, and Limbo/MUF are only bounded
  (< 0.38%). A stratified sample targeting non-Objective-C, non-MATLAB contents
  (cheap to draw with the reclassifier) would size it.
- **Only lowercase `.m`.** The extraction is case-sensitive; `.M` (~26 k
  occurrences) is not covered.
- **One provenance context per content.** A content that exists in many
  repositories is attributed to one; by-repo frames therefore under-count
  widely shared files (templates, vendored libraries) — the direction of this
  bias makes our template shares conservative.
- **Visit timestamps.** The CSV's timestamp is when SWH visited, not when code was
  written; no temporal claim is made.
- **Post-hoc elements are labelled as such**: reclassifier v2 (tuned on the
  tuning split), the comment/string-aware Octave markers, the not-code
  normalisation, frame T.

### 9. Recommendations and future work

**For Software Heritage (Synid).** Two defects, both with a one-line mechanism
and a measured impact (Appendix C): the comment strategy removes Objective-C on
~10% of Objective-C `.m` files; with the local-file and SquashFS content hosts,
non-UTF-8 content silently skips every content strategy. Both are worth
reporting upstream with the sample SWHIDs.

**For our inventory.** Replace the extension fallback in
`master_inventory.match_pygments_name` by name/alias matching only, and route
extension-overlap candidates to the review queue; re-derive `ext_claim.csv`. Add
**Magma** as a `.m` claimant; flag Limbo/MUF claims as unobserved in SWH.

**Next studies.**
- Run the 100-item blind audit (≈ 2 hours) and score all labellers.
- Complete the 10,000-file by-file frame (≈ 8 h of SWH quota) for PPI at N ≫ n.
- A tail-targeted sample (reclassifier says "neither Objective-C nor MATLAB")
  to size Magma, MUMPS, Mercury and the non-code formats properly.
- Extract `.M` and `.mm` (Objective-C++), the two neighbours this study could
  not see.
