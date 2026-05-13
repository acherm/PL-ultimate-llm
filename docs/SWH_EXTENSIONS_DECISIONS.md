# Roberto's SWH-extensions CSV — what we kept, what we cut, and why

Decision log for how the `nb_extensions_alphanum.csv` dataset feeds into the
catalog. Written so that any future maintainer (or any of us, on a different
day) can see *exactly* what got dropped, on what threshold, and what to flip if
the call should be revisited.

## 1. The input

**File:** `/Users/mathieuacher/SANDBOX/PL-roberto/nb_extensions_alphanum.csv`

- Source: Roberto Di Cosmo, extracted from the Software Heritage archive.
- Filter applied at source: file extensions are **alphanumeric, 1–6 characters
  long** (after the leading `.`). Unicode-only extensions are excluded by
  construction; a few literal Unicode rows do leak in (the file's tail shows
  `.𝚁`, `.𝚓𝚜𝚘𝚗`, etc.) but they have negligible counts.
- Shape: **2,960,281 rows** × **76 columns** (459 MB CSV).
  - Column `extension` — the extension string (e.g. `.py`, `.fzf`, `.0`, `.html`).
  - Column `-1` — occurrences with no date / unknown commit date.
  - Columns `1950` … `2023` — occurrence counts per year.
- Aggregate file-content occurrences summed across all years: **~18.97 billion**.

> The "40,000 most popular" mentioned in Roberto's email is **not** the file's
> row count; it appears to be shorthand for the popular subset. Roberto's CSV
> contains the full distribution down to single occurrences.

## 2. The distribution

Once we sum occurrences per extension across all years, the long-tail shape is:

| Threshold (total occurrences) | # extensions | What sits at this cut |
|---|---:|---|
| ≥ 1 B (one billion) | 2 | `.html`, `.json` |
| ≥ 100 M | 26 | the giants (`.py`, `.js`, `.java`, …) |
| ≥ 10 M | 105 | clearly-popular file types |
| ≥ 1 M | 482 | well-used in real projects |
| ≥ 100 K | 1,730 | confidently widely-used |
| ≥ 10 K | 6,050 | likely real PL or domain ext |
| ≥ 1 K | 18,119 | **best fit for Roberto's "40K" intent** |
| ≥ 100 | 59,513 | "Roberto's 40K" upper bound |
| ≥ 10 | 206,230 | mostly project-specific / typos |
| ≥ 1 | 2,960,280 | full long tail |

(Reproduce with: `python3 tools/swh_extension_distribution_stats.py` — TODO,
or the inline snippet in `docs/PHASE2_OVERNIGHT.md`.)

## 3. What we derive

A single per-extension aggregate, written to:

```
data/derived/swh_extensions_popularity.csv
```

Columns:

