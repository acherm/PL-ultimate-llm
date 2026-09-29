### 4. Results — what `.m` is

#### 4.1 Two languages, and the frame decides which one is bigger

![Language share by sampling frame](assets/m/fig_m_frames.png)

⟪FRAMES_TABLE⟫

*(Coarse classes; brackets are 95% intervals — Wilson for simple random samples,
Kish effective n for re-weighted frames, power-tuned PPI for the PPI columns.
Binary contents are never sent to a judge and count as "not code".)*

Read across the Objective-C row. **By file**, `.m` is 54% Objective-C and 43%
MATLAB. **By repository**, it is 71% Objective-C and 27% MATLAB — and the
re-weighted by-file sample (U′) lands on the same answer (70% / 30%) through a
completely different route, which is the best evidence that neither is an
artefact. **By `(repository, path)`**, i.e. with version history collapsed, the
two languages are level (50% / 47%).

> **Finding 1 — `.m` has no frame-free majority language.**
> Most `.m` *repositories* are iOS/macOS projects; most `.m` *files* are split
> almost evenly; with version history collapsed to one content per
> `(repository, path)`, the two are level.
> The mechanism is visible in the population: an Objective-C app carries many
> small template and class files, a MATLAB research repository carries many
> function files **and** more archived revisions of each (the by-path
> re-weighting shifts 4 points toward MATLAB).

Octave-only files are rare (1.1% of files; 16 of the 23 files the Sonnet judge
called Octave use Octave-only syntax — §5.2), and 99.2% of files are in a
programming language at all.

#### 4.2 The tail: seven more notations under one extension

By file, **3.5%** of `.m` is neither Objective-C nor MATLAB-family. Small — but
it spans seven distinct languages or formats, four of them claimed by no source
our mapping uses:

⟪TAIL_TABLE⟫

- **Wolfram** (1.0%): Mathematica packages, symbolic-integration rule sets
  (Rubi), and computer-algebra *output* — e.g. a 250 kB asymptotic expansion
  written by Mathematica itself.
- **MUMPS** (0.6%): VistA and RPMS routines — the US Veterans Affairs hospital
  system, released under FOIA and mirrored across many repositories.
- **Magma** (0.4%, unclaimed): files of the *SolvableDessins* database, generated
  by Magma scripts — one repository with 256,931 `.m` contents, the
  second-largest in the archive.
- **Mercury** (0.3%): the Mercury compiler and standard library.
- **Other languages** (unclaimed): the **FreeBSD kobj interface definition
  language** (`mmcbus_if.m`), a **New Jersey Machine-Code Toolkit** specification
  from the Boomerang decompiler, *Monty* bytecode from a coding-school stack
  interpreter exercise, C code in a `main.m` — and a CSV matrix that the judge
  files here although its own detail field calls it data.
- **Not code** (0.8%): **PML**, the XML morphological layer of the Prague
  Dependency Treebank; Markdown READMEs; a file holding only a UUID; macOS
  AppleDouble metadata (`._vonMiseFourier.m`) and other binaries.

**Limbo** and **MUF**, both claimed by Linguist, never occurred in 2,000 judged
files (by-file upper 95% bound: 0.38%).

#### 4.3 Who wrote it? Much of `.m` was not written by its project

![Provenance by language and frame](assets/m/fig_m_provenance.png)

⟪PROVENANCE_TABLE⟫

The judge's `provenance_kind` separates hand-written code from files a tool or a
template put there. **By file, 22% of Objective-C is not hand-written; by
repository, 58% is** — mostly IDE/framework templates: Xcode's `AppDelegate.m`
and `main.m`, CocoaPods' `Pods-*-dummy.m` stubs, React Native's `AppDelegate`,
Flutter's `GeneratedPluginRegistrant.m`. MATLAB is the opposite: 94–95% is
hand-written in both frames, with a small generated tail (symbolic code exported
from Maple, simulation logs written as `.m` scripts).

This label is not self-certified. The judge never saw how many repositories
share a file's name; the population table knows (`name_popularity.json`):

| judge's `provenance_kind` (by file) | n | median repos sharing the file name |
|---|---:|---:|
| hand-written | 837 | 2 |
| vendored third-party | 21 | 48 |
| IDE / framework template | 91 | 13,334 (quartiles 1 / 567,590) |

Files the judge calls templates have names that recur across **thousands** of
repositories; files it calls hand-written have names that recur in two. (The low
quartile of templates is CocoaPods stubs, whose names embed the project name —
`Pods-MyApp-dummy.m` — and so never repeat.)

