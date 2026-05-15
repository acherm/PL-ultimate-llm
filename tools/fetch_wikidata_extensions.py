#!/usr/bin/env python3
"""Pull every Wikidata item carrying P1195 (file extension).

Output: data/raw/wikidata_p1195.<YYYY-MM-DD>.jsonl — one JSON object per item.

Strategy: three narrow SPARQL queries for the relational rows, then a
batched wbgetentities pass for labels, descriptions, aliases, and
sitelinks. Each call comfortably fits under the WDQS 60s timeout.

This is a refresh extractor in the same spirit as Linguist's languages.yml
fetcher: the JSONL it writes is the pinned snapshot the rest of the build
reads from.
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
    """Strip Wikidata entity / property URI prefix."""
    return uri.rsplit("/", 1)[-1] if uri.startswith("http") else uri


# ---------------------------------------------------------------------------
# SPARQL queries
# ---------------------------------------------------------------------------

Q_EXT = """
SELECT ?item ?stmt ?ext ?rank WHERE {
  ?item p:P1195 ?stmt .
  ?stmt ps:P1195 ?ext .
  ?stmt wikibase:rank ?rank .
}
"""

# Qualifiers on P1195 statements (only ~93 statements have any; thin)
Q_QUAL = """
SELECT ?stmt ?qProp ?qVal WHERE {
  ?item p:P1195 ?stmt .
  ?stmt ?qProp ?qVal .
  FILTER(STRSTARTS(STR(?qProp), "http://www.wikidata.org/prop/qualifier/"))
}
"""

# Notes on `p:` vs `wdt:`:
#   `wdt:P1195` returns only Normal/Preferred-rank statements (the "truthy"
#   view). Deprecated-rank statements are excluded — but they exist in the
#   wild for legitimate items: e.g. Python (Q28865) carries ALL of its
#   filename-extension statements at Deprecated rank, presumably because
#   none are officially-standardized by python.org. We *do* want those in
#   our snapshot (Q_EXT already uses p:P1195 to capture them with rank).
#   Joins downstream of P1195 must therefore also use `p:P1195 []` to keep
#   the same item set — otherwise Python loses its instance_of and falls
#   out of the PL filter in the taxonomy build.
Q_MIME = """
SELECT ?item ?mime WHERE {
  ?item p:P1195 [] ; wdt:P1163 ?mime .
}
"""

Q_TYPE = """
SELECT ?item ?type WHERE {
  ?item p:P1195 [] ; wdt:P31 ?type .
}
"""

# Transitive subclass closure of "programming language" (Q9143) and adjacent
# top-level concepts we treat as PL-shaped (markup, query, logic, esoteric).
# Saved as a separate snapshot so the downstream build can filter the
# P1195-bearing items to PLs without a live SPARQL call.
PL_TYPE_ROOTS = [
    ("Q9143",     "programming language"),
    ("Q37045",    "markup language"),
    ("Q3334629",  "query language"),
    ("Q1418502",  "logic programming language"),
    ("Q56062429", "esoteric programming language"),
]

Q_PL_TYPE_CLOSURE = """
SELECT DISTINCT ?cls WHERE {{
  ?cls wdt:P279* wd:{root} .
}}
"""


def fetch_sparql_tables() -> dict:
    print("[sparql] P1195 extension rows …", flush=True)
    ext_rows = sparql(Q_EXT)
    print(f"         {len(ext_rows)} rows", flush=True)

    print("[sparql] P1195 qualifier rows …", flush=True)
    qual_rows = sparql(Q_QUAL)
    print(f"         {len(qual_rows)} rows", flush=True)

    print("[sparql] P1163 (MIME) rows …", flush=True)
    mime_rows = sparql(Q_MIME)
    print(f"         {len(mime_rows)} rows", flush=True)

    print("[sparql] P31 (instance of) rows …", flush=True)
    type_rows = sparql(Q_TYPE)
    print(f"         {len(type_rows)} rows", flush=True)

    return {"ext": ext_rows, "qual": qual_rows, "mime": mime_rows, "type": type_rows}


# ---------------------------------------------------------------------------
# wbgetentities — labels, descriptions, aliases, sitelinks
# ---------------------------------------------------------------------------

def wbgetentities(qids: list[str], props: str) -> dict:
    """Returns the 'entities' dict from action=wbgetentities.

    We fetch both `en` and `mul` (Wikidata's "multilingual / language-neutral"
    code, used for things like C++ or Python whose name is the same in every
    language) so that an `en` miss can fall back to `mul`.
    """
    res = http_get(WBAPI, {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": props,
        "languages": "en|mul",
        "format": "json",
    })
    return res.get("entities", {})


def fetch_metadata(qids: list[str], props: str, batch_size: int = 50, sleep: float = 0.05) -> dict:
    out: dict = {}
    total = len(qids)
    for i in range(0, total, batch_size):
        chunk = qids[i : i + batch_size]
        entities = wbgetentities(chunk, props)
        out.update(entities)
        if i % 500 == 0:
            print(f"         {min(i + batch_size, total)}/{total}", flush=True)
        time.sleep(sleep)
    return out


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def build_records(rows: dict, item_meta: dict, type_meta: dict) -> list[dict]:
    # statement -> (item, ext, rank)
    stmt_to_ext: dict[str, dict] = {}
    item_stmts: dict[str, list[str]] = defaultdict(list)
    for r in rows["ext"]:
        item = short(r["item"]["value"])
        stmt = r["stmt"]["value"]
        ext_val = r["ext"]["value"]
        rank = short(r["rank"]["value"])  # e.g. NormalRank / DeprecatedRank
        stmt_to_ext[stmt] = {"item": item, "ext": ext_val, "rank": rank, "qualifiers": []}
        item_stmts[item].append(stmt)

    # attach qualifiers
    for r in rows["qual"]:
        stmt = r["stmt"]["value"]
        if stmt not in stmt_to_ext:
            continue  # qualifier on a statement that isn't a P1195 we kept (shouldn't happen)
        qprop = short(r["qProp"]["value"])
        qval_raw = r["qVal"]["value"]
        # qVal can be entity URI or literal — keep raw value, strip entity prefix
        qval = short(qval_raw) if qval_raw.startswith("http://www.wikidata.org/entity/") else qval_raw
        stmt_to_ext[stmt]["qualifiers"].append({"property": qprop, "value": qval})

    # item -> [mimes]
    item_mimes: dict[str, list[str]] = defaultdict(list)
    for r in rows["mime"]:
        item = short(r["item"]["value"])
        mime = r["mime"]["value"]
        if mime not in item_mimes[item]:
            item_mimes[item].append(mime)

    # item -> [type qids]
    item_types: dict[str, list[str]] = defaultdict(list)
    for r in rows["type"]:
        item = short(r["item"]["value"])
        tq = short(r["type"]["value"])
        if tq not in item_types[item]:
            item_types[item].append(tq)

    # build records, sorted by QID numeric value
    def qid_num(qid: str) -> int:
        try:
            return int(qid[1:])
        except ValueError:
            return 0

    records = []
    for item in sorted(item_stmts.keys(), key=qid_num):
        meta = item_meta.get(item, {})
        labels_map = meta.get("labels", {})
        label = (
            labels_map.get("en", {}).get("value")
            or labels_map.get("mul", {}).get("value")
        )
        desc = meta.get("descriptions", {}).get("en", {}).get("value")
        aliases = [a["value"] for a in meta.get("aliases", {}).get("en", [])]
        enwiki = None
        sl = meta.get("sitelinks", {}).get("enwiki")
        if sl:
            enwiki = sl.get("title")

        types = []
        for tq in item_types.get(item, []):
            tlmap = type_meta.get(tq, {}).get("labels", {})
            tlabel = (
                tlmap.get("en", {}).get("value")
                or tlmap.get("mul", {}).get("value")
            )
            types.append({"qid": tq, "label": tlabel})

        extensions = []
        for stmt in item_stmts[item]:
            row = stmt_to_ext[stmt]
            extensions.append({
                "value": row["ext"],
                "rank": row["rank"],
                "qualifiers": row["qualifiers"],
            })

        records.append({
            "qid": item,
            "label": label,
            "description": desc,
            "aliases": aliases,
            "extensions": extensions,
            "mime_types": item_mimes.get(item, []),
            "instance_of": types,
            "enwiki_title": enwiki,
        })

    return records


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    today = dt.date.today().isoformat()
    rows = fetch_sparql_tables()

    # Save raw SPARQL results for reproducibility / debugging.
    for name, data in rows.items():
        (RAW_DIR / f"sparql_{name}.{today}.json").write_text(json.dumps(data))

    item_qids = sorted({short(r["item"]["value"]) for r in rows["ext"]})
    type_qids = sorted({short(r["type"]["value"]) for r in rows["type"]})
    print(f"[meta]  unique items: {len(item_qids)}, unique types: {len(type_qids)}", flush=True)

    print("[meta]  fetching item metadata (labels|descriptions|aliases|sitelinks/enwiki) …", flush=True)
    item_meta = fetch_metadata(item_qids, "labels|descriptions|aliases|sitelinks/urls")
    print("[meta]  fetching type labels …", flush=True)
    type_meta = fetch_metadata(type_qids, "labels")

    records = build_records(rows, item_meta, type_meta)
    out_path = OUT_DIR / f"wikidata_p1195.{today}.jsonl"
    with out_path.open("w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ── PL-type closure ─────────────────────────────────────────────────────
    # Save the transitive P279 closure of every PL-shaped root QID, so the
    # downstream taxonomy build can filter P1195-bearing items to PLs without
    # a live SPARQL call. Each PL root keeps its own QID list for audit.
    print("[sparql] PL-type closures (P279*) for each root …", flush=True)
    pl_type_qids: set[str] = set()
    closures: dict[str, list[str]] = {}
    for root_qid, root_label in PL_TYPE_ROOTS:
        rows_cls = sparql(Q_PL_TYPE_CLOSURE.format(root=root_qid))
        cls_qids = sorted({short(r["cls"]["value"]) for r in rows_cls})
        closures[root_qid] = cls_qids
        pl_type_qids.update(cls_qids)
        print(f"         {root_qid} ({root_label}): {len(cls_qids)} subclasses", flush=True)
    pl_types_payload = {
        "snapshot_date": today,
        "roots": [{"qid": q, "label": l} for q, l in PL_TYPE_ROOTS],
        "pl_type_qids": sorted(pl_type_qids),
        "by_root": closures,
        "query": Q_PL_TYPE_CLOSURE.strip(),
    }
    pl_types_path = OUT_DIR / f"wikidata_pl_types.{today}.json"
    pl_types_path.write_text(json.dumps(pl_types_payload, indent=2))
    print(f"         wrote {pl_types_path}  (total unique QIDs: {len(pl_type_qids)})", flush=True)

    # Also drop a small manifest with counts.
    manifest = {
        "snapshot_date": today,
        "items": len(records),
        "ext_statements": sum(len(r["extensions"]) for r in records),
        "items_with_enwiki": sum(1 for r in records if r["enwiki_title"]),
        "items_with_mime": sum(1 for r in records if r["mime_types"]),
        "statements_with_qualifiers": sum(
            1 for r in records for e in r["extensions"] if e["qualifiers"]
        ),
        "source": {
            "wdqs": WDQS,
            "wbapi": WBAPI,
            "queries": {"ext": Q_EXT, "qual": Q_QUAL, "mime": Q_MIME, "type": Q_TYPE},
        },
    }
    (OUT_DIR / f"wikidata_p1195.{today}.manifest.json").write_text(
        json.dumps(manifest, indent=2)
    )
    print(f"[done]  wrote {out_path}", flush=True)
    print(f"        items={manifest['items']}  ext_stmts={manifest['ext_statements']}  "
          f"enwiki={manifest['items_with_enwiki']}  mime={manifest['items_with_mime']}  "
          f"qualified={manifest['statements_with_qualifiers']}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
