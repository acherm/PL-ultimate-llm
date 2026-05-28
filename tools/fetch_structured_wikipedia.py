#!/usr/bin/env python3
"""Re-extract Wikipedia infobox file-extension fields from the
`wikimedia/structured-wikipedia` Hugging Face dataset (Phase 1 replacement
for tools/fetch_wikipedia_infoboxes.py).

The upstream dataset is the Wikimedia Enterprise "Structured Contents"
snapshot, re-encoded as Parquet. Every row already carries:
  - `main_entity.identifier`  → Wikidata QID (no sitelink resolution needed)
  - `infoboxes`               → JSON-encoded recursive tree of typed nodes
                                (`type` ∈ {infobox, section, field, list, image})

Compared to the legacy MediaWiki API + mwparserfromhell flow, this means:
  1. `<br/>`-separated lists arrive as `type=list` nodes with `values: [...]`
     instead of a wikitext blob — no regex / template unwrapping needed.
  2. Field labels arrive as clean human strings (e.g. "Filename extensions")
     — we still pass them through the same EXT_FIELD_PAT regex as the legacy
     parser for compatibility.
  3. The Wikidata QID arrives on the row, so we no longer need the per-title
     redirect/normalisation dance.

We keep `parse_ext_field` from the legacy parser as a fallback for any
scalar `value` strings the upstream parser couldn't fully unwrap.

Output: data/raw/wikipedia_infobox.<YYYY-MM-DD>.structured.jsonl
        One record per QID with an enwiki_title in the P1195 snapshot,
        schema-compatible with the legacy file plus a few extra fields.

Reproducibility: the HF dataset commit SHA used for this run is recorded
in the sibling .manifest.json so future builds can pin the exact snapshot.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import socket
import sys
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, list_repo_files, dataset_info

# Bound any single TCP read on the HF download socket. Without this, a
# stalled shard download can hang the whole job indefinitely (the default
# socket timeout is None). At 300 s a long-tail shard still completes;
# anything past that raises, the per-shard try/except in main() catches
# it, and we move on to the next shard rather than waiting forever.
socket.setdefaulttimeout(300)

# Re-use the legacy regex + per-value parser. `parse_ext_field` is what we
# use as a fallback when a `type=field` node carries a scalar string that
# still needs to be split / cleaned (the structured dataset's template
# unwrapping is best-effort).
sys.path.insert(0, str(Path(__file__).parent))
from fetch_wikipedia_infoboxes import (  # noqa: E402
    EXT_FIELD_PAT,
    normalize_field_name,
    parse_ext_field,
)

REPO_ID = "wikimedia/structured-wikipedia"
CONFIG = "enwiki_namespace_0"
# Parquet shards live under `enwiki/data/enwiki_namespace_0_<n>.parquet`
# (86 shards, ~400 MB each, total ~34 GiB).
SHARD_PREFIX = "enwiki/data/"
SHARD_RE = re.compile(r"^enwiki/data/enwiki_namespace_0_(\d+)\.parquet$")
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
CACHE_DIR = ROOT / ".cache" / "structured_wikipedia"

# Columns we actually need. Reading a subset keeps the row-group decode
# light — `infoboxes` is the big one.
PARQUET_COLUMNS = ["name", "url", "identifier", "main_entity", "infoboxes", "version"]


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def load_target_qids(p1195_path: Path,
                     pl_items_path: Path | None = None) -> dict[str, dict]:
    """Return {qid: {label, enwiki_title, wikidata_extensions}} for every
    target QID with an enwiki sitelink.

    Two sources, unioned and deduped by QID:
      - `p1195_path` (required): Wikidata items carrying P1195. Carries
        per-item filename-extension claims that the Phase-1 ext extractor
        compares against the structured-wikipedia infobox.
      - `pl_items_path` (optional): Wikidata items typed as a PL via the
        instance-of (P31) closure but NOT necessarily carrying P1195. Closes
        the R-shaped gap where Wikidata is missing the extension claim. The
        `wikidata_extensions` list is empty for these, so downstream
        "wikipedia_missing" stays meaningful.
    """
    out: dict[str, dict] = {}
    with p1195_path.open() as f:
        for line in f:
            rec = json.loads(line)
            qid = rec.get("qid")
            if not qid:
                continue
            if not rec.get("enwiki_title"):
                continue
            out[qid] = {
                "qid": qid,
                "label": rec.get("label") or "",
                "enwiki_title": rec.get("enwiki_title") or "",
                "wikidata_extensions": [
                    (e.get("value") or "").lower() for e in rec.get("extensions") or []
                ],
            }
    if pl_items_path and pl_items_path.exists():
        n_added = 0
        with pl_items_path.open() as f:
            for line in f:
                rec = json.loads(line)
                qid = rec.get("qid")
                if not qid or qid in out:
                    continue
                if not rec.get("enwiki_title"):
                    continue
                out[qid] = {
                    "qid": qid,
                    "label": rec.get("label") or "",
                    "enwiki_title": rec.get("enwiki_title") or "",
                    "wikidata_extensions": [],
                }
                n_added += 1
        print(f"[load] union with {pl_items_path.name}: +{n_added} PL-typed QIDs "
              f"not in P1195", flush=True)
    return out


def list_enwiki_shards() -> list[str]:
    """Return enwiki parquet shards sorted by shard number (0, 1, 2, …) so
    `--limit-shards 1` always hits shard 0 first."""
    files = list_repo_files(REPO_ID, repo_type="dataset")
    matches: list[tuple[int, str]] = []
    for f in files:
        m = SHARD_RE.match(f)
        if m:
            matches.append((int(m.group(1)), f))
    matches.sort()
    return [f for _, f in matches]


def resolve_dataset_revision() -> str | None:
    try:
        info = dataset_info(REPO_ID)
        return info.sha
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] could not resolve dataset revision: {exc!r}", flush=True)
        return None


# ---------------------------------------------------------------------------
# Infobox tree walk
# ---------------------------------------------------------------------------

def _decode_infoboxes(raw):
    """The `infoboxes` column is either a list of JSON strings (one per
    infobox template) or a single JSON-encoded string holding a list — handle
    both. Returns a flat list of root nodes; never raises."""
    if raw is None:
        return []
    if isinstance(raw, (list, tuple)):
        # PyArrow surfaces list<string> as list[str].
        out = []
        for item in raw:
            if not item:
                continue
            try:
                decoded = json.loads(item) if isinstance(item, str) else item
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(decoded, list):
                out.extend(decoded)
            else:
                out.append(decoded)
        return out
    if isinstance(raw, (bytes, bytearray)):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError:
            return []
    if isinstance(raw, str):
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError:
            return []
        return decoded if isinstance(decoded, list) else [decoded]
    if isinstance(raw, dict):
        return [raw]
    return []


def _node_name(node: dict) -> str:
    n = node.get("name")
    if isinstance(n, dict):
        # Defensive: name should be a string, but tolerate {value: "..."}.
        return str(n.get("value") or "")
    return str(n or "")


# Phase 2: PL-fact infobox fields we lift in addition to filename
# extensions. The Wikipedia "Infobox programming language" template uses
# stable label conventions; the patterns below match against the
# normalised (lower, dash/underscore→underscore) field name.
PL_FACT_PATTERNS: dict[str, re.Pattern] = {
    "paradigms": re.compile(
        r"^(paradigms?)$"),
    "typing": re.compile(
        r"^(typing_discipline|typing|type_system)$"),
    "designed_by": re.compile(
        r"^(designed_by|designers?|authors?|developers?|developed_by|created_by)$"),
    "first_appeared": re.compile(
        r"^(first_appeared|appeared_in|initial_release|first_release|released)$"),
    "influenced_by": re.compile(
        r"^(influenced_by)$"),
    "license": re.compile(
        r"^(licen[cs]e)$"),
    "implementation_languages": re.compile(
        r"^(implementation_languages?|implemented_in|implementation)$"),
    "homepage": re.compile(
        r"^(website|homepage|web_site|official_website|url)$"),
}


def classify_field_name(name: str) -> str | None:
    """Return the canonical fact key (e.g. 'paradigms', 'extensions') if
    this infobox field name matches a known pattern, else None.

    `extensions` is a special key handled by EXT_FIELD_PAT so the Phase-1
    extension path remains untouched.
    """
    if not name:
        return None
    norm = normalize_field_name(name)
    if EXT_FIELD_PAT.match(norm):
        return "extensions"
    for key, pat in PL_FACT_PATTERNS.items():
        if pat.match(norm):
            return key
    return None


def walk_infoboxes(roots, by_field: dict[str, list[dict]]) -> None:
    """Recursively descend a list of infobox root nodes. For every
    `field`/`list` node whose `name` classifies into a known fact key,
    append a hit under that key in `by_field`.

    The Wikipedia "Programming language" template surfaces three shapes:
      1. `{type: field, name: "Paradigm", value: "…"}`
         — directly named field. Match by `classify_field_name(name)`.
      2. `{type: list, name: "Filename extensions", values: […]}`
         or with `has_parts: [{type: list_item, value: "…"}]`
         — named list. Both forms handled.
      3. `{type: section, name: "Influenced by", has_parts:
            [{type: field, value: "ABC, Ada, …"}]}`
         — section-wrapped, with an *unnamed* inner field. The section
         name carries the semantics. We propagate the section's name as
         a default field-key into its descendants.
    """
    # Each stack entry is (node, inherited_field_key). The inherited key
    # is the closest enclosing section's classification — only consumed
    # by an inner field/list that has no name of its own.
    stack: list[tuple] = [(n, None) for n in roots]
    while stack:
        node, inherited_key = stack.pop()
        if isinstance(node, list):
            stack.extend((c, inherited_key) for c in node)
            continue
        if not isinstance(node, dict):
            continue

        ntype = node.get("type")
        nname = _node_name(node)
        own_key = classify_field_name(nname) if nname else None

        if ntype == "section":
            # Sections never carry values themselves — they delegate to
            # children. Propagate this section's classification (or the
            # already-inherited one, if this section is unclassified)
            # down to has_parts.
            child_inherited = own_key or inherited_key
            for c in node.get("has_parts") or []:
                stack.append((c, child_inherited))
            continue

        # For field/list: an own-named hit wins; otherwise inherit from
        # the enclosing section.
        field_key = own_key or inherited_key
        consumed_as_list = False

        if field_key:
            if ntype == "field":
                v = node.get("value")
                if v is not None:
                    hit = {"name": nname, "kind": "field", "values": [str(v)]}
                    # Capture links too — needed for `homepage` (the
                    # visible value is often the domain text while the
                    # actual URL lives in `links[0].url`), and useful
                    # context for `influenced_by` / `designed_by`.
                    links = node.get("links") or []
                    if links:
                        hit["links"] = [
                            {"url": l.get("url"), "text": l.get("text")}
                            for l in links if isinstance(l, dict) and l.get("url")
                        ]
                    by_field.setdefault(field_key, []).append(hit)
            elif ntype == "list":
                values = [str(v) for v in (node.get("values") or []) if v is not None]
                if not values:
                    # Form: list_item children carry the scalar in `value`.
                    for part in node.get("has_parts") or []:
                        if isinstance(part, dict):
                            pv = part.get("value")
                            if pv is not None:
                                values.append(str(pv))
                if values:
                    by_field.setdefault(field_key, []).append(
                        {"name": nname, "kind": "list", "values": values})
                consumed_as_list = True

        if not consumed_as_list:
            parts = node.get("has_parts")
            if isinstance(parts, list):
                stack.extend((c, inherited_key) for c in parts)


# Upstream Wikimedia flattens multi-section infobox values like
#   "General-purpose: .hex, .mcs Platform-specific: .h80, .h86"
# into a single scalar. The legacy parser relied on `<br/>` → newline
# splits to separate the section headers from the dot-prefixed tokens;
# we no longer have those. Pre-split on ":\s+(?=\.)" so a section header
# right before a dotted extension becomes its own fragment (and gets
# dropped because it has no dot).
_SECTION_BREAK_RE = re.compile(r":\s+(?=\.)")


def _presplit_for_section_headers(raw: str) -> str:
    """Insert a newline between a section-header colon and a following
    dot-prefixed extension token so `parse_ext_field`'s `[\\n;,]+` split
    catches it as its own line."""
    return _SECTION_BREAK_RE.sub("\n", raw)


def parse_hit(hit: dict) -> list[dict]:
    """Run each value through the legacy `parse_ext_field` to keep schema
    compatibility (returns `[{value, note, raw_line}, …]`). For clean
    `type=list` values like ".php" this is a no-op; for `type=field` and
    `list_item` scalars carrying section-header prose we presplit first."""
    parsed: list[dict] = []
    seen: set[str] = set()
    for raw in hit["values"]:
        prepped = _presplit_for_section_headers(raw)
        for p in parse_ext_field(prepped):
            if p["value"] in seen:
                continue
            seen.add(p["value"])
            parsed.append(p)
    return parsed


# ---------------------------------------------------------------------------
# Phase 2: PL-fact normalisation
# ---------------------------------------------------------------------------
#
# These are intentionally LIGHT — we lowercase, strip a few noise affixes,
# canonicalise dash/space variants, and extract a year for `first_appeared`.
# No controlled vocabulary mapping (that's a separate, curated step).

_UNICODE_DASH_RE = re.compile(r"[‐-―]")
_YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2}|21\d{2})\b")
# Splits an infobox prose value into discrete enumerated items. We try to
# preserve multi-word values like "object-oriented programming" while
# splitting on the separators Wikipedia editors actually use between
# distinct items.
_FACT_LIST_SPLIT_RE = re.compile(r"\s*(?:[\n;,]|\s+(?:and|&)\s+)\s*", re.IGNORECASE)


def normalize_paradigm(v: str) -> str:
    """Drop ' programming' suffix, lowercase, normalise outer dash/space.

    We only canonicalise the OUTER form — inner parenthetical qualifiers
    keep their spaces so the result reads as 'object-oriented (prototype-
    based)' rather than the run-together 'object-oriented-(prototype-
    based)'."""
    v = v.strip().lower()
    v = re.sub(r"\bprogramming\b", "", v).strip()
    v = _UNICODE_DASH_RE.sub("-", v)
    # Collapse runs of spaces, but DO NOT replace space with dash.
    v = re.sub(r"\s+", " ", v)
    v = re.sub(r"-+", "-", v)
    return v.strip(" -")


