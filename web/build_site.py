#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.util import canonical_name, slugify  # noqa: E402

LANGUAGES_DIR = ROOT / "languages"


@dataclass(frozen=True)
class Program:
    sha256: str
    title: str
    origin_url: str
    license_guess: str | None
    added_at: str
    code_source_path: Path | None
    code_bytes: bytes | None
    code_text: str | None
    code_out_name: str | None


@dataclass(frozen=True)
class Language:
    name: str
    aliases: list[str]
    evidence_url: str
    added_at: str
    folder_rel: str
    slug: str
    programs: list[Program]
    # Provenance from git commit trailers (best-effort).
    turn_commit: str | None
    turn_authored_at: str | None
    agent: str | None
    model: str | None
    temperature: float | None
    web_search: str | None


@dataclass(frozen=True)
class TurnInfo:
    commit: str
    authored_at: str
    language: str
    trailers: dict[str, str]


# ---------------------------------------------------------------------------
# Phase 1: PL taxonomy enrichment (cross-source presence + ext claims + SWH samples).
# Loaded from data/derived/pl_taxonomy/ + samples/<pl_id>/ (built by
# tools/build_pl_taxonomy.py and tools/fetch_samples.py respectively).
# ---------------------------------------------------------------------------

TAXONOMY_DIR = ROOT / "data" / "derived" / "pl_taxonomy"
SAMPLES_DIR = ROOT / "samples"
SWH_EXT_POPULARITY_CSV = ROOT / "data" / "derived" / "swh_extensions_popularity.csv"
_TAXONOMY_SOURCES = ("pldb", "linguist", "pygments", "wikipedia",
                     "esolang", "hyperpolyglot", "rosettacode",
                     "manual_add")


@dataclass(frozen=True)
class SwhSample:
    pl_id: str
    sha1_git: str
    filename: str
    length: int
    qualified_swhid: str
    swh_browser_url: str
    swh_raw_url: str
    github_raw_url: str | None
    code_text: str | None  # decoded UTF-8 (best effort) for preview rendering
    ext: str
    occurrences_in_swh: int
    predicted_via: str
    predicted_heuristic_id: str | None


@dataclass(frozen=True)
class TaxonomyEnrichment:
    pl_id: str
    canonical_name: str
    in_sources: dict[str, bool]  # source name -> True/False; covers _TAXONOMY_SOURCES
    extension_claims: list[tuple[str, str, str, str]]  # (ext, source, strength, evidence)
    heuristics_for_my_exts: list[dict]  # heuristic rows touching one of my exts
    swh_samples: list[SwhSample]
    # Provenance: GitHub issue number for PLs added via /contribute/add-pl/.
    # Empty string for PLs derived from upstream sources or LLM /loop turns.
    created_via_issue: str = ""
    # Wikidata / Wikipedia overlay (added by tools/build_pl_taxonomy.py
    # Phase B). Empty string when no matching Wikidata item was found.
    # The per-PL wikipedia_url unblocks the "Wikipedia" source pill on
    # /l/<slug>/ pages, which historically pointed at the
    # List_of_programming_languages roster for every PL.
    wikidata_qid: str = ""
    wikipedia_url: str = ""


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    import csv as _csv
    with path.open(encoding="utf-8") as f:
        return list(_csv.DictReader(f))


_SWH_POPULARITY_CACHE: dict[str, dict] | None = None


def load_swh_ext_popularity() -> dict[str, dict]:
    """Load the SWH-MSR-ARV-derived popularity table (`derived/swh_extensions_popularity.csv`).

    Returns {ext: {total_occ, recent_occ, undated_occ, first_year, last_year}}.
    File is ~80 MB / 3M rows; we keep all rows in memory (small per-row) and
    cache for the lifetime of the build (this function is called from the
    per-language render loop so caching is essential).
    Missing file → empty dict (site degrades gracefully).
    """
    global _SWH_POPULARITY_CACHE
    if _SWH_POPULARITY_CACHE is not None:
        return _SWH_POPULARITY_CACHE
    if not SWH_EXT_POPULARITY_CSV.exists():
        _SWH_POPULARITY_CACHE = {}
        return _SWH_POPULARITY_CACHE
    # Aggregate case variants (SWH-MSR-ARV preserves case, so `.R` and `.r`
    # appear as separate rows). We collapse to the lowercase key and merge:
    #   - total_occ summed
    #   - recent_occ summed
    #   - undated_occ summed
    #   - first_year = min of non-null
    #   - last_year  = max of non-null
    # The case_variants field is preserved verbatim so per-ext pages can show
    # the breakdown ("case variants in archive: .r (Xm), .R (Ym)") and
    # rigorous downstream analysis can still distinguish them.
    out: dict[str, dict] = {}
    import csv as _csv
    with SWH_EXT_POPULARITY_CSV.open(encoding="utf-8") as f:
        for r in _csv.DictReader(f):
            raw_ext = r.get("extension") or ""
            if not raw_ext.startswith("."):
                continue
            key = raw_ext.lower()
            total = int(r.get("total_occ", 0) or 0)
            recent = int(r.get("recent_occ", 0) or 0)
            undated = int(r.get("undated_occ", 0) or 0)
            fy = int(r.get("first_year")) if r.get("first_year") else None
            ly = int(r.get("last_year")) if r.get("last_year") else None
            entry = out.get(key)
            if entry is None:
                out[key] = {
                    "total_occ": total,
                    "recent_occ": recent,
                    "undated_occ": undated,
                    "first_year": fy,
                    "last_year": ly,
                    "case_variants": [(raw_ext, total)],
                }
            else:
                entry["total_occ"] += total
                entry["recent_occ"] += recent
                entry["undated_occ"] += undated
                if fy is not None:
                    entry["first_year"] = fy if entry["first_year"] is None else min(entry["first_year"], fy)
                if ly is not None:
                    entry["last_year"] = ly if entry["last_year"] is None else max(entry["last_year"], ly)
                entry["case_variants"].append((raw_ext, total))
    _SWH_POPULARITY_CACHE = out
    return out


def _fmt_occ(n: int) -> str:
    """Compact int formatter: 12345 -> '12.3K', 12345678 -> '12.3M', etc."""
    if n is None: return "—"
    if n < 1000: return f"{n}"
    for unit, div in [("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if n >= div:
            return f"{n/div:.1f}{unit}"
    return f"{n}"


_NORM_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5",
               "vi": "6", "vii": "7", "viii": "8", "ix": "9", "x": "10"}

# Same special-char mapping that `tools/build_pl_taxonomy.py`'s slugify uses to
# build pl_ids. Mirrored here so in-repo names normalize to the SAME shape as
# the pl_ids: e.g., "Prolog++" -> "prologpp" matches pl_id "pl/prologpp".
_NORM_SPECIAL = [
    ("++", "pp"), ("#", "sharp"), ("*", "star"),
    ("&", "and"), ("@", "at"), ("?", "q"), ("!", "bang"),
]


def _normalize_name(s: str) -> str:
    """Aggressive normalization for fuzzy matching.

    Lowercases, strips parentheticals, maps special chars (`++`, `#`, `*`, …)
    to letter sequences (so pl_id-style slugs match), then drops everything
    non-alphanumeric.
    Examples:
      'BBC BASIC'                  -> 'bbcbasic'
      'JScript.NET'                -> 'jscriptnet'
      'Python (programming lang)'  -> 'python'
      'Prolog++'                   -> 'prologpp'  (matches pl/prologpp)
      'C#'                         -> 'csharp'    (matches pl/csharp)
    """
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)  # drop parentheticals
    for old, new in _NORM_SPECIAL:
        s = s.replace(old, new)
    s = s.lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def _normalize_name_with_roman(s: str) -> str:
    """Like _normalize_name, but also maps roman numerals at word boundaries to digits."""
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)
    s = s.lower()
    # split into words, swap roman → arabic where matching
    tokens = re.split(r"[^a-z0-9]+", s)
    tokens = [_NORM_ROMAN.get(t, t) for t in tokens]
    return "".join(tokens)


_EXTERNAL_EXTENSION_INDEX_CACHE: dict[str, list[dict]] | None = None


def load_external_extension_index() -> dict[str, list[dict]]:
    """Return {ext: [row, row, ...]} from data/derived/external_extension_index.csv.

    The CSV is produced by tools/build_external_extension_index.py from the
    pinned Wikidata + Wikipedia infobox snapshots, excluding items already
    in the PL taxonomy. Each row is one (extension, Wikidata item) pair —
    polysemy is preserved (e.g. .xml has ~118 rows). The site uses this to
    show "what is this extension, per Wikidata?" on /ext/<slug>/ pages,
    feeding the labelling form's reviewer with friendly_name +
    reference_url + suggested controlled-vocab label hints.

    Sorted: rows with a Wikipedia URL first (more authoritative), then by
    label alphabetical. The downstream renderer caps display to keep
    polysemous extensions tractable.
    """
    global _EXTERNAL_EXTENSION_INDEX_CACHE
    if _EXTERNAL_EXTENSION_INDEX_CACHE is not None:
        return _EXTERNAL_EXTENSION_INDEX_CACHE
    out: dict[str, list[dict]] = {}
    path = ROOT / "data" / "derived" / "external_extension_index.csv"
    if path.exists():
        for r in _read_csv(path):
            ext_raw = (r.get("ext") or "").strip().lower()
            if not ext_raw:
                continue
            # CSV stores ext without leading dot; the rest of the site keys
            # extensions with the dot, so normalise here.
            ext_key = "." + ext_raw
            out.setdefault(ext_key, []).append(r)
    # Sort each ext's rows: those with a Wikipedia URL first, then alpha label.
    for rows in out.values():
        rows.sort(key=lambda x: (
            0 if x.get("wikipedia_url") else 1,
            (x.get("label") or "").lower(),
        ))
    _EXTERNAL_EXTENSION_INDEX_CACHE = out
    return out


_LEGACY_WIKIPEDIA_TITLES_CACHE: dict[str, str] | None = None


def load_legacy_wikipedia_titles() -> dict[str, str]:
    """Return {normalized canonical name -> Wikipedia article title}.

    Source: data/raw/wikipedia_lang_titles.json, the 177-entry list
    scraped from `List_of_programming_languages` by master_inventory.py.
    Used as a fallback wikipedia_url for PLs that are flagged
    in_wikipedia=yes but whose Wikidata overlay (Phase B) didn't surface
    an enwiki sitelink — typically because Wikidata's entry for that PL
    lacks P1195 (file extension) and so was outside the Phase B match
    scope. With this fallback, the Wikipedia source pill on /l/<slug>/
    points at the per-PL article for every PL in the legacy list, not
    just the Wikidata-overlap subset.
    """
    global _LEGACY_WIKIPEDIA_TITLES_CACHE
    if _LEGACY_WIKIPEDIA_TITLES_CACHE is not None:
        return _LEGACY_WIKIPEDIA_TITLES_CACHE
    path = ROOT / "data" / "raw" / "wikipedia_lang_titles.json"
    out: dict[str, str] = {}
    if path.exists():
        try:
            titles = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            titles = []
        for title in titles:
            if not isinstance(title, str):
                continue
            for key in (_normalize_name(title), _normalize_name_with_roman(title)):
                if key:
                    out.setdefault(key, title)
    _LEGACY_WIKIPEDIA_TITLES_CACHE = out
    return out


def _legacy_wikipedia_url_for(canonical_name: str) -> str:
    """Return the per-PL Wikipedia URL via the legacy title list, or empty."""
    if not canonical_name:
        return ""
    titles = load_legacy_wikipedia_titles()
    for key in (_normalize_name(canonical_name),
                _normalize_name_with_roman(canonical_name)):
        if key and key in titles:
            title = titles[key]
            return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
    return ""


def load_pl_taxonomy() -> tuple[dict[str, dict], dict[str, str]]:
    """Return (pl_rows_by_id, name_index lower -> pl_id).

    Name index has three layers, each populated only when the previous didn't
    already claim a slot for that key:
      1. raw lowercase (exact match)
      2. _normalize_name (strip non-alphanumerics, drop parentheticals)
      3. _normalize_name_with_roman (also map roman numerals → arabic)
    """
    pl_rows = _read_csv(TAXONOMY_DIR / "pl.csv")
    alias_rows = _read_csv(TAXONOMY_DIR / "pl_alias.csv")
    by_id = {r["pl_id"]: r for r in pl_rows if r.get("pl_id")}
    name_index: dict[str, str] = {}

    def _add(key: str | None, pid: str) -> None:
        if not key:
            return
        for variant in (key.lower(), _normalize_name(key), _normalize_name_with_roman(key)):
            if variant:
                name_index.setdefault(variant, pid)

    for r in pl_rows:
        pid = r.get("pl_id")
        if not pid:
            continue
        for key in (r.get("canonical_name"), r.get("linguist_key"),
                    r.get("pygments_name"), r.get("hyperpolyglot_name"),
                    r.get("rosettacode_name")):
            _add(key, pid)
    for a in alias_rows:
        _add(a.get("alias"), a.get("pl_id"))
    return by_id, name_index


def load_ext_claims() -> dict[str, list[tuple[str, str, str, str]]]:
    """Return {pl_id: [(ext, source, strength, evidence), ...]} ordered by strength."""
    out: dict[str, list[tuple[str, str, str, str]]] = {}
    strength_order = {"primary": 0, "secondary": 1, "unknown": 2}
    for r in _read_csv(TAXONOMY_DIR / "ext_claim.csv"):
        out.setdefault(r["pl_id"], []).append(
            (r["ext"], r["source"], r["strength"], r.get("evidence", ""))
        )
    for lst in out.values():
        lst.sort(key=lambda t: (strength_order.get(t[2], 9), t[0], t[1]))
    return out


def load_heuristics() -> tuple[list[dict], dict[str, list[dict]]]:
    """Return (all_rules, by_ext)."""
    rules = _read_csv(TAXONOMY_DIR / "heuristic.csv")
    by_ext: dict[str, list[dict]] = {}
    for r in rules:
        by_ext.setdefault(r["applies_to_ext"], []).append(r)
    return rules, by_ext


def load_swh_samples() -> dict[str, list[SwhSample]]:
    """Walk samples/ and group by pl_id.

    For samples classified to a specific pl_id (samples/<pl_id>/<sha>/) the
    sample is associated with that pl_id directly. For samples in
    samples/unclassified/<sha>/, the sample is associated with EVERY language
    that claims its extension as a primary claim (per ext_claim.csv) — so an
    ambiguous `.pas` file appears on both Pascal and Delphi pages, flagged as
    a fallback candidate.
    """
    out: dict[str, list[SwhSample]] = {}
    if not SAMPLES_DIR.exists():
        return out

    # Build ext -> [pl_ids that claim it as primary] for ambiguous fan-out.
    # Dedupe per (ext, pl_id) — a single pl_id can claim the same ext from
    # multiple sources (e.g. Pascal claims .pas from both linguist and
    # pygments), which would otherwise duplicate the sample on its page.
    ext_to_primary_pl_ids: dict[str, list[str]] = {}
    try:
        seen_primary: set[tuple[str, str]] = set()
        for c in _read_csv(TAXONOMY_DIR / "ext_claim.csv"):
            if c.get("strength") != "primary":
                continue
            key = (c.get("ext"), c.get("pl_id"))
            if not all(key) or key in seen_primary:
                continue
            seen_primary.add(key)
            ext_to_primary_pl_ids.setdefault(c["ext"], []).append(c["pl_id"])
    except Exception:
        pass

    def _build_sample(sha_dir: Path, pl_id_for_sample: str) -> SwhSample | None:
        meta_path = sha_dir / "metadata.json"
        if not meta_path.exists():
            return None
        try:
            m = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            return None
        filename = m.get("filename") or ""
        code_path = sha_dir / filename
        code_text: str | None = None
        if code_path.exists():
            try:
                code_text = code_path.read_text(encoding="utf-8", errors="replace")
                if len(code_text) > 16_000:
                    code_text = code_text[:16_000] + "\n…(truncated)…"
            except Exception:
                code_text = None
        return SwhSample(
            pl_id=pl_id_for_sample,
            sha1_git=m.get("sha1_git") or sha_dir.name,
            filename=filename,
            length=int(m.get("length_bytes") or 0),
            qualified_swhid=m.get("qualified_swhid") or "",
            swh_browser_url=m.get("swh_browser_url") or "",
            swh_raw_url=m.get("swh_raw_url") or "",
            github_raw_url=m.get("github_raw_url"),
            code_text=code_text,
            ext=m.get("ext") or "",
            occurrences_in_swh=int(m.get("occurrences_in_swh") or 0),
            predicted_via=m.get("predicted_via") or "fallback (ambiguous ext)",
            predicted_heuristic_id=m.get("predicted_heuristic_id"),
        )

    # Path 1: classified samples at samples/pl/<slug>/<sha>/.
    for sha_dir in SAMPLES_DIR.glob("*/*/*"):
        if not sha_dir.is_dir() or not (sha_dir / "metadata.json").exists():
            continue
        try:
            m = json.loads((sha_dir / "metadata.json").read_text(encoding="utf-8"))
        except Exception:
            continue
        pl_id = (m.get("predicted_pl_id") or "").strip()
        if not pl_id:
            pl_id = sha_dir.parent.parent.name + "/" + sha_dir.parent.name
        s = _build_sample(sha_dir, pl_id)
        if s is not None:
            out.setdefault(pl_id, []).append(s)

    # Path 2: unclassified samples at samples/unclassified/<sha>/, fanned out
    # to all primary claimants of their extension.
    unclassified_dir = SAMPLES_DIR / "unclassified"
    if unclassified_dir.exists():
        for sha_dir in unclassified_dir.iterdir():
            if not sha_dir.is_dir() or not (sha_dir / "metadata.json").exists():
                continue
            try:
                m = json.loads((sha_dir / "metadata.json").read_text(encoding="utf-8"))
            except Exception:
                continue
            ext = m.get("ext") or ""
            claimants = ext_to_primary_pl_ids.get(ext, [])
            if not claimants:
                # No primary claimant for this ext — sample stays orphan in the
                # by-pl_id index. It is still surfaced on the per-ext page via
                # `load_swh_samples_by_ext` below.
                continue
            for pl_id in claimants:
                s = _build_sample(sha_dir, pl_id)
                if s is not None:
                    out.setdefault(pl_id, []).append(s)
    return out


def load_swh_samples_by_ext() -> dict[str, list[SwhSample]]:
    """Walk `samples/` and index EVERY sample by its file extension.

    Unlike `load_swh_samples` (which groups by pl_id and drops orphan unclassified
    samples whose ext has no primary claimant), this index includes:

    - Classified samples at `samples/pl/<slug>/<sha>/`
    - Unclassified samples at `samples/unclassified/<sha>/` — regardless of
      whether any PL claims their ext

    Used by per-extension pages so reviewers can see real archived bytes for
    unattributed extensions like `.pbf` or `.fsti` while deciding what they
    actually are.
    """
    out: dict[str, list[SwhSample]] = {}
    if not SAMPLES_DIR.exists():
        return out

    def _read_meta(sha_dir: Path) -> dict | None:
        mp = sha_dir / "metadata.json"
        if not mp.exists():
            return None
        try:
            return json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _build_for_ext(sha_dir: Path, m: dict) -> SwhSample | None:
        ext = (m.get("ext") or "").lower()
        filename = m.get("filename") or ""
        code_path = sha_dir / filename
        code_text: str | None = None
        if code_path.exists():
            try:
                code_text = code_path.read_text(encoding="utf-8", errors="replace")
                if len(code_text) > 16_000:
                    code_text = code_text[:16_000] + "\n…(truncated)…"
            except Exception:
                pass
        return SwhSample(
            pl_id=(m.get("predicted_pl_id") or "").strip() or "unclassified",
            sha1_git=m.get("sha1_git") or sha_dir.name,
            filename=filename,
            length=int(m.get("length_bytes") or 0),
            qualified_swhid=m.get("qualified_swhid") or "",
            swh_browser_url=m.get("swh_browser_url") or "",
            swh_raw_url=m.get("swh_raw_url") or "",
            github_raw_url=m.get("github_raw_url"),
            code_text=code_text,
            ext=ext,
            occurrences_in_swh=int(m.get("occurrences_in_swh") or 0),
            predicted_via=m.get("predicted_via") or "",
            predicted_heuristic_id=m.get("predicted_heuristic_id"),
        )

    # Path A: classified samples at samples/pl/<slug>/<sha>/.
    for sha_dir in SAMPLES_DIR.glob("*/*/*"):
        if not sha_dir.is_dir():
            continue
        m = _read_meta(sha_dir)
        if m is None:
            continue
        ext = (m.get("ext") or "").lower()
        if not ext:
            continue
        s = _build_for_ext(sha_dir, m)
        if s is not None:
            out.setdefault(ext, []).append(s)

    # Path B: unclassified (and ext-mined review-targeted) samples at
    # samples/unclassified/<sha>/.
    unclassified_dir = SAMPLES_DIR / "unclassified"
    if unclassified_dir.exists():
        for sha_dir in unclassified_dir.iterdir():
            if not sha_dir.is_dir():
                continue
            m = _read_meta(sha_dir)
            if m is None:
                continue
            ext = (m.get("ext") or "").lower()
            if not ext:
                continue
            s = _build_for_ext(sha_dir, m)
            if s is not None:
                out.setdefault(ext, []).append(s)
    return out


