## Part I — Revisiting the method

Three extensions have been through the playbook (`docs/swh_extension_study_playbook.md`):
`.cbl`/`.CBL` (COBOL), `.fsf` (FSL FEAT) and `.rpgle` (ILE RPG). Before running a
fourth, we re-read the three toolkits and reports as a reviewer would, asking one
question of each design choice: *would the numbers survive if we had got this
wrong?*

### 1. What held up

- **Content over extension.** Classifying from bytes, never from the name, found
  46% non-COBOL under `.cbl`, 99% non-PL under `.fsf`, and 0.5% under `.rpgle`.
  The same method found rot where there was rot and none where there was none.
- **Two frames, always.** By-file and by-repo answered different questions in
  all three studies, and disagreed materially each time.
- **Enum-constrained structured output.** Thousands of judged files with
  essentially no parse failures (one COBOL verdict truncated mid-JSON, fixed by
  raising `max_tokens`); aggregates never fragment.
- **Graph-derived provenance.** The maintainer's `<ext>_files+origin.csv` turned
  "40% of `.CBL` is noise" into "40% of `.CBL` is *one* GitLab test fixture".
- **Cache everything, resume anything.** Re-analysis costs neither quota nor money.

### 2. What was weak

| # | Weakness | Where it showed | Why it matters | Change in the `.m` study |
|---|---|---|---|---|
| W1 | **No ground truth.** The LLM judge was the reference in every evaluation. | All three. Across the three studies' review directories there is **one** human review. rpgle then showed the judge wrong on 9.1% of a lexical field. | Every accuracy we reported was agreement with one model. | Seven labellers, three of them tools we did not write (Linguist, Pygments, SWH Synid); two judges from different vendors; Dawid–Skene accuracy with no oracle; and a **blind, stratified, weighted human audit** wired into the review tool (§5.8). |
| W2 | **The judge saw the indicators, then was scored against a classifier built from them.** | All three judges received the mechanical indicators in the prompt. COBOL reported "the judge matches the heuristic on 95% — an *independent* cross-check". | Agreement inflated by construction; the two layers were not independent. | The primary judge is **blind** (bytes, filename, path, repo only). An ablation (E5) re-judges 300 files *with* indicators to measure anchoring. |
| W3 | **One model, one run.** | All three (Sonnet 4.6, temperature 0). | No estimate of how much a label depends on the model. | A second judge from another vendor (Gemini 3.8 Flash) on the same 2,000 files; κ per field (E4). E5 doubles as a test–retest of the primary judge. |
| W4 | **Rules tuned and scored on the same labels.** | COBOL's reclassifier (P 1.00 / R 0.79) was distilled from, and scored on, the same 162 judged files. rpgle froze its rules after 326 judgements and scored them on the next 1,146 — a genuine hold-out, but not declared in advance, and its v3 was tuned on everything. | In-sample scores overstate what the rules will do on new files. | A **pre-registration** (hypotheses H1–H7, samples, models, frozen v1 rules, tuning split) was **committed before the first study judgement** (commit `eb988475`). v1 is scored prospectively; v2 is tuned on U ranks 1–300 only and scored on the rest. |
| W5 | **Expensive labels cap the sample.** | ≤ 1,000 judged files per frame; rare classes invisible. | Wide intervals, and nothing to say about the tail. | Cheap labels on every fetched file, combined with the judged subset by **prediction-powered inference** (PPI) for valid, narrower intervals. Post-stratified frames use population weights computed *exactly* from the full 51 M-row table. |
| W6 | **The population file was taken as-is.** | No study accounted for its rows (read vs parsed vs dropped). | Silent loss or duplication skews every frame. | An ingest audit: rows parsed = rows starting `swh:1:cnt:` (51,414,668); three defect classes counted and kept (§2.1). |
| W7 | **The mapping was stress-tested against one claim.** | Each study asked "is it language X?" for the one X the mapping named. | A polysemous extension was never tested. | `.m` is claimed by eight languages in our own `ext_claim.csv`, three more through a join bug (§5.7), and three widely used identifiers disagree about it. |

> **Lesson — "The LLM is not the oracle" generalises: no single labeller is.**
> rpgle showed the judge can be confidently wrong on a lexical fact. The
> remedy is not to swap in a different oracle but to measure *every* labeller —
> ours, the community's, SWH's, two LLMs — against each other and, finally,
> against a small weighted human audit, with the judge's prompt kept blind to
> the features it will be compared on.
