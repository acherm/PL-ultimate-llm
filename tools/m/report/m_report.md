# What is *actually* in the `.m` extension on Software Heritage?

*An empirical study of the `.m` file extension in the Software Heritage (SWH)
archive — the most polysemous extension studied so far. Toolkit: `tools/m/`.
Companion studies: `docs/cobol_swh_study.md`, `docs/fsf_swh_study.md`,
`docs/rpgle_swh_study.md`. Pre-registration:
`data/derived/m_study/PREREGISTRATION.md` (commit `eb988475`).*

> **Bottom line.** A `.m` file is not "a MATLAB file" or "an Objective-C file":
> which one it *probably* is depends on how you count. **By file, `.m` is
> ⟪a:A_language/by_file_coarse/objective-c/pct|.0f⟫ % Objective-C and
> ⟪a:A_language/by_file_coarse/matlab-family/pct|.0f⟫ % MATLAB; by repository,
> ⟪a:A_language/by_repo_coarse/objective-c/pct|.0f⟫ % and
> ⟪a:A_language/by_repo_coarse/matlab-family/pct|.0f⟫ %.** The remaining
> ⟪X:tail_pct⟫ % spans seven more notations — Wolfram, MUMPS, Magma, Mercury, a
> FreeBSD interface language, treebank XML. **Much of `.m` was not written by the
> project that holds it:** ⟪X:oc_nonhand_file⟫ % of Objective-C files
> (⟪X:oc_nonhand_repo⟫ % drawn one per repository) are Xcode/CocoaPods templates,
> vendored libraries or decompiled firmware, and SWH's deduplication cannot merge
> them. The language identifiers the ecosystem runs — including **SWH's own
> Synid, which answers "Text" for one Objective-C file in ten** — each fail on one
> specific, fixable pattern.

## 1. Motivation & questions

The earlier studies asked whether an extension is what it claims: is `.cbl`
COBOL, is `.rpgle` RPG? `.m` makes that question meaningless, because it claims
too much. Our own extension→language mapping (`ext_claim.csv`) already lets
eight languages claim it:

| Claimant | What a `.m` file is there | Claimed by |
|---|---|---|
| **MATLAB** / **GNU Octave** | function file, script, `classdef` class; Octave adds `#` comments, `endfunction`, `printf`, `++`, `!=` | Linguist, Pygments, Wikidata |
| **Objective-C** | class implementation (`@implementation`), `main.m`, test case | Linguist, Pygments, Wikidata |
| **Wolfram Language** | a Mathematica package (`BeginPackage[…]`) | Linguist, Wikidata |
| **Mercury** | a module (`:- module …`) | Linguist, Wikidata |
| **M (MUMPS)** | a routine (GT.M / YottaDB store one routine per `.m`) | Linguist |
| **Limbo**, **MUF** | an Inferno module interface; a TinyMUCK Forth program | Linguist |
| *M4, Monkey C, Win32 Message File* | nothing — they inherit `.m` from Pygments' *Mason* lexer through a join bug (§4.1) | Pygments (spurious) |

So we ask, for `.m`:

- **Q1 — Polysemy.** Which languages and formats actually sit under `.m`, in what
  proportion — per file and per repository — and how does that compare with what
  our mapping claims?
- **Q2 — Composition.** How was the code produced (hand-written, template,
  vendored, generated, decompiled), what kind of code is it, and which answers
  survive a change of sampling frame?
- **Q3 — Provenance.** Where does `.m` come from, how concentrated is it, and how
  much of it is replication?
- **Q4 — Method.** Can the identifiers the ecosystem runs (Linguist, Pygments,
  SWH Synid) tell `.m` apart — and how far can LLM judges be trusted when none of
  the labellers is treated as the oracle?

## 2. Data & method

### 2.1 The population we sample from

The study starts from an extraction of every SWH content that some directory
entry names `*.m`, produced by the maintainer with the Rust `swh-provenance`
tool on the CINES supercomputer (`SWH-m-files.zip`: six headerless CSV shards,
14 GB). Each row is a content SWHID plus **one** provenance context — origin,
branch, path, visit timestamp. At this size the population is loaded with
DuckDB into a Parquet table (`tools/m/ingest.py`, ~20 s), and every row is
accounted for:

| | |
|---|---:|
| rows = **unique contents** (each listed once) | **⟪p:unique_contents|,⟫** |
| contents with an origin (the rest: "no predecessors in this graph") | ⟪p:contents_with_origin|,⟫ |
| **distinct repositories** | **⟪p:unique_origins|,⟫** |
| distinct `(repository, path)` files | ⟪p:distinct_origin_path_files|,⟫ |
| → contents that are later versions of the same file | **⟪p:version_inflation_pct⟫ %** |
| provenance path not ending in `.m` (SVN pristine copies, `.asv` autosaves, `.m~`…) | ⟪s:non_dot_m_context_names/n|,⟫ (⟪s:non_dot_m_context_names/pct⟫ %) |

Three caveats follow from the extraction itself. The reported path is *a* place
the bytes occur, not necessarily the `.m` one (one sampled content is reported as
`test.lua` — 21 bytes that are equally valid Lua and MATLAB). The timestamp is
SWH's visit date (2015–2025), not a commit date. And only lowercase `.m` was
extracted: uppercase `.M` (~26 k occurrences) is not covered.

