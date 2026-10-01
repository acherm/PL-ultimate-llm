# PL identity — records, concepts, and traced `same_as` decisions

Several entries of the catalog denote the same language: `Python` (Linguist,
PLDB, …) and `Python (programming language)` (Wikipedia) each had a page.
Merging them destructively would lose what each source calls the language,
which PLI tools rely on (Linguist says `Python`, Pygments `PythonLexer`,
Wikipedia `Python (programming language)`). This document describes the
layer that joins such entries **without editing any source record**, and the
audit (2026-09-30) that motivates it.

## 1. Model

| Notion | What it is | Where |
|---|---|---|
| **record** | one source's entity, never edited here: a row of `pl.csv` (`pl/<id>`) or an LLM-campaign folder (`repo/<folder>`) | `data/derived/pl_taxonomy/pl.csv`, `languages/` |
| **decision** | a reviewed verdict on a pair of records: `same_as`, `accepted` or `rejected`, with rule, evidence, reviewer, date, note | `data/curated/pl_links.csv` — the only hand-edited file |
| **concept** | records joined by accepted `same_as` decisions (connected components) | `data/derived/pl_concepts/pl_concepts.csv`, `pl_concept_members.csv` |

The site renders **one page per concept**: the other entries' pages redirect
to it, their names become aliases, their programs move to it, and a
*Merged records* panel lists every record with its sources and the decision
that joined it. Undoing a merge = flipping one decision to `rejected`.

## 2. Pipeline

```
raw sources ──> tools/build_pl_taxonomy.py ──> pl.csv (records)
                                                  │
languages/<Name>/meta.json (records) ─────────────┤
                                                  ▼
          tools/build_pl_concepts.py propose ──> data/derived/pl_concepts/link_candidates.csv
                                                  │   (a reviewer decides each pair)
                                                  ▼
                              data/curated/pl_links.csv (decisions)
                                                  │
          tools/build_pl_concepts.py build ──> pl_concepts.csv, pl_concept_members.csv
                                                  │
          web/build_site.py (apply_pl_concepts) ──> one page per concept + redirects
```

`build` runs in the Pages CI after the taxonomy rebuild (stdlib only). It
**fails** if a decision points at a record that no longer exists (a renamed
`pl_id`, a deleted folder): such a decision must be re-reviewed, not silently
dropped. It warns if a concept joins records whose identifiers conflict,
unless an accepted decision links those two records directly.

The site merges an entry through **its own record only** — the folder of a
campaign page, the `pl.csv` row of a taxonomy-only page — never through the
taxonomy record its name matcher attached, which is often wrong (§5).

## 3. Decisions file

`data/curated/pl_links.csv`, one row per reviewed pair:

| Column | Meaning |
|---|---|
| `link_id` | `L-` + sha1(`relation\|min(a,b)\|max(a,b)`)[:10]: stable, order-independent; `build` checks it |
| `record_a`, `record_b` | record references (`pl/<id>`, `repo/<folder>`) |
| `name_a`, `name_b` | names at review time (for humans; not used by the build) |
| `relation` | `same_as` (typed non-merging relations — `version_of`, `dialect_of`, … — are future work) |
| `decision` | `accepted` or `rejected`. A pair with no row stays *undecided* and is reported by `build` |
| `rule` | the rule that proposed the pair (`generic-qualifier`), or `manual` |
| `evidence` | machine evidence from `propose` (names, shared ids) |
| `reviewer`, `reviewed_at` | who judged it, when |
| `note` | why, especially for rejections and caveats |

To add or change a decision: run `propose`, edit the row, run `build`, rebuild
the site. `rejected` rows are kept: they stop the same pair from being
re-proposed as new work and document why it is not a merge.

## 4. Rule `generic-qualifier` and batch 1 (2026-09-30)

**Rule.** Record B is named `<N> (programming language)` (or `(language)`,
`(computer language)`, `(programming)`, `(software)`, `(lang)`: the
Wikipedia disambiguation style) and record A is named `<N>`, compared
case-, accent-, space- and punctuation-insensitively, with `+ ! # *`
significant (`Go` ≠ `Go!`, `XPL` ≠ `XPL+`). Other parentheticals are part of
the name — on Esolang, `(Keymaker)` marks a homonym. Keys shorter than 4
characters are not proposed (`C`, `Go`, `V`, `D` need their own batch).

**Batch 1.** 88 candidate pairs over 16,450 records:

- **81 accepted**, reviewed one by one against the records' sources and ids.
  Where a record carries an Esolang page, the page was read (2026-09-30):
  Esolang's `Python`, `C♯`, `Lisp`, `Forth` describe the mainstream
  languages; `Java'`, `Self`, `Factor` are different languages merged into
  the mainstream records by name upstream — accepted for the mainstream
  record, with the caveat in the note.
