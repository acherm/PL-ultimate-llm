# Heuristic: `wikidata_keyword_pl_shape`

| Field | Value |
|---|---|
| ID | `heuristic:wikidata_keyword_pl_shape` |
| Strength assigned | `proposed` |
| Defined in | `tools/build_pl_taxonomy.py` (regex `_WIKIDATA_PL_KEYWORDS`, loader `load_wikidata_keyword_pl_records`) |
| Output rows | `pl.csv` (new pl_id with `source_flags=heuristic:wikidata_keyword_pl_shape`), `ext_claim.csv` (with `source=heuristic:wikidata_keyword_pl_shape`, `strength=proposed`, `evidence=docs/heuristics/wikidata_keyword_pl_shape.md`) |
| Provenance contract | §11 of [SWH_EXTENSIONS_DECISIONS.md](../SWH_EXTENSIONS_DECISIONS.md#11-provenance-contract-for-ext--pl-mappings) — documented heuristic, requires this file |

## Rule

For each record in the pinned Wikidata snapshot `data/raw/wikidata_p1195.*.jsonl`:

1. If `_is_wikidata_pl(record)` is true (its `instance_of` QIDs intersect the
   175-QID PL-types closure in `data/raw/wikidata_pl_types.*.json`), the record
   is handled by the main `wikidata` source — this heuristic does **not** apply.
2. Otherwise, build a haystack from: **entity label + aliases + description +
   `instance_of` labels**. If the regex `_WIKIDATA_PL_KEYWORDS` matches the
   haystack (case-insensitive):
   - **Try name-match first** against existing `pl_id`s (same matcher as
     the main `wikidata` overlay). If a match exists, attach the
     extensions to the existing `pl_id` with `source=heuristic:...`,
     `strength=proposed` (no new entity). Also overlay
     `wikidata_qid` / `wikipedia_url` onto the existing `pl_id` if it
     has none yet.
   - **Otherwise mint a new `pl_id`** with
     `source_flags=heuristic:wikidata_keyword_pl_shape` and emit its
     extensions as proposed claims (subject to umbrella-protection).

The entity label is included because Wikidata is inconsistent about typing:
many real markup languages (VRML, AIML, TTML, AML, GPML, MSL, …) carry
only `instance_of = "file format" (Q235557)` but their entity label clearly
names them (e.g. "Virtual Reality Modeling Language"). Restricting the
haystack to `instance_of` labels only lets those slip through.

The regex is a hand-curated set of phrases that name a kind of language but
whose corresponding Wikidata QID is not in the closure (typically because
the QID is one or two subclass-of hops away from the 5 closure roots, or
because Wikidata uses parallel taxonomies that don't all reach `Q9143`).

Current phrase list:

```
programming language, markup language, query language, scripting language,
domain-specific language, data serialization language, data serialization format,
configuration language, shader(ing|) language, shading language,
description language, transformation language, stylesheet language,
modeling language, specification language, hardware description language,
functional language, object-oriented language, declarative language,
intermediate language, assembly language, esoteric programming language,
interpreted language, compiled language, template language,
playlist markup language, interface definition language
```

## Inputs

- `data/raw/wikidata_p1195.<date>.jsonl` — pinned Wikidata P1195 snapshot.
- `data/raw/wikidata_pl_types.<date>.json` — pinned closure of PL-shaped QIDs
  (used to *exclude* records already handled by the main path).
- The regex `_WIKIDATA_PL_KEYWORDS` defined in `tools/build_pl_taxonomy.py`.

No live SPARQL calls; output is deterministic given the snapshot pair + regex.

## Expected precision / recall

Estimated on the May-15-2026 snapshot:

| Bucket | Count | Notes |
|---|---:|---|
| P1195-bearing records in snapshot | 13,833 | All Wikidata items with file extensions |
| In PL-types closure (handled by `source=wikidata`) | 220 | Gap A path |
| Outside closure, **keyword hit** (handled here) | 119 | This heuristic — of which 28 name-match an existing pl_id (attach), 91 mint new |
| Outside closure, no keyword hit (correctly excluded) | ~13,494 | File formats / image formats / executables / etc. |

**Precision** (manual review of the ~44 hits): the majority are real DSLs
or markup languages already accepted as PL-shaped by the
[`docs/extension_labels.md`](../extension_labels.md) precedent
(e.g. `.pgn` Portable Game Notation, `.toml`, `.yaml`). Concrete examples:

| Phrase that matched | Wikidata items it catches |
|---|---|
| `data serialization format` | BSON, CBOR, Ion, NBT, N-Triples, TriG, N3 |
| `playlist markup language` | XSPF, ASX |
| `markup language` (via not-quite-closure path) | TTML, SSML, AIML, GPML, RML |
| `description language` | WADL, VRML (subclass), AML |
| `specification language` | SDL |
| `shading language` | Flare3D Shader Language Compiled |

Known false positives (handled by `strength=proposed`, reviewer rejects):

- `.kmz` → "Keyhole Markup Language Zipped" — the entity is a ZIP container
  around KML, not a separate language. Should be labeled `binary:archive`.
- `.compiled` → "Flare3D Shader Language Compiled" — this is the compiled
  form of a shader, not the language itself.
- "Distinguished Encoding Rules" (`.der`) — pure binary encoding rule (X.690).
  Borderline: same shape as ASN.1, which IS catalogued.
- "Perl module" (Q1165116) — the entity's description carries
  "Perl programming language" so the keyword fires, but Perl module is just
  a `.pm` source file. Lands as an orphan `pl_row` with no `ext_claim`
  (`.pm` is umbrella-skipped by Perl/Promela/Raku). Reviewer can either
  delete the row or alias it to `pl/perl`.
- Software-component-of-a-PL labels generally — anything whose description
  reads "X file for the Y programming language" can match. Mitigation:
  umbrella-protection usually drops the ext_claim, and the orphan pl_row
  is visually flagged on the site by its `source_flags=heuristic:...`.

**Recall** is partial by design: the regex only catches phrases we know
about. Adding a phrase is a one-line change here + a one-line change in
`_WIKIDATA_PL_KEYWORDS`. Phrases NOT to add: `file format` (too broad),
`document file format` (covers .pdf / .docx), `audio file format`, etc.

## Known failure modes

1. **Container conflation** (`.kmz`, `.docx`). When a Wikidata item is a
   zipped/packaged form of a known PL, the entity matches the regex but the
   `.zip`-shaped extension is not a separate language. Mitigation:
   `strength=proposed` keeps it out of `primary_claimants` until reviewed.
2. **Compiled-form conflation** (`.compiled`). Same shape — the compiled
   output of a shader/parser is a binary, not the language. Same mitigation.
3. **Phrase drift**. Wikidata editors may rephrase `instance_of` labels
   (e.g. "data-serialization language" with a hyphen, or rewording to
   "serialization format for X"). The regex includes a `[- ]` between
   "data" and "serialization" but not exhaustive across all such pairs.
4. **Closure overlap** (defensive). If a future closure expansion already
   covers a record, `_is_wikidata_pl_by_keyword` short-circuits to False —
   no double-promotion. Verified by `_is_wikidata_pl(record)` short-circuit
   at the top of the keyword check.

## Reviewer workflow

Each row emitted by this heuristic has `source="heuristic:wikidata_keyword_pl_shape"`
and `strength="proposed"`. A maintainer reviewing `ext_claim.csv`:

- **Accept** → bump the row's strength to `primary` (or `secondary`) manually,
  or label the (ext, pl) edge through the standard
  [extension-labels form](../extension_labels.md) which writes a corroborating
  `manual_review:<annotator>` row.
- **Reject** → either:
  - tighten `_WIKIDATA_PL_KEYWORDS` to exclude this entity's `instance_of`
    label (rare — usually too specific to be worth a regex change);
  - label the extension as `binary:archive` / `binary:other` etc. via the
    form, so the site's extension page hides the heuristic's row from
    PL-resolution pipelines.

## Reproducibility

```bash
# Re-run the build to regenerate ext_claim.csv with this heuristic's rows.
python3 tools/build_pl_taxonomy.py

# Inspect which entities this heuristic added on the latest snapshot:
awk -F, '$3 == "heuristic:wikidata_keyword_pl_shape"' \
    data/derived/pl_taxonomy/ext_claim.csv \
    | sort -u
```

The output is fully determined by the snapshot + regex; running the build
twice on the same inputs is bit-for-bit identical.
