## Part II — The `.m` study

### 1. Who claims `.m`? (a two-minute primer)

Every earlier study had one expected answer. `.m` has many, and our own
extension→language mapping (`data/derived/pl_taxonomy/ext_claim.csv`) already
lists eight:

| Claimant | What a `.m` file is in that world | Claimed by |
|---|---|---|
| **MATLAB** | a function file, a script, or a `classdef` class | Linguist, Pygments, Wikidata |
| **GNU Octave** | the same, plus Octave-only syntax (`#` comments, `endfunction`, `printf`, `++`, `!=`) | Pygments, Wikidata |
| **Objective-C** | a class implementation (`@implementation`), `main.m`, a test case | Linguist, Pygments, Wikidata |
| **Wolfram Language** | a Mathematica *package* (`BeginPackage[…]`, `(* ::Package:: *)`) | Linguist, Wikidata |
| **Mercury** | a module (`:- module …`) | Linguist, Wikidata |
| **M (MUMPS)** | a routine (GT.M / YottaDB store one routine per `.m`) | Linguist |
| **Limbo** | an Inferno module *interface* (`Sys: module { … }`) | Linguist |
| **MUF** | a TinyMUCK Forth program | Linguist |
| *M4, Monkey C, Win32 Message File* | none — they inherit `.m` from Pygments' **Mason** lexer through a join bug (§5.7) | Pygments (spurious) |

Reading contents added four notations no source claims: **Magma** (computer
algebra), the **FreeBSD kobj interface definition** language (`*_if.m`), the
**New Jersey Machine-Code Toolkit** specification language, and **PML** — the
XML morphological layer of the Prague Dependency Treebank. There is also plain
C, Markdown and CSV that happen to sit in `.m` files.

So the question is not "is it X?" but **"which of a dozen things is it, how
often, and can anything short of a language model tell them apart?"**

### 2. Data

#### 2.1 The population, and an audit of the population file

The maintainer's export (`SWH-m-files.zip`) is six headerless CSV shards, 14 GB,
produced by the Rust **`swh-provenance`** tool on the CINES supercomputer: one row
per content, `swh:1:cnt:<sha1_git>,<SWH browse URL>`, where the URL carries
`origin_url`, `branch`, `path` and a `timestamp`. It is too large for the
`csv`-module approach of the earlier studies, so `tools/m/ingest.py` loads it with
DuckDB into a 2.8 GB Parquet table in about 20 seconds.

Before sampling we audited the file itself (weakness W6):

| Property | Value |
|---|---|
| Physical lines / records starting `swh:1:cnt:` / records parsed | 51,414,839 / **51,414,668** / 51,414,668 (none lost) |
| Distinct contents | **51,414,668** — each listed exactly once, with a single provenance context |
| `no_origin` rows (`… has no predecessors in this graph`) | 58,549 (0.11%) — kept, excluded from by-repo frames |
| Records split by a newline inside the file name | 100 — first line kept (sha, origin, branch, path prefix intact) |
| Non-data trailer | a CINES job report at the end of each shard — dropped |
| Contents with an origin / **distinct origins** | 51,356,119 / **2,076,824** |
| Distinct `(origin, path)` files | 27,678,487 → **46.1% of contents are later versions of the same file** |
| Contents per repo — median / mean / max | 4 / 24.7 / 429,552 |
| Largest repo / top 10 / top 100 | 0.84% / 3.1% / 6.2% of contents |
| Top 1% / top 10% of repos | 41% / 76% of contents — 265,470 repos (12.8%) cover 80% |
| Provenance context whose name does **not** end in `.m` | 169,231 (0.33%): `.svn-base` 99,782, MATLAB autosave `.asv` 28,939, `.m~`, `.txt`, `.md`, `.c`, `.h`, even `.py` |

Three properties of this file matter for everything that follows.

