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

def load_target_qids(p1195_path: Path) -> dict[str, dict]:
    """Return {qid: {label, enwiki_title, wikidata_extensions}} for every
    P1195 record that has an enwiki sitelink. Matches the legacy filter in
    `fetch_wikipedia_infoboxes.load_enwiki_items`."""
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


def walk_infoboxes(roots, hits: list[dict]) -> None:
    """Recursively descend a list of infobox root nodes; append entries to
    `hits` for any `field`/`list` node whose normalised `name` matches the
    extension-field whitelist.

    Two `type=list` shapes appear in the wild:
      A. `{type: list, values: [str, …]}`               — flat array
      B. `{type: list, has_parts: [{type: list_item,
                                    value: str}, …]}`  — items with values
    We handle both. When we capture a list-shaped extension field, we do
    NOT recurse into its `has_parts` (would double-count the items).
    """
    stack = list(roots)
    while stack:
        node = stack.pop()
        if isinstance(node, list):
            stack.extend(node)
            continue
        if not isinstance(node, dict):
            continue

        ntype = node.get("type")
        nname = _node_name(node)
        is_ext_field = bool(nname) and bool(EXT_FIELD_PAT.match(normalize_field_name(nname)))
        consumed_as_list = False

        if is_ext_field:
            if ntype == "field":
                v = node.get("value")
                if v is not None:
                    hits.append({"name": nname, "kind": "field", "values": [str(v)]})
            elif ntype == "list":
                values = [str(v) for v in (node.get("values") or []) if v is not None]
                if not values:
                    # Form B: list_item children carry the scalar in `value`.
                    for part in node.get("has_parts") or []:
                        if isinstance(part, dict):
                            pv = part.get("value")
                            if pv is not None:
                                values.append(str(pv))
                if values:
                    hits.append({"name": nname, "kind": "list", "values": values})
                consumed_as_list = True

        if not consumed_as_list:
            parts = node.get("has_parts")
            if isinstance(parts, list):
                stack.extend(parts)


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
# Per-shard processing
# ---------------------------------------------------------------------------

def process_shard(shard_path: Path, targets: dict[str, dict], found: dict[str, dict],
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
            hits_raw: list[dict] = []
            walk_infoboxes(roots, hits_raw)

            hits_out: list[dict] = []
            for h in hits_raw:
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

    targets = load_target_qids(p1195_path)
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
            process_shard(local, targets, found)
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
        print(f"       matched so far: {len(found)} / {len(targets)}", flush=True)
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


if __name__ == "__main__":
    sys.exit(main())