def normalize_typing(v: str) -> str:
    v = v.strip().lower()
    v = _UNICODE_DASH_RE.sub("-", v)
    return re.sub(r"\s+", " ", v)


def extract_year(v: str) -> str:
    m = _YEAR_RE.search(v)
    return m.group(1) if m else v.strip()


def _strip_inline_refs(v: str) -> str:
    """Drop bracketed reference markers like `[1]`, `[note 2]` that the
    upstream parser sometimes leaves in scalar values."""
    return re.sub(r"\[[^\]]{1,30}\]", "", v).strip()


def _split_fact_list(v: str) -> list[str]:
    """Split a fact scalar into discrete values on commas / semicolons /
    newlines / ' and '. Returns trimmed, non-empty pieces."""
    pieces = _FACT_LIST_SPLIT_RE.split(_strip_inline_refs(v))
    return [p.strip(" .") for p in pieces if p.strip(" .")]


def normalize_fact_values(key: str, hits: list[dict]) -> list[str]:
    """Turn a list of hits (each carrying `values: [...]` from the tree
    walk) into a deduplicated, normalised list of fact strings."""
    raw_values: list[str] = []
    for h in hits:
        for v in h.get("values") or []:
            raw_values.append(str(v))

    # `type=field` scalars are commonly comma- or semicolon-separated
    # enumerations ("object-oriented, functional, imperative"). For
    # `type=list` we trust the upstream split already. We split scalars
    # for paradigm/influenced_by/implementation_languages where lists are
    # the norm; we keep typing as a single phrase.
    needs_split = key in {"paradigms", "influenced_by",
                          "implementation_languages", "designed_by"}

    pieces: list[str] = []
    for v in raw_values:
        v = _strip_inline_refs(v)
        if not v:
            continue
        if needs_split:
            pieces.extend(_split_fact_list(v))
        else:
            pieces.append(v.strip(" ."))

    out: list[str] = []
    seen: set[str] = set()
    for p in pieces:
        if not p:
            continue
        if key == "paradigms":
            norm = normalize_paradigm(p)
        elif key == "typing":
            norm = normalize_typing(p)
        elif key == "first_appeared":
            norm = extract_year(p)
        else:
            norm = p.strip(" .")
        if not norm:
            continue
        k = norm.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(norm)
    return out