- **The context path is *a* path, not *the* `.m` path.** A content was selected
  because *some* directory entry names it `*.m`; the provenance tool then reports
  *one* place it occurs — which, for 0.33% of contents, is a Subversion pristine
  copy, an editor backup, or a file of another type holding the same bytes. One of
  our sampled contents is reported as `test.lua`: 21 bytes that are equally valid
  Lua and MATLAB.
- **The timestamp is a visit date.** Years run 2015–2025 — SWH's own lifetime — so
  they date the archive's crawl, not the code.
- **Only lowercase `.m` was extracted.** Uppercase `.M` (26 k occurrences in the
  SWH-MSR-ARV counts) is absent; the 1,263 `.M` paths above are contexts of bytes
  that also exist as `.m`. The COBOL lesson — *case matters* — applies here as a
  coverage gap to close in a later extraction.

![Concentration](assets/m/fig_m_concentration.png)

`.m` is not dominated by any single repository — unlike `.CBL` (one fixture held
40%) or `.rpgle` (three parser repos held 21%) — yet it is top-heavy in
aggregate: 1% of repositories hold 41% of the contents. The largest are named in
§4.4, and they are not what a reader expects.

#### 2.2 Duplication signals, measured on the whole population

Because the population is a table, some questions can be answered exactly, for
free, before any file is read (`tools/m/name_pop.py`):

| Family (by file name) | contents | % of contents | repos | % of repos |
|---|---:|---:|---:|---:|
| Xcode template names (`AppDelegate.m`, `main.m`, `ViewController.m`, `SceneDelegate.m`) | 3,243,345 | 6.3% | 880,802 | **42.4%** |
| CocoaPods stubs (`*-dummy.m`) | 493,666 | 1.0% | 241,904 | 11.6% |
| Coursera *Machine Learning* exercises (repos with ≥ 5 exercise names) | 449,136 | 0.9% | 20,942 | 1.0% |
| Flutter plugin registrant (`GeneratedPluginRegistrant.m`) | 19,710 | 0.04% | 13,334 | 0.6% |

![Most replicated file names](assets/m/fig_m_names.png)

`AppDelegate.m` exists in 689,794 repositories — a third of every repository that
contains a `.m` file — as **1,341,866 distinct contents**; `main.m` as 1.0 M and
`ViewController.m` as 0.86 M. Software Heritage deduplicates byte-identical files,
but Xcode stamps each new project's template with a header comment carrying the
project name, author and date. Stripping `//` comment lines from the `main.m`
files in our sample collapses ⟪ND_MAIN_N⟫ distinct contents to ⟪ND_MAIN_K⟫, and **⟪ND_MAIN_C⟫ of them
become one and the same file** — the untouched Xcode template. (`AppDelegate.m` is
edited more often: its largest cluster is ⟪ND_APP_C⟫ of ⟪ND_APP_N⟫.) **Content-level
deduplication does not remove boilerplate that is personalised at creation**; any
count of "`.m` files" carries millions of near-identical templates.

#### 2.3 Sampling frames

| Frame | Definition | fetched | judged |
|---|---|---:|---:|
| **U · by file** | uniform over all 51,414,668 contents; md5 rank | ⟪U_FETCHED⟫ | 1,000 (ranks 1–1,000) |
| **R · by repo** | uniform over the 2,076,824 origins, then one content uniformly within it | ⟪R_FETCHED⟫ | 1,000 (ranks 1–1,000) |
| U″ · by path | U re-weighted by 1 / (versions of its `(origin, path)`) | — | derived, $0 |
| U′ · by repo | U re-weighted by 1 / (contents in its origin) — a cross-check on R | — | derived, $0 |
| **T · heavy tail** | 4 random contents from each of the 25 largest repositories | 100 | 100 |

Every rank prefix of U and R is itself a simple random sample (weakness W5), so
the rate-limited fetch — the token quota turned out to be 1,200 requests an hour —
could stop anywhere without biasing a frame. The weights for U″ and U′ are
**computed exactly from the population table**, not estimated.
