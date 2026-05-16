# Phase 2 — overnight session notes

Status note left for the morning. Read alongside `docs/SOURCES_AND_SWH_EVIDENCE.md`.

## What landed

The static-site generator (`web/build_site.py`) was extended to integrate the cross-source taxonomy + Linguist heuristics catalog + SWH samples into the existing LLM-curated catalog. **No existing functionality was changed — the site grew from ~3,800 LLM-curated PL pages to ~13,755 pages with much richer per-page content.**

### Numbers (before → after this session)

| Metric | Before | After |
|---:|---:|---:|
| PL pages on site | 821 (stale build) / 3,839 (fresh) | **13,755** |
| Per-extension pages | 0 | **1,538** |
| Per-source pages | 0 | **8** (LLM + 7 upstream sources) |
| Pages with cross-source attribution | 0 | **2,271** in-repo + 9,916 taxonomy-only |
| Total HTML files | ~3,840 | **15,304** |
| Site size on disk | ~50 MB | **164 MB** |

### New pages on every PL

Every PL page now carries up to four new sections in addition to the existing LLM-program block:

1. **Sources mentioning this language** — pills showing which of LLM/PLDB/Linguist/Pygments/Wikipedia/Esolang/Hyperpolyglot/Rosetta Code each attest the existence of this PL. Pills are clickable and lead to per-source listings.
2. **Extensions claimed** — table of `(ext, source, strength)` rows. Each `ext` links to its per-extension page. Strength is `primary` / `secondary` / `unknown` based on what the upstream source recorded.
3. **Real programs from Software Heritage** — embedded code preview, full provenance (qualified SWHID, GitHub raw at pinned commit, SWH browser link), and the heuristic rule that classified the bytes. If nothing has been mined for this PL, an explicit "No SWH evidence indexed yet" message replaces the section.
4. **Disambiguation rules** — Linguist heuristic predicates that predict this PL when the ext is shared with another. Each row links into the per-ext page.

### New top-level views

| URL | What it shows |
|---|---|
| `/browse/` | unchanged, but now with filters: `with SWH sample`, `has LLM program`, `taxonomy-only`, `min sources` |
| `/ext/` | catalog of 1,538 extensions; click into any for claimants + heuristics + samples |
| `/ext/<slug>/` | one page per extension. E.g. `/ext/m/` shows the 7 PLs that claim `.m`, the 7 Linguist disambiguation rules, and any mined `.m` samples |
| `/source/` | one page per source listing every PL it attests. Useful for "show me what's only in Esolang" |
| `/samples/` | curated index of every PL that has at least one real archived program from Software Heritage |
| `/stats/` | unchanged + new bottom section "Taxonomy & SWH evidence" with per-source contribution, source-consensus distribution, extension claims by (source, strength), polysemy distribution |

### Phase 2a–2d implementation timeline (this session)

| Phase | Outcome | Time |
|---|---|---|
| 2a — alias-aware PL matching | normalize handles `Prolog++` → `pl/prologpp`, `C#` → `pl/csharp`, roman numerals, parentheticals. 2,084 → 2,271 enriched (+187). | ~15 min |
| 2c — taxonomy-only PL pages | synthesized 9,916 `Language` instances for entities in pl.csv lacking a `languages/<L>/` dir. Visual "Taxonomy-only · no LLM program" pill to distinguish them. | ~30 min |
| 2b — per-extension pages | new `render_per_extension_pages()` writes `/ext/<slug>/` with claimants, heuristics, samples. URL slug helper handles `.++`, `.#`, `.*`. | ~45 min |
| 2d — stats additions | `compute_taxonomy_stats()` + new "Taxonomy & SWH evidence" h1 section on `/stats/` with five new tables. | ~20 min |
| polish — nav, source pages, samples index, dedup, home stats, browse filters | new `/source/<src>/` pages, new `/samples/` curated index, deduped by pl_id, home page now surfaces "PLs with SWH samples" and "SWH samples" headline stats, browse page has four filter checkboxes. | ~40 min |

### Files changed

| File | Lines added | Why |
|---|---:|---|
| `web/build_site.py` | ~+800 | dataclasses, loaders, taxonomy enrichment, synthesizer, per-ext page renderer, per-source page renderer, samples index page, stats additions, home/browse/nav updates |
| `web/assets/style.css` | ~+25 | source pill colors, strength badges, kv-table, anchor pill, taxonomy-only italic pill |
| `web/assets/app.js` | ~+20 | browse filters (has_swh, has_llm, taxonomy_only, min_sources) |
| `docs/PHASE2_OVERNIGHT.md` | new | this note |