**Provenance skew.** The distribution of contents per repository:

| contents per repository | |
|---|---:|
| median | **⟪p:contents_per_repo/median|.0f⟫** |
| mean | ⟪p:contents_per_repo/mean⟫ |
| max (a decompiled iPhone firmware image) | ⟪p:contents_per_repo/max|,⟫ |
| top repository's share | ⟪p:concentration/top1_pct⟫ % |
| top-10 repositories | ⟪p:concentration/top10_pct⟫ % |
| **80 % of all contents come from** | **⟪p:concentration/repos_for_80pct|,⟫ repos (⟪p:concentration/repos_for_80pct_share|.1f⟫ %)** |
| repositories with exactly 1 content | ⟪p:contents_per_repo/repos_with_1|,⟫ |

> **Why this matters for sampling.** Unlike `.CBL` (one fixture = 40 % of files)
> or `.rpgle` (three parser repositories = 21 %), no single repository dominates
> `.m`. What shapes it instead is **replication**: ⟪p:version_inflation_pct|.0f⟫ % of
> contents are later versions of a file already counted; a third of all
> repositories contain an `AppDelegate.m`; and Xcode personalises every copy, so
> content deduplication cannot merge them (§4.3). A by-file, a by-path and a
> by-repo sample therefore estimate *different populations*. Experiments E1–E2
> (§3) are designed to separate them.

**Sampling fractions.**

| Frame | drawn from | drawn | fetched | judged |
|---|---|---:|---:|---:|
| **U** by file — uniform | ⟪p:unique_contents|,⟫ contents | 10 000 | ⟪a:n/U_used|,⟫ | ⟪a:n/U_judged|,⟫ random + ⟪a:M_tail_census/U/judged/tail|,⟫ tail census |
| **R** by repo — uniform repo, then one file | ⟪p:unique_origins|,⟫ repositories | 3 000 | ⟪a:n/R_used|,⟫ | ⟪a:n/R_judged|,⟫ random + ⟪a:M_tail_census/R/judged/tail|,⟫ tail census |
| **T** heavy tail — 4 files × 25 largest repos | 25 repositories | 100 | 100 | ⟪a:n/T_judged⟫ |

The fractions are tiny, but U and R are uniform-random, so each is an unbiased
estimate of its population (±3 points at 95 %). Samples are drawn by ranking on
`md5(seed ‖ key)`, so **every prefix of a frame is itself a simple random
sample**: the rate-limited fetch (1 200 SWH requests an hour) could stop anywhere
without biasing a frame. Two more frames cost nothing: **by path** (U re-weighted
by 1 / versions of its `(repository, path)`) and **by repo, re-weighted** (U
re-weighted by 1 / contents in its repository — a cross-check on R). Their
weights are computed exactly from the full population table. Finally, every
fetched file that our rules place outside Objective-C and MATLAB is judged too —
a **tail census** (E10) that sizes the rare notations.

### 2.2 Pipeline

| Stage | What it does |
|---|---|
| **Ingest** | 14 GB CSV → Parquet (DuckDB); every row accounted for, defective rows kept with a status |
| **Sample** | md5-ranked frames (U, R, T) carrying exact population weights |
| **Fetch** | raw bytes from SWH by `sha1_git` (self-verifying), cached |
| **Indicators** | lexical markers for every claimant: Objective-C `@` directives, MATLAB function headers and `%` comments, Octave-only syntax (comment- and string-aware), Mercury `:-` declarations, MUMPS routine structure, Wolfram package cells, Magma/Maple block terminators… |
| **Labellers** | our reclassifier (v1 frozen before judging, v2 tuned on 300 files), **Linguist**'s `.m` heuristics, **Pygments** `guess_lexer`, **SWH Synid** (two configurations) |
| **LLM judges** | Claude Sonnet 4.6 **and** Gemini 3.8 Flash via OpenRouter, strict `json_schema` (`m-judge/1`): language, content type, provenance kind, unit kind, MATLAB dialect, related languages, domain, maturity — **blind** to the indicators |
| **Estimation** | Wilson intervals; Kish effective n for re-weighted frames; power-tuned prediction-powered inference (PPI++) |
| **Review** | a web app over every label, with a blind, weighted human-audit queue (`tools/m/review_app.py`) |

### 2.3 What changed since the COBOL study

Before running a fourth study we re-read the first three as a reviewer would.
Seven weaknesses, each with a concrete change here (details and the playbook
revision: `docs/swh_extension_study_playbook.md`, *Revision 2*):