def synthesize_taxonomy_only_languages(
    *,
    languages: list["Language"],
    enrichments: dict[str, TaxonomyEnrichment],
) -> tuple[list["Language"], dict[str, TaxonomyEnrichment]]:
    """For PL entities in pl.csv with no in-repo `languages/<L>/`, synthesize a
    Language so they get full pages too. Their enrichment is built directly
    from the taxonomy (no name-matching gap because we use the pl_id key).
    """
    pl_by_id, _ = load_pl_taxonomy()
    ext_claims = load_ext_claims()
    _, heuristics_by_ext = load_heuristics()
    swh_samples = load_swh_samples()
    aliases_by_pl_id: dict[str, list[str]] = {}
    for a in _read_csv(TAXONOMY_DIR / "pl_alias.csv"):
        if a.get("pl_id") and a.get("alias"):
            aliases_by_pl_id.setdefault(a["pl_id"], []).append(a["alias"])

    claimed_pl_ids = {e.pl_id for e in enrichments.values()}
    new_langs: list[Language] = []
    new_enrichments: dict[str, TaxonomyEnrichment] = dict(enrichments)
    used_names: set[str] = {l.name.lower() for l in languages}

    for pl_id, row in pl_by_id.items():
        if pl_id in claimed_pl_ids:
            continue
        canonical = (row.get("canonical_name") or "").strip()
        if not canonical:
            continue
        # Avoid name collisions with in-repo entries (different pl_ids but
        # identical-looking canonicals would create duplicate browse rows).
        if canonical.lower() in used_names:
            continue
        used_names.add(canonical.lower())

        aliases = sorted({a for a in aliases_by_pl_id.get(pl_id, []) if a and a.lower() != canonical.lower()})
        evidence = (row.get("evidence_urls") or "").split(";")[0].strip()
        # Slug: same shape as existing pages so the directory looks uniform.
        # Cap base-slug at 80 chars; the 8-char hash suffix still disambiguates.
        # Some Esolang entries are pathological (e.g., "bf++++...++++" with 200+
        # plus signs), which would exceed filesystem filename limits.
        base_slug = slugify(canonical)[:80].rstrip("-")
        slug = base_slug + "-" + hashlib.sha1(pl_id.encode()).hexdigest()[:8]

        new_lang = Language(
            name=canonical,
            aliases=aliases,
            evidence_url=evidence,
            added_at="",  # Sentinel: empty added_at == taxonomy-only.
            folder_rel="",  # Sentinel: no in-repo folder.
            slug=slug,
            programs=[],
            turn_commit=None, turn_authored_at=None,
            agent=None, model=None, temperature=None, web_search=None,
        )
        new_langs.append(new_lang)

        my_claims = ext_claims.get(pl_id, [])
        my_exts = {c[0] for c in my_claims}
        applicable_heur = [
            h for ext in my_exts
            for h in heuristics_by_ext.get(ext, [])
            if h.get("predicts_pl_id") == pl_id
        ]
        in_sources = {s: (row.get(f"in_{s}", "no") == "yes") for s in _TAXONOMY_SOURCES}
        new_enrichments[canonical] = TaxonomyEnrichment(
            pl_id=pl_id,
            canonical_name=canonical,
            in_sources=in_sources,
            extension_claims=my_claims,
            heuristics_for_my_exts=applicable_heur,
            swh_samples=sorted(swh_samples.get(pl_id, []), key=lambda s: -s.occurrences_in_swh),
            created_via_issue=str(row.get("created_via_issue") or "").strip(),
            wikidata_qid=str(row.get("wikidata_qid") or "").strip(),
            wikipedia_url=str(row.get("wikipedia_url") or "").strip(),
        )
    return new_langs, new_enrichments


def build_taxonomy_enrichments(languages: list["Language"]) -> dict[str, TaxonomyEnrichment]:
    """Match each Language to a pl_id and assemble cross-source / ext / SWH evidence."""
    pl_by_id, name_index = load_pl_taxonomy()
    if not pl_by_id:
        return {}
    ext_claims = load_ext_claims()
    _, heuristics_by_ext = load_heuristics()
    swh_samples = load_swh_samples()

    out: dict[str, TaxonomyEnrichment] = {}
    for lang in languages:
        # Try exact lowercase first, then the two normalization variants,
        # against the language's own name + each alias. First hit wins.
        keys_to_try: list[str] = []
        for raw in [lang.name, *lang.aliases]:
            if not raw:
                continue
            keys_to_try.append(raw.lower())
            keys_to_try.append(_normalize_name(raw))
            keys_to_try.append(_normalize_name_with_roman(raw))
        pl_id = next((name_index[k] for k in keys_to_try if k and k in name_index), None)
        if not pl_id:
            continue
        row = pl_by_id.get(pl_id, {})
        my_claims = ext_claims.get(pl_id, [])
        my_exts = {c[0] for c in my_claims}
        applicable_heur: list[dict] = []
        for ext in my_exts:
            for h in heuristics_by_ext.get(ext, []):
                if h.get("predicts_pl_id") == pl_id:
                    applicable_heur.append(h)
        in_sources = {s: (row.get(f"in_{s}", "no") == "yes") for s in _TAXONOMY_SOURCES}
        out[lang.name] = TaxonomyEnrichment(
            pl_id=pl_id,
            canonical_name=row.get("canonical_name") or lang.name,
            in_sources=in_sources,
            extension_claims=my_claims,
            heuristics_for_my_exts=applicable_heur,
            swh_samples=sorted(swh_samples.get(pl_id, []), key=lambda s: -s.occurrences_in_swh),
            created_via_issue=str(row.get("created_via_issue") or "").strip(),
            wikidata_qid=str(row.get("wikidata_qid") or "").strip(),
            wikipedia_url=str(row.get("wikipedia_url") or "").strip(),
        )
    return out


def parse_iso8601(s: str) -> datetime | None:
    if not s:
        return None
    s = s.strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


TURN_PREFIX = "turn: add "
TURN_SUFFIX = " (+1 program)"
TRAILER_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")