> **Finding 2 — A `.m` count is largely a count of boilerplate, and
> deduplication does not remove it.** 42% of all `.m` repositories contain an
> Xcode-template file name; 12% contain a CocoaPods stub. SWH stores each copy
> as a distinct content because the template is personalised at creation (§2.2:
> ⟪NEARDUP⟫). By repository, more than half of what a
> random Objective-C `.m` file tells you is what Xcode, CocoaPods or React
> Native generated when the project was created.

The judge also surfaces **vendored MathWorks toolboxes** (Model-Based
Calibration, Simulink Coverage, Real-Time Workshop) copied wholesale into
personal repositories, and — at population scale — **commit-bot histories**:
`icestraw/EveryDayOC` keeps 4,016 versions of a single `Code.m` (the version we
sampled holds nothing but a UUID); `duaneking/metrics` holds 19,879 versions of
one `helloWorld.m`.

#### 4.4 The heavy tail, named (frame T)

⟪TOP_TABLE⟫

**Twelve of the 25 largest `.m` repositories are mostly not hand-written**, and
the six largest — 2.7% of every `.m` content in the archive — contain no ordinary
program at all: two **decompiled iOS firmware images** (429,552 and 249,201
files of IDA-style Objective-C pseudo-code), a **Magma-generated** mathematical
database, the **Prague treebank** in XML, and two research projects whose `.m`
files are **machine output** (simulation logs; Maple-generated robot dynamics).
Unlike `.CBL`, no single repository dominates; like `.CBL`, the largest
repositories are the least representative.

### 5. Results — how well can `.m` be labelled?

#### 5.1 Seven labellers against the two-judge consensus (E6)

The two LLM judges, from different vendors and blind to our indicators, give the
same coarse language for **1,991 of 1,997** files judged by both (99.7%). We use
that agreement set as the reference — a consensus, not ground truth (§5.8).

![Seven labellers](assets/m/fig_m_labellers.png)

⟪LABELLERS_TABLE⟫

Recall per class (abstaining counts as a miss) shows *where* each tool fails —
beyond the two big languages, almost everywhere:

⟪PERCLASS_TABLE⟫

When they answer, Linguist and Synid are almost always right (99.7–99.9%);
Pygments never abstains, so its errors surface as wrong answers (6.4%). All
three fail **systematically**, and each failure traces to a specific line of
code:

| Tool | Failure | Share | Mechanism |
|---|---|---:|---|
| **Pygments** | calls MATLAB "Objective-C" | 86 / 695 MATLAB files (12.4%) | `ObjectiveCLexer.analyse_text` scores 0.8 for `\[\s*[a-zA-Z_]\w*\s+…[\]:]` — a message send *or a MATLAB matrix literal* `[a b]`; `MatlabLexer` scores only 0.2 for a `%` comment. Only four lexers claim `*.m`, so Wolfram, Mercury, MUMPS and Magma are unreachable. |
| **Linguist** heuristics | abstain on MATLAB | 97 / 695 (14.0%) | the MATLAB rule is `^\s*%` — any MATLAB file without a comment line falls through to the Bayesian classifier. |
| **SWH Synid** | answers `Text` for Objective-C | 124 / 1,248 Objective-C files (9.9%) | the `comment` strategy runs *before* the Linguist heuristics, scores each candidate by lines that *contain* its comment symbol — `%` inside `@"%@"` counts for MATLAB/Mercury — and drops Objective-C. **Without that one strategy: 3 / 1,248 (0.2%).** Appendix C gives a reproduction and three possible fixes. |
| **SWH Synid** | returns all eight candidates | 42 / 1,991 (2.1%) | **every** such text file is non-UTF-8 (36 of 36 — MATLAB with Latin-1 comments, one Objective-C), and every resolved file is UTF-8 (1,958 of 1,958): in `file` mode (and with the SquashFS content host) a strict UTF-8 read fails and content strategies are skipped. The S3 and Web API hosts decode lossily. The other 6 are binaries. |

> **Finding 3 — The archive's own identifier mislabels one Objective-C `.m`
> file in ten, for a reason that fits in one line.** Synid returns `Text` for
> 9.9% of Objective-C files because its comment heuristic counts `%` inside
> format strings; disabling that step fixes 121 of 124. The general lesson: a
> content heuristic that runs *before* a disambiguation rule can remove the
> right answer from the candidate set, and nothing downstream can bring it back.

A Dawid–Skene model — which estimates every labeller's confusion matrix with no
reference at all — ranks them the same way (judges 99.7–99.8%, ours 99.4%,
Synid 98.5–98.7% when answering, Pygments 93.2%) and agrees with the Sonnet
judge on 99.7% of files. Its independence assumption is violated (Synid embeds
the Linguist rules and the Pygments scorers), so we use it as a consistency
check, not an estimate.

