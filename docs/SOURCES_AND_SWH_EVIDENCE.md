# Programming Languages × Software Heritage: sources, gaps, and the missing step

*A status note for the PL-ultimate / SWH / Code Commons working group.*

## 1. The landscape today

Each existing source captures a different slice of "all programming languages." None of them are anchored in actual code on the planet.

| Source | Cardinality | Captures | Limitation |
|---|---:|---|---|
| **HOPL** (`hopl.info`) | ~8,500 | historical lineage, paper-grounded | frozen ~2005, often unreachable, no code |
| **Esolang.org** | ~6,800 | esoteric / experimental / joke languages | exotic; many have ~zero real usage |
| **PLDB** | ~5,100 | curated DB with paradigms, dates, designers | mostly metadata; sparse on real-world adoption |
| **GitHub Linguist** | ~800 | "detectable" languages + extensions + ambiguity rules | scoped to what GitHub repos contain |
| **Hyperpolyglot** | ~600 | side-by-side comparison tables | English-only; no historical depth |
| **Pygments lexers** | ~600 | syntax highlighters | exists only if someone wrote a lexer |
| **Rosetta Code** | ~560 | task-by-language code examples | examples are toy snippets, not real programs |
| **Wikipedia (PL category)** | ~180 | encyclopedic prose | shallow; no extensions |
| **PL-ultimate** (this repo, `acherm/PL-ultimate`) | **11,963** | union of the seven above | 88% appear in one source only; near-duplicates remain |
| **PL-ultimate-llm** (`acherm/PL-ultimate-llm`) | ~4,000 | LLM-proposed + LLM-generated programs | hallucination risk; generated code may not exist anywhere |
| **Roberto's SWH-extensions CSV** | 40,000 | the most popular alphanumeric (1–6 char) extensions in SWH | extensions, not languages — needs mapping |
| **SWH popular-content-names parquet** (`derived_datasets/<date>/contents/*.parquet`) | billions of (content, popular-filename) rows | actual files in the archive | bytes-level; no language column |

**Two observations from this table.**

First, each source is *opinionated about what counts as a programming language*. HOPL favors historical / academic; Esolang collects oddities; Linguist is GitHub-detection-driven. Their union is large but unevenly weighted toward whichever source has the longest catalog (Esolang, PLDB).

Second, all the language-side sources sit *above* code. Roberto's CSV and the SWH parquet sit *below*: they tell you which extensions and files exist, but not which language those files are in. **There is no first-class link from a language entity to real archived programs in that language.** That link is the missing step.

## 2. Why this matters

A typical question we can't answer today:

> "Give me 10 real, non-toy programs written in Mercury, with citable provenance."

Each source falls short for a different reason:

- HOPL knows Mercury exists historically; no code attached.
- PLDB has a Mercury record; no code attached.
- Linguist says Mercury claims `.m` (shared with MATLAB, Objective-C, Limbo, MUF, M, Wolfram); no code attached.
- Rosetta Code may have one toy snippet; not representative.
- SWH has billions of `.m` files; no language column.
- A naive grep on `.m` yields mostly MATLAB and Objective-C — not Mercury.

The pieces are all there. They just don't talk to each other.

## 3. The missing step

For every language `L` in the corpus, produce one of:

- **Positive evidence**: ≥ K real archived programs that we credibly attribute to `L`, each carrying a citable qualified SWHID and a traceable reason for the attribution (which heuristic? which extension? which source?).
- **Evidence of absence**: a structured "no SWH evidence found" verdict, with reasons — e.g., the language's claimed extensions don't appear in SWH at all, or they appear only as a shared extension where heuristics resolved every observed file to a different language.

The output should let a future reader:

1. Browse programs of a language without rerunning anything.
2. Cite a specific program with a permanent identifier (qualified SWHID).
3. Inspect *why* a given file was attributed to language `L` (provenance chain back to the heuristic rule).
4. See the negative space (languages with zero archived evidence) — interesting in its own right for the HOPL/Esolang long tail.

## 4. What we prototyped this week (in this repo)

Four short scripts and four derived tables. End-to-end demo working on a 1% sample of SWH shard 0.