def parse_trailers(message_body: str) -> dict[str, str]:
    trailers: dict[str, str] = {}
    for raw_line in (message_body or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = TRAILER_RE.match(line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        trailers[key] = value
    return trailers


def parse_temperature(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.strip())
    except Exception:
        return None


def normalize_web_search(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip().lower()
    if v in {"enabled", "true", "yes", "1", "on"}:
        return "enabled"
    if v in {"disabled", "false", "no", "0", "off"}:
        return "disabled"
    return value.strip()


def read_turns_from_git() -> list[TurnInfo]:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        return []
    try:
        proc = subprocess.run(
            ["git", "--no-pager", "log", "--pretty=format:%H%x1f%aI%x1f%s%x1f%b%x1e"],
            cwd=str(ROOT),
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception:
        return []

    turns: list[TurnInfo] = []
    for record in proc.stdout.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 4:
            continue
        commit, authored_at, subject, body = parts[0], parts[1], parts[2], parts[3]
        if not (subject.startswith(TURN_PREFIX) and subject.endswith(TURN_SUFFIX)):
            continue
        lang_raw = subject[len(TURN_PREFIX) : -len(TURN_SUFFIX)]
        lang = canonical_name(lang_raw)
        trailers = parse_trailers(body)
        turns.append(TurnInfo(commit=commit, authored_at=authored_at, language=lang, trailers=trailers))

    return turns


def index_turns_by_language(turns: list[TurnInfo]) -> dict[str, TurnInfo]:
    # git log returns newest-first; we want first (oldest) per language if duplicates exist.
    by_lang: dict[str, TurnInfo] = {}
    for turn in reversed(turns):
        key = canonical_name(turn.language).lower()
        if key not in by_lang:
            by_lang[key] = turn
    return by_lang


def guess_github_owner_repo() -> str | None:
    """
    Best-effort parse of `origin` remote into `owner/repo` for github.com.
    Supports:
      - https://github.com/owner/repo(.git)?/
      - git@github.com:owner/repo(.git)?
    """
    try:
        proc = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(ROOT),
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception:
        return None

    raw = (proc.stdout or "").strip()
    if not raw:
        return None

    # SSH form
    if raw.startswith("git@github.com:"):
        path = raw.split(":", 1)[1].strip()
        path = path.removesuffix(".git").strip("/")
        if path.count("/") >= 1:
            owner, repo = path.split("/", 1)[0], path.split("/", 1)[1]
            if owner and repo:
                return f"{owner}/{repo}"
        return None

    # HTTPS form
    try:
        u = urlparse(raw)
    except Exception:
        return None
    if u.netloc.lower() != "github.com":
        return None

    path = (u.path or "").strip("/")
    path = path.removesuffix(".git").strip("/")
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def github_new_issue_url(*, owner_repo: str, title: str, body: str, labels: list[str] | None = None) -> str:
    base = f"https://github.com/{owner_repo}/issues/new"
    params: dict[str, str] = {"title": title, "body": body}
    if labels:
        params["labels"] = ",".join(labels)
    return base + "?" + urlencode(params, quote_via=quote)


def github_issue_search_url(*, owner_repo: str, query: str) -> str:
    base = f"https://github.com/{owner_repo}/issues"
    return base + "?" + urlencode({"q": query}, quote_via=quote)


def github_commit_url(*, owner_repo: str, commit: str) -> str:
    return f"https://github.com/{owner_repo}/commit/{commit}"


def trigrams(s: str) -> set[str]:
    s = re.sub(r"\s+", " ", (s or "").strip().lower())
    if len(s) <= 3:
        return {s} if s else set()
    pad = f"  {s}  "
    return {pad[i : i + 3] for i in range(0, len(pad) - 2)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    union = len(a) + len(b) - inter
    return inter / union


def compute_related_languages(languages: list[Language], *, k: int = 5) -> dict[str, list[dict[str, Any]]]:
    names = [l.name for l in languages]
    trig = {l.name: trigrams(" ".join([l.name] + list(l.aliases or []))) for l in languages}

    related: dict[str, list[dict[str, Any]]] = {n: [] for n in names}
    for i, a in enumerate(names):
        ta = trig[a]
        for j in range(i + 1, len(names)):
            b = names[j]
            sim = jaccard(ta, trig[b])
            if sim <= 0:
                continue
            related[a].append({"name": b, "score": sim})
            related[b].append({"name": a, "score": sim})

    for n in names:
        related[n].sort(key=lambda x: x["score"], reverse=True)
        related[n] = [{"name": x["name"], "score": round(x["score"], 4)} for x in related[n][:k]]
    return related


def load_audit_summary(audit_path: Path) -> dict[str, Any] | None:
    if not audit_path.exists():
        return None
    try:
        data = json.loads(audit_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    by_severity = Counter()
    by_language: dict[str, Counter] = defaultdict(Counter)
    for f in data.get("findings", []):
        lang = f.get("language")
        sev = (f.get("severity") or "unknown").lower()
        if lang:
            by_language[lang][sev] += 1
            by_language[lang]["total"] += 1
        by_severity[sev] += 1

    top_langs = sorted(
        ((k, v["total"], v.get("error", 0), v.get("warn", 0), v.get("info", 0)) for k, v in by_language.items()),
        key=lambda x: (x[1], x[2], x[3]),
        reverse=True,
    )[:12]

    return {
        "total": sum(by_severity.values()),
        "by_severity": dict(by_severity),
        "by_language": {k: dict(v) for k, v in by_language.items()},
        "top_languages": top_langs,
    }

def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def make_lang_slug(name: str) -> str:
    base = slugify(name) or "lang"
    return f"{base}-{short_hash(name)}"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_lossy(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def find_program_code_file(program_dir: Path) -> Path | None:
    if not program_dir.is_dir():
        return None
    candidates = [p for p in program_dir.iterdir() if p.is_file() and p.name != "manifest.json"]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    codeish = [p for p in candidates if p.name.startswith("code")]
    if len(codeish) == 1:
        return codeish[0]
    return sorted(candidates, key=lambda p: (0 if p.name.startswith("code") else 1, len(p.name), p.name))[0]


def derive_code_out_name(code_source_name: str) -> str:
    # Normalize historical variants:
    # - code.abap      -> code.abap
    # - codepy         -> code.py
    # - coders         -> code.rs
    # - <other file>   -> <other file>
    if "." in code_source_name:
        return code_source_name
    if code_source_name.startswith("code") and len(code_source_name) > 4:
        ext = code_source_name[4:]
        ext = "".join(ch for ch in ext if ch.isalnum() or ch in ("+", "-", "_"))
        if not ext:
            return "code.txt"
        return f"code.{ext}"
    return code_source_name


def rel_prefix(page: Path, dist_root: Path) -> str:
    rel = page.parent.relative_to(dist_root)
    return "../" * len(rel.parts)


def layout(
    *,
    title: str,
    rel: str,
    body: str,
    generated_at: str,
    description: str = "",
    github_owner_repo: str | None = None,
) -> str:
    safe_title = html.escape(title)
    safe_desc = html.escape(description or "Browse programming languages and their example programs.")
    gh_repo_js = json.dumps(github_owner_repo) if github_owner_repo else "null"
    gh_link = f"https://github.com/{github_owner_repo}" if github_owner_repo else ""
    gh_nav = (
        f'<a href="{gh_link}" target="_blank" rel="noopener">GitHub</a>' if github_owner_repo else ""
    )
    gh_footer = (
        f' · <a href="{gh_link}" target="_blank" rel="noopener">Source repo</a>' if github_owner_repo else ""
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <meta name="description" content="{safe_desc}" />
    <link rel="stylesheet" href="{rel}assets/style.css" />
    <script>
      window.__SITE_ROOT__ = {json.dumps(rel)};
      window.__DATA_BASE__ = {json.dumps(rel + "data")};
      window.__GITHUB_OWNER_REPO__ = {gh_repo_js};
    </script>
    <script src="{rel}assets/app.js" defer></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container header-inner">
        <a class="brand" href="{rel}index.html">PL Catalog</a>
        <nav class="nav">
          <a href="{rel}browse/index.html">Browse</a>
          <a href="{rel}ext/index.html">Extensions</a>
          <a href="{rel}source/index.html">Sources</a>
          <a href="{rel}samples/index.html">SWH samples</a>
          <a href="{rel}review/extensions/index.html">Review</a>
          <a href="{rel}review/curator/index.html">Curator</a>
          <a href="{rel}contribute/add-pl/index.html">Add a PL</a>
          <a href="{rel}stats/index.html">Stats</a>
          <a href="{rel}audit/index.html">Audit</a>
          {gh_nav}
          <button id="randomBtn" class="nav-btn" type="button">Random</button>
        </nav>
      </div>
    </header>
    <main class="container">
      {body}
    </main>
    <footer class="site-footer">
      <div class="container">
        Generated at <span class="muted">{html.escape(generated_at)}</span> from this repository{gh_footer}.
      </div>
    </footer>
  </body>
</html>
"""


def letter_counts(languages: list[Language]) -> dict[str, int]:
    counts: dict[str, int] = {chr(c): 0 for c in range(ord("A"), ord("Z") + 1)}
    for lang in languages:
        if not lang.name:
            continue
        ch = lang.name[0].upper()
        if ch in counts:
            counts[ch] += 1
    return counts


def first_letter(name: str) -> str:
    if not name:
        return ""
    ch = name[0].upper()
    return ch if "A" <= ch <= "Z" else "#"


def render_letter_grid(*, rel: str, counts: dict[str, int]) -> str:
    tiles = []
    for letter in sorted(counts.keys()):
        c = counts[letter]
        tiles.append(
            f'<a href="{rel}browse/index.html?letter={letter}" data-letter="{letter}">{letter}<span>{c}</span></a>'
        )
    return f'<div class="letter-grid" id="browseLetters">{"".join(tiles)}</div>'


def safe(s: str) -> str:
    return html.escape(s or "")


def render_home_page(
    *,
    dist_root: Path,
    languages: list[Language],
    counts: dict[str, int],
    generated_at: str,
    programs_total: int,
    github_owner_repo: str | None,
    enrichments: dict[str, TaxonomyEnrichment] | None = None,
) -> None:
    page = dist_root / "index.html"
    rel = rel_prefix(page, dist_root)

    newest = sorted(
        languages,
        key=lambda l: parse_iso8601(l.added_at) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:12]

    recent_items = "\n".join(
        f'<li><a href="{rel}l/{lang.slug}/index.html">{safe(lang.name)}</a><span class="muted">{safe(lang.added_at)}</span></li>'
        for lang in newest
    )

    enrichments = enrichments or {}
    n_in_repo = sum(1 for l in languages if l.added_at)
    # Dedupe by pl_id: multiple in-repo entries can map to the same taxonomy entity.
    pl_ids_with_swh: set[str] = set()
    sample_keys: set[tuple[str, str]] = set()
    for e in enrichments.values():
        if e.swh_samples:
            pl_ids_with_swh.add(e.pl_id)
            for s in e.swh_samples:
                sample_keys.add((e.pl_id, s.sha1_git))
    n_with_swh = len(pl_ids_with_swh)
    n_swh_samples = len(sample_keys)
    # Progress KPI: how many PLs in the taxonomy have at least one extension
    # claim. Grows when manual labelling lands new (pl, ext) edges.
    n_pls_in_taxonomy = 0
    n_pls_with_ext = 0
    try:
        pls_with_ext: set[str] = set()
        n_pls_in_taxonomy = sum(1 for _ in _read_csv(TAXONOMY_DIR / "pl.csv"))
        for r in _read_csv(TAXONOMY_DIR / "ext_claim.csv"):
            if r.get("pl_id"):
                pls_with_ext.add(r["pl_id"])
        n_pls_with_ext = len(pls_with_ext)
    except Exception:
        pass
    pct_pls_with_ext = (100.0 * n_pls_with_ext / n_pls_in_taxonomy) if n_pls_in_taxonomy else 0.0
    stats_html = f"""
    <div class="stats">
      <div class="stat"><div class="num">{len(languages):,}</div><div class="muted">PL pages</div></div>
      <div class="stat"><div class="num">{n_in_repo:,}</div><div class="muted">in-repo (LLM-curated)</div></div>
      <div class="stat"><div class="num">{programs_total:,}</div><div class="muted">LLM programs</div></div>
      <div class="stat" title="Progress KPI — grows as manual labelling lands new (PL, ext) edges in ext_claim.csv"><div class="num">{n_pls_with_ext:,} <span style="font-size:60%; color:var(--muted);">({pct_pls_with_ext:.1f}%)</span></div><div class="muted">PLs with ≥1 ext claim<br/>(of {n_pls_in_taxonomy:,} in taxonomy)</div></div>
      <div class="stat"><div class="num">{n_with_swh:,}</div><div class="muted">PLs with SWH samples</div></div>
      <div class="stat"><div class="num">{n_swh_samples:,}</div><div class="muted">SWH samples</div></div>
      <div class="stat"><div class="num">{generated_at.split('T')[0]}</div><div class="muted">last build (UTC)</div></div>
    </div>
    <p class="muted" style="margin:12px 0 0;">Indexed languages are cross-referenced from <code>languages/**/meta.json</code> (LLM-curated) and seven upstream sources (PLDB, Linguist, Pygments, Wikipedia, Esolang, Hyperpolyglot, Rosetta Code). Each PL page shows which sources mention it, what extensions it claims, and real archived programs from Software Heritage. See <a href="{rel}stats/index.html">Stats</a> for coverage and <a href="{rel}ext/index.html">Extensions catalog</a> for per-extension claimants &amp; heuristics.</p>
    """

    body = f"""
    <section class="panel hero">
      <h1>Programming languages + example programs</h1>
      <p>Browse the repository without dumping everything on one page.</p>
      {stats_html}
      <div class="search-box" style="margin-top:14px;">
        <input id="homeSearch" type="search" placeholder="Search (e.g., Haskell, C#, Prolog, ML/I…)" autocomplete="off" />
        <div id="homeResults" style="margin-top:10px;"></div>
      </div>
    </section>

    <div class="grid" style="margin-top:18px;">
      <section class="panel section">
        <h2>Browse by letter</h2>
        <p class="muted" style="margin: 0 0 12px;">Pick a letter to jump into a manageable list.</p>
        {render_letter_grid(rel=rel, counts=counts)}
      </section>
      <section class="panel section">
        <h2>Recently added</h2>
        <ul class="recent">
          {recent_items}
        </ul>
      </section>
    </div>
    """

    page.write_text(
        layout(
            title="PL Catalog",
            rel=rel,
            body=body,
            generated_at=generated_at,
            description="Browse programming languages with example programs.",
            github_owner_repo=github_owner_repo,
        ),
        encoding="utf-8",
    )


def render_browse_page(
    *, dist_root: Path, languages: list[Language], counts: dict[str, int], generated_at: str, github_owner_repo: str | None
) -> None:
    page = dist_root / "browse" / "index.html"
    rel = rel_prefix(page, dist_root)
    lang_total = f"{len(languages):,}"
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Browse</h1>
      <p class="muted" style="margin:0 0 14px;">Pick a letter or search. Results are paged (no {lang_total}-item dump).</p>
      <div class="search-box" style="margin-bottom: 10px;">
        <input id="browseSearch" type="search" placeholder="Search languages or aliases…" autocomplete="off" />
      </div>
      <div id="browseFilters" style="display:flex; flex-wrap:wrap; gap:14px; margin: 6px 0 14px; font-size: 14px;">
        <label><input type="checkbox" id="fltHasSwh"> with SWH sample</label>
        <label><input type="checkbox" id="fltLlm"> has LLM program</label>
        <label><input type="checkbox" id="fltTaxonomy"> taxonomy-only (no LLM)</label>
        <label>min sources: <input type="number" id="fltMinSources" min="0" max="8" value="0" style="width:48px;"></label>
      </div>
      {render_letter_grid(rel=rel, counts=counts)}
      <div id="browseSummary" class="muted" style="margin-top: 12px;"></div>
      <div id="browseResults" style="margin-top: 10px;"></div>
      <button id="browseMore" class="btn" type="button" style="margin-top: 12px;" hidden>Load more</button>
      <noscript>
        <p class="muted" style="margin-top: 12px;">This page uses a small amount of JavaScript for search/paging.</p>
      </noscript>
    </section>
    """
    page.write_text(
        layout(title="Browse · PL Catalog", rel=rel, body=body, generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )


def render_curator_review_page(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
) -> int:
    """Render /review/curator/ — maintainer-facing triage of submitted labels.

    Reads `data/derived/extension_labels.csv`, groups by curator_status,
    surfaces evidence, link to GH issue, and an "Accept / Reject" action
    (which simply commenting on the issue does in practice).
    """
    labels_csv = ROOT / "data" / "derived" / "extension_labels.csv"
    rows = _read_csv(labels_csv)

    page = dist_root / "review" / "curator" / "index.html"
    rel = rel_prefix(page, dist_root)
    page.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        body = """
        <section class="panel section">
          <h1 style="margin:0 0 8px;">Curator triage</h1>
          <p>No manual labels submitted yet. Once reviewers start labelling extensions
          via the <a href="../extensions/index.html">review queue</a>, this page will
          show their submissions for maintainer review.</p>
          <p class='muted'>To ingest submitted labels:
            <code>python3 tools/process_extension_labels.py</code></p>
        </section>"""
    else:
        by_status: dict[str, list[dict]] = {}
        for r in rows:
            by_status.setdefault(r.get("curator_status") or "new", []).append(r)
        STATUS_ORDER = ["new", "needs-info", "accepted", "rejected"]

        sections = []
        for status in STATUS_ORDER:
            items = by_status.get(status, [])
            if not items:
                continue
            items.sort(key=lambda x: x.get("submitted_at", ""), reverse=True)
            row_html = []
            for r in items:
                ext = r.get("ext", "")
                label = r.get("label", "")
                friendly = r.get("friendly_name", "") or ""
                ref_url = r.get("reference_url", "") or ""
                annotator = r.get("annotator", "?")
                evidence = (r.get("evidence", "") or "")[:200]
                issue_url = r.get("issue_url", "")
                submitted = r.get("submitted_at", "")[:10]
                meta_bits = []
                if friendly:
                    meta_bits.append(f"<div class='muted' style='font-size:12px;'>{safe(friendly)}</div>")
                if ref_url:
                    meta_bits.append(
                        f"<div class='muted' style='font-size:12px;'>"
                        f"<a href='{safe(ref_url)}' target='_blank' rel='noopener'>↗ reference</a>"
                        f"</div>"
                    )
                row_html.append(
                    f"<tr>"
                    f"<td><a href='{rel}ext/{_ext_url_slug(ext)}/index.html'><code>{safe(ext)}</code></a></td>"
                    f"<td><span class='pill'>{safe(label)}</span>{''.join(meta_bits)}</td>"
                    f"<td><a href='https://github.com/{safe(annotator)}' target='_blank' rel='noopener'>@{safe(annotator)}</a></td>"
                    f"<td>{safe(submitted)}</td>"
                    f"<td style='font-size:13px;'>{safe(evidence)}</td>"
                    f"<td><a href='{safe(issue_url)}' target='_blank' rel='noopener'>issue</a></td>"
                    f"</tr>"
                )
            blurb = {
                "new":        "Just imported — needs maintainer review.",
                "needs-info": "Maintainer asked for more evidence; back to the reviewer.",
                "accepted":   "Maintainer-approved. These feed into ext_claim.csv as <code>strength=proposed</code>.",
                "rejected":   "Maintainer rejected. Kept for audit.",
            }.get(status, "")
            sections.append(f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">{safe(status)} ({len(items)})</h2>
          <p class='muted'>{blurb}</p>
          <table class='kv-table'>
            <thead><tr><th>Ext</th><th>Proposed label</th><th>Annotator</th><th>Submitted</th><th>Evidence (excerpt)</th><th></th></tr></thead>
            <tbody>{''.join(row_html)}</tbody>
          </table>
        </section>""")

        body = f"""
        <section class="panel section">
          <h1 style="margin:0 0 8px;">Curator triage</h1>
          <p>Submitted extension labels grouped by status. Maintainer action lives on the GitHub issues themselves: comment to discuss, edit <code>data/derived/extension_labels.csv</code> to set <code>curator_status=accepted</code> / <code>rejected</code> / <code>needs-info</code>, then re-run <code>python3 tools/process_extension_labels.py</code>.</p>
          <p class='muted'>Total submissions: {len(rows)} · See <a href="../extensions/index.html">review queue</a> for the source list.</p>
        </section>
        {''.join(sections)}"""

    page.write_text(
        layout(title="Curator review · PL Catalog", rel=rel, body=body,
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )
    return len(rows)


def render_extension_review_queue_page(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
) -> int:
    """Render /review/extensions/ — the ranked label-this-extension queue.

    Each row has a "Label this" link that opens a pre-filled GitHub issue
    capturing the extension, the annotator's login, the proposed label, and
    free-text evidence.

    Returns the number of queue rows rendered.
    """
    queue_csv = ROOT / "data" / "derived" / "extension_review_queue.csv"
    if not queue_csv.exists():
        return 0
    rows = _read_csv(queue_csv)

    # Existing labels (if any) so reviewers see what's been done.
    labels_csv = ROOT / "data" / "derived" / "extension_labels.csv"
    existing_labels: dict[str, list[dict]] = {}
    for r in _read_csv(labels_csv):
        existing_labels.setdefault(r.get("ext", ""), []).append(r)

    page = dist_root / "review" / "extensions" / "index.html"
    rel = rel_prefix(page, dist_root)
    page.parent.mkdir(parents=True, exist_ok=True)

    # Per-ext sample counts so each row can show "N samples available" — lets
    # reviewers see at a glance whether there's actual SWH evidence to look at
    # before deciding.
    samples_by_ext_for_queue = load_swh_samples_by_ext()

    listing = []
    for r in rows:
        ext = r["ext_canonical"]
        url_slug = _ext_url_slug(ext)
        total = int(r.get("total_occ", 0) or 0)
        ly = r.get("last_year") or ""
        suggested = r.get("suggested_label") or "unknown"
        n_claim = int(r.get("n_current_claimants") or 0)
        current = r.get("current_claimants") or "—"
        prior_labels = existing_labels.get(ext, [])
        prior_html = ""
        if prior_labels:
            prior_html = "<div class='muted' style='font-size:12px;'>"
            for pl in prior_labels[:3]:
                annotator = pl.get("annotator") or "?"
                label_text = pl.get("label") or ""
                prior_html += (
                    f"<span class='pill' title='by @{safe(annotator)}'>"
                    f"{safe(label_text)}</span> "
                )
            prior_html += "</div>"

        # Use the shared helper for the pre-filled issue URL.
        issue_url = _build_label_issue_url(
            ext=ext, total_occ=total, last_year=ly,
            current_claimants=current, suggested_label=suggested,
            github_owner_repo=github_owner_repo,
        )
        label_btn = (
            f"<a class='btn' href='{safe(issue_url)}' target='_blank' rel='noopener'>Label this</a>"
            if issue_url else "<span class='muted'>(GitHub repo not configured)</span>"
        )
        n_samples = len(samples_by_ext_for_queue.get(ext, []))
        samples_pill = (
            f"<a class='pill' style='background:rgba(80,200,120,0.18); color:#c6f0d4;' "
            f"href='{rel}ext/{url_slug}/index.html#samples' title='SWH samples available to inspect'>"
            f"👁 {n_samples}</a>"
            if n_samples else ""
        )

        listing.append(
            f"<tr>"
            f"<td><a href='{rel}ext/{url_slug}/index.html'><code>{safe(r['ext_raw'])}</code></a>"
            f"{prior_html}</td>"
            f"<td>{_fmt_occ(total)}</td>"
            f"<td>{safe(ly)}</td>"
            f"<td>{n_claim}</td>"
            f"<td>{safe(current) if current else '—'}</td>"
            f"<td><span class='pill src-taxonomy'>{safe(suggested)}</span></td>"
            f"<td>{samples_pill}</td>"
            f"<td>{label_btn}</td>"
            f"</tr>"
        )

    n_pending = sum(1 for r in rows if r.get("review_status") == "pending")
    n_labeled = sum(len(v) for v in existing_labels.values())

    # Compute the attribution-state breakdown across the SWH-popular subset
    # that the queue builder considered (≥ 10K occurrences, matching the
    # build_extension_review_queue.py default). Numbers match what the script
    # prints; see docs/SWH_EXTENSIONS_DECISIONS.md §11 for the rule.
    MIN_OCC = 10_000  # mirror tools/build_extension_review_queue.py default
    swh_pop = load_swh_ext_popularity()
    popular_exts: set[str] = {
        e for e, d in swh_pop.items() if (d.get("total_occ") or 0) >= MIN_OCC
    }

    n_well_attributed_in_taxonomy = 0
    n_well_attributed_popular = 0
    n_ext_in_taxonomy = 0
    try:
        ext_claim_csv = TAXONOMY_DIR / "ext_claim.csv"
        if ext_claim_csv.exists():
            AUTH = {"linguist", "pygments"}
            claims_by_ext: dict[str, list[dict]] = {}
            for c in _read_csv(ext_claim_csv):
                claims_by_ext.setdefault(c["ext"], []).append(c)
            n_ext_in_taxonomy = len(claims_by_ext)
            for ext, ext_claims in claims_by_ext.items():
                has_auth_primary = any(
                    c.get("strength") == "primary" and c.get("source") in AUTH
                    for c in ext_claims
                )
                distinct_entities = {
                    _canonical_pl_entity(c.get("pl_id", ""))
                    for c in ext_claims if c.get("pl_id")
                }
                if has_auth_primary or len(distinct_entities) == 1:
                    n_well_attributed_in_taxonomy += 1
                    if ext in popular_exts:
                        n_well_attributed_popular += 1
    except Exception:
        pass

    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Extension review queue</h1>
      <p>Ranked queue of file extensions present in Software Heritage that need a label. Sorted by priority — highest = most files in SWH and least already claimed by a PL in our taxonomy.</p>

      <div style='display:flex; flex-wrap:wrap; gap:10px; margin: 12px 0;'>
        <div class="stat"><div class="num">{len(rows):,}</div><div class="muted">in queue<br/>(popular ≥ {_fmt_occ(MIN_OCC)} occurrences &amp; not well-attributed)</div></div>
        <div class="stat"><div class="num">{n_well_attributed_popular:,}</div><div class="muted">popular exts skipped<br/>(≥ {_fmt_occ(MIN_OCC)} occurrences &amp; already well-attributed)</div></div>
        <div class="stat"><div class="num">{n_well_attributed_in_taxonomy:,}</div><div class="muted">well-attributed exts<br/>(whole taxonomy, any popularity)</div></div>
        <div class="stat"><div class="num">{n_ext_in_taxonomy:,}</div><div class="muted">total exts<br/>in taxonomy</div></div>
        <div class="stat"><div class="num">{n_labeled:,}</div><div class="muted">manual labels<br/>submitted so far</div></div>
      </div>

      <p class='muted'>An extension is "well-attributed" (skipped from this queue) if it has at least one primary claim from Linguist or Pygments, OR all claims agree on a single PL entity after consolidating master_inventory near-duplicates. See <a href='https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/SWH_EXTENSIONS_DECISIONS.md#11-provenance-contract-for-ext--pl-mappings' target='_blank' rel='noopener'>SWH_EXTENSIONS_DECISIONS.md §11</a> for the full attribution-state rule.</p>

      <p class='muted'>Vocabulary: <a href='https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/extension_labels.md' target='_blank' rel='noopener'>docs/extension_labels.md</a>.</p>
    </section>
    <section class="panel section">
      <p class='muted'>Auto-suggested labels are <em>hints</em> (rule-based on the extension string). Always override based on actual evidence.</p>
      <table class='kv-table'>
        <thead><tr><th>Extension</th><th>SWH</th><th>Last</th><th>#Claim</th><th>Current claimants</th><th>Auto-suggested</th><th>Samples</th><th>Action</th></tr></thead>
        <tbody>{''.join(listing)}</tbody>
      </table>
    </section>
    """
    page.write_text(
        layout(title="Extension review queue · PL Catalog", rel=rel, body=body,
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )
    return len(rows)


def render_samples_index_page(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
    languages: list[Language],
    enrichments: dict[str, TaxonomyEnrichment],
) -> int:
    """Write /samples/index.html — the curated index of every PL that has at
    least one real archived program from Software Heritage. Returns count.
    """
    # Dedupe by pl_id: multiple in-repo entries (e.g. "OCaml" and "Objective
    # Caml") can map to the same taxonomy entity. Pick the in-repo entry whose
    # canonical name best matches the taxonomy's canonical_name (shortest).
    rows_by_pl_id: dict[str, dict] = {}
    for lang in languages:
        enr = enrichments.get(lang.name)
        if not enr or not enr.swh_samples:
            continue
        prev = rows_by_pl_id.get(enr.pl_id)
        if prev is None or len(lang.name) < len(prev["lang"].name):
            rows_by_pl_id[enr.pl_id] = {
                "lang": lang,
                "enr": enr,
                "sample_count": len(enr.swh_samples),
                "total_occurrences": sum(s.occurrences_in_swh for s in enr.swh_samples),
                "top_sample": enr.swh_samples[0],
            }
    rows = list(rows_by_pl_id.values())
    rows.sort(key=lambda r: (-r["sample_count"], -r["total_occurrences"], r["lang"].name.lower()))

    page = dist_root / "samples" / "index.html"
    rel = rel_prefix(page, dist_root)
    page.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        body = f"""
        <section class="panel section">
          <h1 style="margin:0 0 8px;">Programs from Software Heritage</h1>
          <p>No PL has a mined SWH sample yet. Run
            <code>python3 tools/swh_extension_mining.py --shard '/tmp/swh_shards/0.parquet' --execute --sample-percent 1</code>
            then <code>python3 tools/fetch_samples.py</code>.</p>
        </section>"""
    else:
        list_rows = []
        for r in rows:
            lang, enr, top = r["lang"], r["enr"], r["top_sample"]
            # Bare content SWHID — always resolves on SWH browser even when the
            # qualified form's `;origin=...` fails (origin not in SWH's index).
            bare_browser_url = f"https://archive.softwareheritage.org/swh:1:cnt:{top.sha1_git}/"
            list_rows.append(
                f"<tr>"
                f"<td><a href='{rel}l/{lang.slug}/index.html'>{safe(lang.name)}</a></td>"
                f"<td><code>{safe(enr.pl_id)}</code></td>"
                f"<td>{r['sample_count']}</td>"
                f"<td>{r['total_occurrences']:,}</td>"
                f"<td>"
                f"<a href='{safe(bare_browser_url)}' target='_blank' rel='noopener'>"
                f"<code>{safe(top.filename)}</code> ({top.length} B)</a>"
                f"</td>"
                f"</tr>"
            )
        body = f"""
        <section class="panel section">
          <h1 style="margin:0 0 8px;">Programs from Software Heritage</h1>
          <p class='muted'>The {len(rows):,} programming languages in this catalog with at least one real archived program byte-verified against the SWH archive. Click a row for the full provenance chain and embedded source.</p>
        </section>
        <section class="panel section">
          <table class='kv-table'>
            <thead><tr><th>Language</th><th>pl_id</th><th>Samples</th><th>Σ origin occurrences</th><th>Top sample</th></tr></thead>
            <tbody>{''.join(list_rows)}</tbody>
          </table>
        </section>"""
    page.write_text(
        layout(title="Samples · PL Catalog", rel=rel, body=body,
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )
    return len(rows)


def render_source_pages(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
    languages: list[Language],
    enrichments: dict[str, TaxonomyEnrichment],
) -> int:
    """Write /source/<src>/index.html for each upstream taxonomy source, plus an
    index at /source/. Each lists all PLs the source asserts the existence of.
    Returns count of source pages written (excludes the index)."""
    # pl_id -> slug for linking back to PL pages.
    pl_id_to_slug: dict[str, str] = {}
    pl_id_to_name: dict[str, str] = {}
    for lang in languages:
        enr = enrichments.get(lang.name)
        if enr:
            pl_id_to_slug.setdefault(enr.pl_id, lang.slug)
            pl_id_to_name.setdefault(enr.pl_id, lang.name)

    # Group enriched langs by source.
    by_source: dict[str, list[tuple[str, str, str]]] = {s: [] for s in _TAXONOMY_SOURCES}
    by_source["llm"] = []  # LLM-curated in-repo
    for lang in languages:
        enr = enrichments.get(lang.name)
        if not enr:
            continue
        for src in _TAXONOMY_SOURCES:
            if enr.in_sources.get(src):
                by_source[src].append((lang.name, lang.slug, enr.pl_id))
        if lang.programs:
            by_source["llm"].append((lang.name, lang.slug, enr.pl_id))

    SOURCE_BLURBS = {
        "pldb": "Programming Language DataBase — a curated community DB.",
        "linguist": "GitHub's Linguist — the file-type detector used to render \"% of repo\" stats on GitHub.",
        "pygments": "Pygments — the syntax highlighter; entry means there's a hand-written lexer.",
        "wikipedia": "Wikipedia article in the Programming Language category.",
        "esolang": "esolangs.org — the catalog of esoteric languages.",
        "hyperpolyglot": "hyperpolyglot.org — side-by-side language comparison tables.",
        "rosettacode": "Rosetta Code — task implementations across languages.",
        "llm": "Curated by an LLM agent in this repo (has at least one example program).",
    }

    out_dir = dist_root / "source"
    out_dir.mkdir(parents=True, exist_ok=True)

    n_pages = 0
    for src, entries in by_source.items():
        if not entries:
            continue
        entries.sort(key=lambda t: t[0].lower())
        rows = []
        for name, slug, pl_id in entries:
            rows.append(
                f"<tr><td><a href='../../l/{slug}/index.html'>{safe(name)}</a></td>"
                f"<td><code>{safe(pl_id)}</code></td></tr>"
            )
        page = out_dir / src / "index.html"
        rel = rel_prefix(page, dist_root)
        body = f"""
        <div class="breadcrumbs">
          <a href="{rel}index.html">Home</a> · <a href="{rel}source/index.html">Sources</a> · {safe(src.capitalize())}
        </div>
        <section class="panel section">
          <h1 style="margin:0 0 8px;"><span class='pill src-{src}'>{safe(src.capitalize())}</span></h1>
          <p class='muted'>{safe(SOURCE_BLURBS.get(src, ''))}</p>
          <div style='display:flex; flex-wrap:wrap; gap:10px;'>
            <span class='pill'>{len(entries):,} languages</span>
          </div>
        </section>
        <section class="panel section">
          <table class='kv-table'>
            <thead><tr><th>Language</th><th>pl_id</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </section>
        """
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            layout(title=f"{src.capitalize()} · Sources · PL Catalog", rel=rel,
                   body=body, generated_at=generated_at,
                   github_owner_repo=github_owner_repo),
            encoding="utf-8",
        )
        n_pages += 1

    # /source/index.html
    listing = []
    for src in ["llm"] + list(_TAXONOMY_SOURCES):
        n = len(by_source.get(src, []))
        if n == 0:
            continue
        listing.append(
            f"<tr><td><a href='./{src}/index.html'><span class='pill src-{src}'>{safe(src.capitalize())}</span></a></td>"
            f"<td>{n:,}</td><td>{safe(SOURCE_BLURBS.get(src, ''))}</td></tr>"
        )
    page = out_dir / "index.html"
    rel = rel_prefix(page, dist_root)
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Sources</h1>
      <p class='muted'>Where each programming-language record comes from. A PL can be in multiple sources; cross-presence is what makes attribution credible.</p>
    </section>
    <section class="panel section">
      <table class='kv-table'>
        <thead><tr><th>Source</th><th>PLs</th><th>What it is</th></tr></thead>
        <tbody>{''.join(listing)}</tbody>
      </table>
    </section>
    """
    page.write_text(
        layout(title="Sources · PL Catalog", rel=rel, body=body,
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )
    return n_pages


# Suffixes that master_inventory appends when canonical-name slugs collide or
# when a name has the form "Foo (programming language)". Stripped before
# comparing pl_ids for the attribution-state heuristic, so that `pl/cpp` and
# `pl/cpp-3` (the same C++ under two upstream-source spellings) don't count
# as separate claimants of `.cc`.
_PL_ENTITY_DEDUP_SUFFIXES = [
    "-programming-language",
    "-the-programming-language",
    "-programminglanguage",
    "-lang",
    "-language",
]


def _canonical_pl_entity(pl_id: str) -> str:
    """Normalise a pl_id to its 'conceptual entity' base.

    Examples:
      pl/cpp                          -> pl/cpp
      pl/cpp-3                        -> pl/cpp   (numeric collision dedup)
      pl/python-programming-language  -> pl/python
      pl/hack                         -> pl/hack  (unchanged)
    """
    base = pl_id
    for s in _PL_ENTITY_DEDUP_SUFFIXES:
        if base.endswith(s):
            base = base[: -len(s)]
            break
    return re.sub(r"-\d+$", "", base)


def _ext_url_slug(ext: str) -> str:
    """Filesystem/URL-safe key for an extension. `.m` -> 'm'; `.++` -> 'pp'."""
    s = ext.lstrip(".")
    s = s.replace("+", "p").replace("#", "sharp").replace("@", "at").replace("*", "star")
    s = re.sub(r"[^a-z0-9_-]+", "-", s.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unknown"


def compute_taxonomy_stats(
    *,
    languages: list[Language],
    enrichments: dict[str, TaxonomyEnrichment],
) -> dict[str, Any]:
    """Aggregate stats about the cross-source taxonomy + SWH evidence."""
    n_total = len(languages)
    n_in_repo = sum(1 for l in languages if l.added_at)  # taxonomy-only langs have added_at=""
    n_taxonomy_only = n_total - n_in_repo
    n_enriched = len(enrichments)

    # PLs with at least 1 SWH sample.
    n_with_swh = sum(1 for e in enrichments.values() if e.swh_samples)
    total_swh_samples = sum(len(e.swh_samples) for e in enrichments.values())

    # Per-source counts.
    per_source = {s: 0 for s in _TAXONOMY_SOURCES}
    source_count_distribution: dict[int, int] = {}
    for e in enrichments.values():
        n_present = 0
        for s, present in e.in_sources.items():
            if present:
                per_source[s] += 1
                n_present += 1
        source_count_distribution[n_present] = source_count_distribution.get(n_present, 0) + 1

    # ext_claim breakdown.
    claim_breakdown: dict[tuple[str, str], int] = {}
    for r in _read_csv(TAXONOMY_DIR / "ext_claim.csv"):
        k = (r.get("source", ""), r.get("strength", ""))
        claim_breakdown[k] = claim_breakdown.get(k, 0) + 1

    # Polysemy distribution from ext_summary.
    polysemy_dist: dict[int, int] = {}
    n_with_heuristic_ext = 0
    heur_exts = set()
    for h in _read_csv(TAXONOMY_DIR / "heuristic.csv"):
        if h.get("applies_to_ext"):
            heur_exts.add(h["applies_to_ext"])
    n_ext_total = 0
    for r in _read_csv(TAXONOMY_DIR / "ext_summary.csv"):
        n_ext_total += 1
        np = int(r.get("n_primary", 0) or 0)
        polysemy_dist[np] = polysemy_dist.get(np, 0) + 1
    n_with_heuristic_ext = len(heur_exts)

    # How many PLs have at least one extension claim? Key progress indicator:
    # over time, manual labelling promotes new (pl, ext) edges into
    # ext_claim.csv, so this number should grow. Counts the *number of pl_ids*
    # that appear in ext_claim.csv (any source, any strength).
    pl_rows = _read_csv(TAXONOMY_DIR / "pl.csv")
    n_pls_in_taxonomy = sum(1 for p in pl_rows if p.get("pl_id"))
    pls_with_ext: set[str] = set()
    for r in _read_csv(TAXONOMY_DIR / "ext_claim.csv"):
        if r.get("pl_id"):
            pls_with_ext.add(r["pl_id"])
    n_pls_with_ext = len(pls_with_ext)
    pct_pls_with_ext = (100.0 * n_pls_with_ext / n_pls_in_taxonomy) if n_pls_in_taxonomy else 0.0

    return {
        "n_total_pl_pages": n_total,
        "n_in_repo": n_in_repo,
        "n_taxonomy_only": n_taxonomy_only,
        "n_enriched": n_enriched,
        "n_with_swh_evidence": n_with_swh,
        "total_swh_samples": total_swh_samples,
        "per_source": per_source,
        "source_count_distribution": dict(sorted(source_count_distribution.items())),
        "claim_breakdown": claim_breakdown,
        "polysemy_dist": dict(sorted(polysemy_dist.items())),
        "n_ext_total": n_ext_total,
        "n_exts_with_heuristic": n_with_heuristic_ext,
        "n_pls_in_taxonomy": n_pls_in_taxonomy,
        "n_pls_with_ext": n_pls_with_ext,
        "pct_pls_with_ext": pct_pls_with_ext,
    }


def _build_label_issue_url(
    *, ext: str, total_occ: int, last_year: str | int | None,
    current_claimants: str, suggested_label: str,
    github_owner_repo: str | None,
) -> str | None:
    """Build the GitHub pre-filled-issue URL for labelling an extension.

    Used as a fallback / shareable link. The preferred path on per-ext pages
    is the inline form which builds the URL client-side from form fields
    (label, friendly_name, reference_url, evidence) — this server-side helper
    is the "no-form" backup with just the suggested label pre-filled.
    """
    if not github_owner_repo:
        return None
    body = (
        f"<!-- ext-review: structured block below is parsed by tools/process_extension_labels.py -->\n"
        f"```yaml\n"
        f"ext: \"{ext}\"\n"
        f"label: \"{suggested_label}\"\n"
        f"friendly_name: \"\"\n"
        f"reference_url: \"\"\n"
        f"evidence: |\n"
        f"  (1-2 sentences justifying the label; cite URLs if available.)\n"
        f"```\n\n"
        f"## Context\n\n"
        f"- Extension: `{ext}` ({_fmt_occ(total_occ)} occurrences in SWH, "
        f"last seen {last_year or 'unknown'})\n"
        f"- Current PL claimants: {current_claimants or '(none)'}\n"
        f"- Auto-suggested label: `{suggested_label}`\n"
        f"- Full vocabulary: <https://github.com/{github_owner_repo}/blob/main/docs/extension_labels.md>\n"
    )
    return github_new_issue_url(
        owner_repo=github_owner_repo,
        title=f"Label extension: {ext}",
        body=body,
    ) + "&labels=ext-review"


def _build_sample_request_block(
    ext: str,
    *,
    github_owner_repo: str | None,
    sample_count: int,
) -> str:
    """Render the "Request SWH samples for this extension" panel.

    Opens a pre-filled GitHub issue with the `sample-request` label that
    `tools/process_sample_requests.py` later picks up to drive an explicit
    SWH mining run targeted at this extension.

    Returns an empty string when no GitHub repo is configured.
    """
    if not github_owner_repo:
        return ""
    headline = (
        "Need an archived example for this extension?"
        if sample_count == 0 else
        "Request more SWH-mined examples"
    )
    blurb = (
        f"No verbatim file with extension <code>{safe(ext)}</code> in our local "
        f"SWH mirror yet. Submit a sample-mining request and a maintainer will run "
        f"<code>swh_extension_mining.py</code> against the live archive for this "
        f"extension; samples land here once the run completes."
        if sample_count == 0 else
        f"If the examples above don't disambiguate what <code>{safe(ext)}</code> is, "
        f"request a fresh mining run."
    )
    return f"""
          <form class="sample-request-form"
                data-ext="{safe(ext)}"
                data-repo="{safe(github_owner_repo)}"
                style="margin-top:14px; padding:12px; border:1px dashed var(--border, #2a2a2a); border-radius:8px;">
            <div style="display:flex; flex-direction:column; gap:8px;">
              <div>
                <strong>{headline}</strong>
                <div class="muted" style="font-size:13px; margin-top:4px;">{blurb}</div>
              </div>
              <label style="display:flex; flex-direction:column; gap:4px;">
                <span class="muted" style="font-size:12px;">Optional notes — what are you trying to figure out? (e.g., "disambiguate from .java", "looking for examples that show macro expansion")</span>
                <textarea name="notes" rows="2" placeholder="(optional)"
                          style="font-family:inherit; font-size:13px;"></textarea>
              </label>
              <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                <button class="btn" type="submit">Request SWH samples (opens GitHub)</button>
                <a class="sample-request-fallback-link btn" href="#" target="_blank" rel="noopener"
                   style="text-decoration:none; font-size:13px;">
                  (or open the pre-filled issue directly)
                </a>
              </div>
              <div class="sample-request-status muted" style="font-size:12px; min-height:1em;"></div>
            </div>
          </form>"""


# Vocabulary used by the per-extension labelling form. Mirrors `docs/extension_labels.md`.
LABEL_VOCAB_GROUPS = [
    ("Programming language", [
        ("pl/<id>",            "existing PL — enter pl_id in custom field"),
        ("pl/new:<name>",      "propose a NEW PL"),
        ("pl/dialect:<parent>", "dialect of an existing PL"),
        ("pl/family:<family>", "shared by a family (e.g., basic, pascal)"),
    ]),
    ("Binary formats", [
        ("binary:image",       "PNG, JPG, SVG, …"),
        ("binary:audio",       "MP3, WAV, …"),
        ("binary:video",       "MP4, WebM, …"),
        ("binary:font",        "TTF, WOFF, …"),
        ("binary:archive",     "ZIP, TAR, GZ, …"),
        ("binary:executable",  "DLL, EXE, .pyc, .class, …"),
        ("binary:db",          "DB, SQLite, …"),
        ("binary:other",       "PDF, DOCX, …"),
    ]),
    ("Data / config", [
        ("data:json-like",     "JSON or JSON-derived"),
        ("data:xml-like",      "XML or XML-derived"),
        ("data:yaml",          "YAML"),
        ("data:csv-tsv",       "tabular plain text"),
        ("data:config",        "INI, TOML, etc."),
        ("data:domain",        "domain-specific (.npy, .mat, .uasset)"),
    ]),
    ("Other", [
        ("docs",               "documentation / markup"),
        ("lock/cache",         "lock files, caches, backups"),
        ("build-artifact",     "build outputs"),
        ("model/data",         "ML model files"),
        ("license/manifest",   "project meta-files"),
        ("numeric-suffix",     "manpage section / version"),
        ("sha-filename",       "content-addressable hex name"),
        ("noise",              "single-project / typo / not worth labelling"),
        ("unknown",            "I looked and couldn't classify"),
    ]),
]


def _load_extension_labels() -> dict[str, list[dict]]:
    """Return {ext: [label_rows]} from data/derived/extension_labels.csv."""
    path = ROOT / "data" / "derived" / "extension_labels.csv"
    out: dict[str, list[dict]] = {}
    if not path.exists():
        return out
    for r in _read_csv(path):
        ext = r.get("ext", "")
        if ext:
            out.setdefault(ext, []).append(r)
    return out


def render_per_extension_pages(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
    languages: list[Language],
    enrichments: dict[str, TaxonomyEnrichment],
) -> int:
    """Write /ext/<slug>/index.html for every extension that has at least one
    taxonomy claim, heuristic, or mined SWH sample. Returns page count."""
    # Build pl_id -> in-site language slug index (for linking).
    pl_id_to_slug: dict[str, str] = {}
    for lang in languages:
        enr = enrichments.get(lang.name)
        if enr:
            pl_id_to_slug.setdefault(enr.pl_id, lang.slug)

    ext_summary_rows = _read_csv(TAXONOMY_DIR / "ext_summary.csv")
    ext_claim_rows = _read_csv(TAXONOMY_DIR / "ext_claim.csv")
    heuristic_rows = _read_csv(TAXONOMY_DIR / "heuristic.csv")
    pl_rows = _read_csv(TAXONOMY_DIR / "pl.csv")
    pl_canonical = {r["pl_id"]: (r.get("canonical_name") or r["pl_id"])
                    for r in pl_rows if r.get("pl_id")}

    claims_by_ext: dict[str, list[dict]] = {}
    for c in ext_claim_rows:
        claims_by_ext.setdefault(c["ext"], []).append(c)
    heur_by_ext: dict[str, list[dict]] = {}
    for h in heuristic_rows:
        heur_by_ext.setdefault(h["applies_to_ext"], []).append(h)

    swh_by_pl = load_swh_samples()
    # `swh_by_ext` is built independently via `load_swh_samples_by_ext` so that
    # orphan unclassified samples (those whose ext has no primary claimant in
    # the taxonomy) ALSO appear on the per-ext page. Critical for the review
    # workflow: a reviewer landing on /ext/.pbf/ needs to see actual `.pbf`
    # bytes to decide it's Protocol Buffers binary, not a programming
    # language.
    swh_by_ext: dict[str, list[SwhSample]] = load_swh_samples_by_ext()

    strength_rank = {"primary": 0, "secondary": 1, "unknown": 2}

    # SWH-MSR-ARV-derived per-extension popularity (one row per ext, year-by-year totals).
    swh_pop = load_swh_ext_popularity()

    # Existing manual labels (from extension_labels.csv).
    existing_labels = _load_extension_labels()

    # External (non-PL) extension index — Wikidata + Wikipedia infobox.
    external_ext = load_external_extension_index()
    EXTERNAL_DISPLAY_LIMIT = 20

    # Union of every extension we know about (taxonomy summary + heuristics + samples
    # + external Wikidata index + top-N most-popular from SWH that aren't
    # otherwise covered). Adding the external index keys ensures that
    # Wikipedia-only extensions like .mpga (which Wikidata doesn't model
    # but the Wikipedia MP3 infobox does carry) get their own /ext/ page.
    all_exts: set[str] = set()
    for r in ext_summary_rows:
        all_exts.add(r["ext"])
    all_exts.update(heur_by_ext.keys())
    all_exts.update(swh_by_ext.keys())
    all_exts.update(external_ext.keys())
    # Include top SWH-popular extensions even if our taxonomy doesn't claim them.
    # Cap at 8000 so per-extension pages stay manageable (2.96M total in SWH-MSR-ARV's
    # CSV; most have <100 occurrences total or are non-PL artifacts).
    SWH_POPULARITY_PAGE_LIMIT = 8000
    popular_swh = sorted(swh_pop.items(), key=lambda kv: -kv[1]["total_occ"])[:SWH_POPULARITY_PAGE_LIMIT]
    for ext, _ in popular_swh:
        all_exts.add(ext)

    summary_by_ext = {r["ext"]: r for r in ext_summary_rows}
    ext_dir = dist_root / "ext"
    ext_dir.mkdir(parents=True, exist_ok=True)
    n_pages = 0

    for ext in sorted(all_exts):
        url_slug = _ext_url_slug(ext)
        page = ext_dir / url_slug / "index.html"
        rel = rel_prefix(page, dist_root)

        summary = summary_by_ext.get(ext, {})
        n_total = int(summary.get("n_claimants", 0) or 0)
        n_primary = int(summary.get("n_primary", 0) or 0)
        n_secondary = int(summary.get("n_secondary", 0) or 0)
        polysemy_pill = ""
        if n_primary >= 2:
            polysemy_pill = f"<span class='pill strength-unknown'>shared primary ({n_primary})</span>"
        elif n_primary == 1:
            polysemy_pill = "<span class='pill strength-primary'>unambiguous primary</span>"
        elif n_secondary > 0:
            polysemy_pill = "<span class='pill strength-secondary'>secondary-only</span>"

        # Claimants table.
        claims = sorted(
            claims_by_ext.get(ext, []),
            key=lambda c: (strength_rank.get(c["strength"], 9),
                           pl_canonical.get(c["pl_id"], "").lower()),
        )
        claim_rows_html = []
        for c in claims:
            pid = c["pl_id"]
            name = pl_canonical.get(pid, pid)
            slug = pl_id_to_slug.get(pid)
            link = f"<a href='{rel}l/{slug}/index.html'>{safe(name)}</a>" if slug else safe(name)
            badge = f"<span class='pill strength-{c['strength']}'>{safe(c['strength'])}</span>"
            claim_rows_html.append(
                f"<tr><td>{link}</td><td>{safe(c['source'])}</td><td>{badge}</td></tr>"
            )

        # Heuristics table.
        heur_rows_html = []
        for h in heur_by_ext.get(ext, []):
            pid = h.get("predicts_pl_id", "")
            name = pl_canonical.get(pid, h.get("predicts_language", "") or pid or "?")
            slug = pl_id_to_slug.get(pid)
            link = f"<a href='{rel}l/{slug}/index.html'>{safe(name)}</a>" if slug else safe(name)
            heur_rows_html.append(
                f"<tr><td><code>{safe(h.get('heuristic_id',''))}</code></td>"
                f"<td>{link}</td>"
                f"<td>{safe(h.get('pattern_kind',''))}</td>"
                f"<td><code style='white-space:pre-wrap; word-break:break-all;'>"
                f"{safe((h.get('predicates_json','') or '')[:200])}</code></td></tr>"
            )

        # SWH samples (grouped by predicted PL for clarity).
        sample_items = []
        for s in sorted(swh_by_ext.get(ext, []), key=lambda x: -x.occurrences_in_swh):
            pid = s.pl_id
            name = pl_canonical.get(pid, pid)
            slug = pl_id_to_slug.get(pid)
            pl_link = f"<a href='{rel}l/{slug}/index.html'>{safe(name)}</a>" if slug else safe(name)
            # Bare-SWHID browser URL (always resolves; the qualified one can
            # 404 if SWH hasn't indexed the attributed origin yet).
            bare_browser_url = f"https://archive.softwareheritage.org/swh:1:cnt:{s.sha1_git}/"
            sample_items.append(f"""
              <article class="panel" style="margin-bottom:10px; padding:12px;">
                <header style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; align-items:baseline;">
                  <div><strong>{safe(s.filename)}</strong> <span class='muted'>· {s.length} B · seen {s.occurrences_in_swh}× in SWH</span></div>
                  <div>predicted: {pl_link} <span class='pill'>via {safe(s.predicted_via)}</span></div>
                </header>
                <div class='muted' style='font-family:monospace; word-break:break-all; margin-top:4px;'>{safe(s.qualified_swhid)}</div>
                <div style='margin-top:6px;'>
                  <a href='{safe(bare_browser_url)}' target='_blank' rel='noopener'>Open in SWH</a> ·
                  <a href='{safe(s.swh_raw_url)}' target='_blank' rel='noopener'>Raw bytes</a>
                </div>
              </article>""")

        # SWH popularity block (SWH-MSR-ARV-derived). Case-aggregated.
        swh_pop_html = ""
        swh_pop_info = swh_pop.get(ext)
        if swh_pop_info:
            total = swh_pop_info["total_occ"]
            recent = swh_pop_info["recent_occ"]
            fy = swh_pop_info["first_year"]
            ly = swh_pop_info["last_year"]
            span = f"{fy}–{ly}" if (fy and ly) else "n/a"
            recent_pct = (100 * recent / total) if total else 0
            variants = swh_pop_info.get("case_variants") or []
            variants_html = ""
            if len(variants) > 1:
                sorted_var = sorted(variants, key=lambda v: -v[1])
                variants_html = (
                    "<p class='muted' style='margin-top:8px;'>Case variants in archive: "
                    + ", ".join(f"<code>{safe(v[0])}</code> ({_fmt_occ(v[1])})" for v in sorted_var)
                    + " &mdash; aggregated above.</p>"
                )
            swh_pop_html = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">SWH popularity</h2>
          <p class='muted'>From the <strong>SWH-MSR-ARV</strong> dataset (Desmazières, Di Cosmo, Lorentz, <em>MSR 2025</em>; file <code>nb_extensions_alphanum.csv</code>) — one row per (ext, year) in the full SWH archive. Case-aggregated. <a href='https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/citations.md' target='_blank' rel='noopener'>citation</a>.</p>
          <div style='display:flex; flex-wrap:wrap; gap:10px;'>
            <div class="stat"><div class="num">{_fmt_occ(total)}</div><div class="muted">total occurrences</div></div>
            <div class="stat"><div class="num">{_fmt_occ(recent)}</div><div class="muted">since 2019 ({recent_pct:.1f}%)</div></div>
            <div class="stat"><div class="num">{span}</div><div class="muted">years active</div></div>
          </div>
          {variants_html}
        </section>"""

        claimants_section = ""
        if claim_rows_html:
            claimants_section = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Claimants ({len(claim_rows_html)})</h2>
          <div class='muted' style='margin-bottom:8px;'>Languages that list <code>{safe(ext)}</code> among their extensions. Strength reflects whether the upstream source treated it as their primary extension.</div>
          <table class='kv-table'>
            <thead><tr><th>Language</th><th>Source</th><th>Strength</th></tr></thead>
            <tbody>{''.join(claim_rows_html)}</tbody>
          </table>
        </section>"""

        # ----- Non-PL Wikidata/Wikipedia claimants (Phase C external index) -----
        # File formats, image formats, audio codecs, etc. that claim this
        # extension per Wikidata's P1195 — anything that's not a programming
        # language. Designed to help labelling-form reviewers identify e.g.
        # `.mp3` as "MP3 audio" without leaving the page.
        external_rows = external_ext.get(ext, [])
        external_section = ""
        if external_rows:
            shown = external_rows[:EXTERNAL_DISPLAY_LIMIT]
            n_more = len(external_rows) - len(shown)
            ext_html_rows = []
            for r in shown:
                qid = r.get("qid") or ""
                label = r.get("label") or qid
                desc = r.get("description") or ""
                wd_url = r.get("wikidata_url") or ""
                wp_url = r.get("wikipedia_url") or ""
                wp_note = r.get("wikipedia_note") or ""
                source_tag = r.get("source") or ""
                rank = r.get("wikidata_rank") or ""
                mime = r.get("mime_types") or ""
                instance_of = r.get("instance_of_labels") or ""
                suggested = r.get("suggested_label") or ""
                # Show only the first two instance_of labels — enough for
                # the reviewer to recognise the class, full list is in the CSV.
                instance_of_short = "; ".join(
                    [t.strip() for t in instance_of.split(";") if t.strip()][:2]
                )
                # Label cell: link to Wikipedia if we have it, else Wikidata.
                primary_link = wp_url or wd_url
                if primary_link:
                    label_html = (
                        f"<a href='{safe(primary_link)}' target='_blank' "
                        f"rel='noopener'>{safe(label)}</a>"
                    )
                else:
                    label_html = safe(label)
                # Secondary link to Wikidata (always present).
                if wd_url:
                    label_html += (
                        f" <a class='muted' href='{safe(wd_url)}' "
                        f"target='_blank' rel='noopener' "
                        f"title='Wikidata item'>{safe(qid)}</a>"
                    )
                # Notes: combine wikipedia_note + rank=deprecated marker + source tag
                note_bits = []
                if wp_note:
                    note_bits.append(f"<em>{safe(wp_note)}</em>")
                if rank == "deprecated":
                    note_bits.append("<span class='pill strength-deprecated'>deprecated</span>")
                if source_tag == "wikipedia":
                    note_bits.append(
                        "<span class='muted' title='From Wikipedia infobox, "
                        "not Wikidata structured data'>wp-only</span>"
                    )
                notes_html = " ".join(note_bits) or "&mdash;"
                suggested_cell = (
                    f"<span class='pill'>{safe(suggested)}</span>" if suggested else "&mdash;"
                )
                ext_html_rows.append(
                    f"<tr>"
                    f"<td>{label_html}"
                    + (f"<div class='muted' style='font-size:12px;'>{safe(desc)}</div>" if desc else "")
                    + f"</td>"
                    f"<td><span class='muted'>{safe(instance_of_short)}</span></td>"
                    f"<td>{suggested_cell}</td>"
                    f"<td><code class='muted'>{safe(mime) or '&mdash;'}</code></td>"
                    f"<td>{notes_html}</td>"
                    f"</tr>"
                )
            more_row = ""
            if n_more > 0:
                more_row = (
                    f"<tr><td colspan='5' class='muted' style='text-align:center;'>"
                    f"… and {n_more} more in "
                    f"<code>data/derived/external_extension_index.csv</code>"
                    f"</td></tr>"
                )
            external_section = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Wikidata says… ({len(external_rows)})</h2>
          <div class='muted' style='margin-bottom:8px;'>
            File formats, image formats, audio codecs and other non-PL
            entities that claim <code>{safe(ext)}</code> on Wikidata
            (property <code>P1195</code>) or in the Wikipedia infobox.
            Independent from the language taxonomy above &mdash;
            useful when labelling the extension as
            <code>binary:*</code> / <code>data:*</code> rather than a PL.
            Source: <code>data/derived/external_extension_index.csv</code>.
          </div>
          <table class='kv-table'>
            <thead><tr><th>Format</th><th>Class (Wikidata <code>P31</code>)</th><th>Suggested label</th><th>MIME</th><th>Notes</th></tr></thead>
            <tbody>{''.join(ext_html_rows)}{more_row}</tbody>
          </table>
        </section>"""
        heur_section = ""
        if heur_rows_html:
            heur_section = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Disambiguation rules ({len(heur_rows_html)})</h2>
          <div class='muted' style='margin-bottom:8px;'>Linguist heuristics that decide, by content, which language a <code>{safe(ext)}</code> file actually is.</div>
          <table class='kv-table'>
            <thead><tr><th>Rule</th><th>Predicts</th><th>Kind</th><th>Predicates (truncated)</th></tr></thead>
            <tbody>{''.join(heur_rows_html)}</tbody>
          </table>
        </section>"""
        sample_request_block = _build_sample_request_block(
            ext, github_owner_repo=github_owner_repo, sample_count=len(sample_items),
        )
        if sample_items:
            swh_section = f"""
        <section id="samples" class="panel section">
          <h2 style="margin:0 0 8px;">SWH-mined examples ({len(sample_items)})</h2>
          <div class='muted' style='margin-bottom:10px;'>Real archived programs with this extension, byte-verified against the SWH archive. Useful for deciding what this extension actually is when the attribution is uncertain.</div>
          {''.join(sample_items)}
          {sample_request_block}
        </section>"""
        elif claim_rows_html or heur_rows_html:
            # Has claims/heuristics but no archived bytes yet — surface the
            # request form so reviewers can ask for samples to disambiguate.
            swh_section = f"""
        <section id="samples" class="panel section">
          <h2 style="margin:0 0 8px;">SWH-mined examples (0)</h2>
          <p class='muted'>No archived examples for <code>{safe(ext)}</code> in our local mirror yet.</p>
          {sample_request_block}
        </section>"""
        else:
            swh_section = f"""
        <section id="samples" class="panel section">
          <h2 style="margin:0 0 8px;">SWH-mined examples (0)</h2>
          <p class='muted'>No claimants, heuristics, or SWH samples indexed for <code>{safe(ext)}</code> yet.</p>
          {sample_request_block}
        </section>"""

        # ----- Label-this section: adapt to attribution status -----
        # Classify the extension's attribution state:
        #   well-attributed: ≥1 primary claim from {linguist, pygments} (authoritative
        #     upstream sources). Most reviewers shouldn't need to label these;
        #     surface a small "Disagree?" link instead of a prominent button.
        #   weakly-attributed: only secondary / unknown / proposed claims.
        #     Reviewers may want to confirm or correct.
        #   unattributed: no claims at all. Prime review target.
        AUTHORITATIVE = {"linguist", "pygments"}
        n_primary_authoritative = sum(
            1 for c in claims
            if c.get("strength") == "primary" and c.get("source") in AUTHORITATIVE
        )
        # Reasons to call an extension well-attributed:
        # 1. At least one authoritative primary claim (the canonical case).
        # 2. ALL claims (across all sources, all strengths) point to ONE PL
        #    entity. E.g. `.cc` is secondary in both Linguist and Pygments but
        #    every claimant is C++.
        # pl_ids are consolidated through `_canonical_pl_entity` so that
        # master_inventory duplicates (`pl/cpp` + `pl/cpp-3`) collapse.
        distinct_entities = {
            _canonical_pl_entity(c["pl_id"]) for c in claims if c.get("pl_id")
        }
        all_claims_agree_on_one_pl = len(distinct_entities) == 1 and bool(claims)

        # `confirmed-polysemous`: there ARE multiple distinct PL entities, but
        # every authoritative upstream source (Linguist + Pygments) that
        # touches this ext produces the SAME set of entities. The ambiguity is
        # real (content needed to disambiguate) but it's not a data quality
        # problem — both sources agree on the shape. Classic case: `.h` is
        # C / C++ / Objective-C in both Linguist and Pygments. The disambig
        # layer (Linguist heuristics) handles it at content time, so reviewers
        # don't need to "label" it manually.
        auth_source_entity_sets: dict[str, frozenset[str]] = {}
        for c in claims:
            src = c.get("source", "")
            pid = c.get("pl_id", "")
            if src in AUTHORITATIVE and pid:
                ent = _canonical_pl_entity(pid)
                cur = auth_source_entity_sets.get(src, frozenset())
                auth_source_entity_sets[src] = cur | {ent}
        all_auth_sources_agree = (
            len(auth_source_entity_sets) >= 2
            and len(set(auth_source_entity_sets.values())) == 1
        )

        if n_primary_authoritative >= 1 or all_claims_agree_on_one_pl:
            attribution_state = "well-attributed"
        elif all_auth_sources_agree and len(distinct_entities) >= 2:
            attribution_state = "confirmed-polysemous"
        elif claims:
            attribution_state = "weakly-attributed"
        else:
            attribution_state = "unattributed"

        # Suggested label for the pre-filled issue:
        #   - well-attributed: no-change-needed (reviewer must explicitly change to dispute)
        #   - weakly-attributed: the top-claimant pl_id (the reviewer might confirm or refute)
        #   - unattributed: "unknown" (reviewer picks)
        if attribution_state == "well-attributed":
            suggested_for_label = "no-change-needed"
        elif claims:
            suggested_for_label = claims[0].get("pl_id", "unknown")
        else:
            suggested_for_label = "unknown"

        prior_for_ext = existing_labels.get(ext, [])
        prior_block = ""
        if prior_for_ext:
            rows_lbl = []
            for pl in prior_for_ext:
                annotator = pl.get("annotator") or "?"
                lbl = pl.get("label") or ""
                friendly = pl.get("friendly_name") or ""
                ref_url = pl.get("reference_url") or ""
                status = pl.get("curator_status") or "new"
                issue_url = pl.get("issue_url") or ""
                evidence = (pl.get("evidence") or "")[:140]
                friendly_html = (
                    f"<div class='muted' style='font-size:12px;'>{safe(friendly)}"
                    + (f" — <a href='{safe(ref_url)}' target='_blank' rel='noopener'>ref</a>" if ref_url else "")
                    + "</div>"
                    if friendly or ref_url else ""
                )
                rows_lbl.append(
                    f"<tr><td><span class='pill'>{safe(lbl)}</span>{friendly_html}</td>"
                    f"<td><a href='https://github.com/{safe(annotator)}' target='_blank' rel='noopener'>@{safe(annotator)}</a></td>"
                    f"<td><span class='pill strength-{safe(status)}'>{safe(status)}</span></td>"
                    f"<td>{safe(evidence)}</td>"
                    f"<td><a href='{safe(issue_url)}' target='_blank' rel='noopener'>discuss</a></td></tr>"
                )
            prior_block = f"""
          <h3 style='margin:14px 0 6px;'>Prior manual labels ({len(prior_for_ext)})</h3>
          <table class='kv-table'>
            <thead><tr><th>Label</th><th>Annotator</th><th>Status</th><th>Evidence (excerpt)</th><th></th></tr></thead>
            <tbody>{''.join(rows_lbl)}</tbody>
          </table>"""

        # Vocabulary <optgroup> options for the inline form.
        vocab_opts = []
        for group, items in LABEL_VOCAB_GROUPS:
            opts = "".join(
                f'<option value="{safe(label)}">{safe(label)} — {safe(desc)}</option>'
                for label, desc in items
            )
            vocab_opts.append(f'<optgroup label="{safe(group)}">{opts}</optgroup>')
        vocab_html = "".join(vocab_opts)

        label_issue_url = _build_label_issue_url(
            ext=ext,
            total_occ=(swh_pop.get(ext, {}).get("total_occ") or 0),
            last_year=(swh_pop.get(ext, {}).get("last_year")),
            current_claimants="; ".join(pl_canonical.get(c["pl_id"], c["pl_id"]) for c in claims[:5]),
            suggested_label=suggested_for_label,
            github_owner_repo=github_owner_repo,
        )

        # Compose label_section from three optional sub-panels:
        #   panel_well       — visible only when fully primary-attributed
        #   panel_polysemous — visible when confirmed-polysemous (multi-PL set)
        #   panel_form       — visible when reviewer input is welcome
        panel_well = panel_polysemous = panel_form = ""

        if attribution_state == "well-attributed":
            primary_names = "; ".join(
                pl_canonical.get(c["pl_id"], c["pl_id"])
                for c in claims if c.get("strength") == "primary"
            )
            disagree_link = (
                f"<a href='{safe(label_issue_url)}' target='_blank' rel='noopener'>"
                f"Disagree or have a correction? Open a labelling issue.</a>"
                if label_issue_url else ""
            )
            panel_well = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Attribution status</h2>
          <p>This extension is <strong>already attributed</strong> as <code>primary</code> by an authoritative upstream source ({n_primary_authoritative} primary claim{'' if n_primary_authoritative == 1 else 's'} from Linguist / Pygments).
          {f"Claimed by: <strong>{safe(primary_names)}</strong>." if primary_names else ""}</p>
          <p class='muted'>{disagree_link}</p>
          {prior_block}
        </section>"""

        if attribution_state == "confirmed-polysemous":
            # All authoritative sources agree on the same set of ≥2 PL entities.
            # Show the set, link to each PL page, mention content-level rules.
            entities_seen: dict[str, str] = {}
            for c in claims:
                if c.get("pl_id"):
                    ent = _canonical_pl_entity(c["pl_id"])
                    entities_seen.setdefault(ent, c["pl_id"])
            shared_links = []
            for ent_base, original_pl_id in entities_seen.items():
                slug = pl_id_to_slug.get(ent_base) or pl_id_to_slug.get(original_pl_id)
                name = pl_canonical.get(ent_base) or pl_canonical.get(original_pl_id) or original_pl_id
                if slug:
                    shared_links.append(f"<a href='{rel}l/{safe(slug)}/index.html'>{safe(name)}</a>")
                else:
                    shared_links.append(safe(name))
            shared_html = ", ".join(shared_links)
            n_heur = len(heur_by_ext.get(ext, []))
            heur_blurb = (
                f"Content-level disambiguation is handled by <strong>{n_heur} Linguist heuristic rule{'s' if n_heur != 1 else ''}</strong> — see the table below."
                if n_heur else
                "No automatic content-level disambiguation rule is defined yet."
            )
            panel_polysemous = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Shared extension</h2>
          <p>This extension legitimately belongs to <strong>{len(distinct_entities)} languages</strong>: {shared_html}.</p>
          <p>Every authoritative source (Linguist <em>and</em> Pygments) agrees on this set, so the ambiguity is genuine — not a data-quality issue. {heur_blurb}</p>
          <p class='muted'>To propose <em>adding</em> a missing PL or <em>disputing</em> one of these, fill the form below. For a multi-PL submission, enter <code>pl/&lt;id&gt;, pl/&lt;id&gt;, …</code> (comma-separated) in the custom field.</p>
        </section>"""

        if attribution_state in ("unattributed", "weakly-attributed", "confirmed-polysemous"):
            if attribution_state == "unattributed":
                heading = "Help label this extension"
                blurb = "No PL in our taxonomy claims this extension. If you know what it's used for, fill the form below."
            elif attribution_state == "weakly-attributed":
                heading = "Confirm or correct this extension"
                blurb = "Existing claims are only <em>secondary</em> or weakly-attested. A confirmation (or correction) would strengthen the catalog."
            else:  # confirmed-polysemous
                heading = "Propose addition or dispute"
                blurb = "All authoritative sources already agree on the set above. Use this form only if you want to add another claimant or contest one of the existing ones."
            # Inline form. JS in app.js handles the submit — builds the GH issue
            # body from the form fields and opens the pre-filled issue page.
            # No YAML editing required from the reviewer.
            suggested_friendly = ""  # could be populated from a future "known formats" table
            # For confirmed-polysemous, pre-fill the custom label field with the
            # confirmed comma-separated list of pl_ids. The reviewer can then
            # add or remove entries directly.
            if attribution_state == "confirmed-polysemous":
                custom_prefill = ", ".join(
                    sorted({_canonical_pl_entity(c["pl_id"]) for c in claims if c.get("pl_id")})
                )
                custom_helper = (
                    "Pre-filled with the current confirmed set. "
                    "Edit (comma-separated) to <strong>add</strong> a missing PL or <strong>remove</strong> one you dispute. "
                    "Multi-PL submissions create one ext_claim row per pl_id."
                )
            else:
                custom_prefill = ""
                custom_helper = (
                    "If label has &lt;...&gt;, fill it here (e.g. for <code>pl/&lt;id&gt;</code> type <code>rust</code>). "
                    "For multi-PL submissions, enter several <code>pl/&lt;id&gt;</code> separated by commas."
                )

            # Proposed PLs to display as one-click chips above the dropdown.
            # Pulls from two sources: existing claimants (typically secondary
            # for `weakly-attributed`) and Linguist heuristic predictions.
            # Each chip carries the BARE pl_id (no `pl/` prefix); ticking it
            # auto-fills `label_custom` and selects the `pl/<id>` option in
            # the dropdown, sparing the reviewer from typing the id.
            def _bare_id(pid: str) -> str:
                # pl_ids in ext_claim.csv look like `pl/bazel`, `pl/cpp`, ...
                # Strip the redundant `pl/` prefix so chip values are bare ids
                # consistent with the existing single-PL convention (customPart
                # = "rust" combined with dropdown "pl/<id>" → label "pl/rust").
                return pid[3:] if pid.startswith("pl/") else pid
            proposed_pls: list[dict] = []
            seen_entities: set[str] = set()
            preset_entities = {
                _bare_id(_canonical_pl_entity(p.strip()))
                for p in custom_prefill.split(",") if p.strip()
            }
            for c in claims:
                pid = c.get("pl_id", "")
                if not pid:
                    continue
                ent = _canonical_pl_entity(pid)
                bare = _bare_id(ent)
                if bare in seen_entities:
                    continue
                seen_entities.add(bare)
                proposed_pls.append({
                    "bare_id": bare,
                    "name": pl_canonical.get(ent) or pl_canonical.get(pid) or pid,
                    "slug": pl_id_to_slug.get(ent) or pl_id_to_slug.get(pid),
                    "via": f"{c.get('source','?')} · {c.get('strength','?')}",
                    "checked": bare in preset_entities,
                })
            for h in heur_by_ext.get(ext, []):
                pid = h.get("predicts_pl_id", "")
                if not pid:
                    continue
                ent = _canonical_pl_entity(pid)
                bare = _bare_id(ent)
                if bare in seen_entities:
                    continue
                seen_entities.add(bare)
                proposed_pls.append({
                    "bare_id": bare,
                    "name": pl_canonical.get(ent) or h.get("predicts_language", "") or pid,
                    "slug": pl_id_to_slug.get(ent) or pl_id_to_slug.get(pid),
                    "via": f"heuristic · {h.get('heuristic_id','')}",
                    "checked": bare in preset_entities,
                })

            quick_pick_html = ""
            if proposed_pls:
                chip_html = []
                for p in proposed_pls:
                    name_html = (
                        f"<a href='{rel}l/{safe(p['slug'])}/index.html' target='_blank' rel='noopener' "
                        f"style='color:inherit;'>{safe(p['name'])}</a>"
                        if p["slug"] else safe(p["name"])
                    )
                    chip_html.append(
                        f"<label class='proposed-pl-chip' "
                        f"style='display:inline-flex; align-items:center; gap:6px; padding:6px 10px; "
                        f"border:1px solid var(--border, #2a2a2a); border-radius:14px; "
                        f"background:rgba(255,255,255,0.02); cursor:pointer; font-size:13px;'>"
                        f"<input type='checkbox' class='proposed-pl' value='{safe(p['bare_id'])}' "
                        f"data-name='{safe(p['name'])}'{' checked' if p['checked'] else ''} "
                        f"style='margin:0;' />"
                        f"<strong>{name_html}</strong> "
                        f"<code style='font-size:11px; color:var(--muted);'>pl/{safe(p['bare_id'])}</code> "
                        f"<span class='muted' style='font-size:11px;'>via {safe(p['via'])}</span>"
                        f"</label>"
                    )
                quick_pick_html = f"""
              <div style="grid-column:1 / -1; display:flex; flex-direction:column; gap:6px;">
                <div class="muted" style="font-size:13px;">
                  <strong>Quick pick — proposed PLs.</strong>
                  Tick one or more to auto-fill the label as <code>pl/&lt;id&gt;</code>.
                  Each chip is a PL that upstream sources or Linguist heuristics already
                  suggest for <code>{safe(ext)}</code>. Multi-tick for a polysemous extension.
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:6px;">
                  {''.join(chip_html)}
                </div>
              </div>"""

            form_html = f"""
          <form class="ext-label-form"
                data-ext="{safe(ext)}"
                data-repo="{safe(github_owner_repo) if github_owner_repo else ''}">
            <div style="display:grid; gap:10px; grid-template-columns: 1fr 1fr; margin-top:10px;">
              {quick_pick_html}
              <label style="grid-column:1 / -1; display:flex; flex-direction:column; gap:4px;">
                <span class="muted">Label *</span>
                <select name="label" required>
                  <option value="">— pick a label from the vocabulary —</option>
                  {vocab_html}
                </select>
              </label>
              <label style="display:flex; flex-direction:column; gap:4px;">
                <span class="muted">{custom_helper}</span>
                <input type="text" name="label_custom" placeholder="e.g. rust  —or—  pl/c, pl/cpp, pl/objective-c" value="{safe(custom_prefill)}" />
              </label>
              <label style="display:flex; flex-direction:column; gap:4px;">
                <span class="muted">Friendly name (optional)</span>
                <input type="text" name="friendly_name" placeholder="e.g. Portable Network Graphics" value="{safe(suggested_friendly)}" />
              </label>
              <label style="grid-column:1 / -1; display:flex; flex-direction:column; gap:4px;">
                <span class="muted">Reference URL (optional, but recommended — spec / Wikipedia / vendor)</span>
                <input type="url" name="reference_url" placeholder="https://www.w3.org/TR/png/" />
              </label>
              <label style="grid-column:1 / -1; display:flex; flex-direction:column; gap:4px;">
                <span class="muted">Evidence / notes *</span>
                <textarea name="evidence" rows="3" required placeholder="Why this label fits — 1-3 sentences. Cite URLs if you have them."></textarea>
              </label>
              <div style="grid-column:1 / -1; display:flex; flex-direction:column; gap:6px;">
                <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                  <button class="btn" type="submit">Submit via GitHub (opens new tab)</button>
                  <span class="muted" style="font-size:12px;">— or, if the button is blocked, use the link just below:</span>
                </div>
                <a class="ext-label-fallback-link btn" href="#" target="_blank" rel="noopener"
                   style="text-decoration:none; align-self:flex-start; font-size:13px;">
                  (fill the form to enable this link)
                </a>
              </div>
              <div class="ext-label-status muted" style="grid-column:1 / -1; font-size:13px;"></div>
            </div>
          </form>
          <details style="margin-top:14px;">
            <summary class="muted" style="cursor:pointer;">What happens after I submit?</summary>
            <ol style="margin-top:8px; color:var(--muted); font-size:13px; line-height:1.55;">
              <li>A new GitHub issue is opened in this repo with your form contents
                  in a structured YAML block and the label <code>ext-review</code>.
                  Your GitHub login becomes the <em>annotator</em>; the issue's
                  <code>created_at</code> is the submission timestamp.</li>
              <li>A curator script (<code>tools/process_extension_labels.py</code>)
                  fetches all <code>ext-review</code> issues and writes their
                  parsed contents into
                  <code>data/derived/extension_labels.csv</code> with
                  <code>curator_status="new"</code>. Until this script runs, your
                  submission lives only as the GitHub issue.</li>
              <li>Your submission shows up on the curator triage page
                  (<a href="../../review/curator/index.html">/review/curator/</a>)
                  under "new". Maintainers review the issue (comment, ask for
                  clarification, accept or reject) and edit
                  <code>extension_labels.csv</code> to set
                  <code>curator_status</code> to <code>accepted</code>.</li>
              <li>For <code>pl/&lt;id&gt;</code> labels, <code>build_pl_taxonomy.py</code>
                  promotes accepted labels into
                  <code>ext_claim.csv</code> with
                  <code>source="manual_review:&lt;your-login&gt;"</code> and
                  <code>strength="proposed"</code>. The next site rebuild then
                  shows your claim on this extension's page and on the
                  language's page.</li>
              <li>Friendly-name + reference-URL labels (e.g.
                  <code>binary:image</code> for <code>.png</code>) are not
                  promoted into <code>ext_claim.csv</code> (they aren't PL
                  claims) but are surfaced on this page's "Prior labels"
                  table so anyone landing here sees them next to the auto-detected
                  category.</li>
            </ol>
            <p class="muted" style="font-size:12px; margin-top:6px;">
              In short: submitting opens an issue (provenance), and a small
              ingestion pipeline turns issues into rows the site renders. The
              loop is currently manual (the curator script must be run by a
              maintainer); GitHub Actions could automate it on each new issue.
            </p>
          </details>"""
            panel_form = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">{safe(heading)}</h2>
          <p class='muted'>{blurb} Vocabulary reference: <a href='https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/extension_labels.md' target='_blank' rel='noopener'>docs/extension_labels.md</a>.</p>
          {form_html if github_owner_repo else "<p class='muted'>GitHub repo not configured; form disabled.</p>"}
          {prior_block}
        </section>"""

        # Final composition: stack panel_well, panel_polysemous, panel_form
        # in that order. Each may be empty depending on attribution_state.
        # `prior_block` is included inside whichever of panel_well or panel_form
        # was rendered (they reference it directly above).
        label_section = panel_well + panel_polysemous + panel_form

        body = f"""
        <div class="breadcrumbs">
          <a href="{rel}index.html">Home</a> · <a href="{rel}ext/index.html">Extensions</a> · <code>{safe(ext)}</code>
        </div>
        <section class="panel section">
          <h1 style="margin:0 0 8px;"><code>{safe(ext)}</code></h1>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <span class='pill'>{n_total} claimant{'' if n_total == 1 else 's'}</span>
            <span class='pill'>{n_primary} primary</span>
            <span class='pill'>{n_secondary} secondary</span>
            {polysemy_pill}
          </div>
        </section>
        {swh_pop_html}
        {claimants_section}
        {external_section}
        {heur_section}
        {swh_section}
        {label_section}
        """
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            layout(title=f"{ext} · PL Catalog", rel=rel, body=body,
                   generated_at=generated_at, github_owner_repo=github_owner_repo),
            encoding="utf-8",
        )
        n_pages += 1

    # /ext/index.html — a listing of all per-extension pages, sorted by SWH popularity.
    def _row_sort_key(ext: str) -> tuple:
        pop = swh_pop.get(ext, {}).get("total_occ", 0) or 0
        return (-pop, ext)

    listing_rows = []
    for ext in sorted(all_exts, key=_row_sort_key):
        url_slug = _ext_url_slug(ext)
        summary = summary_by_ext.get(ext, {})
        n_total = int(summary.get("n_claimants", 0) or 0)
        n_primary = int(summary.get("n_primary", 0) or 0)
        n_sample = len(swh_by_ext.get(ext, []))
        has_heur = len(heur_by_ext.get(ext, []))
        pop = swh_pop.get(ext)
        flags = []
        if n_primary >= 2: flags.append("<span class='pill strength-unknown'>shared primary</span>")
        if has_heur:       flags.append("<span class='pill'>has heuristic</span>")
        if n_sample:       flags.append(f"<span class='pill'>{n_sample} sample{'' if n_sample==1 else 's'}</span>")
        if not n_total and pop and pop["total_occ"] > 0:
            flags.append("<span class='pill src-taxonomy'>unattributed</span>")
        pop_cell = f"{_fmt_occ(pop['total_occ'])}" if pop else "—"
        last_year_cell = str(pop["last_year"]) if pop and pop.get("last_year") else "—"
        listing_rows.append(
            f"<tr><td><a href='./{url_slug}/index.html'><code>{safe(ext)}</code></a></td>"
            f"<td>{pop_cell}</td><td>{last_year_cell}</td>"
            f"<td>{n_total}</td><td>{n_primary}</td>"
            f"<td>{' '.join(flags) or '—'}</td></tr>"
        )
    page = dist_root / "ext" / "index.html"
    rel = rel_prefix(page, dist_root)
    n_with_pop = sum(1 for e in all_exts if e in swh_pop)
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">All extensions ({len(all_exts):,})</h1>
      <p class="muted">Sorted by total occurrence count in the Software Heritage archive (the <strong>SWH-MSR-ARV</strong> dataset — Desmazières, Di Cosmo, Lorentz, <em>MSR 2025</em> — file <code>nb_extensions_alphanum.csv</code>; {n_with_pop:,} of these {len(all_exts):,} have SWH popularity data). Click into any extension for claimants, disambiguation rules, and SWH-mined examples. <a href='https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/citations.md' target='_blank' rel='noopener'>citation</a>.</p>
    </section>
    <section class="panel section">
      <table class='kv-table'>
        <thead><tr><th>Extension</th><th>SWH occurrences</th><th>Last seen</th><th>Claimants</th><th>Primary</th><th>Flags</th></tr></thead>
        <tbody>{''.join(listing_rows)}</tbody>
      </table>
    </section>
    """
    page.write_text(
        layout(title="Extensions index · PL Catalog", rel=rel, body=body,
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )
    return n_pages


def render_extensions_page(*, dist_root: Path, generated_at: str, github_owner_repo: str | None) -> None:
    page = dist_root / "extensions" / "index.html"
    rel = rel_prefix(page, dist_root)
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Extensions</h1>
      <p class="muted" style="margin:0 0 14px;">Browse programming languages grouped by code file extension.</p>
      <p style="margin:0 0 6px;">
        Looking for the cross-source taxonomy view per extension (claimants, Linguist heuristics, SWH samples)?
        <a href="{rel}ext/index.html"><strong>Extensions catalog</strong></a>.
      </p>
    </section>

    <div class="grid" style="margin-top:18px;">
      <section class="panel section">
        <h2>Extensions</h2>
        <div class="search-box" style="margin-bottom: 14px;">
          <input id="extSearch" type="search" placeholder="Filter extensions (e.g., py, bas, lisp)" autocomplete="off" />
        </div>
        <div id="extList" class="muted">Loading extensions…</div>
      </section>

      <section class="panel section">
        <h2>Details</h2>
        <div id="extDetails" class="muted">Select an extension to view associated languages and examples.</div>
      </section>
    </div>
    """
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        layout(title="Extensions · PL Catalog", rel=rel, body=body, generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )


def render_stats_page(
    *,
    dist_root: Path,
    languages: list[Language],
    counts: dict[str, int],
    programs_total: int,
    generated_at: str,
    top_domains: list[tuple[str, int]],
    top_licenses: list[tuple[str, int]],
    top_exts: list[tuple[str, int]],
    langs_added_by_day: list[tuple[str, int]],
    turns_total: int,
    unique_agents: int,
    unique_models: int,
    top_agents: list[tuple[str, int]],
    top_models: list[tuple[str, int]],
    web_search_counts: list[tuple[str, int]],
    temps_count: int,
    temps_min: float | None,
    temps_max: float | None,
    temps_avg: float | None,
    temp_buckets: list[tuple[str, int]],
    github_owner_repo: str | None,
    audit_summary: dict[str, Any] | None,
    audit_page_rel: str,
    taxonomy_stats: dict[str, Any] | None = None,
) -> None:
    page = dist_root / "stats" / "index.html"
    rel = rel_prefix(page, dist_root)

    nested_langs = sorted({l.folder_rel for l in languages if "/" in (l.folder_rel or "")}, key=str.lower)
    nested_count = len(nested_langs)
    top_level_indexed_count = max(0, len(languages) - nested_count)

    top_level_dirs = sorted([p.name for p in LANGUAGES_DIR.iterdir() if p.is_dir()], key=str.lower)
    top_level_dir_count = len(top_level_dirs)
    top_level_dirs_missing_meta = sorted(
        [d for d in top_level_dirs if not (LANGUAGES_DIR / d / "meta.json").exists()],
        key=str.lower,
    )

    orphan_program_manifests: list[tuple[str, int]] = []
    orphan_program_missing_manifests: list[tuple[str, int]] = []
    for d in top_level_dirs_missing_meta:
        programs_dir = LANGUAGES_DIR / d / "programs"
        if not programs_dir.is_dir():
            continue
        with_manifest = 0
        missing_manifest = 0
        for prog_dir in [p for p in programs_dir.iterdir() if p.is_dir()]:
            if (prog_dir / "manifest.json").exists():
                with_manifest += 1
            else:
                missing_manifest += 1
        if with_manifest:
            orphan_program_manifests.append((d, with_manifest))
        if missing_manifest:
            orphan_program_missing_manifests.append((d, missing_manifest))

    pl_list_path = ROOT / "data" / "pl_list.txt"
    pl_list_count: int | None = None
    pl_list_missing_meta: list[str] = []
    meta_missing_pl_list: list[str] = []
    if pl_list_path.exists():
        pl_names = [ln.strip() for ln in pl_list_path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
        pl_list_count = len(pl_names)
        pl_set = set(pl_names)
        meta_set = set(l.name for l in languages)
        pl_list_missing_meta = sorted(pl_set - meta_set, key=str.lower)
        meta_missing_pl_list = sorted(meta_set - pl_set, key=str.lower)

    catalog_path = ROOT / "data" / "catalog.csv"
    catalog_rows: int | None = None
    catalog_unique_languages: int | None = None
    if catalog_path.exists():
        try:
            import csv

            langs_in_catalog = set()
            rows = 0
            with catalog_path.open(newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows += 1
                    lang = (row.get("language") or "").strip()
                    if lang:
                        langs_in_catalog.add(lang)
            catalog_rows = rows
            catalog_unique_languages = len(langs_in_catalog)
        except Exception:
            catalog_rows = None
            catalog_unique_languages = None

    max_letter = max(counts.values()) if counts else 1
    letter_rows = "\n".join(
        f'<li class="bar-row"><div class="muted">{letter}</div><div class="bar" style="--w:{(counts[letter]/max_letter)*100:.1f}%"><div></div></div><div class="muted" style="text-align:right;">{counts[letter]}</div></li>'
        for letter in sorted(counts.keys())
        if counts[letter] > 0
    )

    def bar_rows(items: list[tuple[str, int]]) -> str:
        maxv = max((c for _, c in items), default=1)
        return "\n".join(
            f'<li class="bar-row"><div class="muted">{safe(label)}</div><div class="bar" style="--w:{(count/maxv)*100:.1f}%"><div></div></div><div class="muted" style="text-align:right;">{count}</div></li>'
            for label, count in items
        )

    last_30_days = langs_added_by_day[-30:] if len(langs_added_by_day) > 30 else langs_added_by_day

    if turns_total > 0:
        if temps_count > 0 and temps_min is not None and temps_max is not None and temps_avg is not None:
            temp_summary = f"{temps_count} commits include Temperature · avg {temps_avg:.2f} (min {temps_min:.2f}, max {temps_max:.2f})"
            temp_bucket_html = f"<ul class='bar-list'>{bar_rows(temp_buckets)}</ul>" if temp_buckets else "<div class='muted'>No temperature buckets.</div>"
        else:
            temp_summary = "No Temperature trailers found."
            temp_bucket_html = "<div class='muted'>—</div>"

        llm_section = f"""
        <section class="panel section" style="margin-top: 18px;">
          <h2>Agents &amp; LLMs</h2>
          <p class="muted" style="margin:0 0 14px;">Derived from git commit trailers in <code>turn: add …</code> commits.</p>
          <div class="stats">
            <div class="stat"><div class="num">{turns_total}</div><div class="muted">turn commits</div></div>
            <div class="stat"><div class="num">{unique_agents}</div><div class="muted">agents</div></div>
            <div class="stat"><div class="num">{unique_models}</div><div class="muted">models</div></div>
          </div>
        </section>

        <div class="grid" style="margin-top: 18px;">
          <section class="panel section">
            <h2>Top agents</h2>
            <ul class="bar-list">{bar_rows(top_agents)}</ul>
          </section>
          <section class="panel section">
            <h2>Top models</h2>
            <ul class="bar-list">{bar_rows(top_models)}</ul>
          </section>
        </div>

        <div class="grid" style="margin-top: 18px;">
          <section class="panel section">
            <h2>WebSearch usage</h2>
            <ul class="bar-list">{bar_rows(web_search_counts)}</ul>
          </section>
          <section class="panel section">
            <h2>Temperature (where recorded)</h2>
            <p class="muted" style="margin:0 0 10px;">{safe(temp_summary)}</p>
            {temp_bucket_html}
          </section>
        </div>
        """
    else:
        llm_section = """
        <section class="panel section" style="margin-top: 18px;">
          <h2>Agents &amp; LLMs</h2>
          <p class="muted" style="margin:0;">Git history not available; cannot compute agent/model statistics.</p>
        </section>
        """

    audit_available = audit_summary is not None
    if audit_available:
        sev = audit_summary.get("by_severity", {})
        total_findings = int(audit_summary.get("total", 0))
        audit_section = f"""
        <section class="panel section" style="margin-top: 18px;">
          <h2>Data quality audit</h2>
          <div class="stats">
            <div class="stat"><div class="num">{total_findings}</div><div class="muted">findings</div></div>
            <div class="stat"><div class="num">{int(sev.get("error", 0))}</div><div class="muted">errors</div></div>
            <div class="stat"><div class="num">{int(sev.get("warn", 0))}</div><div class="muted">warnings</div></div>
          </div>
          <div style="margin-top: 12px; display:flex; gap:10px; flex-wrap:wrap;">
            <a class="btn" href="{rel}data/audit.json">Open audit.json</a>
            <a class="btn" href="{audit_page_rel}">Open audit view</a>
          </div>
        </section>
        """
    else:
        audit_section = f"""
        <section class="panel section" style="margin-top: 18px;">
          <h2>Data quality audit</h2>
          <p class="muted" style="margin:0 0 10px;">
            Run <code>python3 tools/audit_repo.py --out web/dist/data/audit.json</code> to generate a machine-readable report
            (duplicates, integrity checks, clustering hints).
          </p>
          <div class="muted">audit.json not generated in this build.</div>
          <div style="margin-top: 12px;">
            <a class="btn" href="{audit_page_rel}">Open audit view</a>
          </div>
        </section>
        """

    # --- Phase 2d: taxonomy / SWH evidence summary section ---
    taxonomy_stats_html = ""
    if taxonomy_stats:
        t = taxonomy_stats
        pct = lambda n, d: f"{100*n/d:.1f}%" if d else "—"
        per_source_rows = "".join(
            f"<tr><td><span class='pill src-{s}'>{safe(s.capitalize())}</span></td>"
            f"<td>{n}</td><td>{pct(n, t['n_enriched'])}</td></tr>"
            for s, n in sorted(t["per_source"].items(), key=lambda kv: -kv[1])
        )
        src_dist_rows = "".join(
            f"<tr><td>{k} source{'' if k == 1 else 's'}</td><td>{v}</td>"
            f"<td>{pct(v, t['n_enriched'])}</td></tr>"
            for k, v in t["source_count_distribution"].items()
        )
        claim_rows = "".join(
            f"<tr><td>{safe(src)}</td>"
            f"<td><span class='pill strength-{strength}'>{safe(strength)}</span></td>"
            f"<td>{n}</td></tr>"
            for (src, strength), n in sorted(t["claim_breakdown"].items(), key=lambda kv: -kv[1])
        )
        polysemy_rows = "".join(
            f"<tr><td>{k} primary claimant{'' if k == 1 else 's'}</td><td>{v}</td></tr>"
            for k, v in t["polysemy_dist"].items()
        )
        taxonomy_stats_html = f"""
    <section class="panel section" style="margin-top:18px;">
      <h1 style="margin:0 0 8px;">Taxonomy &amp; SWH evidence</h1>
      <p class='muted'>Coverage of the PL taxonomy ({len(_TAXONOMY_SOURCES)} upstream sources) and how much of the catalog has real archived programs.</p>
      <div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(190px, 1fr)); gap:10px;'>
        <div class="stat"><div class="num">{t['n_total_pl_pages']:,}</div><div class="muted">PL pages total</div></div>
        <div class="stat"><div class="num">{t['n_in_repo']:,}</div><div class="muted">In-repo (LLM-curated)</div></div>
        <div class="stat"><div class="num">{t['n_taxonomy_only']:,}</div><div class="muted">Taxonomy-only (no LLM)</div></div>
        <div class="stat"><div class="num">{t['n_enriched']:,}</div><div class="muted">With cross-source data</div></div>
        <div class="stat" title="Progress indicator: grows as manual labelling promotes new (pl, ext) edges into ext_claim.csv"><div class="num">{t['n_pls_with_ext']:,} <span style="font-size:60%; color:var(--muted);">({t['pct_pls_with_ext']:.1f}%)</span></div><div class="muted">PLs with ≥1 ext claim<br/>(of {t['n_pls_in_taxonomy']:,} in taxonomy)</div></div>
        <div class="stat"><div class="num">{t['n_with_swh_evidence']:,}</div><div class="muted">With ≥1 SWH sample</div></div>
        <div class="stat"><div class="num">{t['total_swh_samples']:,}</div><div class="muted">SWH samples total</div></div>
        <div class="stat"><div class="num">{t['n_ext_total']:,}</div><div class="muted">Extensions in taxonomy</div></div>
        <div class="stat"><div class="num">{t['n_exts_with_heuristic']:,}</div><div class="muted">Exts with disambiguation rule</div></div>
      </div>
    </section>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Per-source contribution</h2>
        <p class='muted'>How many PL entities each upstream source asserts the existence of.</p>
        <table class='kv-table'>
          <thead><tr><th>Source</th><th>PLs</th><th>% of enriched</th></tr></thead>
          <tbody>{per_source_rows}</tbody>
        </table>
      </section>
      <section class="panel section">
        <h2>Source consensus distribution</h2>
        <p class='muted'>How many sources mention each PL (1 = single-source, 7 = mentioned everywhere).</p>
        <table class='kv-table'>
          <thead><tr><th>Number of sources</th><th>PL count</th><th>%</th></tr></thead>
          <tbody>{src_dist_rows}</tbody>
        </table>
      </section>
    </div>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Extension claims by (source, strength)</h2>
        <p class='muted'>Linguist tracks primary vs secondary; PLDB does not.</p>
        <table class='kv-table'>
          <thead><tr><th>Source</th><th>Strength</th><th>Claims</th></tr></thead>
          <tbody>{claim_rows}</tbody>
        </table>
      </section>
      <section class="panel section">
        <h2>Polysemy (per extension)</h2>
        <p class='muted'>How many languages claim each ext as primary. ≥2 means the ext is ambiguous without content heuristics.</p>
        <table class='kv-table'>
          <thead><tr><th>Bucket</th><th>Ext count</th></tr></thead>
          <tbody>{polysemy_rows}</tbody>
        </table>
      </section>
    </div>
        """

    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Statistics</h1>
      <p class="muted" style="margin:0 0 14px;">Quick aggregates computed from `languages/**/meta.json` and program manifests.</p>

      <div class="stats">
        <div class="stat"><div class="num">{len(languages)}</div><div class="muted">indexed languages</div></div>
        <div class="stat"><div class="num">{programs_total}</div><div class="muted">programs</div></div>
        <div class="stat"><div class="num">{(programs_total / max(1, len(languages))):.2f}</div><div class="muted">avg programs / language</div></div>
      </div>
    </section>

    <section class="panel section" style="margin-top: 18px;">
      <h2>Counts &amp; sources</h2>
      <p class="muted" style="margin:0 0 12px;">The website indexes languages by scanning <code>languages/**/meta.json</code>. Other files count different things.</p>
      <table class="audit-table">
        <thead>
          <tr><th>Artifact</th><th>Count</th><th>Meaning</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>languages/**/meta.json</code></td>
            <td>{len(languages)}</td>
            <td>Indexed languages (this website’s primary source of truth)</td>
          </tr>
          <tr>
            <td>Top-level <code>languages/</code> dirs</td>
            <td>{top_level_dir_count}</td>
            <td>Folder names at depth 1 (may include “group” folders)</td>
          </tr>
          <tr>
            <td>Nested language folders</td>
            <td>{nested_count}</td>
            <td>Languages stored below depth 1 (e.g., <code>languages/PL/0</code>)</td>
          </tr>
          <tr>
            <td>Top-level dirs missing <code>meta.json</code></td>
            <td>{len(top_level_dirs_missing_meta)}</td>
            <td>Not indexed at depth 1 (may be incomplete metadata, or group folders)</td>
          </tr>
          <tr>
            <td><code>data/pl_list.txt</code></td>
            <td>{safe(str(pl_list_count) if pl_list_count is not None else "—")}</td>
            <td>Upstream name list (not necessarily ingested into <code>languages/</code>)</td>
          </tr>
          <tr>
            <td><code>data/catalog.csv</code></td>
            <td>{safe(str(catalog_rows) if catalog_rows is not None else "—")}</td>
            <td>Program rows (not a language count)</td>
          </tr>
        </tbody>
      </table>

      <details style="margin-top: 12px;">
        <summary>Show details</summary>
        <div class="muted" style="margin-top: 10px; display:grid; gap:8px;">
          <div><strong>Top-level indexed languages:</strong> {top_level_indexed_count}</div>
          <div><strong>Nested indexed languages:</strong> {nested_count}{f" · {', '.join(f'<code>{safe(x)}</code>' for x in nested_langs)}" if nested_langs else ""}</div>
          <div><strong>Top-level dirs missing <code>meta.json</code>:</strong> {len(top_level_dirs_missing_meta)}{f" · {', '.join(f'<code>{safe(x)}</code>' for x in top_level_dirs_missing_meta)}" if top_level_dirs_missing_meta else ""}</div>
          <div><strong>Dirs with program manifests but no <code>meta.json</code>:</strong> {', '.join(f'<code>{safe(n)}</code> ({c})' for n, c in orphan_program_manifests) if orphan_program_manifests else "—"}</div>
          <div><strong>Dirs with program folders missing <code>manifest.json</code>:</strong> {', '.join(f'<code>{safe(n)}</code> ({c})' for n, c in orphan_program_missing_manifests) if orphan_program_missing_manifests else "—"}</div>
          <div><strong>Names in <code>pl_list.txt</code> but not indexed:</strong> {len(pl_list_missing_meta) if pl_list_count is not None else "—"}{f" · {', '.join(f'<code>{safe(x)}</code>' for x in pl_list_missing_meta)}" if pl_list_missing_meta else ""}</div>
          <div><strong>Names indexed but not in <code>pl_list.txt</code>:</strong> {len(meta_missing_pl_list) if pl_list_count is not None else "—"}{f" · {', '.join(f'<code>{safe(x)}</code>' for x in meta_missing_pl_list)}" if meta_missing_pl_list else ""}</div>
          <div><strong>Unique languages in <code>catalog.csv</code>:</strong> {safe(str(catalog_unique_languages) if catalog_unique_languages is not None else "—")}</div>
        </div>
      </details>
    </section>

    {llm_section}
    {audit_section}

    <section class="panel section">
      <h2>Languages by first letter</h2>
      <ul class="bar-list">{letter_rows}</ul>
    </section>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Top origin domains</h2>
        <ul class="bar-list">{bar_rows(top_domains)}</ul>
      </section>
      <section class="panel section">
        <h2>Top license guesses</h2>
        <ul class="bar-list">{bar_rows(top_licenses)}</ul>
      </section>
    </div>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Top code file extensions</h2>
        <ul class="bar-list">{bar_rows([(f'.{e}' if e and e != 'unknown' else e, c) for e, c in top_exts])}</ul>
      </section>
      <section class="panel section">
        <h2>Languages added (last 30 days)</h2>
        <ul class="bar-list">{bar_rows(last_30_days)}</ul>
      </section>
    </div>
    {taxonomy_stats_html if taxonomy_stats else ''}
    """

    page.write_text(
        layout(title="Stats · PL Catalog", rel=rel, body=body, generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )


def render_language_pages(
    *,
    dist_root: Path,
    languages: list[Language],
    generated_at: str,
    slug_to_prev_next: dict[str, tuple[Language | None, Language | None]],
    github_owner_repo: str | None,
    related_by_language: dict[str, list[dict[str, Any]]],
    audit_summary: dict[str, Any] | None,
    enrichments: dict[str, TaxonomyEnrichment] | None = None,
) -> None:
    enrichments = enrichments or {}
    lang_by_name = {l.name: l for l in languages}
    for lang in languages:
        page = dist_root / "l" / lang.slug / "index.html"
        rel = rel_prefix(page, dist_root)

        alias_html = (
            f"<div class='muted'>Aliases: {safe(', '.join(lang.aliases))}</div>" if lang.aliases else "<div class='muted'>Aliases: —</div>"
        )
        prov_pills: list[str] = []
        if lang.agent:
            prov_pills.append(f"<span class='pill'>Agent: {safe(lang.agent)}</span>")
        if lang.model:
            prov_pills.append(f"<span class='pill'>Model: {safe(lang.model)}</span>")
        if lang.temperature is not None:
            prov_pills.append(f"<span class='pill'>Temp: {lang.temperature:g}</span>")
        if lang.web_search:
            prov_pills.append(f"<span class='pill'>WebSearch: {safe(lang.web_search)}</span>")

        prov_bits: list[str] = []
        if lang.turn_commit:
            if github_owner_repo:
                url = github_commit_url(owner_repo=github_owner_repo, commit=lang.turn_commit)
                prov_bits.append(f"commit <a href='{safe(url)}' target='_blank' rel='noopener'>{safe(lang.turn_commit[:10])}</a>")
            else:
                prov_bits.append(f"commit {safe(lang.turn_commit[:10])}")
        if lang.turn_authored_at:
            prov_bits.append(f"authored {safe(lang.turn_authored_at)}")
        if lang.agent:
            prov_bits.append(f"agent {safe(lang.agent)}")
        if lang.model:
            prov_bits.append(f"model {safe(lang.model)}")
        prov_line = f"<div class='muted'>Provenance: {' · '.join(prov_bits)}</div>" if prov_bits else ""

        audit_pill = ""
        audit_line = ""
        if audit_summary:
            per_lang = audit_summary.get("by_language", {}).get(lang.name)
            if per_lang:
                total = int(per_lang.get("total", 0))
                err = int(per_lang.get("error", 0))
                warn = int(per_lang.get("warn", 0))
                if total > 0:
                    audit_pill = f"<span class='pill'>Audit: {total} (err {err}, warn {warn})</span>"
                    audit_line = "<div class='muted'>Audit findings present for this language. See audit.json for details.</div>"

        related_items = related_by_language.get(lang.name, [])
        related_html = ""
        if related_items:
            related_links = []
            for item in related_items:
                other_name = item["name"]
                other = lang_by_name.get(other_name)
                if other:
                    related_links.append(
                        f"<span class='pill'><a href='{rel}l/{other.slug}/index.html'>{safe(other.name)}</a> <span class='muted'>({item['score']:.2f})</span></span>"
                    )
            if related_links:
                related_html = f"""
                <section class="panel section" style="margin-top: 18px;">
                  <h2>Related languages</h2>
                  <div style="display:flex; flex-wrap:wrap; gap:10px;">{''.join(related_links)}</div>
                </section>
                """

        lang_page_path = f"l/{lang.slug}/index.html"
        report_lang_url = ""
        issues_lang_url = ""
        if github_owner_repo:
            title = f"Data issue: {lang.name}"
            body_lines = [
                "Category: data-quality",
                "",
                f"Language: {lang.name}",
                f"Language folder: languages/{lang.folder_rel}",
                f"Language page: {lang_page_path}",
                f"Evidence URL: {lang.evidence_url}",
            ]
            if lang.turn_commit:
                body_lines.append(f"Turn commit: {lang.turn_commit}")
            if lang.turn_authored_at:
                body_lines.append(f"Turn authored_at: {lang.turn_authored_at}")
            body_lines += [
                "",
                "Describe the issue:",
                "- …",
            ]
            report_lang_url = github_new_issue_url(owner_repo=github_owner_repo, title=title, body="\n".join(body_lines))
            issues_lang_url = github_issue_search_url(owner_repo=github_owner_repo, query=f'is:issue \"{lang.name}\"')

        programs_html = []
        if not lang.programs:
            programs_html.append("<p class='muted'>No programs recorded for this language yet.</p>")
        else:
            for idx, prog in enumerate(lang.programs):
                code_id = f"code-{idx}"
                manifest_link = f"{rel}code/{prog.sha256}/manifest.json"
                download_link = f"{rel}code/{prog.sha256}/{safe(prog.code_out_name or 'code.txt')}" if prog.code_out_name else ""

                links = [f"<a href='{safe(prog.origin_url)}' target='_blank' rel='noopener'>Origin</a>"]
                if prog.code_out_name:
                    links.append(f"<a href='{download_link}' download>Download</a>")
                links.append(f"<a href='{manifest_link}'>manifest.json</a>")
                if github_owner_repo:
                    title = f"Program issue: {lang.name} — {prog.title}"
                    body_lines = [
                        "Category: data-quality",
                        "",
                        f"Language: {lang.name}",
                        f"Language folder: languages/{lang.folder_rel}",
                        f"Language page: {lang_page_path}",
                        f"Evidence URL: {lang.evidence_url}",
                        "",
                        f"Program title: {prog.title}",
                        f"Program sha256: {prog.sha256}",
                        f"Program folder: languages/{lang.folder_rel}/programs/{prog.sha256}",
                        f"Origin URL: {prog.origin_url}",
                    ]
                    if lang.turn_commit:
                        body_lines.append(f"Turn commit: {lang.turn_commit}")
                    if lang.turn_authored_at:
                        body_lines.append(f"Turn authored_at: {lang.turn_authored_at}")
                    body_lines += [
                        "",
                        "Describe the issue:",
                        "- …",
                    ]
                    report_prog_url = github_new_issue_url(owner_repo=github_owner_repo, title=title, body="\n".join(body_lines))
                    links.append(f"<a href='{safe(report_prog_url)}' target='_blank' rel='noopener'>Report</a>")
                links_html = " · ".join(links)

                prog_prov_bits: list[str] = []
                if lang.turn_commit:
                    if github_owner_repo:
                        url = github_commit_url(owner_repo=github_owner_repo, commit=lang.turn_commit)
                        prog_prov_bits.append(f"commit <a href='{safe(url)}' target='_blank' rel='noopener'>{safe(lang.turn_commit[:10])}</a>")
                    else:
                        prog_prov_bits.append(f"commit {safe(lang.turn_commit[:10])}")
                if lang.turn_authored_at:
                    prog_prov_bits.append(f"authored {safe(lang.turn_authored_at)}")
                if lang.agent:
                    prog_prov_bits.append(f"agent {safe(lang.agent)}")
                if lang.model:
                    prog_prov_bits.append(f"model {safe(lang.model)}")
                prog_prov_line = f"<div class='muted'>Provenance: {' · '.join(prog_prov_bits)}</div>" if prog_prov_bits else ""

                meta_bits = []
                if prog.license_guess:
                    meta_bits.append(f"license: {safe(prog.license_guess)}")
                meta_bits.append(f"added: {safe(prog.added_at)}")
                meta_str = " · ".join(meta_bits)

                code_block = ""
                if prog.code_text is not None:
                    code_block = f"""
                    <div class="codeblock" style="margin-top: 10px;">
                      <div class="codebar">
                        <div class="meta">{safe(prog.code_out_name or '')} · {meta_str}</div>
                        <button class="btn copy-btn" type="button" data-copy-target="#{code_id}">Copy</button>
                      </div>
                      <pre><code id="{code_id}">{safe(prog.code_text)}</code></pre>
                    </div>
                    """
                else:
                    code_block = "<p class='muted'>Code file missing.</p>"

                programs_html.append(
                    f"""
                    <section class="panel section" style="margin-top: 18px;">
                      <h2 style="margin:0 0 8px;">{safe(prog.title)}</h2>
                      <div class="muted">{links_html}</div>
                      {prog_prov_line}
                      {code_block}
                    </section>
                    """
                )

        # ----- Phase 1: cross-source presence / ext claims / SWH samples / heuristics -----
        enr = enrichments.get(lang.name)
        cross_source_html = ""
        ext_claims_html = ""
        swh_samples_html = ""
        heuristics_html = ""

        # 1a. Cross-source presence pills. Always emit a "Sources mentioning"
        # section when the PL has *any* attestation (LLM + taxonomy sources),
        # even if name-matching to the taxonomy failed.
        pills = []
        if lang.programs:
            pills.append(
                f"<a class='pill src-llm' href='{rel}source/llm/index.html' "
                f"title='Curated by an LLM in this repo'>LLM (this repo) · {len(lang.programs)}</a>"
            )
        taxonomy_pill_count = 0
        if enr is not None:
            # For "wikipedia" specifically: prefer the per-PL Wikipedia URL
            # from pl.csv:wikipedia_url (populated by build_pl_taxonomy.py's
            # Wikidata sitelink overlay) over the roster page. Fall back to
            # the legacy wikipedia_lang_titles.json title list for PLs that
            # don't have a Wikidata match but ARE in the 177-entry roster.
            # Final fallback is the roster page when we have nothing better.
            wikipedia_url = enr.wikipedia_url or ""
            if not wikipedia_url and enr.in_sources.get("wikipedia"):
                wikipedia_url = _legacy_wikipedia_url_for(enr.canonical_name)
            wikipedia_present = enr.in_sources.get("wikipedia") or bool(wikipedia_url)
            for src in _TAXONOMY_SOURCES:
                if src == "wikipedia":
                    if not wikipedia_present:
                        continue
                    if wikipedia_url:
                        pills.append(
                            f"<a class='pill src-wikipedia' href='{safe(wikipedia_url)}' "
                            f"target='_blank' rel='noopener' title='Wikipedia article'>"
                            f"Wikipedia</a>"
                        )
                    else:
                        pills.append(
                            f"<a class='pill src-wikipedia' href='{rel}source/wikipedia/index.html'>"
                            f"Wikipedia</a>"
                        )
                    taxonomy_pill_count += 1
                    continue
                if enr.in_sources.get(src):
                    pills.append(
                        f"<a class='pill src-{src}' href='{rel}source/{src}/index.html'>"
                        f"{safe(src.capitalize())}</a>"
                    )
                    taxonomy_pill_count += 1
            # Wikidata pill: stable cross-system identifier for the PL,
            # populated by Phase B of the taxonomy overlay. Render alongside
            # the per-PL Wikipedia article link; the two complement each
            # other (Wikipedia = prose, Wikidata = structured data + QID).
            # Not part of _TAXONOMY_SOURCES (no /source/wikidata/ roster
            # page — this is a pure external link).
            if enr.wikidata_qid:
                wikidata_url = f"https://www.wikidata.org/wiki/{enr.wikidata_qid}"
                pills.append(
                    f"<a class='pill src-wikidata' href='{safe(wikidata_url)}' "
                    f"target='_blank' rel='noopener' "
                    f"title='Wikidata item — structured cross-system identifier'>"
                    f"Wikidata · {safe(enr.wikidata_qid)}</a>"
                )
                taxonomy_pill_count += 1
        n_present = taxonomy_pill_count + (1 if lang.programs else 0)
        pl_id_line = (
            f"<div class='muted' style='margin-bottom:8px;'>{n_present} source{'s' if n_present != 1 else ''} · pl_id: <code>{safe(enr.pl_id)}</code></div>"
            if enr is not None else
            f"<div class='muted' style='margin-bottom:8px;'>{n_present} source{'s' if n_present != 1 else ''} · "
            f"not in taxonomy (canonical name didn't match any upstream)</div>"
        )
        # Provenance for PLs added via the /contribute/add-pl/ web form:
        # show "Submitted via #N" with a link to the originating GitHub issue.
        # This is what makes /l/<pl>/ pages traceable back to crowdsource
        # submissions, separately from the LLM /loop turn provenance.
        provenance_line = ""
        if enr is not None and enr.created_via_issue and github_owner_repo:
            issue_url = f"https://github.com/{github_owner_repo}/issues/{enr.created_via_issue}"
            provenance_line = (
                f"<div class='muted' style='margin-bottom:8px;'>"
                f"Submitted via <a href='{safe(issue_url)}' target='_blank' rel='noopener'>"
                f"#{safe(enr.created_via_issue)}</a> "
                f"on the <a href='{rel}contribute/add-pl/index.html'>Add-a-PL form</a>."
                f"</div>"
            )
        if pills:
            cross_source_html = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Sources mentioning this language</h2>
          {pl_id_line}
          {provenance_line}
          <div style='display:flex; flex-wrap:wrap; gap:8px;'>{''.join(pills)}</div>
        </section>
        """

        if enr is not None:

            # 1b. Extension claims with (source, strength).
            if enr.extension_claims:
                rows_html = []
                # Look up popularity to surface usage in SWH next to each claim.
                _swh_pop = load_swh_ext_popularity()
                for ext, src, strength, evidence in enr.extension_claims:
                    badge_cls = f"strength-{strength}"
                    ext_link = f"{rel}ext/{_ext_url_slug(ext)}/index.html"
                    pop = _swh_pop.get(ext)
                    pop_cell = (
                        f"<td title='Total file occurrences with this ext in the SWH archive'><span class='muted'>{_fmt_occ(pop['total_occ'])} files</span></td>"
                        if pop else "<td class='muted'>—</td>"
                    )
                    # If evidence is a URL, hyperlink the source label so a
                    # reader can click straight to it — useful for sources
                    # like `manual_add:#16` (→ GitHub issue) and `linguist`
                    # (→ languages.yml).
                    if evidence.startswith("http://") or evidence.startswith("https://"):
                        src_cell = (
                            f"<a href='{safe(evidence)}' target='_blank' rel='noopener' "
                            f"title='{safe(evidence)}'>{safe(src)}</a>"
                        )
                    else:
                        src_cell = (
                            f"<span title='{safe(evidence)}'>{safe(src)}</span>"
                        )
                    rows_html.append(
                        f"<tr><td><a href='{ext_link}'><code>{safe(ext)}</code></a></td>"
                        f"<td>{src_cell}</td>"
                        f"<td><span class='pill {badge_cls}'>{safe(strength)}</span></td>"
                        f"{pop_cell}</tr>"
                    )
                ext_claims_html = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Extensions claimed by this language</h2>
          <div class='muted' style='margin-bottom:8px;'>{len(enr.extension_claims)} claim{'s' if len(enr.extension_claims) != 1 else ''}. Each row is one upstream assertion with its strength. <code>SWH</code> column shows file occurrences with that extension across the entire archive.</div>
          <table class='kv-table'>
            <thead><tr><th>Extension</th><th>Source</th><th>Strength</th><th>SWH</th></tr></thead>
            <tbody>{''.join(rows_html)}</tbody>
          </table>
        </section>
        """

            # 1c. SWH-mined samples: real archived programs in this language.
            if enr.swh_samples:
                items = []
                for s in enr.swh_samples:
                    code_block = ""
                    if s.code_text is not None:
                        code_block = (
                            "<details style='margin-top:8px;'>"
                            "<summary class='muted'>Show source</summary>"
                            f"<pre style='overflow:auto;'><code>{safe(s.code_text)}</code></pre>"
                            "</details>"
                        )
                    via_pill = f"<span class='pill'>via {safe(s.predicted_via)}</span>" if s.predicted_via else ""
                    h_pill = ""
                    if s.predicted_heuristic_id:
                        ext_link = f"{rel}ext/{_ext_url_slug(s.ext)}/index.html"
                        h_pill = (
                            f"<a class='pill' href='{ext_link}' "
                            f"title='See the disambiguation rule on the per-extension page'>"
                            f"rule {safe(s.predicted_heuristic_id)}</a>"
                        )
                    gh_link = f"<a href='{safe(s.github_raw_url)}' target='_blank' rel='noopener'>GitHub raw</a>" if s.github_raw_url else ""
                    # Use the BARE content SWHID for the "Open in SWH" link.
                    # The qualified form with `;origin=...` 404s when SWH hasn't
                    # indexed that origin (real case: we attributed an origin
                    # via the GitHub side-channel that SWH hadn't crawled yet).
                    # The bare SWHID is content-addressable and resolves
                    # whenever the file is in the archive. The qualified
                    # string remains visible above as the citation.
                    bare_browser_url = f"https://archive.softwareheritage.org/swh:1:cnt:{s.sha1_git}/"
                    items.append(f"""
              <article class="panel" style="margin-bottom:10px; padding:12px;">
                <header style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; align-items:baseline;">
                  <div><strong>{safe(s.filename)}</strong> <span class='muted'>· {s.length} B · ext <code>{safe(s.ext)}</code> · seen {s.occurrences_in_swh}× in SWH</span></div>
                  <div style='display:flex; flex-wrap:wrap; gap:6px;'>{via_pill}{h_pill}</div>
                </header>
                <div class='muted' style='font-family:monospace; word-break:break-all; margin-top:4px;'>{safe(s.qualified_swhid)}</div>
                <div style='margin-top:6px;'>
                  <a href='{safe(bare_browser_url)}' target='_blank' rel='noopener'>Open in SWH</a> ·
                  <a href='{safe(s.swh_raw_url)}' target='_blank' rel='noopener'>Raw bytes (SWH)</a>
                  {' · ' + gh_link if gh_link else ''}
                </div>
                {code_block}
              </article>""")
                swh_samples_html = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Real programs from Software Heritage</h2>
          <div class='muted' style='margin-bottom:10px;'>{len(enr.swh_samples)} sample{'s' if len(enr.swh_samples) != 1 else ''} mined from <code>derived_datasets/&lt;date&gt;/contents/*.parquet</code>, byte-verified against the SWH archive. Citation-grade qualified SWHIDs preserved.</div>
          {''.join(items)}
        </section>
        """
            else:
                swh_samples_html = """
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Real programs from Software Heritage</h2>
          <p class='muted'>No SWH evidence indexed yet for this language. (Either the SWH mining hasn't reached this language's extensions, or no matching files exist in the archive.)</p>
        </section>
        """

            # 1d. Heuristics applicable to this PL (Linguist disambiguation rules).
            if enr.heuristics_for_my_exts:
                rows = []
                for h in enr.heuristics_for_my_exts:
                    h_ext = h.get('applies_to_ext','')
                    ext_link = f"{rel}ext/{_ext_url_slug(h_ext)}/index.html"
                    rows.append(
                        f"<tr><td><code>{safe(h.get('heuristic_id',''))}</code></td>"
                        f"<td><a href='{ext_link}'><code>{safe(h_ext)}</code></a></td>"
                        f"<td>{safe(h.get('pattern_kind',''))}</td>"
                        f"<td><code style='white-space:pre-wrap; word-break:break-all;'>{safe((h.get('predicates_json','') or '')[:200])}</code></td></tr>"
                    )
                heuristics_html = f"""
        <section class="panel section">
          <h2 style="margin:0 0 8px;">Disambiguation rules</h2>
          <div class='muted' style='margin-bottom:8px;'>Linguist heuristic rules that predict this language when one of its claimed extensions is shared with another.</div>
          <table class='kv-table'>
            <thead><tr><th>Rule</th><th>Ext</th><th>Kind</th><th>Predicates (truncated)</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </section>
        """

        prev_lang, next_lang = slug_to_prev_next.get(lang.slug, (None, None))
        prev_href = f"{rel}l/{prev_lang.slug}/index.html" if prev_lang else f"{rel}index.html"
        prev_label = f"← {safe(prev_lang.name)}" if prev_lang else "← Home"
        next_href = f"{rel}l/{next_lang.slug}/index.html" if next_lang else f"{rel}browse/index.html"
        next_label = f"{safe(next_lang.name)} →" if next_lang else "Browse →"
        pager = f"""
        <div class="pager">
          <a href="{prev_href}" aria-label="Previous language">{prev_label}</a>
          <a href="{next_href}" aria-label="Next language">{next_label}</a>
        </div>
        """

        # A taxonomy-only PL is identified by the sentinel `added_at == ""` set
        # in synthesize_taxonomy_only_languages. Surface that to the reader.
        is_taxonomy_only = (not lang.added_at) and (not lang.programs)
        taxonomy_only_pill = (
            "<span class='pill src-taxonomy'>Taxonomy-only · no LLM program</span>"
            if is_taxonomy_only else ""
        )
        added_at_pill = (
            f"<span class='pill'>Added {safe(lang.added_at)}</span>"
            if lang.added_at else ""
        )
        evidence_pill = (
            f"<a class='pill' href='{safe(lang.evidence_url)}' target='_blank' rel='noopener'>Evidence</a>"
            if lang.evidence_url else ""
        )

        body = f"""
        <div class="breadcrumbs">
          <a href="{rel}index.html">Home</a> · <a href="{rel}browse/index.html?letter={first_letter(lang.name)}">Browse</a> · {safe(lang.name)}
        </div>
        <section class="panel section">
          <h1 style="margin:0 0 8px;">{safe(lang.name)}</h1>
          <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <span class="pill">{len(lang.programs)} program{'' if len(lang.programs)==1 else 's'}</span>
            {added_at_pill}
            {taxonomy_only_pill}
            {"".join(prov_pills)}
            {evidence_pill}
            {f'<a class=\"pill\" href=\"{safe(report_lang_url)}\" target=\"_blank\" rel=\"noopener\">Report issue</a>' if report_lang_url else ''}
            {f'<a class=\"pill\" href=\"{safe(issues_lang_url)}\" target=\"_blank\" rel=\"noopener\">View issues</a>' if issues_lang_url else ''}
            {audit_pill}
          </div>
          {alias_html}
          {prov_line}
          {audit_line}
        </section>
        {cross_source_html}
        {ext_claims_html}
        {related_html}
        <section class="panel section">
          <h2 style="margin:0 0 10px;">LLM-contributed programs</h2>
          {"".join(programs_html)}
        </section>
        {swh_samples_html}
        {heuristics_html}
        {pager}
        """

        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            layout(
                title=f"{lang.name} · PL Catalog",
                rel=rel,
                body=body,
                generated_at=generated_at,
                github_owner_repo=github_owner_repo,
            ),
            encoding="utf-8",
        )


def render_contribute_add_pl_page(
    *,
    dist_root: Path,
    generated_at: str,
    github_owner_repo: str | None,
) -> None:
    """Write /contribute/add-pl/index.html — a form to propose a new PL.

    Submit → opens a pre-filled GitHub issue with the `pl-add` label.
    A maintainer-side workflow then creates a PR that materializes the files
    (languages/<Name>/meta.json, optional program example, pl_list.txt
    insertion) per docs/add_pl.md.

    Required fields: name + evidence_url. Program example is optional
    (skeleton proposals are accepted; maintainers add the program later).
    """
    page = dist_root / "contribute" / "add-pl" / "index.html"
    rel = rel_prefix(page, dist_root)
    page.parent.mkdir(parents=True, exist_ok=True)

    repo_attr = f'data-repo="{safe(github_owner_repo)}"' if github_owner_repo else 'data-repo=""'
    no_repo_warn = "" if github_owner_repo else (
        "<p class='muted'><strong>Note:</strong> no GitHub repository is configured "
        "for this site, so the Submit button is disabled. Set "
        "<code>GITHUB_OWNER_REPO</code> at build time.</p>"
    )

    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Add a programming language</h1>
      <p class="muted" style="margin:0 0 14px;">Propose a new PL for the catalog.
      Required: language name + evidence URL. A program example is encouraged
      but optional — skeleton proposals are accepted (a maintainer will add the
      program later). Submit opens a pre-filled GitHub issue tagged
      <code>pl-add</code>; an auto-PR workflow turns the issue into a pull
      request that materializes <code>languages/&lt;Name&gt;/meta.json</code>,
      the program files, and the <code>pl_list.txt</code> insertion.</p>
      <p class="muted">Existing rules in
      <a href="https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/CLAUDE.md" target="_blank" rel="noopener">CLAUDE.md</a>
      and the auto-PR workflow in
      <a href="https://github.com/{safe(github_owner_repo) if github_owner_repo else ''}/blob/main/docs/add_pl.md" target="_blank" rel="noopener">docs/add_pl.md</a>.</p>
      {no_repo_warn}
    </section>

    <section class="panel section">
      <form class="pl-add-form" {repo_attr}
            style="display:flex; flex-direction:column; gap:14px;">

        <fieldset style="border:1px solid var(--border, #2a2a2a); border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:10px;">
          <legend style="padding:0 8px; font-weight:600;">Language</legend>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Canonical name *</span>
            <input type="text" name="pl_name" required placeholder="e.g. Portable Game Notation" />
          </label>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Aliases (optional, comma-separated)</span>
            <input type="text" name="aliases" placeholder="e.g. PGN, ChessPGN" />
          </label>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Evidence URL * — Wikipedia or official site</span>
            <input type="url" name="evidence_url" required placeholder="https://en.wikipedia.org/wiki/..." />
          </label>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Known file extensions (comma-separated, leading dot optional) — first one is treated as primary. E.g. <code>.pgn</code> or <code>.py, .pyi, .pyx</code></span>
            <input type="text" name="extensions" placeholder="e.g. .pgn  —or—  .py, .pyi, .pyx" />
          </label>
        </fieldset>

        <fieldset style="border:1px solid var(--border, #2a2a2a); border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:10px;">
          <legend style="padding:0 8px; font-weight:600;">Program example <span class="muted" style="font-weight:normal; font-size:12px;">(optional — skeleton proposals accepted)</span></legend>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Title — e.g. "Hello World", "Famous game: Adams vs Torre"</span>
            <input type="text" name="program_title" placeholder="(optional)" />
          </label>
          <div style="display:grid; gap:10px; grid-template-columns:1fr 1fr;">
            <label style="display:flex; flex-direction:column; gap:4px;">
              <span class="muted" style="font-size:12px;">File extension — e.g. .pgn</span>
              <input type="text" name="program_ext" placeholder=".ext" />
            </label>
            <label style="display:flex; flex-direction:column; gap:4px;">
              <span class="muted" style="font-size:12px;">License guess (optional)</span>
              <input type="text" name="program_license" placeholder="MIT, Apache-2.0, Public Domain, …" />
            </label>
          </div>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Origin URL — public URL where this code appears (GitHub, Rosetta Code, official docs)</span>
            <input type="url" name="program_origin_url" placeholder="https://..." />
          </label>
          <label style="display:flex; flex-direction:column; gap:4px;">
            <span class="muted" style="font-size:12px;">Code — paste the program (a real, non-trivial example, &lt;200 lines)</span>
            <textarea name="program_code" rows="12" placeholder="(paste code here)" style="font-family:monospace; font-size:13px;"></textarea>
          </label>
        </fieldset>

        <fieldset style="border:1px solid var(--border, #2a2a2a); border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:10px;">
          <legend style="padding:0 8px; font-weight:600;">Notes <span class="muted" style="font-weight:normal; font-size:12px;">(optional)</span></legend>
          <textarea name="notes" rows="3" placeholder="Anything else the maintainer should know (e.g. inclusion-bar rationale for borderline cases)"></textarea>
        </fieldset>

        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
          <button class="btn" type="submit">Submit via GitHub (opens new tab)</button>
          <a class="pl-add-fallback-link btn" href="#" target="_blank" rel="noopener"
             style="text-decoration:none; font-size:13px;">
            (or open the pre-filled issue directly)
          </a>
        </div>
        <div class="pl-add-status muted" style="font-size:13px; min-height:1em;"></div>
      </form>
    </section>

    <section class="panel section">
      <h2 style="margin:0 0 8px;">What happens after I submit?</h2>
      <ol style="color:var(--muted); font-size:13px; line-height:1.55;">
        <li>A GitHub issue opens in this repo, tagged <code>pl-add</code>, carrying your form fields in a structured YAML block.</li>
        <li>A scheduled workflow (<code>.github/workflows/pl-add-pr.yml</code>) picks up the issue and runs <code>tools/process_pl_addition.py</code> against it: validates the name isn't already in <code>pl_list.txt</code>, materializes <code>languages/&lt;Name&gt;/meta.json</code> and (if provided) the program files (<code>code.&lt;ext&gt;</code> + <code>manifest.json</code>), and appends the name to <code>pl_list.txt</code>.</li>
        <li>The workflow opens a draft pull request from a feature branch <code>pl-add/&lt;sanitized-name&gt;</code>, with <code>Resolves #&lt;issue&gt;</code> in the body.</li>
        <li>A maintainer reviews the PR (sanity-checks the evidence URL, the program source, the license). On merge, the new PL appears in the next site build.</li>
        <li>For skeleton proposals (no program), the PR creates the meta.json but flags the missing program in the PR description; a separate follow-up commit (manual or via the agentic <code>/loop</code>) adds the example.</li>
      </ol>
    </section>"""

    page.write_text(
        layout(title="Add a PL · PL Catalog", rel=rel, body=body,
               description="Propose a new programming language for the catalog.",
               generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )


def render_audit_page(*, dist_root: Path, generated_at: str, github_owner_repo: str | None) -> None:
    page = dist_root / "audit" / "index.html"
    rel = rel_prefix(page, dist_root)
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Audit view</h1>
      <p class="muted" style="margin:0 0 14px;">Explainable, on-demand rendering of <code>data/audit.json</code>.</p>
      <button id="auditLoad" class="btn" type="button">Load audit</button>
      <span id="auditStatus" class="muted" style="margin-left:10px;"></span>
    </section>

    <section class="panel section" id="auditSummary" style="margin-top:18px;">
      <div class="muted">Audit not loaded yet.</div>
    </section>

    <section class="panel section" style="margin-top:18px;">
      <h2>Most-affected languages</h2>
      <div id="auditTopLangs" class="muted">Audit not loaded yet.</div>
    </section>

    <section class="panel section" style="margin-top:18px;">
      <h2>Findings</h2>
      <div class="audit-controls" style="margin: 10px 0 12px;">
        <input id="auditFilter" type="search" placeholder="Filter by language, kind, or text…" autocomplete="off" />
        <select id="auditSeverity">
          <option value="all">All severities</option>
          <option value="error">Errors</option>
          <option value="warn">Warnings</option>
          <option value="info">Infos</option>
        </select>
      </div>
      <div id="auditFindings" class="muted">Audit not loaded yet.</div>
    </section>

    <div class="audit-grid" style="margin-top:18px;">
      <section class="panel section">
        <h2>Duplicate candidates</h2>
        <div id="auditDuplicates" class="muted">Audit not loaded yet.</div>
      </section>
      <section class="panel section">
        <h2>Clusters</h2>
        <div id="auditClusters" class="muted">Audit not loaded yet.</div>
      </section>
    </div>
    """

    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        layout(title="Audit · PL Catalog", rel=rel, body=body, generated_at=generated_at, github_owner_repo=github_owner_repo),
        encoding="utf-8",
    )


def build_languages(*, turns_by_language: dict[str, TurnInfo]) -> list[Language]:
    meta_paths = sorted(LANGUAGES_DIR.rglob("meta.json"))
    languages: list[Language] = []
    for meta_path in meta_paths:
        try:
            meta = read_json(meta_path)
        except Exception as e:
            raise SystemExit(f"Failed to parse {meta_path}: {e}") from e

        name = str(meta.get("name") or "").strip()
        if not name:
            continue
        aliases = list(meta.get("aliases") or [])
        evidence_url = str(meta.get("evidence_url") or "").strip()
        added_at = str(meta.get("added_at") or "").strip()

        folder = meta_path.parent
        folder_rel = folder.relative_to(LANGUAGES_DIR).as_posix()
        slug = make_lang_slug(name)

        turn = turns_by_language.get(canonical_name(name).lower())
        agent = turn.trailers.get("Agent") if turn else None
        model = turn.trailers.get("Model") if turn else None
        temperature = parse_temperature(turn.trailers.get("Temperature") if turn else None)
        web_search = normalize_web_search(turn.trailers.get("WebSearch") if turn else None)

        programs: list[Program] = []
        programs_dir = folder / "programs"
        if programs_dir.is_dir():
            for prog_dir in sorted([p for p in programs_dir.iterdir() if p.is_dir()]):
                manifest_path = prog_dir / "manifest.json"
                if not manifest_path.exists():
                    continue
                manifest = read_json(manifest_path)
                sha256 = str(manifest.get("code_sha256") or prog_dir.name)
                title = str(manifest.get("title") or "Untitled program")
                origin_url = str(manifest.get("origin_url") or "")
                license_guess = manifest.get("license_guess")
                license_guess = str(license_guess) if license_guess else None
                prog_added_at = str(manifest.get("added_at") or "")

                code_path = find_program_code_file(prog_dir)
                code_bytes = None
                code_text = None
                code_out_name = None
                if code_path is not None and code_path.exists():
                    code_bytes = code_path.read_bytes()
                    code_text = code_bytes.decode("utf-8", errors="replace")
                    code_out_name = derive_code_out_name(code_path.name)

                programs.append(
                    Program(
                        sha256=sha256,
                        title=title,
                        origin_url=origin_url,
                        license_guess=license_guess,
                        added_at=prog_added_at,
                        code_source_path=code_path,
                        code_bytes=code_bytes,
                        code_text=code_text,
                        code_out_name=code_out_name,
                    )
                )

        languages.append(
            Language(
                name=name,
                aliases=aliases,
                evidence_url=evidence_url,
                added_at=added_at,
                folder_rel=folder_rel,
                slug=slug,
                programs=programs,
                turn_commit=turn.commit if turn else None,
                turn_authored_at=turn.authored_at if turn else None,
                agent=agent,
                model=model,
                temperature=temperature,
                web_search=web_search,
            )
        )

    languages.sort(key=lambda l: l.name.lower())
    return languages


def copy_assets(*, out: Path) -> None:
    assets_src = Path(__file__).parent / "assets"
    assets_dst = out / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)
    for p in assets_src.iterdir():
        if p.is_file():
            shutil.copy2(p, assets_dst / p.name)


def write_index_json(
    *,
    out: Path,
    languages: list[Language],
    generated_at: str,
    enrichments: dict[str, TaxonomyEnrichment] | None = None,
) -> None:
    enrichments = enrichments or {}
    entries = []
    for l in languages:
        enr = enrichments.get(l.name)
        entries.append({
            "name": l.name,
            "slug": l.slug,
            "aliases": l.aliases,
            "evidence_url": l.evidence_url,
            "added_at": l.added_at,
            "program_count": len(l.programs),
            "first_letter": first_letter(l.name),
            "turn_commit": l.turn_commit,
            "turn_authored_at": l.turn_authored_at,
            "agent": l.agent,
            "model": l.model,
            "temperature": l.temperature,
            "web_search": l.web_search,
            # New cross-source / SWH evidence fields.
            "pl_id": enr.pl_id if enr else None,
            "has_swh": bool(enr and enr.swh_samples),
            "swh_sample_count": len(enr.swh_samples) if enr else 0,
            "taxonomy_only": (not l.added_at) and (not l.programs),
            "source_count": (
                sum(1 for v in enr.in_sources.values() if v) + (1 if l.programs else 0)
                if enr else (1 if l.programs else 0)
            ),
            "in_sources": list(s for s, v in (enr.in_sources.items() if enr else []) if v),
        })
    payload = {"generated_at": generated_at, "languages": entries}
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "data" / "index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_ext_index_json(*, out: Path, languages: list[Language], generated_at: str) -> None:
    ext_map: dict[str, dict[str, Any]] = {}
    for lang in languages:
        for prog in lang.programs:
            if prog.code_out_name:
                ext = Path(prog.code_out_name).suffix.lower().lstrip(".")
                if not ext:
                    ext = "unknown"
            else:
                ext = "unknown"
            item = ext_map.setdefault(ext, {"extension": ext, "program_count": 0, "languages": set(), "examples": []})
            item["program_count"] += 1
            item["languages"].add(lang.name)
            if len(item["examples"]) < 6:
                item["examples"].append(
                    {
                        "language": lang.name,
                        "title": prog.title,
                        "sha256": prog.sha256,
                    }
                )

    extensions = []
    for ext, item in ext_map.items():
        langs = sorted(item["languages"], key=str.lower)
        extensions.append(
            {
                "extension": ext,
                "program_count": item["program_count"],
                "language_count": len(langs),
                "languages": langs,
                "examples": item["examples"],
            }
        )

    extensions.sort(key=lambda x: (-x["program_count"], x["extension"]))
    payload = {"generated_at": generated_at, "extensions": extensions}
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "data" / "ext_index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def copy_program_files(*, out: Path, languages: list[Language]) -> None:
    code_root = out / "code"
    for lang in languages:
        for prog in lang.programs:
            if not prog.sha256:
                continue
            out_dir = code_root / prog.sha256
            out_dir.mkdir(parents=True, exist_ok=True)

            # Copy manifest if it exists in the source folder.
            if prog.code_source_path is not None:
                prog_dir = prog.code_source_path.parent
                manifest_src = prog_dir / "manifest.json"
                if manifest_src.exists():
                    shutil.copy2(manifest_src, out_dir / "manifest.json")

            if prog.code_bytes is None:
                continue

            out_name = prog.code_out_name or "code.txt"
            (out_dir / out_name).write_bytes(prog.code_bytes)


def compute_top_domains_licenses_exts(
    languages: list[Language],
) -> tuple[list[tuple[str, int]], list[tuple[str, int]], list[tuple[str, int]]]:
    domains = Counter()
    licenses = Counter()
    exts = Counter()
    for lang in languages:
        for prog in lang.programs:
            if prog.origin_url:
                try:
                    domains[urlparse(prog.origin_url).netloc.lower() or "(unknown)"] += 1
                except Exception:
                    domains["(invalid url)"] += 1
            licenses[prog.license_guess or "Unknown"] += 1
            if prog.code_out_name:
                suffix = Path(prog.code_out_name).suffix.lower().lstrip(".")
                exts[suffix or "unknown"] += 1
            else:
                exts["unknown"] += 1
    return domains.most_common(12), licenses.most_common(12), exts.most_common(12)


def compute_added_by_day(languages: list[Language]) -> list[tuple[str, int]]:
    ctr = Counter()
    for lang in languages:
        dt = parse_iso8601(lang.added_at)
        if dt is None:
            continue
        ctr[dt.date().isoformat()] += 1
    return sorted(ctr.items())


def temperature_bucket(temp: float) -> str:
    if temp < 0:
        return "<0"
    if temp < 0.2:
        return "0.0–0.2"
    if temp < 0.4:
        return "0.2–0.4"
    if temp < 0.6:
        return "0.4–0.6"
    if temp < 0.8:
        return "0.6–0.8"
    if temp < 1.0:
        return "0.8–1.0"
    return "≥1.0"


def compute_turn_stats(turns: list[TurnInfo]) -> dict[str, Any]:
    models = Counter()
    agents = Counter()
    web_search = Counter()
    temps: list[float] = []
    temp_buckets = Counter()

    for turn in turns:
        model = (turn.trailers.get("Model") or "").strip() or "Unknown"
        agent = (turn.trailers.get("Agent") or "").strip() or "Unknown"
        ws = normalize_web_search(turn.trailers.get("WebSearch"))
        ws = (ws or "").strip() or "Unknown"

        models[model] += 1
        agents[agent] += 1
        web_search[ws] += 1

        temp = parse_temperature(turn.trailers.get("Temperature"))
        if temp is not None:
            temps.append(temp)
            temp_buckets[temperature_bucket(temp)] += 1

    bucket_order = ["<0", "0.0–0.2", "0.2–0.4", "0.4–0.6", "0.6–0.8", "0.8–1.0", "≥1.0"]
    temp_bucket_rows = [(b, int(temp_buckets.get(b, 0))) for b in bucket_order if temp_buckets.get(b, 0)]

    if temps:
        temps_min = min(temps)
        temps_max = max(temps)
        temps_avg = sum(temps) / len(temps)
    else:
        temps_min = temps_max = temps_avg = None

    return {
        "turns_total": len(turns),
        "unique_models": len(models),
        "unique_agents": len(agents),
        "top_models": models.most_common(12),
        "top_agents": agents.most_common(12),
        "web_search": web_search.most_common(12),
        "temps_count": len(temps),
        "temps_min": temps_min,
        "temps_max": temps_max,
        "temps_avg": temps_avg,
        "temp_buckets": temp_bucket_rows,
    }


def compute_prev_next(languages: list[Language]) -> dict[str, tuple[Language | None, Language | None]]:
    if not languages:
        return {}
    mapping: dict[str, tuple[Language | None, Language | None]] = {}
    for i, lang in enumerate(languages):
        prev_lang = languages[i - 1] if i > 0 else None
        next_lang = languages[i + 1] if i + 1 < len(languages) else None
        mapping[lang.slug] = (prev_lang, next_lang)
    return mapping


def build_site(*, out: Path, github_owner_repo: str | None, with_audit: bool) -> None:
    if not LANGUAGES_DIR.exists():
        raise SystemExit(f"Missing {LANGUAGES_DIR}")

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    turns = read_turns_from_git()
    turns_by_language = index_turns_by_language(turns)
    turn_stats = compute_turn_stats(turns)

    languages = build_languages(turns_by_language=turns_by_language)
    counts = letter_counts(languages)
    programs_total = sum(len(l.programs) for l in languages)
    top_domains, top_licenses, top_exts = compute_top_domains_licenses_exts(languages)
    langs_added_by_day = compute_added_by_day(languages)
    slug_to_prev_next = compute_prev_next(languages)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "browse").mkdir(parents=True, exist_ok=True)
    (out / "extensions").mkdir(parents=True, exist_ok=True)
    (out / "stats").mkdir(parents=True, exist_ok=True)
    (out / "audit").mkdir(parents=True, exist_ok=True)
    (out / "data").mkdir(parents=True, exist_ok=True)

    copy_assets(out=out)
    # write_index_json is deferred until after enrichments are computed so the
    # JSON can carry `has_swh`, `taxonomy_only`, source-count, etc. for filters.
    write_ext_index_json(out=out, languages=languages, generated_at=generated_at)
    copy_program_files(out=out, languages=languages)

    audit_available = False
    if with_audit:
        audit_out = out / "data" / "audit.json"
        try:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "audit_repo.py"), "--out", str(audit_out)],
                cwd=str(ROOT),
                check=True,
                text=True,
                capture_output=True,
            )
            audit_available = audit_out.exists()
        except Exception:
            audit_available = False

    audit_summary = load_audit_summary(out / "data" / "audit.json")
    if audit_summary:
        audit_available = True

    related_by_language = compute_related_languages(languages, k=5)

    # Phase 1: cross-source presence + ext claims + SWH samples. Best-effort:
    # missing taxonomy / samples dirs are tolerated (sections degrade quietly).
    try:
        enrichments = build_taxonomy_enrichments(languages)
        print(f"Loaded taxonomy enrichments for {len(enrichments)} / {len(languages)} in-repo languages.")
    except Exception as e:
        print(f"WARNING: taxonomy load failed ({type(e).__name__}: {e}); pages will lack enrichments.")
        enrichments = {}

    # Phase 2c: extend `languages` with synthesized entries for PLs that exist in
    # the taxonomy but have no in-repo `languages/<L>/` directory. These pages
    # have no LLM section but do carry the cross-source + ext-claim + SWH sample
    # sections. They get the same alphabetical browse / prev-next treatment.
    if enrichments:
        try:
            synth, enrichments = synthesize_taxonomy_only_languages(
                languages=languages, enrichments=enrichments)
            if synth:
                languages = sorted(languages + synth, key=lambda l: l.name.lower())
                print(f"Added {len(synth)} taxonomy-only PL pages "
                      f"(total: {len(languages)}).")
                # Recompute downstream tables that depend on the full list.
                counts = letter_counts(languages)
                slug_to_prev_next = compute_prev_next(languages)
        except Exception as e:
            print(f"WARNING: taxonomy-only expansion failed ({type(e).__name__}: {e}).")

    # Now safe to write the language index with enrichment-derived flags.
    write_index_json(out=out, languages=languages, generated_at=generated_at, enrichments=enrichments)

    render_home_page(
        dist_root=out,
        languages=languages,
        counts=counts,
        generated_at=generated_at,
        programs_total=programs_total,
        github_owner_repo=github_owner_repo,
        enrichments=enrichments,
    )
    render_browse_page(
        dist_root=out, languages=languages, counts=counts, generated_at=generated_at, github_owner_repo=github_owner_repo
    )
    render_extensions_page(dist_root=out, generated_at=generated_at, github_owner_repo=github_owner_repo)
    taxonomy_stats = compute_taxonomy_stats(languages=languages, enrichments=enrichments) if enrichments else None
    render_stats_page(
        dist_root=out,
        languages=languages,
        counts=counts,
        programs_total=programs_total,
        generated_at=generated_at,
        top_domains=top_domains,
        top_licenses=top_licenses,
        top_exts=top_exts,
        langs_added_by_day=langs_added_by_day,
        turns_total=int(turn_stats["turns_total"]),
        unique_agents=int(turn_stats["unique_agents"]),
        unique_models=int(turn_stats["unique_models"]),
        top_agents=list(turn_stats["top_agents"]),
        top_models=list(turn_stats["top_models"]),
        web_search_counts=list(turn_stats["web_search"]),
        temps_count=int(turn_stats["temps_count"]),
        temps_min=turn_stats["temps_min"],
        temps_max=turn_stats["temps_max"],
        temps_avg=turn_stats["temps_avg"],
        temp_buckets=list(turn_stats["temp_buckets"]),
        github_owner_repo=github_owner_repo,
        audit_summary=audit_summary if audit_available else None,
        audit_page_rel=f"{rel_prefix(out / 'audit' / 'index.html', out)}audit/index.html",
        taxonomy_stats=taxonomy_stats,
    )
    render_language_pages(
        dist_root=out,
        languages=languages,
        generated_at=generated_at,
        slug_to_prev_next=slug_to_prev_next,
        github_owner_repo=github_owner_repo,
        related_by_language=related_by_language,
        audit_summary=audit_summary if audit_available else None,
        enrichments=enrichments,
    )
    render_audit_page(dist_root=out, generated_at=generated_at, github_owner_repo=github_owner_repo)
    render_contribute_add_pl_page(
        dist_root=out, generated_at=generated_at, github_owner_repo=github_owner_repo,
    )

    # Phase 2b: per-extension pages.
    try:
        n_ext_pages = render_per_extension_pages(
            dist_root=out,
            generated_at=generated_at,
            github_owner_repo=github_owner_repo,
            languages=languages,
            enrichments=enrichments,
        )
        print(f"Wrote {n_ext_pages} per-extension pages + index at /ext/.")
    except Exception as e:
        print(f"WARNING: per-extension page rendering failed ({type(e).__name__}: {e}).")

    # Phase 2 polish: per-source pages (list of PLs from each upstream source).
    try:
        n_src_pages = render_source_pages(
            dist_root=out,
            generated_at=generated_at,
            github_owner_repo=github_owner_repo,
            languages=languages,
            enrichments=enrichments,
        )
        print(f"Wrote {n_src_pages} per-source pages + index at /source/.")
    except Exception as e:
        print(f"WARNING: per-source page rendering failed ({type(e).__name__}: {e}).")

    # Crowd-source: extension review queue.
    try:
        n_review = render_extension_review_queue_page(
            dist_root=out,
            generated_at=generated_at,
            github_owner_repo=github_owner_repo,
        )
        if n_review:
            print(f"Wrote /review/extensions/ ({n_review} extensions to label).")
    except Exception as e:
        print(f"WARNING: extension review queue rendering failed ({type(e).__name__}: {e}).")

    # Maintainer triage view.
    try:
        n_curator = render_curator_review_page(
            dist_root=out,
            generated_at=generated_at,
            github_owner_repo=github_owner_repo,
        )
        print(f"Wrote /review/curator/ ({n_curator} submitted labels).")
    except Exception as e:
        print(f"WARNING: curator review rendering failed ({type(e).__name__}: {e}).")

    # Phase 2 polish: /samples/ index — every PL that has real SWH evidence.
    try:
        n_with_samples = render_samples_index_page(
            dist_root=out,
            generated_at=generated_at,
            github_owner_repo=github_owner_repo,
            languages=languages,
            enrichments=enrichments,
        )
        print(f"Wrote /samples/ index ({n_with_samples} PLs with SWH samples).")
    except Exception as e:
        print(f"WARNING: samples index rendering failed ({type(e).__name__}: {e}).")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build a static website from languages/* data.")
    parser.add_argument("--out", default=str(Path("web") / "dist"), help="Output directory (default: web/dist)")
    parser.add_argument(
        "--github",
        default=None,
        help="GitHub repo as owner/repo for “Report issue” links (default: auto from git origin). Use '-' to disable.",
    )
    parser.add_argument(
        "--with-audit",
        action="store_true",
        help="Also generate data/audit.json (duplicates/integrity/clustering hints).",
    )
    args = parser.parse_args(argv)

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out

    # Safety: refuse to delete something that doesn't look like a build dir.
    out_str = str(out)
    if os.path.abspath(out_str) in ("/", str(ROOT)):
        raise SystemExit(f"Refusing to use --out={out}")

    if args.github == "-":
        github_owner_repo = None
    else:
        github_owner_repo = (args.github or "").strip() or guess_github_owner_repo()

    build_site(out=out, github_owner_repo=github_owner_repo, with_audit=bool(args.with_audit))
    print(f"[web] built site at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