| Weakness in the `.cbl` / `.fsf` / `.rpgle` studies | Change in the `.m` study |
|---|---|
| The LLM judge was the only reference; across the three studies there is **one** human review. | Seven labellers, three of them tools we did not write; two judges from different vendors; Dawid–Skene accuracy with no gold standard; a blind, weighted human audit (Appendix A). |
| The judge was **shown the indicators**, then compared with a classifier built on them — so COBOL's "95 % judge vs heuristic, an independent cross-check" was not independent. | The primary judge is **blind**; an ablation (E5) re-judges 300 files with indicators to measure anchoring. |
| One model, one run. | A second vendor on the same 2 000 files; κ per field (E4); E5 doubles as a test–retest. |
| Rules tuned and scored on the same labels (COBOL's P 1.00 / R 0.79 over the 162 files they came from). | Seven predictions, the samples and frozen v1 rules **committed before judging**; v2 tuned on 300 files only, scored on the other 1 700. |
| ≤ 1 000 judged files per frame; the tail invisible. | Free labels on every fetched file, joined to the judged subset by PPI++; a judged census of the tail stratum (E10). |
| The population file was never row-audited. | Rows read = rows parsed = 51 414 668; three defect classes counted. |
| The mapping was tested against the one language it named. | Every claimant tested, plus the mapping's own construction (§4.1). |

> **Lesson — "the LLM is not the oracle" generalises: no single labeller is.**
> The rpgle study showed the judge can be confidently wrong on a lexical fact.
> The remedy is not to swap in another oracle but to measure *every* labeller —
> ours, the community's, SWH's, two LLMs — against each other and, finally,
> against a small weighted human audit, with the judge kept blind to the features
> it will be compared on.

## 3. Experiments (settings, stated up front)

The crucial design variable is again the **sampling frame**; the new one is the
**labeller**.

| # | Experiment | Sample (frame) | N judged | What it isolates → what it shows |
|---|---|---|---:|---|
| **E1** | File-level population | U, uniform by file | 1 000 | which language a random `.m` *file* is |
| **E2** | Project-level population | R, one file per repo (+ free re-weightings of U) | 1 000 | which language a random `.m` *repository* holds |
| **E3** | Lexical vs semantic | MATLAB-family files of E1–E2 | 698 | who decides "Octave": the syntax or the judge? |
| **E4** | Inter-model agreement | E1 + E2, second vendor | 1 991 | how much each field depends on the model |
| **E5** | Anchoring | U ranks 1–300, judged *with* indicators | 299 | does showing features pull the judge toward our rules? |
| **E6** | Existing identifiers | E1 + E2, 7 labellers | — | how Linguist, Pygments and Synid fail, and why |
| **E7** | Cheap labels | U ranks 1 001–10 000, R 1 001–3 000 (free labels only) | — | how much a free classifier adds to 1 000 judged files |
| **E8** | Heavy tail | T, 4 files × 25 largest repos | 100 | what the biggest repositories actually contain |
| **E9** | Human audit | 100 from E1, stratified, weighted | pending | who is right when labellers disagree |
| **E10** | Tail census | every fetched U/R file our rules place outside Objective-C/MATLAB | ⟪X:census_judged⟫ | how big each rare notation really is (two-phase stratified) |

> **Why seven labellers and two judges?** Every earlier accuracy figure was
> agreement with *one* model that had seen *our* features. Here the question
> "how accurate is the judge?" is replaced by one that has an answer without
> ground truth: *how do independent labellers agree, and where exactly does each
> one break?*

Fixed throughout: temperature 0, structured outputs, sources truncated to 16 000
characters for the judges, binary contents never sent to a judge (they count as
"not code"). Spend: ⟪X:spend⟫. Seven hypotheses (H1–H7) were committed before the
first judgement; they are scored in §4.4. E10 was added afterwards (disclosed in
the pre-registration's post-hoc notes).

## 4. Results

### 4.1 Polysemy — which language, and *at which level*? (Q1)

![What is in the .m space](assets/m/fig_m_languages.png)

**Two languages share the extension, and the frame decides which one is bigger.**

⟪T:frames⟫

*(Brackets: 95 % intervals — Wilson for simple random samples, Kish effective n
for re-weighted frames, PPI++ for the PPI columns.)*

![Language share by sampling frame](assets/m/fig_m_frames.png)

By file, `.m` is ⟪a:A_language/by_file_coarse/objective-c/pct|.0f⟫ % Objective-C and
⟪a:A_language/by_file_coarse/matlab-family/pct|.0f⟫ % MATLAB. By repository it is
⟪a:A_language/by_repo_coarse/objective-c/pct|.0f⟫ % and
⟪a:A_language/by_repo_coarse/matlab-family/pct|.0f⟫ % — and the re-weighted by-file
sample reaches the same answer (⟪a:A_language/by_repo_reweighted_coarse/objective-c/pct|.0f⟫ % /
⟪a:A_language/by_repo_reweighted_coarse/matlab-family/pct|.0f⟫ %) by a completely
different route. With version history collapsed (by path) the two are level
(⟪a:A_language/by_path_coarse/objective-c/pct|.0f⟫ % / ⟪a:A_language/by_path_coarse/matlab-family/pct|.0f⟫ %).

> **Key finding — `.m` has no frame-free majority language.** Most `.m`
> *repositories* are iOS/macOS projects; `.m` *files* split almost evenly; with
> version history collapsed, the two languages tie. An iOS app carries many small
> template and class files; a MATLAB research repository carries many function
> files **and** more archived revisions of each.

**The tail: seven more notations.** In the judged sample, ⟪X:tail_pct⟫ % of files
are neither Objective-C nor MATLAB — about 35 files, too few to size anything.
The **tail census** (E10) fixes that. Of the ⟪X:census_u_phase1⟫ by-file and
⟪X:census_r_phase1⟫ by-repo contents fetched, our rules place ⟪X:census_u_tail⟫ and
⟪X:census_r_tail⟫ outside the two big languages; every one of them was judged, and a
two-phase estimator combines that census with the random judged sample of the
rest (`tools/m/tail.py`):

⟪T:tail_census⟫

*(Two-phase stratified estimates, 95 % intervals. The upper end allows for tail
files our rules missed, bounded by the ⟪X:census_main_judged⟫ judged files of the
main stratum — only ⟪X:census_missed⟫ of which turned out to be tail; conversely
⟪X:census_false_tail⟫ files the rules sent to the tail were Objective-C or MATLAB.
\* = claimed by no source in our mapping.)*

- **Wolfram** — Mathematica packages (IGraph/M, FeynCalc, MathSBML's SBML
  generator), symbolic-integration rule sets (Rubi), and computer-algebra
  *output* (a 250 kB asymptotic expansion written by Mathematica).
- **MUMPS** — VistA and RPMS routines of the US Veterans Affairs hospital system,
  released under FOIA and mirrored across many repositories.
- **Magma** (*claimed by nothing*) — as frequent as MUMPS by file: the
  *SolvableDessins* databases generated by Magma scripts (the second-largest `.m`
  repository in the archive) and research packages such as CHAMP.
- **Mercury** — the Mercury compiler and standard library.
- **Other languages** (*unclaimed*) — the **FreeBSD kobj interface definition
  language** (`mmcbus_if.m`), a **New Jersey Machine-Code Toolkit** specification
  from the Boomerang decompiler, *Monty* bytecode from a coding-school exercise, C
  in a `main.m`.
- **Not code** (*unclaimed*) — **PML**, the XML morphological layer of the Prague
  Dependency Treebank; READMEs; a file holding only a UUID; macOS AppleDouble
  metadata; one git-annex pointer.

**Against the mapping.** The mapping gets the two big languages right and four
more that are really there (Octave, Wolfram, Mercury, MUMPS). It misses **Magma**,
lists **Limbo** and **MUF**, which never occurred — not in the judged samples, not
in the tail census (by-file upper bound ⟪a:M_tail_census/U/estimates/limbo/ci/1⟫ %) —
and lists three languages that have nothing to do with `.m`:
**M4, Monkey C and Win32 Message File**. The cause is in
`tools/master_inventory.py::match_pygments_name`: when a language's name matches
no Pygments lexer, it falls back to *any lexer sharing an extension*. All three
list `.mc`; Pygments' *Mason* lexer claims `*.mc` and `*.m`; so all three became
"Mason" and inherited `.m`. Across the inventory, **114 of 588 Pygments identities
(19 %) were decided by extension overlap** — some harmless (`standard-ml`→SML),
many not (Mercury→MOOCode, NASL/bitbake/SourcePawn→POV-Ray,
OpenCL/qmake/Proguard→Visual Prolog, Motoko→Modelica).

> **Key finding — an extension used as an identity key corrupts the mapping
> meant to test extensions.** The shortcut this line of work warns against —
> trusting what an extension claims — was built into our own inventory join.
> Match by name or alias; treat a shared extension as evidence to review, never
> as identity.

### 4.2 Composition — who wrote it, and what is it? (Q2)

Restricting to what the files are, one property is invariant and most are not.

**Invariants** (true in both frames): MATLAB is hand-written
(⟪a:B_what/by_file/per_language/matlab/provenance_kind/hand-written/pct|.0f⟫ % by file,
⟪a:B_what/by_repo/per_language/matlab/provenance_kind/hand-written/pct|.0f⟫ % by repo);
Octave-only code is ~1 %; ⟪a:B_what/by_file/is_pl_pct|.0f⟫ % of files are in a
programming language at all.

**Everything else depends on the frame:**

⟪T:composition⟫

![Provenance by language and frame](assets/m/fig_m_provenance.png)

⟪T:per_language⟫

**What each frame shows.** By file, ⟪X:oc_nonhand_file⟫ % of Objective-C is not
hand-written; by repository, **⟪X:oc_nonhand_repo⟫ %** is — mostly IDE and framework
templates: Xcode's `AppDelegate.m` and `main.m`, CocoaPods' `Pods-*-dummy.m`
stubs, React Native's `AppDelegate`, Flutter's `GeneratedPluginRegistrant.m`.
The judge's label is not self-certified: the population table records how many
repositories share each file's name, a signal the judge never saw.

| judge's `provenance_kind` (by file) | n | median repositories sharing the file name |
|---|---:|---:|
| hand-written | ⟪a:J_duplication/by_file/hand-written/n⟫ | ⟪a:J_duplication/by_file/hand-written/median_name_repos|,.0f⟫ |
| vendored third-party | ⟪a:J_duplication/by_file/vendored-third-party/n⟫ | ⟪a:J_duplication/by_file/vendored-third-party/median_name_repos|,.0f⟫ |
| IDE / framework template | ⟪a:J_duplication/by_file/ide-or-framework-template/n⟫ | ⟪a:J_duplication/by_file/ide-or-framework-template/median_name_repos|,.0f⟫ |

> **Key finding — much of `.m` was not written by the project that holds it.**
> MATLAB `.m` is overwhelmingly hand-written research and course code in every
> frame. Objective-C `.m` is not: drawn one per repository, more than half of it
> is what Xcode, CocoaPods or React Native generated when the project was created.

### 4.3 Provenance — where it comes from, and how replicated (Q3)

**Forges.** By content: GitHub ⟪p:forges_by_content/github.com|,⟫, Bitbucket
⟪p:forges_by_content/bitbucket.org|,⟫, GitLab ⟪p:forges_by_content/gitlab.com|,⟫,
SourceForge SVN/CVS/Git ~470 k, then package registries and archives — npm
(⟪p:forges_by_content/www.npmjs.com|,⟫), Launchpad, `doi.org` (Zenodo/Figshare
deposits, ⟪p:forges_by_content/doi.org|,⟫), Ifremer's GitLab
(⟪p:forges_by_content/gitlab.ifremer.fr|,⟫, the SonarScope acoustics toolbox),
`pkg.go.dev`. By repository, npm (⟪p:forges_by_repo/www.npmjs.com|,⟫ packages) and
Dart's `pub.dev` (⟪p:forges_by_repo/pub.dev|,⟫) appear — Objective-C shims vendored in
React Native and Flutter plugins.

![Concentration](assets/m/fig_m_concentration.png)

**The largest repositories are not ordinary code** (frame T):

⟪T:top10⟫

**⟪X:t_nonhand⟫ of the 25 largest repositories are mostly not hand-written.** The six
largest — 2.7 % of every `.m` content — hold two **decompiled iOS firmware
images** (IDA-style Objective-C pseudo-code), a **Magma-generated** database, the
**Prague treebank** XML, and two research projects whose `.m` files are machine
output (simulation logs; Maple-generated robot dynamics). Further down,
MathWorks' own toolboxes (Model-Based Calibration, Simulink Coverage) appear
copied into personal repositories.

**Replication, measured on the whole population:**

| family (by file name) | contents | repositories | % of `.m` repositories |
|---|---:|---:|---:|
| Xcode template names (`AppDelegate`, `main`, `ViewController`, `SceneDelegate`) | ⟪s:families/xcode_template_names/contents|,⟫ | ⟪s:families/xcode_template_names/repos|,⟫ | **⟪s:families/xcode_template_names/pct_repos⟫ %** |
| CocoaPods stubs (`*-dummy.m`) | ⟪s:families/cocoapods_dummy/contents|,⟫ | ⟪s:families/cocoapods_dummy/repos|,⟫ | ⟪s:families/cocoapods_dummy/pct_repos⟫ % |
| Coursera *Machine Learning* exercises (≥ 5 exercise names) | ⟪s:families/coursera_ml_repos_ge5_exercises/contents|,⟫ | ⟪s:families/coursera_ml_repos_ge5_exercises/repos|,⟫ | ⟪s:families/coursera_ml_repos_ge5_exercises/pct_repos⟫ % |
| Flutter plugin registrant | ⟪s:families/flutter_registrant/contents|,⟫ | ⟪s:families/flutter_registrant/repos|,⟫ | ⟪s:families/flutter_registrant/pct_repos⟫ % |

![Most replicated file names](assets/m/fig_m_names.png)

SWH deduplicates byte-identical files, yet there are 1.34 M distinct
`AppDelegate.m` and 1.02 M distinct `main.m` contents: Xcode stamps each new
project's template with a header comment carrying its name, author and date.
Stripping `//` comment lines from the sampled `main.m` files collapses
⟪a:L_near_duplicates/main.m/distinct_contents⟫ distinct contents to
⟪a:L_near_duplicates/main.m/distinct_without_comments⟫, and
⟪a:L_near_duplicates/main.m/largest_cluster⟫ of them become one and the same file
— the untouched template. History inflates too: ⟪p:version_inflation_pct|.0f⟫ % of
contents are later versions of a file, including commit bots (`icestraw/EveryDayOC`
keeps 4 016 versions of one `Code.m`; the version we sampled holds only a UUID).

> **Key finding — replication, not concentration, is the population
> artefact of `.m`.** No repository dominates, but personalised templates,
> course clones (Coursera's ML exercises in ~21 000 repositories), vendored
> libraries and bot histories multiply near-identical files that content-level
> deduplication cannot merge. A count of "`.m` files" is to a large extent a
> count of copies.

### 4.4 Method validation (Q4)

**Existing identifiers (E6).** The two judges, from different vendors and blind
to our features, agree on the coarse language of
⟪a:C_labellers/consensus_n|,⟫ of ⟪a:C_labellers/consensus_of|,⟫ files. Against that
consensus — a consensus, not ground truth:

![Seven labellers](assets/m/fig_m_labellers.png)

⟪T:labellers⟫

When they answer, Linguist and Synid are almost always right; Pygments never
abstains, so its errors surface as wrong answers. Each failure traces to a line
of code:

- **Pygments calls MATLAB "Objective-C"** — ⟪X:pyg⟫.
  `ObjectiveCLexer.analyse_text` scores 0.8 for `\[\s*[a-zA-Z_]\w*\s+…` — an
  Objective-C message send *or a MATLAB matrix literal* `[a b]` — while MATLAB
  scores only 0.2 for a `%` comment. Only four lexers claim `*.m`, so Wolfram,
  Mercury, MUMPS and Magma are unreachable.
- **Linguist abstains on MATLAB** — ⟪X:ling⟫. Its MATLAB rule is `^\s*%`: no
  comment line, no decision (Linguist then falls back to a Bayesian classifier).
- **SWH Synid answers `Text` for Objective-C** — ⟪X:synid_text⟫; **without its
  `comment` strategy, ⟪X:synid_nc⟫.** That strategy runs *before* the Linguist
  rules and scores each candidate by the lines that *contain* its comment symbol:
  the `%` in `@"%@"` counts for MATLAB, Objective-C's `//` scores zero, and
  Objective-C is dropped from the candidate set.
- **SWH Synid returns all eight candidates** for ⟪a:C_labellers/synid_utf8/unresolved_text⟫
  text files — **every one** of them invalid UTF-8, while all
  ⟪a:C_labellers/synid_utf8/resolved_text|,⟫ resolved files are valid UTF-8. In `file`
  mode and with the SquashFS host, a strict UTF-8 read fails and every content
  strategy is skipped.

> **Key finding — the archive's own identifier mislabels one Objective-C `.m`
> file in ten, for a reason that fits in one line.** A content heuristic that
> runs *before* a disambiguation rule can remove the right answer from the
> candidate set, and nothing downstream brings it back. Both Synid defects are
> written up for upstream in Appendix B.

**Two judges (E4).** Identity is settled; judgement is not.

⟪T:intermodel⟫

Language agreement is near perfect (κ ⟪a:F_intermodel/language/kappa|.2f⟫). Fields that
ask for judgement degrade in a fixed order — provenance kind, domain, MATLAB
dialect, maturity — and the same order appears when the *same* model re-judges
299 files (E5: language ⟪X:retest_lang⟫ % identical, maturity ⟪X:retest_mat⟫ %).
`confidence` shows the κ paradox: 99.7 % agreement, κ = 0, because both models
always say "high".

**Lexical vs semantic (E3).** The prompt defined `octave` *lexically*: only when
the file uses syntax MATLAB rejects.

⟪T:octave3⟫

As pre-registered, with regex markers, the disagreement looked two-sided (7 vs 4)
— but three of the four "MATLAB with Octave syntax" cases were **our** errors:
`!=` inside a string, `printf(` inside a comment, the valid-MATLAB `1;` idiom.
With markers computed on code only, the models split. **Gemini follows the
definition exactly. Sonnet calls seven syntax-free files "Octave"** — three
because they sit in an Octave-Forge package tree (`inst/`), one by its file name,
three because they use double-quoted strings, legal MATLAB since R2017a. On the
purely semantic *portability* question the split is starker: Sonnet calls
⟪X:port_s⟫ % of MATLAB files MATLAB-specific, Gemini calls ⟪X:port_g⟫ % portable to
Octave, while only ⟪X:port_lex⟫ % use a lexical MATLAB-only construct.

> **Lesson — lexical facts need a lexer; semantic facts depend on the model.**
> Our first "lexical" rule manufactured three of four apparent judge errors
> because it could not see strings and comments. Once fixed, one judge honoured
> the definition and the other overrode it with context — the rpgle failure,
> reproduced by one vendor and absent in the other. Report κ per field and do not
> aggregate fields below ~0.7 (`maturity`, `matlab_dialect`) without a human audit.

**Anchoring (E5).** Shown the indicators, the judge changed its language label on
⟪a:E_anchoring/language_flips⟫ of ⟪a:E_anchoring/n⟫ files (one toward our rules, one
away); agreement with our rules was ⟪a:E_anchoring/agree_with_ours_blind⟫ % blind and
⟪a:E_anchoring/agree_with_ours_shown⟫ % shown. On a task this lexical, the indicators
add nothing the judge does not already read in the bytes.

**Our reclassifier, prospectively.**

⟪T:reclass⟫

The frozen v1 — written before any judge label existed — agrees with the judge
on ⟪X:v1_heldout⟫ % of held-out files; v2, tuned on 300, gains
⟪X:v2_gain⟫ points. Its errors are abstentions on the tail, plus a known blind
spot: `printf(` and `!=` are Octave-only *relative to MATLAB* but ordinary in C,
so a few C and MUMPS files are called Octave.

**Cheap labels (E7).** PPI++ combines the free reclassifier labels on the
unjudged files with the judge on the judged ones:

⟪X:ppi_table⟫

With ⟪X:ppi_pool_u⟫ free labels by file and ⟪X:ppi_pool_r⟫ by repository, the tuned
weights are λ = ⟪X:ppi_lambda_u⟫ and ⟪X:ppi_lambda_r⟫, and intervals narrow by
⟪X:ppi_gain_u⟫ % and ⟪X:ppi_gain_r⟫ % — the precision of ~⟪X:ppi_eff_u⟫× and
~⟪X:ppi_eff_r⟫× as many judged files, at no API cost. For the rare notations, where
PPI helps little, the tail census (E10) does the work.

**Pre-registration.** Seven predictions were committed before judging; the
verdicts are computed by `analysis.py`:

| | Prediction | Observed | Verdict |
|---|---|---|---|
| H1 | Objective-C + MATLAB ≥ 95 % by file; rest spans ≥ 6 notations | ⟪X:h1⟫ | held |
| H2 | Objective-C share differs ≥ 10 pts between frames | ⟪X:h2⟫ | held (direction guessed wrong) |
| H3 | ≥ 15 % of Objective-C not hand-written (by file) | ⟪X:h3⟫ | held |
| H4 | Linguist abstains ≥ 5 %; Pygments MATLAB→ObjC ≥ 5 %; Synid ≥ 10 % | ⟪X:h4⟫ | consistent (not a blind test) |
| H5 | the judge's `octave` disagrees with the lexical definition one-sidedly | ⟪X:h5⟫ | **failed** as registered; holds for Sonnet only post hoc |
| H6 | shown the indicators, the judge agrees more with our rules | ⟪X:h6⟫ | **failed** |
| H7 | κ ≥ 0.9 on language; < 0.7 on provenance and maturity | ⟪X:h7⟫ | half held |

Writing them down first is what made the failures informative: H5's failure is
how the lexer bug in our own markers was found.

## 5. Key findings & lessons (summary)

> **Findings.**
>
> 1. **`.m` has no frame-free majority language:** Objective-C
>    ⟪a:A_language/by_file_coarse/objective-c/pct|.0f⟫ % / MATLAB
>    ⟪a:A_language/by_file_coarse/matlab-family/pct|.0f⟫ % by file,
>    ⟪a:A_language/by_repo_coarse/objective-c/pct|.0f⟫ % /
>    ⟪a:A_language/by_repo_coarse/matlab-family/pct|.0f⟫ % by repository, a tie by path.
> 2. A **tail of seven notations** (tail census, by file: ⟪X:m_u⟫) — four of them
>    (Magma, the FreeBSD IDL, NJMC, PML XML) claimed by no source; Limbo and MUF,
>    claimed, never seen.
> 3. **Much of `.m` is replication:** ⟪X:oc_nonhand_repo⟫ % of Objective-C drawn per
>    repository is templates, vendored or dumped; Xcode template names sit in
>    ⟪s:families/xcode_template_names/pct_repos|.0f⟫ % of `.m` repositories;
>    ⟪p:version_inflation_pct|.0f⟫ % of contents are later versions; deduplication
>    cannot merge personalised templates.
> 4. **MATLAB is the stable half:** hand-written research and course code in every
>    frame.
> 5. **Every identifier fails in a specific way** — Pygments (matrix literals),
>    Linguist (no `%` comment), Synid (a comment heuristic, and non-UTF-8 in file
>    mode) — and our own mapping gave `.m` to three unrelated languages.

> **Lessons for extension studies.**
>
> 1. For a polysemous extension, ask *which* language per file **and** per
>    repository — and state the frame with every number (again).
> 2. **Measure every labeller; privilege none.** Two judges from different vendors
>    plus the ecosystem's own tools turn "the judge said" into measured agreement
>    — and produced three bug reports.
> 3. **Keep the judge blind** to the features it will be compared against; the
>    ablation costs little and settles the question.
> 4. **Lexical facts need a lexer.** Regexes that cannot see strings and comments
>    produce false "judge errors".
> 5. **Pre-register, and let cheap labels carry the volume.** Failed predictions
>    were the most informative results; a validated free classifier multiplies the
>    effective judged sample (~⟪X:ppi_eff_u⟫× by file via PPI++) and makes a judged
>    census of the rare strata affordable.

## 6. Limitations

- **The consensus is not ground truth.** Two LLMs agreeing is strong but
  correlated evidence (same bytes, same path). The 100-item blind audit queued in
  the review app (Appendix A) is the step that replaces it — none of the four
  studies has run one yet.
- **The tail is sized, not settled.** The census pins each rare notation from
  below; the upper ends are limited by the ~1 000 judged main-stratum files per
  frame, where a tail file our rules missed would hide (only ⟪X:census_missed⟫ did).
- **One provenance context per content;** by-repo frames under-count widely
  shared files, so template shares are conservative. Timestamps are visit dates.
- **Only lowercase `.m`** — `.M` and `.mm` (Objective-C++) are outside the
  extraction.
- **Post-hoc elements are marked as such:** reclassifier v2, the comment- and
  string-aware Octave markers, the "unknown → not code" normalisation for the
  judges' non-code labels, frame T.

## 7. Reproducibility & artefacts

```bash
unzip SWH-m-files.zip -d .cache/m/csv
.venv/bin/python -m tools.m.ingest && .venv/bin/python -m tools.m.ingest --stats
.venv/bin/python -m tools.m.name_pop                               # replication signals
.venv/bin/python -m tools.m.sample --n-uniform 10000 --n-repo 3000 --seed 17
.venv/bin/python -m tools.m.sample --top-repos 25 --per-repo 4     # frame T
python3 -m tools.m.fetch                                           # SWH_TOKEN in .swh_token
python3 -m tools.m.study --label && python3 -m tools.m.run_synid   # free labellers
python3 -m tools.m.study --judge --n 1000                          # + --model google/gemini-3.8-flash
python3 -m tools.m.study --judge --n 300 --frames U --with-indicators   # E5
python3 -m tools.m.tail --select && python3 -m tools.m.tail --judge     # E10 tail census
python3 -m tools.m.analysis && .venv/bin/python -m tools.m.make_figures
python3 -m tools.m.build_report --pdf                              # this report
python3 -m tools.m.audit --build && python3 -m tools.m.review_app  # E9
```

Artefacts in `data/derived/m_study/`: `PREREGISTRATION.md`, `population.json`,
`population_signals.json`, `worklist_*.csv`, one layer per labeller
(`labels/`, `synid.jsonl`, `judge/<model>/`), `analysis.json` (every number in
this report), `audit_queue.csv`. Figures in `docs/assets/m/`. Spend:
⟪X:spend_short⟫.

*Models: claude-sonnet-4.6 and gemini-3.8-flash (judges) · study authored with Claude Code.*

## Appendix A — The review tool

Every content accumulates labels from **seven labellers** — two LLM judges, our
reclassifier, Linguist, Pygments, and Synid in two configurations — plus its
provenance and, the point of the tool, a **human**. `tools/m/review_app.py` puts
them in one pane, surfaces where they disagree, and records ground truth.

```bash
python3 -m tools.m.review_app --reviewer <you>     # http://127.0.0.1:8769
```

### A.1 Dashboard

![Review app — dashboard](assets/m/app_dashboard.png)

Language by frame (by file, by repo, the 25 largest repositories), every
labeller's agreement and abstention against the primary judge — labelled
explicitly as *not* ground truth — provenance kinds, and one-click work queues
for each disagreement type: judges disagree, judge ≠ our rules, Pygments ≠ judge,
Synid `Text`/unresolved, Linguist abstains, Octave lexical/semantic split, the
tail, not hand-written.

### A.2 Browse & filter

![Review app — Pygments ≠ judge](assets/m/app_list.png)

Filter by frame, judge language, flag, or name/origin. Each row shows all seven
labellers as coloured tags (agrees with the judge / disagrees / abstains), so a
column of red is one tool's failure mode at a glance — here, Pygments calling
MATLAB and Wolfram files Objective-C.

### A.3 Per-file view, and group assertions

![Review app — a file page](assets/m/app_detail.png)

The screenshot is a React-Native test file that every labeller calls Objective-C
— except SWH Synid, which answers `Text` (§4.4). The page shows the source; the
provenance (forge link at the archived branch, SWH browse context, qualified
SWHID) with three population signals the judges never saw — contents in the
repository, archived versions of this path, repositories sharing this file name;
all labellers with their raw answers; both judges' full verdicts side by side,
differences shaded; the non-zero indicators; and two forms. As in the COBOL
tool, **"assert for a group"** records one fact for an origin, a filename regex
or a path regex — e.g. *every file of `CrackerCat/iPhone15-3_…_Restore` is
decompiled firmware*, one assertion for an origin that holds 429 552 `.m`
contents. Rules are append-only in
`reviews_m/_rules.jsonl`.

### A.4 The blind audit

![Review app — blind audit item](assets/m/app_blind.png)

`/audit` serves a **stratified random sample** of the judged by-file frame: 60 of
the 77 files where at least one labeller dissents (weight 1.28) and 40 of the 919
where all agree (weight 22.98), so the scores estimate accuracy over the whole
population rather than over hard cases. Items open **blind**: machine labels stay
hidden until the reviewer saves — the human version of the anchoring ablation.
`Save & next` (or the `n` key) walks the queue; `python3 -m tools.m.audit
--score` turns the reviews into a weighted accuracy with a 95 % interval for every
labeller.

### A.5 Storage

Reviews are **append-only JSON, one file per review**
(`reviews_m/<sha1_git>/<UTC>--<reviewer>--<hash8>.json`), recording whether they
were made blind. Git is the sync layer; changing your mind means writing a new
review.

> **Why human review still matters.** Queue item #25 is
> `moxunit_fieldtrip_util_parse_walltime.m`: a **git-annex pointer** — a symlink
> path stored as file content. Sonnet and our rules call it MATLAB (from its
> name and path), Gemini calls it not code, and Linguist and Synid abstain. No
> majority of machines settles that; a person does in five seconds.

## Appendix B — Two Synid defects, ready to report upstream

**Tool.** `swh-syntax-identification` (Synid), commit `9bc1c32` (2026-06-15), `synid
file`, default strategies minus the network-bound `linguistapi`.

**1 · The comment strategy removes Objective-C.** Reproduction: any `.m` file
with `@interface`/`@implementation`, no `//` or `/* */` comment, and a format
string such as `@"%@"` (e.g. `swh:1:cnt:bbbcb890d40628ee37cff8c5f3d1a9791212ea63`).
The *extension* strategy yields eight candidates; the *comment* strategy
(`src/strategies/comment_strategy/mod.rs`) scores each by the lines that *contain*
its comment symbol — `line.contains(c)`, string literals included — and keeps
only the maximum: `%` scores for MATLAB and Mercury, Objective-C's `//` scores
zero, Objective-C is dropped. The Linguist rule that would have decided runs
next, on a set that no longer contains the answer; the pipeline returns `Text`.
Impact: ⟪X:synid_text⟫ of Objective-C files; ⟪X:synid_nc⟫ without the strategy. Fixes
(any one): count a symbol only at line start or outside strings; run
`hyplyheuristics` before `comment` when a Linguist disambiguation block exists;
down-weight instead of eliminate.

**2 · Non-UTF-8 content is never content-identified in `file` / SquashFS mode.**
All ⟪a:C_labellers/synid_utf8/unresolved_text⟫ text files left with the full candidate
set are invalid UTF-8 (typically MATLAB with Latin-1 comments); all
⟪a:C_labellers/synid_utf8/resolved_text|,⟫ resolved files are valid UTF-8.
`FileFetcher` and the SquashFS host read with `std::fs::read_to_string`, which
fails; the AWS S3 host (`from_utf8_lossy`) and the Web API host (`reqwest`
`text()`) decode lossily and are not affected. A lossy read everywhere would let
Linguist's `^\s*%` rule resolve ⟪a:C_labellers/synid_utf8/unresolved_matlab_with_pct_comment⟫
of the ⟪a:C_labellers/synid_utf8/unresolved_matlab⟫ MATLAB files.
