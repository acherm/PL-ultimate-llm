# Per-program reviews (ground-truth collection)

Reviews collect ground truth about **what PL a given program is written
in**, one judgment at a time, from humans, PLI tools, and LLMs. They feed
three downstream uses: refining the file-extension ↔ PL mapping, labelling
example corpora, and evaluating PL-identification tools.

Design summary: **facts as files, aggregates as derived CSVs** — the same
convention as the rest of the repo.

## Storage

One immutable JSON file per review:

    reviews/<sha1_git>/<UTC-stamp>--<reviewer-id>--<hash8>.json

- **Keyed by content** (`sha1_git`, same key as `samples/<slot>/<sha>/`),
  not by sample path: reviews survive sample reclassification and apply to
  any future sample with the same bytes.
- **Append-only**: a review is never edited. Changing your mind = writing a
  new review whose `verdict.supersedes` names your previous file.
  Aggregation takes each reviewer's latest.
- **Conflict-free by construction**: one file per review means concurrent
  reviewers (or bots) can never produce a git merge conflict. Git is the
  sync layer — clone, review, commit, push. No PRs, no central database.
- The server/UI is stateless; the disk is the database. Everything stays
  readable with `jq` + this document if the tooling disappears.

## Record schema (`"schema": 1`)

```json
{
  "schema": 1,
  "subject": {
    "sha1_git": "f851a314d7b2dfc8949028f3671dba8f268ac4ee",
    "swhid": "swh:1:cnt:f851a314d7b2dfc8949028f3671dba8f268ac4ee",
    "filename": "XSetModifierMapping.m",
    "ext": ".m"
  },
  "reviewer": {
    "kind": "human",            // human | tool | llm
    "id": "mathieu-acher",      // slug; tools: "pygments", llm: model slug
    "version": null,            // tool/LLM version, null for humans
    "runner": null,             // e.g. "tools/auto_review.py@<commit>"
    "params": null              // e.g. {"mode": "content-only"} — whether a
  },                            //   tool saw the filename (blinding trace)
  "verdict": {
    "label": "pl/new:tet-scenario",   // vocabulary below; null = comment-only
    "confidence": "high",             // high | medium | low
    "supersedes": null                // filename of my earlier review, if any
  },
  "comment": "xts5 TET 'mc' format: C embedded in >>CODE blocks.",
  "shown": {                    // anchoring-bias trace: what the UI displayed
    "predicted_pl_id": "",
    "claimants": ["pl/m4", "pl/matlab", "pl/mercury", "..."],
    "suggestions_rev": "2170bff9"
  },
  "created_at": "2026-06-12T09:31:02Z"
}
```

`verdict.label` reuses the [extension-label vocabulary](extension_labels.md)
at program granularity: `pl/<id>` (must exist in the taxonomy),
`pl/new:<slug>`, `pl/dialect:<parent>`, `pl/family:<name>`, and the fixed
non-PL labels (`binary:*`, `data:*`, `docs`, `unknown`, `noise`, …).

Disagreement between reviews is **expected and preserved** — consensus is
computed later (Phase 2: `build_review_consensus.py` →
`data/derived/review_consensus.csv` with gold/silver/disputed tiers), and
can be recomputed under different rules without touching the facts.

## The review UI

```
python3 tools/review_server.py            # http://127.0.0.1:8765
python3 tools/review_server.py --open     # + open browser
python3 tools/review_server.py --as alice # review under another id
python3 tools/review_server.py --host 0.0.0.0   # LAN session (no auth!)
python3 tools/review_server.py --autocommit     # git-commit reviews on Ctrl-C
```

- Left: the program bytes, **deliberately not syntax-highlighted**
  (picking a lexer would leak a language guess to the reviewer).
- Right: suggestions — the pipeline's `predicted_pl_id` (★) and the
  extension's claimant PLs (hotkeys 1–9) — plus PL search over the
  taxonomy, `pl/new:` proposal, non-PL labels, confidence, comment.
- **Blinding**: other reviewers' verdicts show as a count only, and are
  revealed after you submit yours.
- Queue strategies: `unreviewed-by-me` (default), `unreviewed` (by anyone),
  `second-opinion` (others reviewed it, you haven't), `all`; optional ext
  filter. Order is a deterministic shuffle seeded by reviewer id, so
  distributed reviewers naturally spread coverage without coordination.
- **Browse mode** (`b`): a filterable table of every program (filename,
  ext, slot, predicted PL, human/machine review counts, your own label —
  others' labels stay blind here too). Click a row to review it; skip
  returns to the queue.
- Identity is claimed (`git config user.name` by default, or the UI field /
  `--as`), corroborated by the git commit that introduces the files.

## Distributed reviewing

- Push access → review, commit (`--autocommit` or manual), push. File-per-
  review means pushes never conflict.
- No push access → (Phase 4) export a review pack and have a maintainer run
  `ingest_reviews.py`. Until then: send the `reviews/<sha>/*.json` files.
- Note the commit-message hook: commits need a `List-Digest:` trailer
  (`--autocommit` handles it).

## Roadmap

- Phase 2 — `build_review_consensus.py` (gold/silver/disputed,
  Krippendorff's α) + `auto_review.py` (pygments first, blinded +
  filename-aware modes; LLM reviewers later).
- Phase 3 — public-site integration: read-only review panels on sample
  cards + a `/reviews/` dashboard (coverage, agreement, tool-vs-human).
- Phase 4 — review packs + `ingest_reviews.py` for clone-less reviewers.
