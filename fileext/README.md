# fileext/ — moved

This directory was the exploratory home for the Wikidata + Wikipedia
filename-extension work. Everything has moved into the main project
layout. Look here:

| Was | Now |
|---|---|
| `fileext/fetch_wikidata.py` | [`tools/fetch_wikidata_extensions.py`](../tools/fetch_wikidata_extensions.py) |
| `fileext/enrich_wikipedia.py` | [`tools/fetch_wikipedia_infoboxes.py`](../tools/fetch_wikipedia_infoboxes.py) |
| `fileext/build_index.py` | [`tools/build_wikidata_wikipedia_index.py`](../tools/build_wikidata_wikipedia_index.py) (debug merge) |
| `fileext/data/wikidata_p1195.<date>.jsonl` | [`data/raw/wikidata_p1195.<date>.jsonl`](../data/raw/) (pinned snapshot) |
| `fileext/data/wikipedia_infobox.<date>.jsonl` | [`data/raw/wikipedia_infobox.<date>.jsonl`](../data/raw/) (pinned snapshot) |
| `fileext/cache/wikipedia_pages/` | `.cache/wikipedia_pages/` (gitignored, regenerable) |
| `fileext/cache/wikidata_raw/` | `.cache/wikidata_sparql/` (gitignored, regenerable) |

Integration into the main taxonomy build (`tools/build_pl_taxonomy.py`)
adds `wikidata` and `wikipedia` as first-class `ext_claim.source` values,
and adds `wikidata_qid` + `wikipedia_url` columns to `pl.csv`. For non-PL
items (file formats, image formats, etc.) the side artifact is
[`data/derived/external_extension_index.csv`](../data/derived/) (built by
`tools/build_external_extension_index.py`).

This stub is kept so old links don't 404. Safe to delete once everyone is
on the new locations.
