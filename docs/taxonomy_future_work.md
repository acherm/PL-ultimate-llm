# Taxonomy — future considerations

Open questions and deferred work for the PL taxonomy. Each entry includes
context, the trigger that surfaced it, and a sketch of what a solution
might look like. Nothing here is committed work — it's a queue of
"worth-deciding-eventually."

## Secondary qualifiers for PLs

**Trigger.** Submitting `.pgn` as `pl/new:pgn` (issue #15) raised the
question: PGN is genuinely a domain-specific notation *and* a data
interchange format. The current vocabulary forces a single primary
classification (`pl/<id>` *or* `data:domain`, not both).

**Why it matters.** Many entries in `pl_list.txt` are in this same
situation: a single label flattens two real properties.
- **YAML, TOML, JSON-Schema** — declarative data formats AND included as PLs.
- **GraphQL** — a query language AND a schema language AND an IDL.
- **DOT, POV-Ray** — domain-specific notations (graphs, ray-traced
  scenes) AND fully-formed languages with grammars and tools.
- **PGN** — chess move notation AND a structured data format.

A reader asking "what is `.dot`?" gets a clear answer from the current
taxonomy ("it's a programming language"). A reader asking "what kind
of PL is it?" — declarative? imperative? notation? data-only? — has to
infer from the language page.

**Sketch of a solution.** Add an optional `qualifiers` field to
`pl.csv` (or to `languages/<Name>/meta.json`), drawn from a curated
vocabulary:

| Qualifier | Meaning | Examples |
|---|---|---|
| `data-interchange` | Primary purpose is encoding state for cross-tool exchange. | YAML, TOML, Protocol Buffers, Avro IDL, ASN.1, PGN |
| `markup` | Annotates content with structure or presentation. | HTML, LaTeX, Markdown, AsciiDoc, BBCode |
| `notation` | Compact domain-specific syntax for a single problem domain. | DOT, regex, Lilypond, Music XML, PGN, Z notation |
| `query` | Expresses a question over a data model. | SQL, GraphQL, Cypher, SPARQL, KQL |
| `schema` | Constrains the shape of other data. | JSON Schema, XSD, Avro IDL, protobuf |
| `config` | Encodes runtime/build configuration. | TOML, INI, Dhall, Cue, KCL |
| `dsl-embedded` | Implemented as a library on top of a host PL. | Ruby/RSpec, Scala/Spark-DSL, Haskell/QuasiQuotes |
| `pure-functional` / `imperative` / `logic` / … | Paradigm classification. | Haskell, C, Prolog |
| `turing-incomplete` | Doesn't admit general computation. | YAML, TOML, regex, PGN, JSON-Schema (mostly) |

A PL row could carry multiple qualifiers — e.g. PGN = `notation` +
`data-interchange` + `turing-incomplete`. The qualifiers wouldn't gate
inclusion in `pl_list.txt`; they'd refine what kind of PL each entry is.

**Open design choices.**

- *Source of truth.* Should qualifiers come from the upstream sources
  (PLDB, Linguist, Wikipedia category links) when possible, or be
  hand-curated? A first pass: derive from existing upstream sources +
  let crowdsource fill gaps via the existing labelling form.
- *Form integration.* The `/contribute/add-pl/` form could expose
  qualifier checkboxes (matching the controlled vocab). For existing
  PLs, a separate "Qualify this PL" form could append to a
  `pl_qualifiers.csv`.
- *Site rendering.* PL pages already show "sources that mention this
  PL" — qualifier pills would slot in next to that, e.g. `notation`,
  `turing-incomplete`, `data-interchange` for PGN.
- *Search/filter.* `/browse/` could gain a "Filter by qualifier"
  control. The exists-as-PL-yes/no question stays binary; everything
  else becomes a *faceting* layer on top.

**Decision deferred until.** The `pl-add` web-form flow stabilises and
we see how many borderline cases (data-format-or-PL) actually arrive
from the crowd. If it's two or three a month, plain free-text notes
are enough. If it's many, the qualifier vocabulary becomes worth
building.

**Related entries to revisit when this lands.** `.pgn` (issue #15),
`.h` (multi-PL, issue #12), `.toml`, `.yaml`, `.dot`, `.svg`, `.tex`.

## In-repo-only PLs aren't visited by build_pl_taxonomy.py

**Trigger.** Issue #16 added "Portable Game Notation" via the Add-PL form.
It landed in `pl_list.txt` and `languages/Portable_Game_Notation/meta.json`
— and PGN appears in `/browse/`. But `build_pl_taxonomy.py` iterates
`master_inventory` rows (the union of 7 upstream sources), and PGN isn't
in any of them. So:

- No `pl/portable-game-notation` row is minted in `pl.csv`.
- The new `repo_meta` ext_claim block (added in `62e7cf90`) can't fire
  for PGN, even though `meta.json` lists `extensions: [".pgn"]`.
- The accepted ext-review row (`.pgn → pl/portable-game-notation`) can't
  promote because the target `pl_id` doesn't exist in `pl.csv`.

PGN is in the catalog (browse + per-PL page), but its extension
attribution is half-wired.

**Why it matters.** Every PL added through the web form hits this: the
data lives in `languages/<Name>/`, never reaches the taxonomy tables,
treated as a "name only" entry. Search works; per-ext pages don't.

**Sketch of the fix.** After the outer `for row in master:` loop in
`build_pl_taxonomy.build()`, walk `LANGUAGES_DIR` for any `meta.json`
whose canonical name isn't already a `pl_rows` entry. For each, mint a
row with `pl_id = slugify(name)` (same `used_ids` collision handling),
`canonical_name = name`, `in_repo = True`, all other source flags
False, and aliases/extensions read from `meta.json`. Then re-run the
`# 4. In-repo meta.json` ext_claim block for these. ~30 lines.

## Add-PL ↔ ext-review reconciliation

**Trigger.** PGN was simultaneously proposed via:
- Issue #15 (ext-review, `pl/new:pgn`) — would mint `pl/pgn`
- Issue #16 (Add-PL form) — minted `pl/portable-game-notation`

Two different `pl_id`s for the same conceptual language. Resolved by
hand: edited #15's body to point at `pl/portable-game-notation`, the
reconciliation pass dropped the orphan row.

**Why it matters.** A submitter who fills both forms (or two
submitters racing on the same PL) creates duplicate identity. The
catalog ends up with conflicting `pl_id`s that don't auto-merge.

**Sketch of the fix.** When `tools/process_pl_addition.py` runs, it
should (after writing `meta.json`) scan open `ext-review` issues for
any `pl/new:<x>` labels where `<x>` matches the new PL's name
(case-insensitive) or any alias. For each match, edit the issue's
body via `gh issue edit` to swap `pl/new:<x>` → `pl/<canonical_pl_id>`.
The curator's reconciliation pass absorbs them on the next ingest. Add
a note to the new Add-PL PR's body listing the re-pointed issues so
the maintainer can audit the link.

**Decision deferred until.** Multiple PLs come in via the web form per
month. Right now this is a manual one-shot fix.

## Other deferred topics

(Empty — append future-work notes here as they come up.)