![Pairwise κ](assets/m/fig_m_kappa.png)

#### 5.2 Lexical vs semantic: who decides "Octave"? (E3, H5)

The prompt defined `octave` lexically: *only* when the file uses Octave-only syntax
that MATLAB rejects. The rpgle study found the judge over-applying a lexical label
one-sidedly. Here:

| language label × Octave-only syntax present? | Sonnet 4.6 | Gemini 3.8 Flash | ours v2 |
|---|---:|---:|---:|
| `octave`, syntax present | ⟪OCT_S_TT⟫ | ⟪OCT_G_TT⟫ | ⟪OCT_O_TT⟫ |
| `octave`, **no** Octave-only syntax | ⟪OCT_S_TF⟫ | ⟪OCT_G_TF⟫ | ⟪OCT_O_TF⟫ |
| `matlab`, **with** Octave-only syntax | ⟪OCT_S_FT⟫ | ⟪OCT_G_FT⟫ | ⟪OCT_O_FT⟫ |

*(Syntax detected by comment- and string-aware markers — see below.)*

As registered, with **regex** markers, the Sonnet judge's disagreements were 7 vs
4 — not one-sided, and H5 fails. Reading the four "`matlab` with Octave syntax"
cases showed three were **our** errors: `!=` inside a string, `printf(` inside a
`%` comment, and the `1;` script idiom (valid MATLAB). With markers computed on
code only (comments and strings blanked by a small scanner), the picture is
sharp — and it splits the two models:

- **Sonnet** calls 7 files Octave that use no Octave-only syntax. Three sit in an
  Octave-Forge package tree (`inst/`, `inst/private/`) and one is named
  `fhr_open_octave.m` — it answers "which ecosystem is this from?" instead of the
  question asked. The other three it justifies by double-quoted strings, which
  have been legal MATLAB since R2017a: an outdated rule, applied confidently. One
  justification cites an `endfunction` that is not in the file. Its two
  "`matlab` with Octave syntax" cases are one genuine miss (`printf` in
  `default.m`) and one **git-annex pointer** — a symlink path stored as file
  content, the DataLad artefact of the `.fsf` study — that both it and our marker
  misread (Gemini correctly called it not code).
- **Gemini** follows the definition to the letter: every file it calls Octave
  has Octave-only syntax, and none it calls MATLAB does.

> **Finding 4 — "Lexical facts in code" needs a lexer, and "semantic facts to
> the LLM" depends on the LLM.** Our first lexical rule had a 3-in-4 false
> positive rate on the disagreements because it could not see strings and
> comments. Once fixed, one judge honoured a lexical definition exactly and the
> other overrode it with context — the rpgle failure, reproduced by one vendor
> and absent in the other.

The same split, larger, appears on a purely semantic field. Asked whether MATLAB
code is portable to Octave (`matlab_dialect`), Sonnet says **84% MATLAB-specific**;
Gemini says **63% portable**. Only 7% of those files use a lexical MATLAB-only
construct (`classdef`, `arguments`, `matlab.*` packages, GUIDE). Two models giving
opposite majority answers means the field, as defined, measures the model.

#### 5.3 Two judges, one schema (E4, H7)

⟪INTERMODEL_TABLE⟫

Identity is settled: κ 0.98 on the fine language label, 0.99 coarse. Everything
that asks for *judgement* degrades in a clear order — `provenance_kind` 0.84,
`domain` 0.73, `matlab_dialect` 0.67, `maturity` 0.54. The same order appears
when the *same* model judges the same 299 files twice (E5): language 99.3%
identical, provenance 98.0%, domain 93.0%, maturity 87.3%. `confidence` shows the
κ paradox: 99.7% agreement, κ = 0 — both models say "high" almost always, so the
field carries no information.

The provenance disagreements are mostly *boundary* cases, not contradictions:
"hand-written vs vendored" (58) and "template vs tool-generated" (39) — whether a
modified copy of AFNetworking is "vendored", whether a CocoaPods stub is a
"template" or "generated". Maturity disagreements are pervasive (36%).

> **Finding 5 — Report κ per field, and drop fields below ~0.7.** A second
> model is cheap (Gemini cost a third of Sonnet here) and turns "the judge said"
> into a measured reliability. In our schema `maturity` and `matlab_dialect`
> fail that bar and should not be aggregated without a human audit.

#### 5.4 Does showing the indicators anchor the judge? (E5, H6)