| Column | Meaning |
|---|---|
| `extension` | the ext string (e.g. `.py`) |
| `total_occ` | sum of occurrences across all years + `-1` |
| `recent_occ` | sum across years 2019–2023 (proxy for "still alive") |
| `undated_occ` | the `-1` column (commits SWH couldn't date) |
| `first_year` | earliest year with a positive count (or empty) |
| `last_year` | latest year with a positive count (or empty) |

**This file keeps every one of the 2,960,281 rows** — no threshold is applied at
the derivation step. The rationale is that anyone doing rigorous analysis (e.g.
"is there an SWH presence for `.fsf`?") needs to query the full distribution,
not a website-sized subset. The 459 MB original is preserved at Roberto's path;
our 77 MB derivative is the convenient form for downstream tools.

## 4. The website's threshold

The static site generator (`web/build_site.py`) renders one HTML page per
extension. We cap the universe of generated pages to keep the site browsable.

**Current decision:** generate per-ext pages for the **union** of:

1. Every extension claimed by some PL in our taxonomy (1,538 entries from
   Linguist / Pygments / master_inventory).
2. Every extension that has at least one Linguist disambiguation rule.
3. Every extension that has at least one mined SWH sample.
4. **The top 8,000 extensions by `total_occ` from Roberto's CSV.**

Total today: **8,344 pages.**

The 8,000 cap sits between the "≥10K" (6,050) and "≥1K" (18,119) thresholds.
Below ~7K occurrences, extensions are almost always one of:

- Single-project filenames (`.tmpconfig123`, `.mybackup`)
- Typos of common extensions (`.htmll`, `.cpy`)
- Build/cache artifacts unique to a tool (`.somecache`)
- Truly esoteric languages — but indistinguishable from noise at this scale

**This is a pragmatic web-readability choice, not a data-curation claim.** The
underlying CSV still has every row.

## 5. What's NOT on the site (but is in the derived CSV)

Concrete examples of the ~2.95 M extensions we *don't* render per-ext pages for:

- `.tmpconfig123` — only this one repo
- `.gitignore_bak` — backup-of-config style
- `.fsf` — fewer than 8 K occurrences but **a known neuroimaging language** —
  this is the kind of case the threshold cuts that we'd be sad about.
- Any of the 200K+ single-digit-occurrence extensions

**If we ever do a rigorous "PL coverage in SWH" analysis, we should query
`swh_extensions_popularity.csv` directly, not the website's per-ext pages.**

## 6. Heuristics applied to *interpret* extensions

Even within the 8,344 rendered pages, we apply heuristics:

- **Blocklist of clearly non-PL extensions** (`.png`, `.jpg`, `.dll`, `.json`,
  `.xml`, `.lock`, …) — these still get per-ext pages because they're popular,
  but they're not expected to have PL claimants. Defined in `EXT_BLOCKLIST` in
  `tools/swh_extension_mining.py`.
- **"Unattributed" flag** on the `/ext/` index — surfaces extensions with
  significant SWH presence but no taxonomy claimant. These are candidates for
  catalog expansion (the genuine ones) or for the blocklist (the noise).
- **Per-PL "SWH" column** on the extension-claims table — surfaces real-world
  usage of each claimed extension. A PL whose only claimed extension has
  ≤ 100 occurrences is probably not really used.

## 7. Limitations & things to revisit

| Concern | What's true today | When to revisit |
|---|---|---|
| 1–6 char alphanumeric filter at source | Roberto's pre-filter; Unicode and special-char extensions are missing | If we find evidence of significant non-alphanumeric PL extensions (e.g., `.f95+`) |
| "Recent" = 2019 onwards | Arbitrary 5-year window | If we want a different liveness signal |
| `-1` column lumped into total | Undated occurrences count the same as dated ones | Could weight them differently |
| Single shard (shard 0) was used for **mining sample programs**; Roberto's CSV covers the whole archive | The 2.96 M-row aggregate IS for the full SWH archive; only our `samples/` mining is shard-0-only | If we run the SWH mining at full archive scale |
| Top-8K page limit | Tunable; see § 4 | If we want to surface the "≥1K" set (~19.5K pages) |

## 8. How to change the threshold

Single constant in `web/build_site.py`:

```python
SWH_POPULARITY_PAGE_LIMIT = 8000   # ← change to 18000, 50000, or even -1 (no cap)
```

Then `python3 web/build_site.py`. No data is regenerated; only the page set
grows or shrinks.

## 9. How to challenge a specific exclusion

```bash
# Did our website include .fzf?
grep -i ',\\.fzf,\\|^.fzf,' data/derived/swh_extensions_popularity.csv

# What's its rank by total_occ?
sort -t, -k2 -rn data/derived/swh_extensions_popularity.csv | grep -n '^.fzf,' | head -1

# Force-include by lowering the cap, or by adding it explicitly to the
# `all_exts` set in render_per_extension_pages().
```

## 10. The PL ↔ extension asymmetry

A common assumption is that "PL pages" and "extension pages" should roughly
balance. They don't, by a wide margin, and the imbalance is informative.

### Headline cardinalities

| Side | Count |
|---|---:|
| PL pages on the site | **13,755** |
| Taxonomy entities (`pl.csv`) | 11,963 |
| PLs with **at least one** claimed extension | **935** (7.8 %) |
| PLs with **no** claimed extension | **11,028** (92.2 %) |
| Extension pages on the site (top-8K cut) | 8,344 |
| Extensions in our taxonomy (`ext_summary.csv`) | 1,538 |
| Extensions in Roberto's CSV (alphanumeric 1–6 char) | 2,960,280 |
| Extensions in **both** taxonomy & Roberto's CSV | 1,491 |

### Per-PL: how many extensions does each PL claim?

| # extensions claimed | PLs |
|---:|---:|
| **0** (un-locatable by filename) | **11,028** |
| 1 | 552 |
| 2–3 | 249 |
| 4–10 | 104 |
| 11+ | 30 (Python, Ruby, Pascal-ecosystem, …) |

### Per-extension: how many PLs claim each?

| # PL claimants | Extensions |
|---:|---:|
| 1 (unambiguous) | 1,137 (74 %) |
| 2 | 263 |
| 3–5 | 102 |
| 6+ (`.m`, `.h`, `.pl`, `.t`, …) | 36 |

### Why so many PLs have no extension

Of the 11,028 PLs with zero claimed extensions:

- The vast majority are Esolang entries — joke languages, conceptual languages,
  single-author experiments. Esolang catalogs the *idea* of a language but
  rarely a file type.
- Wikipedia-only entries (e.g., historical languages from the 1950s that never
  produced surviving code).
- PLDB entries for languages whose upstream sources didn't record extensions.

Implication: **a PL having a page in the catalog does not imply that it can be
located in the SWH archive**. About 92 % of catalogued PLs are findable only by
name, not by extension. This is *expected* — the catalog is a cross-source
union, and Esolang's long tail is intentionally generous about what counts as a
"language."

### Where the unattributed extensions land (by popularity tier)

Among the SWH-popular extensions (Roberto's CSV), how many have **no PL claim**
in our taxonomy? Bucketing by total occurrence count:

| Tier | Claimed (in taxonomy) | Unattributed | Of which look like binary/noise | Of which might be PL-ish |
|---:|---:|---:|---:|---:|
| ≥ 100M | 21 | 5 | 5 | 0 |
| ≥ 10M  | 44 | 35 | 19 | **16** |
| ≥ 1M   | 189 | 188 | 24 | **164** |
| ≥ 100K | 338 | 910 | 17 | **893** |
| ≥ 10K  | 509 | 3,811 | 23 | **3,788** |
| ≥ 1K   | 251 | 11,818 | 18 | **11,800** |
| ≥ 100  | (cum.) 1,352 | (cum.) 16,767 | ~100 | ~16,600 |

(Cumulative figures: the ~1,352 claimed extensions sum to most of the
taxonomy's intersection with SWH. The ~16,800 unattributed extensions are
candidates to either (a) add to the catalog as new PLs, (b) classify as
domain-specific data formats, or (c) add to the blocklist.)

### A few notable "unattributed but probably interesting" cases

From the ≥ 10M tier with no PL claim today:

| Extension | SWH occurrences | What it likely is |
|---|---:|---|
| `.R` | 21,469,901 | **R language (capital-R variant) — our matching is case-sensitive and missed this** |
| `.map` | 87,757,804 | source maps (data) — not a PL |
| `.pbf` | 53,718,721 | Protocol Buffers binary — not a PL |
| `.info` | 46,441,693 | GNU Info docs — borderline |
| `.flat` | 39,313,382 | build artefact |
| `.uasset` | 24,753,440 | Unreal Engine assets — not a PL |
| `.npy` | 22,649,386 | NumPy binary — data |
| `.pdb` | 21,791,259 | Python pdb / Protein DataBank / debug — ambiguous |

So at the very top of the unattributed list, exactly one is a real PL we miss
(`.R`). The rest are correctly excluded — but **the ≥ 1M and ≥ 100K tiers
likely contain a meaningful number of small / domain / regional PLs** (the
neuroimaging `.fsf` case is an example we identified earlier).

### The in-repo gap (worth knowing)

A separate sub-bias: of the 3,839 in-repo (LLM-curated) PLs, **only 678 have an
extension claim in the taxonomy**. The other 3,161 *do* have actual program
files at `languages/<L>/programs/<sha>/code.<ext>` — the file extensions are
*de facto* primary for those PLs but were never harvested into `ext_claim.csv`.
Closing this gap (treating in-repo program extensions as `source=repo`,
`strength=primary`) would lift the "PLs with at least one ext" figure from 935
toward ~3,500.

### What this means for queries

- **"Languages using `.X`"**: well-defined and uses `ext_claim.csv`.
- **"Extensions used by language L"**: same, reverse direction.
- **"How is language L locatable in SWH?"**: ambiguous if L has no ext claim
  (must rely on alternative methods — content classifiers, repo metadata).
- **"How many of catalogued PLs are findable in SWH?"**: at most ~935 today
  (8 %), bounded by ext claims. Closes toward ~3,500 if we harvest in-repo
  extensions, ~5,000 if we expand the taxonomy with high-occurrence unattributed
  extensions (per the table above) plus a content-classification pass.

## 11. Provenance contract for ext ↔ PL mappings

This is the rule we apply, and propose to keep applying, when *anything* asserts
a `(PL, extension)` edge in the catalog. The schema lives in
`data/derived/pl_taxonomy/ext_claim.csv`, with these columns:

| Column | Required | Meaning |
|---|---|---|
| `pl_id` | yes | the PL the claim is about |
| `ext` | yes | the extension (lowercased, leading `.`) |
| `source` | yes | named upstream (e.g., `linguist`, `pygments`) **or** a documented heuristic id (e.g., `heuristic:repo_program_ext`, `heuristic:swh_popular_unattributed`) |
| `strength` | yes | one of `primary` / `secondary` / `unknown` / `proposed` / `disputed` |
| `source_key` | optional | the upstream's own key (e.g., Linguist's language name, Pygments lexer class) — pins to the source's namespace |
| `evidence` | required | a URL or path that anyone can read to verify the claim |

### Strength values

| Value | When to use |
|---|---|
| `primary` | source explicitly marks this as the canonical extension (Linguist `extensions[0]`, Pygments first `filenames` glob). |
| `secondary` | source lists the extension but not as primary (Linguist `extensions[1:]`). |
| `unknown` | source provides the extension in a flat list with no primary distinction (PLDB-style). |
| `proposed` | derived by a heuristic; needs review before being treated as canonical. |
| `disputed` | conflicting upstream evidence (e.g., one source says yes, another absent). |

### Acceptable provenance for a *new* mapping

A new mapping can be added only if it falls into one of these categories:

1. **Cross-source corroboration (no heuristic needed).** Two or more upstream
   sources independently list `(PL, ext)`. Each contributes a row in
   `ext_claim.csv` with its own `source` and `evidence`. No new tooling needed.

2. **Single-source assertion, well-documented.** One source (Linguist /
   Pygments / PLDB / etc.) lists the mapping. One row, `source=<name>`,
   `evidence=<URL of the source's data file or specification>`, `strength` per
   the source's own primary/secondary distinction (or `unknown`).

3. **In-repo evidence.** A PL has at least one program file at
   `languages/<L>/programs/<sha>/code.<ext>`. This is *de facto* evidence that
   the PL uses that extension. Add a row with
   `source="repo"`,
   `evidence="languages/<L>/programs/<sha>/manifest.json"`,
   `strength="primary"` if it's the language's only / most-common extension in
   the repo, else `secondary`.

4. **Documented heuristic, written down.** A rule that derives the mapping
   from observable signals (file content, popularity, naming pattern). Each
   heuristic gets:
   - A stable id (`heuristic:<short-name>`)
   - A short Markdown file in `docs/heuristics/<id>.md` describing the rule, its
     inputs, its expected precision/recall, and its known failure modes.
   - Output rows with `source="heuristic:<id>"`,
     `evidence="docs/heuristics/<id>.md"`,
     `strength="proposed"` by default (downstream consumers can promote to
     `primary` after human review).

### What is NOT acceptable

- Inferring a mapping from a single high-occurrence number alone, without a
  named heuristic file describing what was inferred and why.
- Silently adding entries to `ext_claim.csv` without an `evidence` URL or path.
- Merging two `pl_id`s into one without recording the alias in `pl_alias.csv`
  with `source` explaining the merge rule.

### Reproducibility check

Anyone (or any agent) reviewing a mapping should be able to:

1. Run `python3 tools/build_pl_taxonomy.py` from a clean checkout and get
   the same `ext_claim.csv` as exists today.
2. Click the `evidence` URL/path on any row and see the original assertion.
3. For `source="heuristic:..."` rows, read the corresponding
   `docs/heuristics/<id>.md` and re-run any computation the heuristic relied on.

### Examples that meet the bar

The taxonomy today already follows this for its 2,818 rows:

```
pl_id,ext,source,strength,source_key,evidence
pl/perl,.pl,linguist,primary,Perl,https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml
pl/perl,.pl,pygments,primary,PerlLexer,pygments.lexers._mapping.LEXERS (via master CSV)
pl/prolog,.pl,linguist,primary,Prolog,https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml
```

Three rows, three distinct sources, each pinning its own assertion. The
shared-primary polysemy of `.pl` (Perl vs Prolog) is *fully traceable*: you can
see exactly who claims it and where to verify each claim.

### A case study: the `.R` capital-R fix (May 2026)

R's primary extension in Linguist is `.r` (lowercase). Roberto's SWH CSV
preserves case, so `.R` (21.5M occurrences) and `.r` (1.7M) appear as separate
rows. Before the fix, our cross-reference matched `.r` only — `.R` looked like
an unattributed extension at the top of the popularity tier.

The fix didn't add a new `ext_claim.csv` row. Instead, the SWH popularity
loader now case-aggregates: `.R` and `.r` are summed under the lowercase key
and case variants are recorded in the entry for transparency. Per-extension
pages show "Case variants in archive: `.R` (21.5M), `.r` (1.7M) — aggregated
above."

This is the right shape for case-only ambiguity: the *mapping* `(pl/r, .r)`
was already in the taxonomy via Linguist (provenance: linguist YAML). The fix
was about the *cross-reference layer*, not the taxonomy itself. The doc trail
is:

- `ext_claim.csv` row: `pl/r,.r,linguist,primary,R,<linguist URL>` — unchanged.
- `web/build_site.py` `load_swh_ext_popularity()`: now lowercases the
  Roberto-CSV ext key when aggregating, preserves case variants for display.
- Per-ext page: shows the aggregate + the case breakdown.

## 12. Manual labelling — ranked queue + crowd-source loop

To close the gap between (a) the 2,960,280 extensions in Roberto's CSV and
(b) the 1,538 in our taxonomy, we want human review at scale. The site has a
review queue at `/review/extensions/` (rendered by `build_site.py`). The loop:

1. **Ranking** — `tools/build_extension_review_queue.py` writes
   `data/derived/extension_review_queue.csv` (5,000 rows by default, configurable
   via `--min-occurrences` and `--max-rows`). Priority score:
   `log10(total_occ) − 1·n_current_claimants + 0.3 if last_year ≥ 2020`.
   So an extension with **high SWH popularity and no PL claim** floats to the
   top.

2. **Hint** — each row carries a rule-based `suggested_label` from
   `tools/build_extension_review_queue.py:HINT_LABELS` (e.g., `.png` →
   `binary:image`, `.pyc` → `binary:executable`, `.yaml` → `data:yaml`). The
   hint is intentionally conservative — most non-obvious extensions stay
   `unknown` so the reviewer has to actually look.

3. **Vocabulary** — `docs/extension_labels.md` lists the controlled labels
   (`pl/<id>`, `pl/new:<name>`, `pl/dialect:<parent>`, `pl/family:<family>`,
   `binary:image|audio|video|font|archive|executable|db|other`,
   `data:json-like|xml-like|yaml|csv-tsv|config|domain`,
   `docs`, `lock/cache`, `build-artifact`, `model/data`, `license/manifest`,
   `numeric-suffix`, `sha-filename`, `unknown`, `noise`).

4. **Submission** — clicking "Label this" on a row opens a **pre-filled
   GitHub issue** with:
   - title `Label extension: .X`
   - label `ext-review`
   - a structured `yaml` block in the body (`ext:`, `proposed_label:`,
     `evidence:`) that the curator parses
   - context (SWH occurrences, current claimants, vocabulary link)

5. **Provenance captured automatically** — annotator's GitHub login (issue
   author), timestamp (issue `created_at`), URL of the issue (re-readable
   discussion), and the free-text `evidence` block.

