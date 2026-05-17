#!/usr/bin/env python3
"""Generate `data/derived/pl_candidates.csv` — Wikidata items that look like
PLs but aren't `instance_of programming-language (Q9143)` and aren't yet
in `data/pl_list.txt`.

Moderate filter (rationale: keep precision via the Wikipedia-article
requirement, broaden recall to file-format families so canonical
entries like PDF, SVG, JSON, RSS land in the candidates list):

- `instance_of` contains one of:
    Q37045    markup language
    Q1144882  query language
    Q3071980  data interchange format
    Q174923   serialization format
    Q199897   domain-specific language
    Q1135808  specification language
    Q1330336  stylesheet language
    Q235557   file format
    Q26085352 file format family
    Q24566596 text-based file format
    Q24451526 data format
    Q694975   electronic document
- has an enwiki sitelink (means there's a Wikipedia article)
- canonical name (case-insensitive) is NOT already in pl_list.txt

Reads:
  - data/raw/wikidata_p1195.<YYYY-MM-DD>.jsonl   (most recent)
  - data/pl_list.txt

Writes:
  - data/derived/pl_candidates.csv  (one row per candidate; refresh in place)

Run:
  python3 tools/build_pl_candidates.py
"""
from __future__ import annotations
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PL_LIST = ROOT / "data" / "pl_list.txt"
PL_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "pl.csv"
PL_ALIAS_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "pl_alias.csv"
RAW_DIR = ROOT / "data" / "raw"
OUT_CSV = ROOT / "data" / "derived" / "pl_candidates.csv"

STRICT_INSTANCE_QIDS = {
    # Pure-PL-shaped categories (high precision).
    "Q37045":    "markup language",
    "Q1144882":  "query language",
    "Q3071980":  "data interchange format",
    "Q174923":   "serialization format",
    "Q199897":   "domain-specific language",
    "Q1135808":  "specification language",
    "Q1330336":  "stylesheet language",
    # Broader file-format categories — needed so canonical entries like
    # PDF (Q42332), SVG (Q2078), JSON (Q2063), RSS (Q45432) land in the
    # candidates list. The enwiki-sitelink + alias dedup filter keeps the
    # noise (codecs, vendor-proprietary binaries) manageable.
    "Q235557":   "file format",
    "Q26085352": "file format family",
    "Q24566596": "text-based file format",
    "Q24451526": "data format",
    "Q694975":   "electronic document",
}


def _latest_snapshot(pattern: str) -> Path | None:
    paths = sorted(RAW_DIR.glob(pattern))
    return paths[-1] if paths else None


def main() -> int:
    p_list_path = PL_LIST
    if not p_list_path.exists():
        raise SystemExit(f"ERROR: {p_list_path} not found.")
    existing = {ln.strip().lower() for ln in p_list_path.read_text(encoding="utf-8").splitlines() if ln.strip()}
    # Also exclude PLs known to pl.csv (the much larger taxonomy derived from
    # upstream sources). Without this, /candidates/ leaks Q's like Q2115
    # (XML) — present in master_inventory via Linguist/PLDB but not in the
    # LLM-curated pl_list.txt. Two dedup signals:
    #   - canonical names + aliases from pl.csv / pl_alias.csv
    #   - wikidata_qid already attached to a pl_row (Phase B + Phase C)
    attached_qids: set[str] = set()
    if PL_CSV.exists():
        for r in csv.DictReader(PL_CSV.open(encoding="utf-8")):
            cn = (r.get("canonical_name") or "").strip().lower()
            if cn:
                existing.add(cn)
            q = (r.get("wikidata_qid") or "").strip()
            if q:
                attached_qids.add(q)
    if PL_ALIAS_CSV.exists():
        for r in csv.DictReader(PL_ALIAS_CSV.open(encoding="utf-8")):
            a = (r.get("alias") or "").strip().lower()
            if a:
                existing.add(a)

    snap = _latest_snapshot("wikidata_p1195.*.jsonl")
    if not snap:
        raise SystemExit("ERROR: no wikidata_p1195.*.jsonl snapshot under data/raw/.")
    print(f"Reading snapshot: {snap.name}")

    rows: list[dict] = []
    for line in snap.open(encoding="utf-8"):
        if not line.strip():
            continue
        rec = json.loads(line)
        instance_qids = {io["qid"] for io in (rec.get("instance_of") or [])}
        if "Q9143" in instance_qids:
            continue  # already counted as a PL
        if not (instance_qids & set(STRICT_INSTANCE_QIDS.keys())):
            continue
        if not rec.get("enwiki_title"):
            continue
        # Drop Q's already attached to an existing pl_row (Phase B or C).
        if rec.get("qid", "") in attached_qids:
            continue
        label = (rec.get("label") or "").strip()
        if not label:
            continue
        if label.lower() in existing:
            continue
        # Aliases that ARE in pl_list also disqualify (avoid duplicates) —
        # but only when the alias is at least 4 characters. Short Wikidata
        # aliases are often noise (e.g. "jj" for RSS, "ai" for Adobe
        # Illustrator) and case-insensitively collide with unrelated 2-3
        # char PLs in pl_list.txt. The maintainer would notice a real
        # duplicate at PR-review time anyway.
        aliases = [(a or "").strip() for a in (rec.get("aliases") or [])]
        if any(a.lower() in existing for a in aliases if a and len(a) >= 4):
            continue

        extensions = []
        for ext_entry in rec.get("extensions") or []:
            v = ext_entry["value"] if isinstance(ext_entry, dict) else str(ext_entry)
            v = v.strip().lstrip(".")
            if v:
                extensions.append("." + v.lower())

        # Subset of instance_of that matched (for sortability + display).
        matched_io = sorted(
            STRICT_INSTANCE_QIDS[q] for q in instance_qids if q in STRICT_INSTANCE_QIDS
        )
        all_io = "; ".join(io["label"] for io in (rec.get("instance_of") or []))

        rows.append({
            "qid": rec["qid"],
            "label": label,
            "description": (rec.get("description") or "").strip(),
            "aliases": "; ".join(a for a in aliases if a),
            "enwiki_title": rec.get("enwiki_title") or "",
            "wikipedia_url": (
                f"https://en.wikipedia.org/wiki/" +
                (rec.get("enwiki_title") or "").replace(" ", "_")
            ),
            "wikidata_url": f"https://www.wikidata.org/wiki/{rec['qid']}",
            "extensions": "; ".join(extensions),
            "matched_pl_kind": "; ".join(matched_io),
            "instance_of_labels": all_io,
            "mime_types": "; ".join(rec.get("mime_types") or []),
        })

    rows.sort(key=lambda r: (r["matched_pl_kind"], r["label"].lower()))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "qid", "label", "description", "aliases", "enwiki_title",
        "wikipedia_url", "wikidata_url", "extensions",
        "matched_pl_kind", "instance_of_labels", "mime_types",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} ({len(rows)} candidates).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
