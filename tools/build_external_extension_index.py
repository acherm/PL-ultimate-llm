#!/usr/bin/env python3
"""Build the non-PL extension index from the pinned Wikidata + Wikipedia snapshots.

This is the "anything with a filename extension that isn't a programming
language" side artifact. It feeds the extension-labelling form on the site
(`/ext/<slug>/`) with friendly_name / reference_url / MIME / suggested-label
hints when a reviewer is labelling an extension whose owner is a file
format (MP3, ZIP, PNG, …) rather than a PL.

Inputs (pinned snapshots, refreshed by `tools/fetch_wikidata_extensions.py`
and `tools/fetch_wikipedia_infoboxes.py`):
  data/raw/wikidata_p1195.<date>.jsonl
  data/raw/wikipedia_infobox.<date>.jsonl

Plus, to know what's already in the PL taxonomy and should be excluded:
  data/derived/pl_taxonomy/pl.csv

Output:
  data/derived/external_extension_index.csv

Each row is one (extension, Wikidata item) pair. Items with multiple
extensions get multiple rows. Polysemy is preserved — `.xml` will appear
in dozens of rows, one per claimant — and downstream code can rank or
filter as it sees fit.

Schema
------
  ext                  e.g. "mp3" (no leading dot, lowercased)
  source               "wikidata" | "wikipedia" — origin of the extension claim
                       ("wikipedia" means the claim came only from the
                       parsed enwiki infobox, not from Wikidata's P1195)
  qid                  Wikidata item QID (e.g. "Q42591")
  label                Wikidata English label (e.g. "MP3")
  description          one-line Wikidata description
  aliases              semicolon-joined alternative names
  enwiki_title         English Wikipedia article title (may be empty)
  wikidata_url         https://www.wikidata.org/wiki/<qid>
  wikipedia_url        https://en.wikipedia.org/wiki/<title> (empty if no sitelink)
  mime_types           semicolon-joined MIME types from Wikidata (P1163)
  instance_of_labels   semicolon-joined English labels of P31 values
  suggested_label      best-guess controlled-vocab label (binary:audio etc.)
                       Empty when no rule matched — that's the signal for the
                       reviewer to label by hand.
  wikidata_rank        Wikidata statement rank (normal/preferred/deprecated)
                       Empty when source="wikipedia".
  wikipedia_note       Per-line note parsed from the infobox value
                       (e.g. "rarely", "before 1995"). Empty when none.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DERIVED_DIR = ROOT / "data" / "derived"
PL_CSV = DERIVED_DIR / "pl_taxonomy" / "pl.csv"


# ---------------------------------------------------------------------------
# Heuristic mapping: Wikidata instance_of labels → controlled vocabulary
# label from docs/extension_labels.md.
# ---------------------------------------------------------------------------
# Substring match against lowercased instance_of labels. First rule wins.
# Empty result means "we don't have a confident suggestion" — the reviewer
# still has to choose. This list is intentionally short; extend per
# experience as the labelling queue gets used.
SUGGESTED_LABEL_RULES = [
    # binary:audio
    ("audio file format", "binary:audio"),
    ("audio compression", "binary:audio"),
    ("lossy audio coding format", "binary:audio"),
    ("lossless audio coding format", "binary:audio"),
    ("music file format", "binary:audio"),
    # binary:video
    ("video file format", "binary:video"),
    ("video coding format", "binary:video"),
    ("lossy video coding format", "binary:video"),
    ("digital container format", "binary:video"),
    ("multimedia container", "binary:video"),
    # binary:image
    ("raster-graphics file format", "binary:image"),
    ("raster graphics file format", "binary:image"),
    ("vector graphics file format", "binary:image"),
    ("image file format", "binary:image"),
    ("graphics file format", "binary:image"),
    # binary:archive
    ("archive file format", "binary:archive"),
    ("compression format", "binary:archive"),
    # binary:font
    ("font file format", "binary:font"),
    # binary:executable
    ("executable file format", "binary:executable"),
    # binary:db
    ("database file", "binary:db"),
    ("database management system file", "binary:db"),
    # data:xml-like
    ("xml-based format", "data:xml-like"),
    # data:domain (catch-all for raw image, 3D, scientific, etc.)
    ("raw image format", "data:domain"),
    # docs (markup languages excluded because they're treated as PLs and live
    # in pl.csv; the few that don't match a pl_id stay unsuggested here).
    # data:domain — broad domain-specific
    ("disk image format", "binary:other"),
    ("rom image", "binary:other"),
    # document
    ("document file format", "binary:other"),
]


def suggest_label(instance_of_labels: list[str]) -> str:
    """Return the first controlled-vocab label whose rule's substring is
    in any instance_of label. Empty when nothing matches.
    """
    lowered = [(lbl or "").lower() for lbl in instance_of_labels]
    for needle, target in SUGGESTED_LABEL_RULES:
        if any(needle in lbl for lbl in lowered):
            return target
    return ""


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _latest(pattern: str) -> Path | None:
    matches = sorted(RAW_DIR.glob(pattern))
    return matches[-1] if matches else None


def load_wikidata() -> list[dict]:
    path = _latest("wikidata_p1195.*.jsonl")
    if path is None:
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_wikipedia_by_qid() -> dict[str, dict]:
    path = _latest("wikipedia_infobox.*.jsonl")
    if path is None:
        return {}
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("qid"):
                out[r["qid"]] = r
    return out


def load_taxonomy_qids() -> set[str]:
    """Wikidata QIDs already attached to a pl_id in the taxonomy build."""
    if not PL_CSV.exists():
        return set()
    out: set[str] = set()
    with PL_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q = (r.get("wikidata_qid") or "").strip()
            if q:
                out.add(q)
    return out


def _norm_ext(value: str | None) -> str:
    s = (value or "").strip().lower().lstrip(".")
    return s


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_rows(
    wikidata_records: list[dict],
    wikipedia_by_qid: dict[str, dict],
    taxonomy_qids: set[str],
) -> list[dict]:
    rows: list[dict] = []
    n_skipped_pl = 0
    for rec in wikidata_records:
        qid = rec.get("qid") or ""
        if qid in taxonomy_qids:
            n_skipped_pl += 1
            continue

        label = rec.get("label") or ""
        description = rec.get("description") or ""
        aliases = rec.get("aliases") or []
        enwiki = rec.get("enwiki_title") or ""
        mime_types = rec.get("mime_types") or []
        types_labels = [(t.get("label") or "") for t in rec.get("instance_of") or []]
        types_qids = [(t.get("qid") or "") for t in rec.get("instance_of") or []]
        wikidata_url = f"https://www.wikidata.org/wiki/{qid}" if qid else ""
        wikipedia_url = (
            f"https://en.wikipedia.org/wiki/{enwiki.replace(' ', '_')}"
            if enwiki else ""
        )
        suggested = suggest_label(types_labels)

        # Wikidata-sourced extensions
        wd_exts_seen: set[str] = set()
        for e in rec.get("extensions") or []:
            ext = _norm_ext(e.get("value"))
            if not ext or ext in wd_exts_seen:
                continue
            wd_exts_seen.add(ext)
            rows.append({
                "ext": ext,
                "source": "wikidata",
                "qid": qid,
                "label": label,
                "description": description,
                "aliases": "; ".join(aliases),
                "enwiki_title": enwiki,
                "wikidata_url": wikidata_url,
                "wikipedia_url": wikipedia_url,
                "mime_types": "; ".join(mime_types),
                "instance_of_labels": "; ".join(types_labels),
                "instance_of_qids": "; ".join(types_qids),
                "suggested_label": suggested,
                "wikidata_rank": _rank_short(e.get("rank")),
                "wikipedia_note": "",
            })

        # Wikipedia-only extensions (parsed from infobox), only when the
        # Wikipedia article surfaces an extension Wikidata doesn't carry.
        wp_rec = wikipedia_by_qid.get(qid)
        if not wp_rec:
            continue
        wp_seen: set[str] = set()
        for hit in wp_rec.get("infobox_hits") or []:
            for parsed in hit.get("parsed") or []:
                ext = _norm_ext(parsed.get("value"))
                if not ext or ext in wp_seen:
                    continue
                wp_seen.add(ext)
                if ext in wd_exts_seen:
                    continue  # already covered by the Wikidata row above
                rows.append({
                    "ext": ext,
                    "source": "wikipedia",
                    "qid": qid,
                    "label": label,
                    "description": description,
                    "aliases": "; ".join(aliases),
                    "enwiki_title": enwiki,
                    "wikidata_url": wikidata_url,
                    "wikipedia_url": wikipedia_url,
                    "mime_types": "; ".join(mime_types),
                    "instance_of_labels": "; ".join(types_labels),
                    "instance_of_qids": "; ".join(types_qids),
                    "suggested_label": suggested,
                    "wikidata_rank": "",
                    "wikipedia_note": (parsed.get("note") or "").strip(),
                })

    print(f"[index] kept {len(rows)} (ext, item) pairs from "
          f"{len(wikidata_records) - n_skipped_pl} non-PL Wikidata items "
          f"(excluded {n_skipped_pl} already in pl.csv)", flush=True)
    return rows


def _rank_short(rank: str | None) -> str:
    if not rank:
        return ""
    # Convert "ontology#NormalRank" → "normal"
    base = rank.split("#", 1)[-1]
    return base.replace("Rank", "").lower()


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------

FIELDS = [
    "ext", "source", "qid", "label", "description", "aliases",
    "enwiki_title", "wikidata_url", "wikipedia_url",
    "mime_types", "instance_of_labels", "instance_of_qids",
    "suggested_label", "wikidata_rank", "wikipedia_note",
]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        # Sort by ext, then qid for stable output.
        for r in sorted(rows, key=lambda x: (x["ext"], x["qid"])):
            w.writerow({k: r.get(k, "") for k in FIELDS})


def main() -> int:
    wd = load_wikidata()
    wp = load_wikipedia_by_qid()
    tax_qids = load_taxonomy_qids()
    print(f"[load] wikidata items: {len(wd)}", flush=True)
    print(f"[load] wikipedia infoboxes: {len(wp)}", flush=True)
    print(f"[load] taxonomy QIDs to exclude: {len(tax_qids)}", flush=True)

    rows = build_rows(wd, wp, tax_qids)

    out_path = DERIVED_DIR / "external_extension_index.csv"
    write_csv(out_path, rows)
    print(f"[done] wrote {out_path}", flush=True)

    # Small summary, mirroring the existing build_pl_taxonomy.py sanity check.
    from collections import Counter
    by_ext = Counter(r["ext"] for r in rows)
    by_label_suggestion = Counter(r["suggested_label"] for r in rows if r["suggested_label"])
    src_breakdown = Counter(r["source"] for r in rows)
    print()
    print(f"  distinct extensions: {len(by_ext)}")
    print(f"  source breakdown:    {dict(src_breakdown)}")
    print(f"  suggested-label coverage: "
          f"{sum(1 for r in rows if r['suggested_label'])} / {len(rows)} rows")
    print(f"  top suggested labels: {by_label_suggestion.most_common(8)}")
    print(f"  most-claimed extension: .{by_ext.most_common(1)[0][0]} "
          f"({by_ext.most_common(1)[0][1]} items)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