- **5 rejected**: `pl/pico`, `pl/charm`, `pl/cedar` (their Esolang part is a
  different language — the campaign records `repo/Pico`, `repo/Charm`,
  `repo/Cedar` are linked instead), `pl/arrow` (two different esolangs),
  `pl/j-a-v-a` (Esolang `J.A.V.A.` ≠ Java; the key collides because dots are
  ignored).
- **2 undecided**: `zeta` and `Pencil Code` — no evidence beyond the names.

**Effect on the site.** 43 concepts over 124 records. 42 entries fold into
40 pages (14,242 → 14,200 browsable entries), e.g. `Python`, `Java`, `Julia`,
`Swift`, `Erlang`, `C#` (+ `csharp`, `C Sharp (programming language)`),
`A+` (+ `aplus`), `Karel` (two campaign folders: 2 programs on one page).
`Boomerang`, `Darwin`, `Source` get the *Merged records* panel only: their
Wikipedia record had no page of its own.

## 5. Audit behind the next batches (2026-09-30)

Measured on the 14,242 entries the site listed (3,842 campaign languages +
10,400 taxonomy-only pages). Pairs linked by any identity signal were split
into classes; 20 pairs per class were labelled by one reviewer
(`claude-opus-5-5`): S = same language, V = related but distinct (version,
dialect, implementation, successor), X = different. Rates are ±15–20 points.

| Class | Pairs | S | V | X |
|---|---|---|---|---|
| A — two campaign entries on one taxonomy record, same name key | 60 | 14 | 2 | 4 |
| B — two campaign entries on one taxonomy record, alias link | 182 | 14 | 4 | 2 |
| C — two campaign entries on one taxonomy record, different names | 68 | 2 | 8 | 10 |
| D — different records sharing a Wikidata/Wikipedia/Esolang/Rosetta/Linguist id | 231 | 15 | 4 | 1 |
| E — different records, same name key only | 161 | 18 | 0 | 2 |
| F — different records with conflicting ids | 431 | 1 | 5 | 14 |
| G — alias / lexer / homepage link only | 384 | 5 | 8 | 7 |

A broader same-name rule (case/spacing/punctuation/accents/PLDB slug,
symbols significant, keys ≥ 4 chars, no conflicting ids) finds 272 pairs,
28/30 correct in a sample (misses: `SA-C`/`SAC`, `Small Basic`/`SmallBASIC`),
removing 215 entries. Deduplication is worth ~2–3 % of the catalog; the
larger problem is **wrong links**:

- **The site's name matcher attaches records greedily** (first hit over name
  + aliases): 214 taxonomy records are attached to ≥ 2 campaign pages (470
  pages); in class C, half the sample is wrong — `Comenius Logo` via alias
  `CL` → Common Lisp, `B Method` via `B` → B, `µLISP` → `lisp` (non-ASCII
  dropped), `Es` → ECMAScript (Wikidata alias `ES`). Those pages show another
  language's Wikidata/Wikipedia/extension facts.
- **Pygments lexer aliases are stored as language aliases** (649 rows of
  `pl_alias.csv`, 90 of ≤ 2 characters): `vb.net` → B4X, `vfp` → Clipper,
  and Python's aliases include `bazel`, `sage`, `starlark`.
- **The Wikidata overlay attaches a QID to every record matched by name or
  alias**: 132 QIDs sit on > 1 record, 81 across different names (Q28865
  Python on `bazel`, `py`, `sage`, `starlark`; one BASIC QID on 7 BASICs).
- **Esolang homonyms are merged into mainstream records by name**: 402
  records combine an Esolang page with a mainstream source and all are typed
  `esolang` (C, C++, C#, Java, Python, Haskell, COBOL, …).
- **Three name normalizers** (`master_inventory.normalize_key`,
  `build_pl_taxonomy._norm_name`, `build_site._normalize_name`) disagree,
  which explains both missed duplicates and false matches.

## 6. Next steps (in this order)

1. Fix the matchers before more merging: lexer aliases in their own
   lexer → languages table; QIDs only on unambiguous matches; one shared
   normalizer (symbols and author qualifiers significant, non-ASCII kept);
   no alias matches of ≤ 3 characters.
2. Batch 2: the rest of the same-name rule (≈ 230 pairs at ≈ 93 %), then
   short names (`C`, `Go`, `V`, `D`, …) with id evidence.
3. Expert batch: classes B and D (≈ 400 pairs at 70–75 %).
4. Typed non-merging relations (`version_of`, `dialect_of`,
   `implementation_of`, `renamed_to`) for class G and the V labels: shown as
   a family box, not merged. `cannot_link` rows for known homonyms
   (`Go`/`Go!`, `Small Basic`/`SmallBASIC`). Started 2026-10-01: a `same_as`
   row with decision `rejected` already acts as one — `web/build_site.py`
   will not attach the campaign page to that record (first: `repo/M`, Power
   Query M, vs `pl/m`, MUMPS — `L-c9f8895c83`).
5. A *kind* facet (programming / markup / data / format) from Linguist and
   PLDB types — today the only type carried is `esolang`.