```
master_inventory.py                            (existed; collects entities)
        │
        ▼
build_pl_taxonomy.py  ────────────────────►  data/derived/pl_taxonomy/
                                              ├── pl.csv          (11,963 entities)
                                              ├── pl_alias.csv    (1,049)
                                              ├── ext_claim.csv   (2,818 with source+strength)
                                              ├── ext_summary.csv (1,538 per-ext summaries)
                                              └── heuristic.csv   (377 Linguist disambiguation rules)
        │
        ▼
swh_extension_mining.py  ─────────────────►  data/derived/swh_extension_samples.csv
  DuckDB over SWH parquet                     (per-row: SWHID + qualified SWHID +
  GitHub side-channel → bytes + commit         predicted_pl_id + matched_heuristic_id +
  pl_classify.Classifier → predicted PL        predicted_matches_claim)
        │
        ▼
fetch_samples.py  ─────────────────────────►  samples/<pl_id>/<sha1_git>/
                                               ├── <filename>     (the actual bytes)
                                               └── metadata.json  (full provenance chain)
```

**Key design choices, all enabled by the work this week:**

- **Provenance per claim**, not per language. `Python → .rpy` is recorded as `(source=linguist, strength=secondary)`, separately from `Ren'Py → .rpy` recorded as `(source=linguist, strength=primary)`. Downstream consumers can ask "who *primarily* owns this ext?" instead of "is this language one of N claimants?"
- **A runnable heuristics catalog.** Linguist's `heuristics.yml` (377 regex rules across 148 ambiguous extensions) is loaded once and applied to each fetched file. We can answer "this `.m` file is Mercury because rule `h/linguist/.m/1` matched `:- module`" — programmatically, not by inspection.
- **The SWHID is the citation primitive.** A bare `swh:1:cnt:<sha1_git>` is computable from the bytes alone (no SWH-side resolve). The qualified form `swh:1:cnt:<HASH>;origin=...;anchor=swh:1:rev:<COMMIT>;path=/...` is buildable from GitHub at sub-second cost, because a git commit's SHA1 *is* an SWH revision SWHID — they're literally the same hash.
- **No cnt-nodes parquet download needed.** The cnt-nodes table is ~840 GB. We avoid it entirely by computing SWHIDs from bytes and pinning provenance via GitHub's commit history.

**Demonstrated end to end on `samples/pl/perl/c5ecce.../resultset_overload.t`:**

- Mined from SWH parquet (filename `resultset_overload.t`, length 543, 1858 origin occurrences).
- `.t` extension is shared between Perl, Raku, Terra, Turing.
- Classifier ran Linguist's heuristic `h/linguist/.t/0` on the bytes → matched → predicted `pl/perl`.
- Bytes fetched from GitHub at pinned commit `9f8135f8...`; sha1_git verified byte-perfect.
- SWHID resolves on archive.softwareheritage.org with HTTP 200, matching all hashes.
- Citation-ready: `swh:1:cnt:c5ecce87...;origin=https://github.com/st3fan/osx-10.9;anchor=swh:1:rev:9f8135f8...;path=/CPANInternal-140/DBIx-Class/t/resultset_overload.t`.

This is the shape every PL entry should eventually have.

## 5. What's needed to go from prototype to encyclopedia

Roughly in increasing order of effort:

1. **Fix master_inventory's near-duplicate entities.** `Python` / `py` / `Python (programming language)` survive the union as three distinct PLs, polluting `.py`'s primary-claimants set with phantom claimants. A canonical-alias-aware merge pass is a one-day fix and would clean up phase-1 visibly.
2. **Cross-reference Roberto's 40K-extensions CSV with `ext_claim`.** Every popular SWH extension should either map to a language (via our taxonomy) or be flagged as "popular in SWH but unattributed" — those flags are interesting (e.g., are they binary formats? text data? a language we missed?).
3. **Run the mining at full scale.** Local sequential scan is ~10 hours on a laptop (~3 GB × 30 shards). Trivially parallelizable per-shard; on an EC2 box near the SWH bucket, this is well under an hour.
4. **Wire SWHID resolution properly.** For provenance citations we currently use the GitHub side-channel (one origin per file), which has rate limits and depends on a repo still being public. SWH's `first_occurrence_origin` numeric id resolves to a canonical archive-internal origin via the ori-nodes parquet (much smaller than cnt-nodes). That's the real authoritative provenance and should be the fallback when the GitHub side-channel can't pin a commit.
5. **Generate per-PL "evidence cards."** For each `pl_id`, a small static page or JSON:
   - Claimed extensions and their `(source, strength)` evidence
   - Sample programs (qualified SWHIDs, byte sha1, occurrence counts)
   - Heuristic rules that fired (if any)
   - The evidence-of-absence verdict if no samples found
   - Links to HOPL graph node and other authoritative entries
