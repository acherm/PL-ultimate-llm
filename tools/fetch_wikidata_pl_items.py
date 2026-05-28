#!/usr/bin/env python3
"""Pull every Wikidata item whose `instance of` (P31) is in our PL-types
closure, regardless of whether the item carries P1195 (filename extension).

Why this exists: the P1195-based pipeline at
`tools/fetch_wikidata_extensions.py` is excellent at finding PLs Wikidata
has labelled with at least one file extension, but it silently drops
languages whose Wikidata entry has no P1195 claim — even when the
language genuinely has well-known extensions and a rich enwiki article.
A glaring example is R (Q206904): no P1195 on Wikidata as of 2026-05-27,
so our structured-wikipedia fact extraction never reaches it.

This fetcher closes that gap. For every QID in the precomputed PL-types
closure at `data/raw/wikidata_pl_types.<date>.json`, it asks WDQS for the
items typed as that QID, retains those with an enwiki sitelink (no
sitelink = no infobox to parse), and writes a thin per-item record:

  {"qid", "label", "aliases", "enwiki_title", "instance_of": [{qid,label}]}

Output: data/raw/wikidata_pl_items.<YYYY-MM-DD>.jsonl

Downstream: `tools/fetch_structured_wikipedia.py` unions this file with
the existing P1195 file to form the target QID set for the Parquet pass.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

UA = "PL-ext-explorer/0.1 (https://github.com/acherm/PL-ultimate; mathieu.acher@irisa.fr)"
WDQS = "https://query.wikidata.org/sparql"
WBAPI = "https://www.wikidata.org/w/api.php"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw"
RAW_DIR = ROOT / ".cache" / "wikidata_sparql"

# Chunk size for the per-type SPARQL query. Keeping it modest (30 type
# QIDs at a time) holds the result count under WDQS's per-query budget
# even for popular roots like Q9143 (programming language, ~700 direct
# instances) without splintering into 175 single-type queries.
CHUNK_SIZE = 30


def http_post(url: str, data: dict, accept: str) -> dict:
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Accept": accept, "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def http_get(url: str, params: dict) -> dict:
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{url}?{qs}",
        headers={"Accept": "application/json", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def sparql(query: str) -> list[dict]:
    res = http_post(WDQS, {"query": query}, "application/sparql-results+json")
    return res["results"]["bindings"]


def short(uri: str) -> str:
    return uri.rsplit("/", 1)[-1] if uri.startswith("http") else uri


# Items typed as any QID in the chunk, that ALSO have an enwiki sitelink
# (no sitelink = no Wikipedia infobox to walk, so the row would be useless
# to the structured-wikipedia downstream).
Q_ITEMS_BY_TYPE = """
SELECT DISTINCT ?item ?type ?enwiki_title WHERE {{
  VALUES ?type {{ {type_values} }}
  ?item wdt:P31 ?type .
  ?article schema:about ?item ;
           schema:isPartOf <https://en.wikipedia.org/> ;
           schema:name ?enwiki_title .
}}
"""


def latest_snapshot(pattern: str) -> Path | None:
    matches = sorted(OUT_DIR.glob(pattern))
    return matches[-1] if matches else None


def load_pl_type_closure() -> tuple[list[str], dict[str, str]]:
    """Return (sorted_qid_list, label_by_qid). label_by_qid is best-effort —
    `wikidata_pl_types.<date>.json` has only the closure QIDs, no labels,
    so we synthesize an empty map and fill it from the per-item SPARQL
    response later."""
    path = latest_snapshot("wikidata_pl_types.*.json")
    if path is None:
        sys.exit("no wikidata_pl_types.*.json snapshot — run "
                 "tools/fetch_wikidata_extensions.py first")
    payload = json.loads(path.read_text())
    qids = sorted(set(payload.get("pl_type_qids") or []))
    print(f"[load] PL-types closure: {path.name} → {len(qids)} type QIDs",
          flush=True)
    return qids, {}


def fetch_items_for_types(type_qids: list[str]) -> tuple[
        dict[str, set[str]], dict[str, str]]:
    """Run the items-by-type SPARQL in chunks. Returns:
    - item_to_types: {item_qid: {type_qid, …}}
    - item_to_enwiki: {item_qid: enwiki_title}
    """
    item_to_types: dict[str, set[str]] = defaultdict(set)
    item_to_enwiki: dict[str, str] = {}
    n_chunks = (len(type_qids) + CHUNK_SIZE - 1) // CHUNK_SIZE
    for i in range(0, len(type_qids), CHUNK_SIZE):
        chunk = type_qids[i : i + CHUNK_SIZE]
        values = " ".join(f"wd:{q}" for q in chunk)
        q = Q_ITEMS_BY_TYPE.format(type_values=values)
        try:
            rows = sparql(q)
        except Exception as exc:  # noqa: BLE001
            # Retry once, then move on. A failed chunk costs at most ~200
            # QIDs of recall; not worth blocking the whole refresh.
            print(f"[sparql] chunk {i//CHUNK_SIZE+1}/{n_chunks} failed "
                  f"({exc!r}); retrying once after 5s …", flush=True)
            time.sleep(5)
            try:
                rows = sparql(q)
            except Exception as exc2:  # noqa: BLE001
                print(f"         retry failed ({exc2!r}); skipping chunk",
                      flush=True)
                continue
        for r in rows:
            iq = short(r["item"]["value"])
            tq = short(r["type"]["value"])
            t = r["enwiki_title"]["value"]
            item_to_types[iq].add(tq)
            item_to_enwiki.setdefault(iq, t)
        print(f"[sparql] chunk {i//CHUNK_SIZE+1}/{n_chunks}: "
              f"+{len(rows)} rows  (items so far: {len(item_to_types)})",
              flush=True)
        # Be polite to WDQS: short pause between chunks.
        time.sleep(0.3)
    return item_to_types, item_to_enwiki


def wbgetentities(qids: list[str], props: str) -> dict:
    res = http_get(WBAPI, {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": props,
        "languages": "en|mul",
        "format": "json",
    })
    return res.get("entities", {})


def fetch_metadata(qids: list[str], props: str,
                   batch_size: int = 50, sleep: float = 0.05) -> dict:
    out: dict = {}
    total = len(qids)
    for i in range(0, total, batch_size):
        chunk = qids[i : i + batch_size]
        entities = wbgetentities(chunk, props)
        out.update(entities)
        if (i // batch_size) % 10 == 0:
            print(f"         {min(i + batch_size, total)}/{total}", flush=True)
        time.sleep(sleep)
    return out


def already_in_p1195() -> set[str]:
    """QIDs already covered by the P1195 snapshot — we INCLUDE them in
    our output anyway (the downstream union dedupes by QID) so the file
    is self-contained, but knowing the overlap helps the manifest tell
    a clearer story."""
    path = latest_snapshot("wikidata_p1195.*.jsonl")
    if path is None:
        return set()
    qids: set[str] = set()
    with path.open() as f:
        for line in f:
            rec = json.loads(line)
            q = rec.get("qid")
            if q:
                qids.add(q)
    return qids


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()

    type_qids, _ = load_pl_type_closure()
    p1195_qids = already_in_p1195()
    print(f"[load] P1195 snapshot covers {len(p1195_qids)} QIDs (overlap stats only)",
          flush=True)

    item_to_types, item_to_enwiki = fetch_items_for_types(type_qids)
    item_qids = sorted(item_to_types.keys(),
                       key=lambda q: int(q[1:]) if q[1:].isdigit() else 0)
    type_qid_set = sorted({t for ts in item_to_types.values() for t in ts})
    print(f"[load] items found: {len(item_qids)}; type QIDs touched: {len(type_qid_set)}",
          flush=True)

    print("[meta] fetching item labels|aliases|sitelinks/urls …", flush=True)
    item_meta = fetch_metadata(item_qids, "labels|aliases|sitelinks/urls")
    print("[meta] fetching type labels …", flush=True)
    type_meta = fetch_metadata(type_qid_set, "labels")

    records: list[dict] = []
    for q in item_qids:
        meta = item_meta.get(q, {})
        labels_map = meta.get("labels", {})
        label = (
            labels_map.get("en", {}).get("value")
            or labels_map.get("mul", {}).get("value")
        )
        aliases = [a["value"] for a in meta.get("aliases", {}).get("en", [])]
        sl = meta.get("sitelinks", {}).get("enwiki")
        enwiki = sl.get("title") if sl else item_to_enwiki.get(q)

        types = []
        for tq in sorted(item_to_types.get(q, ())):
            tlmap = type_meta.get(tq, {}).get("labels", {})
            tlabel = (
                tlmap.get("en", {}).get("value")
                or tlmap.get("mul", {}).get("value")
            )
            types.append({"qid": tq, "label": tlabel})

        records.append({
            "qid": q,
            "label": label,
            "aliases": aliases,
            "enwiki_title": enwiki,
            "instance_of": types,
        })

    out_path = OUT_DIR / f"wikidata_pl_items.{today}.jsonl"
    with out_path.open("w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    n_in_p1195 = sum(1 for r in records if r["qid"] in p1195_qids)
    n_new = len(records) - n_in_p1195

    manifest = {
        "snapshot_date": today,
        "items_total": len(records),
        "items_in_p1195": n_in_p1195,
        "items_new_vs_p1195": n_new,
        "type_qids_input": len(type_qids),
        "type_qids_with_instances": len(type_qid_set),
        "source": {
            "wdqs": WDQS,
            "wbapi": WBAPI,
            "query": Q_ITEMS_BY_TYPE.strip(),
            "chunk_size": CHUNK_SIZE,
        },
    }
    (OUT_DIR / f"wikidata_pl_items.{today}.manifest.json").write_text(
        json.dumps(manifest, indent=2)
    )
    print(f"[done] wrote {out_path}", flush=True)
    print(f"       items total:      {len(records)}", flush=True)
    print(f"       already in P1195: {n_in_p1195}", flush=True)
    print(f"       NEW vs P1195:     {n_new}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