def extract_homepage(hits: list[dict]) -> str | None:
    """Pick the best URL for a `homepage`-classified field. Prefer a link
    URL (the visible value is often just the domain text), then any
    https/http scalar."""
    for h in hits:
        for l in h.get("links") or []:
            url = (l.get("url") or "").strip()
            if url and url.startswith(("http://", "https://")) \
                    and "wikipedia.org" not in url:
                return url
    # Fall back to any URL-looking scalar.
    for h in hits:
        for v in h.get("values") or []:
            s = str(v).strip()
            if s.startswith(("http://", "https://")):
                return s
    return None


# ---------------------------------------------------------------------------
# Per-shard processing
# ---------------------------------------------------------------------------

def process_shard(shard_path: Path, targets: dict[str, dict],
                  found: dict[str, dict], facts_found: dict[str, dict],
                  batch_size: int = 1024) -> None:
    pf = pq.ParquetFile(shard_path)
    available = [c for c in PARQUET_COLUMNS if c in pf.schema_arrow.names]
    for batch in pf.iter_batches(columns=available, batch_size=batch_size):
        rows = batch.to_pylist()
        for row in rows:
            me = row.get("main_entity") or {}
            qid = me.get("identifier") if isinstance(me, dict) else None
            if not qid or qid not in targets or qid in found:
                continue

            roots = _decode_infoboxes(row.get("infoboxes"))
            by_field: dict[str, list[dict]] = {}
            walk_infoboxes(roots, by_field)

            # ---- Extensions (Phase 1, schema unchanged) ----
            hits_out: list[dict] = []
            for h in by_field.get("extensions", []):
                parsed = parse_hit(h)
                if not parsed:
                    continue
                hits_out.append({
                    "field": normalize_field_name(h["name"]),
                    "field_label": h["name"],
                    "kind": h["kind"],
                    "raw": " | ".join(h["values"]),
                    "parsed": parsed,
                })

            tgt = targets[qid]
            wd_exts = set(tgt["wikidata_extensions"])
            wp_exts = {p["value"] for h in hits_out for p in h["parsed"]}
            version = row.get("version") or {}
            version_id = version.get("identifier") if isinstance(version, dict) else None

            found[qid] = {
                "qid": qid,
                "label": tgt["label"],
                "enwiki_title": tgt["enwiki_title"],
                "wikipedia_name": row.get("name"),
                "wikipedia_url": row.get("url"),
                "page_id": row.get("identifier"),
                "revision_id": version_id,
                "had_wikitext": True,  # legacy-compat flag — we got the row
                "infobox_hits": hits_out,
                "wikidata_extensions": sorted(wd_exts),
                "wikipedia_extensions": sorted(wp_exts),
                "wikipedia_extra": sorted(wp_exts - wd_exts),
                "wikipedia_missing": sorted(wd_exts - wp_exts),
                "parser": "structured",
            }

            # ---- Phase 2: PL facts (paradigms, typing, designer, …) ----
            facts: dict[str, list[str] | str] = {}
            for key in PL_FACT_PATTERNS:
                hits = by_field.get(key) or []
                if not hits:
                    continue
                if key == "homepage":
                    url = extract_homepage(hits)
                    if url:
                        facts["homepage"] = url
                    continue
                vals = normalize_fact_values(key, hits)
                if not vals:
                    continue
                # `typing`, `first_appeared`, `license` are conventionally
                # single-valued; the others are lists.
                if key in {"typing", "first_appeared", "license"}:
                    facts[key] = vals[0]
                else:
                    facts[key] = vals

            if facts:
                facts_found[qid] = {
                    "qid": qid,
                    "label": tgt["label"],
                    "enwiki_title": tgt["enwiki_title"],
                    "wikipedia_url": row.get("url"),
                    "revision_id": version_id,
                    "facts": facts,
                    "parser": "structured",
                }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--input",
        help="wikidata_p1195.<date>.jsonl path. Defaults to the latest "
             "matching snapshot under data/raw/.",
    )
    p.add_argument(
        "--pl-items",
        help="wikidata_pl_items.<date>.jsonl path (PL-typed items, may or "
             "may not carry P1195). Defaults to the latest matching "
             "snapshot under data/raw/. Pass --no-pl-items to disable the "
             "union and run with only the P1195 set.",
    )
    p.add_argument(
        "--no-pl-items", action="store_true",
        help="Disable the PL-items union; restrict targets to the P1195 set.",
    )
    p.add_argument(
        "--limit-shards", type=int, default=None,
        help="Stop after N parquet shards (smoke test).",
    )
    p.add_argument(
        "--out-suffix", default="structured",
        help="Suffix for the output filename: "
             "wikipedia_infobox.<date>.<suffix>.jsonl (default: structured)",
    )
    p.add_argument(
        "--keep-shards", action="store_true",
        help="Keep downloaded parquet shards under .cache/ (default: delete "
             "each shard immediately after processing to bound disk use).",
    )
    p.add_argument(
        "--revision", default=None,
        help="Pin a specific HF dataset revision (commit SHA). Defaults to "
             "the current HEAD of the dataset repo.",
    )
    args = p.parse_args()

    # Resolve P1195 snapshot.
    if args.input:
        p1195_path = Path(args.input)
    else:
        candidates = sorted(DATA_DIR.glob("wikidata_p1195.*.jsonl"))
        if not candidates:
            sys.exit("no wikidata_p1195.*.jsonl under data/raw/")
        p1195_path = candidates[-1]
    print(f"[load] P1195 snapshot: {p1195_path}", flush=True)

    # Resolve optional PL-items snapshot (closes the no-P1195 gap, e.g. R).
    pl_items_path: Path | None = None
    if not args.no_pl_items:
        if args.pl_items:
            pl_items_path = Path(args.pl_items)
        else:
            candidates = sorted(DATA_DIR.glob("wikidata_pl_items.*.jsonl"))
            if candidates:
                pl_items_path = candidates[-1]
        if pl_items_path:
            print(f"[load] PL-items snapshot: {pl_items_path}", flush=True)
        else:
            print("[load] no wikidata_pl_items.*.jsonl under data/raw/ — "
                  "running with P1195 only", flush=True)

    targets = load_target_qids(p1195_path, pl_items_path)
    print(f"[load] {len(targets)} target QIDs (with enwiki_title)", flush=True)

    revision = args.revision or resolve_dataset_revision()
    print(f"[hf]   repo={REPO_ID} config={CONFIG} revision={revision or 'HEAD'}",
          flush=True)

    shards = list_enwiki_shards()
    print(f"[hf]   {len(shards)} parquet shards", flush=True)
    if args.limit_shards:
        shards = shards[: args.limit_shards]
        print(f"       limited to {len(shards)} shards (smoke test)", flush=True)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    found: dict[str, dict] = {}
    facts_found: dict[str, dict] = {}
    for i, shard_name in enumerate(shards, 1):
        print(f"[shard {i}/{len(shards)}] {shard_name}", flush=True)
        try:
            local = Path(hf_hub_download(
                REPO_ID, shard_name, repo_type="dataset",
                revision=revision, cache_dir=str(CACHE_DIR),
            ))
        except Exception as exc:  # noqa: BLE001
            print(f"       download failed: {exc!r}", flush=True)
            continue
        try:
            process_shard(local, targets, found, facts_found)
        finally:
            if not args.keep_shards:
                # `hf_hub_download` returns a symlink into the blobs/ store.
                # Resolve and unlink the underlying blob too so we don't keep
                # ~400 MB per shard around.
                try:
                    real = local.resolve()
                    if local.is_symlink():
                        local.unlink()
                    if real.exists() and real.is_file():
                        real.unlink()
                except OSError:
                    pass
        print(f"       matched so far: {len(found)} / {len(targets)}  "
              f"(facts: {len(facts_found)})", flush=True)
        # Early exit if we've already matched everything.
        if len(found) == len(targets):
            print("       all targets matched — stopping early", flush=True)
            break

    today = dt.date.today().isoformat()
    suffix = f".{args.out_suffix}" if args.out_suffix else ""
    out_path = DATA_DIR / f"wikipedia_infobox.{today}{suffix}.jsonl"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Mirror the legacy file's row-per-(enwiki_title) contract: emit a row
    # for every target QID, even the ones we didn't find in the HF dump
    # (with `parser=missing`), so downstream loaders can see the same set
    # they saw before.
    n_with_box = 0
    n_extra = 0
    n_missing = 0
    with out_path.open("w") as f:
        for qid, tgt in targets.items():
            if qid in found:
                rec = found[qid]
            else:
                wd_exts = set(tgt["wikidata_extensions"])
                rec = {
                    "qid": qid,
                    "label": tgt["label"],
                    "enwiki_title": tgt["enwiki_title"],
                    "wikipedia_name": None,
                    "wikipedia_url": None,
                    "page_id": None,
                    "revision_id": None,
                    "had_wikitext": False,
                    "infobox_hits": [],
                    "wikidata_extensions": sorted(wd_exts),
                    "wikipedia_extensions": [],
                    "wikipedia_extra": [],
                    "wikipedia_missing": sorted(wd_exts),
                    "parser": "missing",
                }
                n_missing += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if rec["infobox_hits"]:
                n_with_box += 1
            if rec["wikipedia_extra"]:
                n_extra += 1

    manifest_path = out_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps({
        "snapshot_date": today,
        "source": {
            "repo": REPO_ID,
            "config": CONFIG,
            "revision": revision,
            "shards_processed": len(shards),
        },
        "input_p1195": p1195_path.name,
        "items_in_output": len(targets),
        "items_matched_in_hf": len(found),
        "items_missing": n_missing,
        "items_with_infobox_hits": n_with_box,
        "items_with_wikipedia_extra": n_extra,
        "parser": "structured-wikipedia/enterprise-snapshot",
    }, indent=2) + "\n")

    print(f"[done] wrote {out_path}", flush=True)
    print(f"       items in output:       {len(targets)}", flush=True)
    print(f"       matched in HF dump:    {len(found)}", flush=True)
    print(f"       missing (not in HF):   {n_missing}", flush=True)
    print(f"       with infobox hits:     {n_with_box}", flush=True)
    print(f"       Wikipedia adds extras: {n_extra}", flush=True)
    print(f"       manifest: {manifest_path.name}", flush=True)

    # ----- Phase 2: write the PL-facts sidecar ----------------------------
    facts_out_path = DATA_DIR / f"wikipedia_pl_facts.{today}.jsonl"
    fact_field_counts: dict[str, int] = {k: 0 for k in PL_FACT_PATTERNS}
    with facts_out_path.open("w") as f:
        for qid in sorted(facts_found):
            rec = facts_found[qid]
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            for k in rec["facts"]:
                fact_field_counts[k] = fact_field_counts.get(k, 0) + 1

    facts_manifest_path = facts_out_path.with_suffix(".manifest.json")
    facts_manifest_path.write_text(json.dumps({
        "snapshot_date": today,
        "source": {
            "repo": REPO_ID,
            "config": CONFIG,
            "revision": revision,
            "shards_processed": len(shards),
        },
        "input_p1195": p1195_path.name,
        "items_with_facts": len(facts_found),
        "fields": fact_field_counts,
        "parser": "structured-wikipedia/enterprise-snapshot",
    }, indent=2) + "\n")

    print(f"[done] wrote {facts_out_path}", flush=True)
    print(f"       items with ≥1 fact:    {len(facts_found)}", flush=True)
    for k, v in sorted(fact_field_counts.items(), key=lambda x: -x[1]):
        print(f"       {k:<28} {v}", flush=True)
    print(f"       manifest: {facts_manifest_path.name}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