### Mining run — DONE

The background mining job (`--shard 0.parquet --top-k 2 --sample-percent 1`) ran to completion overnight. Final tally:

- **1,057 unique (filename, length) candidates** explored
- **224 successfully qualified** (≈21 % hit rate against GitHub's 9-req/min code-search ceiling)
- **248 SWH sample blobs** materialized on disk (some samples cover multiple PL claimants for ambiguous extensions)
- **176 distinct PLs** now have at least one SWH sample on their page (deduped by pl_id)

Two follow-up improvements were applied after fetch:

1. **`tools/pl_classify.py` consolidates near-duplicate pl_ids** like `pl/zig` and `pl/zig-programming-language` that master_inventory currently keeps separate. Without this, the "unique-primary" fast path bailed for many extensions and samples landed in `samples/unclassified/`.
2. **`load_swh_samples()` fans out polysemy samples** across all primary claimants of the extension. So an ambiguous `.pas` sample shows on both `/l/pascal/` and `/l/delphi/`, an ambiguous `.bas` on B4X / FreeBASIC / QuickBASIC / VBA / VB.NET / etc. Real claim ambiguity is preserved as evidence, not hidden as "unclassified".
3. **`tools/reclassify_samples.py`** is a one-shot helper that re-runs the (improved) classifier over existing sample directories and relocates them. Useful if pl_classify is changed again later — no re-mining needed.

### Numbers, final-final

| Metric | Before | After |
|---:|---:|---:|
| PL pages on site | 821 (stale) / 3,839 (fresh) | **13,755** |
| Per-extension pages | 0 | **1,538** |
| Per-source pages | 0 | **8** |
| Pages with cross-source attribution | 0 | **2,272** in-repo + 9,916 taxonomy-only |
| **PLs with SWH samples** | 0 | **176** |
| **SWH sample blobs** | 0 | **248** |
| Total HTML files | ~3,840 | **15,304** |
| Site size on disk | ~50 MB | **166 MB** |

### Pages worth opening first

```
http://localhost:9123/                            home (new headline stats)
http://localhost:9123/samples/                    176 PLs with real SWH evidence
http://localhost:9123/l/pascal-<hash>/            6 samples — biggest single PL
http://localhost:9123/l/perl-eca37636/            classic disambiguation demo
http://localhost:9123/ext/m/                      .m polysemy resolved by Linguist heuristics
http://localhost:9123/ext/bas/                    5-language BASIC polysemy
http://localhost:9123/source/esolang/             6,755 long-tail PLs from Esolang
http://localhost:9123/stats/                      "Taxonomy & SWH evidence" section
http://localhost:9123/browse/?fltHasSwh=1         (or check the filter) – 176-PL list
```

## Known issues / things to look at

1. **Master_inventory duplicates** — `Python` / `py` / `Python (programming language)` are still three separate pl_ids. Surface effect: `.py` shows 6 "primary claimants" instead of 1. Fix lives in `tools/master_inventory.py`, not in this session's work. A canonical-alias merge pass is the proper fix.
2. **1,568 in-repo PLs unmatched** — agent-added esolangs absent from PLDB/Linguist/Pygments/Wikipedia/Esolang/Hyperpolyglot/Rosetta Code. These pages now show "Sources mentioning this language: LLM (this repo)" and note `not in taxonomy`. They're still browsable and have LLM programs; just no cross-source attribution.
3. **Site footer date label** says `data` was generated at build time, not mining time. Probably wants disambiguation in a later pass.
4. **SWH ori-nodes parquet not yet integrated** — qualified SWHIDs use GitHub as the side-channel for origin/anchor. Fine for browse, but if a GitHub repo gets deleted/private the citation would point to a dead origin. Resolving via SWH's ori-nodes would give an archive-canonical origin. ~9 GB download, deferable.

## Quick-start (for waking up)

```bash
# Preview the new site:
python3 -m http.server --directory web/dist 9123
open http://localhost:9123/

# Recommended pages to verify:
#   /                                  (home, new headline stats)
#   /l/perl-eca37636/                  (rich PL page: 8 sources, ext claims, SWH sample, heuristic)
#   /samples/                          (curated SWH evidence index)
#   /ext/m/                            (the .m polysemy case)
#   /ext/                              (extensions catalog, 1,538 entries)
#   /source/                           (per-source PL lists)
#   /stats/                            (new "Taxonomy & SWH evidence" section at the bottom)
#   /browse/?letter=P                  (filters now include has-SWH-sample, etc.)
```

Nothing has been committed. All output is in `web/dist/`; the live `docs/` is untouched.