Re-judging U ranks 1–300 *with* the mechanical indicators in the prompt changed
the language label of 2 files out of 299 — one toward our reclassifier, one away
from it. Agreement with our rules was 99.0% blind and 99.0% shown. **H6 is not
supported**: on a task this lexical, the indicators add nothing the judge does not
already read in the bytes. The blind protocol costs nothing and removes the
question; we keep it. (The one flip toward our rules was `read_hist_simulator.m`,
from `octave` to `matlab` once the prompt listed its indicators — none of them
Octave-specific. The effect exists; it is just rare on this task.)

#### 5.5 Our reclassifier, scored prospectively (G)

⟪RECLASS_TABLE⟫

The frozen v1 — written before any judge label existed — agrees with the judge on
98.2% of 1,700 held-out files at the coarse level. v2, revised after reading the
seven disagreements in the 300-file tuning split, gains 0.2 points on held-out
data (100% in-sample: the usual optimism of tuning). Held-out errors are mostly
**abstentions** (`→ unknown`) on the tail; the most frequent *wrong* answer is
`octave` for files that are not MATLAB at all (two C files, a MUMPS routine, a
data file), because `printf(` and `!=` are Octave-only *relative to MATLAB* but
ordinary in C. That fix belongs in v3 and has to be scored on fresh data.

#### 5.6 Cheap labels, valid intervals (E7)

The frozen v1 reclassifier labelled every fetched content for free. PPI combines
it with the judge: the 1,000 judged files per frame estimate the reclassifier's
bias, the unjudged files add precision. Because our unlabelled pool (⟪POOL⟫) is not
much larger than the labelled set, we use the power-tuned variant (PPI++), which
weights the cheap labels by how much they help and can never do worse than
the judged sample alone.

⟪PPI_TEXT⟫

> **Finding 6 — A validated rule-based classifier doubles the judged sample for
> free.** With the unlabelled pool equal to the judged set, the tuned weight is
> λ ≈ ⟪PPI_LAMBDA⟫ — a free label is worth about half a judged one — and intervals
> narrow by ⟪PPI_GAIN⟫, the precision of roughly ⟪PPI_EFF⟫× as many judged files at
> no API cost. The gain grows with the pool; the bottleneck is now the SWH rate
> limit (1,200 requests an hour), not the budget.

#### 5.7 The mapping, stress-tested (E8)

⟪MAPPING_TABLE⟫

Our mapping gets the two big languages right and lists four more that are really
there (Octave, Wolfram, Mercury, MUMPS). It misses **Magma** (as frequent as
MUMPS), and lists **Limbo** and **MUF**, which never occurred. It also lists three
languages that have nothing to do with `.m`: **M4**, **Monkey C** and **Win32
Message File** claim it through Pygments' *Mason* lexer. The cause is in
`tools/master_inventory.py::match_pygments_name`: when a language's name matches
no Pygments lexer, it falls back to **any lexer sharing an extension** — all three
list `.mc`, Mason lists `*.mc` and `*.m`, so all three become "Mason" and inherit
`.m`.

The fallback is not a `.m` accident. Across the master inventory, **114 of 588
Pygments identities (19%) were decided by extension overlap**, not by name. Some
are harmless (`standard-ml`→SML, `visual-basic-.net`→VB.NET), many are not:
**Mercury → MOOCode** (via `.moo`), NASL / bitbake / SourcePawn → POV-Ray,
OpenCL / qmake / Proguard / Cool → Visual Prolog, JetBrains MPS → Maple,
Motoko → Modelica. The full list is in
`data/derived/m_study/mapping_pygments_ext_fallback.json`.

> **Finding 7 — Using an extension as an identity key corrupts the mapping that
> is supposed to *test* extensions.** The same shortcut this whole line of work
> warns against — trusting what a file extension claims — was built into our own
> inventory join. Match by name or alias; treat a shared extension as evidence
> for review, never as identity.

#### 5.8 Who is right when they disagree? (E9 — ready, not yet run)

Every accuracy above is agreement with a two-LLM consensus. The last step is a
human, and it is set up so that a few hours of reviewing yield population-level
numbers:

- `tools/m/audit.py --build` drew **100** files from the judged by-file frame,
  stratified: 60 of the 77 files where at least one labeller dissents (weight
  1.28 each) and 40 of the 919 where all agree (weight 22.98 each). The weights
  make the audit estimate *population* accuracy, not accuracy on hard cases.
- The review app serves the queue in **blind mode**: machine labels stay hidden
  until the reviewer has saved an answer (the human version of E5).
- `audit --score` turns the reviews into a weighted accuracy with a 95% interval
  for each of the eight labellers.

This is the step none of the three earlier studies completed (one human review
exists across them); it is the single most valuable next hour of work.