6. **Curator ingestion** — `tools/process_extension_labels.py` fetches issues
   with label `ext-review` via `gh api`, parses each body's structured block,
   and updates `data/derived/extension_labels.csv` with columns
   `ext, label, annotator, submitted_at, evidence, issue_url, issue_state,
   issue_number, curator_status`. `curator_status` starts at `new` and is
   updated by maintainers to `accepted` / `rejected` / `needs-info`.

7. **Re-incorporation** (next step, not yet wired) — accepted labels feed
   back into `ext_claim.csv` (for `pl/...` labels) or modify the auto-suggested
   tagging (for `binary:`/`data:`/etc. labels). Per the provenance contract in
   §11, manual-review entries get `source="manual_review:<annotator>"` and
   `strength="proposed"` until a maintainer promotes them.

The end-to-end loop is reproducible: anyone can re-run any step from the data
on disk + the issues on GitHub. The chain is:

```
Roberto CSV → swh_extensions_popularity.csv → extension_review_queue.csv
       → /review/extensions/ → GitHub issue → process_extension_labels.py
       → extension_labels.csv → ext_claim.csv → site rebuild
```

Every arrow is a script with a single source / single sink. Every annotation
has a permanent URL (the GitHub issue) and an annotator identity (GitHub
login). Disagreements between annotators are surfaced as multiple rows on the
same `ext`, resolved by maintainers in the issue thread.

## 13. TL;DR for a paper

If we publish based on this data:

- **Cite Roberto's CSV** (`nb_extensions_alphanum.csv`) as the source.
- **Cite `data/derived/swh_extensions_popularity.csv`** as the per-ext aggregate
  we computed (full 2.96 M rows, no cutoff).
- **State explicitly** that the website's `/ext/` view is capped at top 8 K by
  popularity and that this is a UX decision, not a data-curation claim.
- For any per-PL "SWH coverage" claim, **use the derived CSV** (query by ext),
  not the site (which truncates).