6. **Decide what "evidence of absence" means.** Three flavors worth distinguishing:
   - **No extension claimed**: language has no extension in any source (typical of Esolang entries that are interpreters of natural-language games). No file can be mined.
   - **Extension claimed but absent in SWH**: the parquet has zero files with that name pattern. Genuinely absent, or just unindexed.
   - **Extension claimed, files exist, but every classifier verdict went elsewhere**: the language is overshadowed by a shared-extension competitor (e.g., a language claiming `.m` whose heuristic never fires because MATLAB/Objective-C grab all real `.m` files).
7. **Bring HOPL in.** HOPL's strength is genealogy (which language influenced which), which our master_inventory lacks. A merge would let us answer "show me programs from descendants of ALGOL 60." Requires reviving / re-scraping HOPL since it's been frozen since 2005.
8. **LLM-augmented disambiguation for the long tail.** For the ~70 extensions with multiple primary claimants and no Linguist heuristic, an LLM can write a content-based classifier from a handful of training examples. Cheaper than authoring rules by hand and may close the gap for niche languages.

## 6. Open design questions worth a meeting

- **Identity at the language level.** When PLDB says "Python" and Linguist says "Python (programming language)," are these the same entity? Currently no. A canonical PL-id authority is needed (we suggest the form `pl/<slug>` with explicit alias mapping; see `pl_alias.csv`). This is the same identity problem that ORCID solves for people.
- **Authority of the heuristic.** Linguist's `heuristics.yml` is permissively licensed and well-maintained, but it embeds GitHub's worldview (mainstream extensions only). For Esolang's long tail we'd need either authored rules or learned classifiers, with provenance preserved.
- **Citation policy.** Do we cite the bare SWHID (content only) or the qualified one (with origin/anchor)? The qualified form is more useful for readers but binds to a possibly-mortal repo. Recommend: store both, present the qualified, fall back to bare if the origin dies.
- **Generated vs. archived code.** PL-ultimate-llm produces LLM-generated programs per language. Should those be merged with SWH-archived samples? They serve different purposes (existence vs. usage). Probably both, in separate buckets.
- **Negative space as a first-class artifact.** "Languages with no SWH evidence" is publication-grade in its own right — likely correlates strongly with Esolang's long tail and HOPL's pre-1980s entries. Worth reporting.

## 7. Quick reproduction

Everything below runs from the repository root. The SWH mining step is the only one that needs network and the only one that touches large data.

```bash
# 1. Build the taxonomy + heuristics catalog (offline, seconds)
python3 tools/build_pl_taxonomy.py

# 2. Smoke-test the classifier on a known-ambiguous file
python3 tools/pl_classify.py -v path/to/some_file.m

# 3. Mine SWH (defaults to dry-run; prints SQL only)
python3 tools/swh_extension_mining.py

# 4. Smoke-test mining on a 1% sample of one shard (~30s)
python3 tools/swh_extension_mining.py \
    --only "Perl,Prolog,Lua,OCaml" \
    --shard 's3://softwareheritage/derived_datasets/2026-03-02/contents/0.parquet' \
    --top-k 1 --sample-percent 1 --skip-resolve --execute

# 5. Materialize sample programs to disk
python3 tools/fetch_samples.py
ls samples/pl/perl/c5ecce*/      # actual bytes + metadata.json
```

## 8. Status of this prototype

| Piece | State |
|---|---|
| Taxonomy with provenance per claim | ✅ done (this week) |
| Linguist heuristics catalog as runnable predicates | ✅ done |
| Content-based classifier | ✅ done |
| SWH parquet mining (DuckDB query, IN-set shape, sample mode) | ✅ done |
| Qualified SWHID per row via GitHub side-channel | ✅ done |
| Sample bytes on disk with metadata.json | ✅ done |
| Full-scale mining (all 30 shards) | not yet run; ~10 h on laptop, ~1 h on EC2 |
| ori-nodes resolution for SWH-canonical origin | not implemented |
| Per-PL evidence cards / static index | not implemented |
| Evidence-of-absence categorization | scaffold exists, no formal output yet |
| HOPL graph integration | not started |
| Cross-reference with Roberto's 40K-ext CSV | not started |
| LLM-assisted heuristics for long tail | not started |
