#!/usr/bin/env python3
"""Enrich a single `languages/<Name>/meta.json` with Wikipedia + Wikidata.

When a new PL is proposed via /contribute/add-pl/, the submitter typically
only provides a canonical name + one evidence URL. This script "activates"
the existing data-source extractors *for that specific PL*: it queries
Wikipedia (opensearch) and Wikidata (wbsearchentities) for matching
entries, then writes the discovered URLs back into the PL's meta.json.

The downstream build then surfaces them on the per-PL page just like any
upstream-source link.

Usage:
    # Single PL (canonical name match against the languages/ dir).
    python3 tools/enrich_pl_meta.py --name "Attribute-Relation File Format"

    # All in-repo PLs missing `wikipedia_url` or `wikidata_qid`.
    python3 tools/enrich_pl_meta.py --all

    # Dry-run: show what would be added; don't touch meta.json.
    python3 tools/enrich_pl_meta.py --name "PGN" --dry-run

Notes:
- Live API calls. Respect rate limits — sleep 1s between calls, identify
  via a project User-Agent.
- Match quality: we accept a Wikipedia article whose title (or one of its
  redirects, when the API surfaces them) equals the PL name or an alias
  (case-insensitive); otherwise we record `wikipedia_url = null` and a
  short list of `wikipedia_candidates` so a maintainer can pick.
- Wikidata: prefer entities whose `instance of` includes file-format /
  programming-language / data-format / markup-language / query-language
  Q-ids; record the top candidate's Q-id.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES_DIR = ROOT / "languages"
UA = (
    "PL-ext-explorer/0.1 enrich_pl_meta "
    "(https://github.com/acherm/PL-ultimate-llm; mathieu.acher@irisa.fr)"
)
MWAPI = "https://en.wikipedia.org/w/api.php"
WBAPI = "https://www.wikidata.org/w/api.php"

# Wikidata Q-ids we treat as "this entity is the kind of thing we care
# about." Anything whose `instance of` overlaps these is preferred.
RELEVANT_INSTANCE_QIDS = {
    "Q9143",     # programming language
    "Q235557",   # file format
    "Q24451526", # data format
    "Q37045",    # markup language
    "Q1144882",  # query language
    "Q3071980",  # data interchange format
    "Q174923",   # serialization format
    "Q24566596", # text-based file format
}


def _http_get(url: str, params: dict, timeout: int = 20) -> dict:
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{url}?{qs}",
        headers={"Accept": "application/json", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def wikipedia_search(name: str, *, limit: int = 5) -> list[dict]:
    """Wikipedia opensearch + per-title summary. Returns top-k candidates."""
    try:
        data = _http_get(MWAPI, {
            "action": "opensearch",
            "search": name,
            "limit": str(limit),
            "format": "json",
            "namespace": "0",
        })
    except Exception as e:
        print(f"  [warn] wikipedia opensearch failed: {e}", file=sys.stderr)
        return []
    # opensearch returns [query, [titles], [descs], [urls]]
    if not isinstance(data, list) or len(data) < 4:
        return []
    titles, descs, urls = data[1], data[2], data[3]
    return [
        {"title": t, "description": d, "url": u}
        for t, d, u in zip(titles, descs, urls)
    ]


def _normalize_for_match(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def pick_wikipedia(name: str, aliases: list[str],
                   candidates: list[dict]) -> tuple[dict | None, list[dict]]:
    """Return (best_match_or_None, all_candidates).

    Best-match rule: title (case-insensitive, space-collapsed) equals the
    canonical name or any alias. If multiple match, keep the first
    candidate in opensearch order.
    """
    targets = {_normalize_for_match(name)}
    targets |= {_normalize_for_match(a) for a in aliases if a}
    for c in candidates:
        if _normalize_for_match(c["title"]) in targets:
            return c, candidates
    return None, candidates


def wikidata_search(name: str, *, limit: int = 5) -> list[dict]:
    """Wikidata wbsearchentities. Returns [{id, label, description}, ...]."""
    try:
        data = _http_get(WBAPI, {
            "action": "wbsearchentities",
            "search": name,
            "language": "en",
            "type": "item",
            "limit": str(limit),
            "format": "json",
        })
    except Exception as e:
        print(f"  [warn] wikidata wbsearchentities failed: {e}", file=sys.stderr)
        return []
    return [
        {
            "id": r.get("id", ""),
            "label": r.get("label", ""),
            "description": r.get("description", ""),
            "url": f"https://www.wikidata.org/wiki/{r.get('id', '')}",
        }
        for r in data.get("search", [])
    ]


def wikidata_get_instance_of(qid: str) -> set[str]:
    """Return the set of `instance of` (P31) Q-ids for an entity."""
    try:
        data = _http_get(WBAPI, {
            "action": "wbgetentities",
            "ids": qid,
            "props": "claims",
            "languages": "en",
            "format": "json",
        })
    except Exception as e:
        print(f"  [warn] wikidata wbgetentities({qid}) failed: {e}", file=sys.stderr)
        return set()
    out: set[str] = set()
    ent = (data.get("entities") or {}).get(qid) or {}
    for claim in (ent.get("claims") or {}).get("P31", []) or []:
        try:
            v = claim["mainsnak"]["datavalue"]["value"]["id"]
            out.add(v)
        except Exception:
            continue
    return out


def pick_wikidata(name: str, aliases: list[str],
                  candidates: list[dict]) -> tuple[dict | None, list[dict]]:
    """Return (best_match_or_None, all_candidates).

    Best-match rule:
      1. Filter candidates whose `instance of` overlaps RELEVANT_INSTANCE_QIDS.
      2. Among those, prefer entities whose label matches the canonical name
         or any alias (case-insensitive); else the top remaining.
      3. If nothing matches the relevant-instance filter, fall back to
         "label matches exactly" without the instance-of filter.
    """
    targets = {_normalize_for_match(name)}
    targets |= {_normalize_for_match(a) for a in aliases if a}

    relevant: list[dict] = []
    for c in candidates:
        if not c["id"]:
            continue
        time.sleep(0.5)
        instance_qids = wikidata_get_instance_of(c["id"])
        c["instance_of"] = sorted(instance_qids)
        if instance_qids & RELEVANT_INSTANCE_QIDS:
            relevant.append(c)

    # 2: label match within relevant
    for c in relevant:
        if _normalize_for_match(c["label"]) in targets:
            return c, candidates
    # 2b: any relevant (highest WBsearch rank)
    if relevant:
        return relevant[0], candidates
    # 3: fallback to a strict label match outside the relevant filter
    for c in candidates:
        if _normalize_for_match(c["label"]) in targets:
            return c, candidates
    return None, candidates


def enrich_one(meta_path: Path, *, dry_run: bool = False) -> dict:
    """Enrich the meta.json at `meta_path`. Returns the diff dict."""
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    name = meta.get("name") or meta_path.parent.name
    aliases = list(meta.get("aliases") or [])
    print(f"\nEnriching: {name}  ({meta_path.relative_to(ROOT)})")

    diff: dict = {}

    if not meta.get("wikipedia_url"):
        wp_cands = wikipedia_search(name)
        time.sleep(1.0)
        best, all_cands = pick_wikipedia(name, aliases, wp_cands)
        if best:
            diff["wikipedia_url"] = best["url"]
            diff["wikipedia_title"] = best["title"]
            print(f"  wikipedia: {best['title']}  →  {best['url']}")
        else:
            cand_short = [{"title": c["title"], "url": c["url"]} for c in all_cands[:3]]
            diff["wikipedia_candidates"] = cand_short
            print(f"  wikipedia: no exact match (recorded {len(cand_short)} candidates)")

    if not meta.get("wikidata_qid"):
        wd_cands = wikidata_search(name)
        time.sleep(1.0)
        best, all_cands = pick_wikidata(name, aliases, wd_cands)
        if best:
            diff["wikidata_qid"] = best["id"]
            diff["wikidata_url"] = best["url"]
            diff["wikidata_label"] = best["label"]
            print(f"  wikidata:  {best['id']} {best['label']}  →  {best['url']}")
        else:
            cand_short = [{"id": c["id"], "label": c["label"], "url": c["url"]} for c in all_cands[:3]]
            diff["wikidata_candidates"] = cand_short
            print(f"  wikidata:  no relevant match (recorded {len(cand_short)} candidates)")

    if not diff:
        print("  (nothing to enrich — wikipedia_url + wikidata_qid already set)")
        return {}

    if dry_run:
        print("  (dry-run; meta.json NOT written)")
        return diff

    meta.update(diff)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {meta_path.relative_to(ROOT)}")
    return diff


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--name", help="Canonical name (matches languages/<Name>/meta.json's `name`).")
    g.add_argument("--dir", help="Direct directory under languages/ (e.g., Attribute-Relation_File_Format).")
    g.add_argument("--all", action="store_true", help="Enrich every meta.json missing wikipedia_url or wikidata_qid.")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, default=200, help="Cap on --all to keep rate-limits sane.")
    args = p.parse_args()

    if args.all:
        candidates: list[Path] = []
        for d in sorted(LANGUAGES_DIR.iterdir()):
            mp = d / "meta.json"
            if not mp.exists():
                continue
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if not m.get("wikipedia_url") or not m.get("wikidata_qid"):
                candidates.append(mp)
            if len(candidates) >= args.limit:
                break
        print(f"--all: {len(candidates)} meta.json files to consider (limit={args.limit}).")
        for mp in candidates:
            try:
                enrich_one(mp, dry_run=args.dry_run)
            except Exception as e:
                print(f"  [error] {mp.relative_to(ROOT)}: {e}", file=sys.stderr)
        return 0

    if args.dir:
        meta_path = LANGUAGES_DIR / args.dir / "meta.json"
        if not meta_path.exists():
            sys.exit(f"ERROR: {meta_path} not found.")
    else:
        # Resolve canonical name to a directory by reading every meta.json.
        meta_path = None
        for d in LANGUAGES_DIR.iterdir():
            mp = d / "meta.json"
            if not mp.exists():
                continue
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if (m.get("name") or "").strip() == args.name.strip():
                meta_path = mp
                break
        if not meta_path:
            sys.exit(f"ERROR: no meta.json with name=={args.name!r} under {LANGUAGES_DIR}.")

    enrich_one(meta_path, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
