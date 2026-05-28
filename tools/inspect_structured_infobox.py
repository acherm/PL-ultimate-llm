#!/usr/bin/env python3
"""Stream the wikimedia/structured-wikipedia enwiki shards and dump the
raw `infoboxes` JSON tree for a small set of target QIDs. Used to diagnose
why Phase 1's structured-tree walk is missing extensions some legacy
mwparserfromhell extractions found.

Output: data/derived/structured_infobox_inspect.json — pretty-printed map
of `qid → {label, raw_infoboxes_decoded, …}` so we can eyeball whether
the upstream tree really is flat (limitation) or whether we're failing
to descend a `has_parts` branch (fixable).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

sys.path.insert(0, str(Path(__file__).parent))
from fetch_structured_wikipedia import (  # noqa: E402
    REPO_ID, SHARD_RE, CACHE_DIR, PARQUET_COLUMNS,
    list_enwiki_shards, resolve_dataset_revision, _decode_infoboxes,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "derived" / "structured_infobox_inspect.json"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--targets", required=True,
                   help="Comma-separated QIDs to inspect (e.g. Q572649,Q300036)")
    p.add_argument("--out", default=str(OUT_PATH))
    args = p.parse_args()

    targets = set(args.targets.split(","))
    print(f"[inspect] target QIDs: {sorted(targets)}", flush=True)

    revision = resolve_dataset_revision()
    shards = list_enwiki_shards()
    print(f"[inspect] {len(shards)} shards available; revision={revision}", flush=True)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    found: dict[str, dict] = {}

    for i, shard_name in enumerate(shards, 1):
        if not targets:
            break
        print(f"[shard {i}/{len(shards)}] {shard_name}  remaining={len(targets)}",
              flush=True)
        try:
            local = Path(hf_hub_download(
                REPO_ID, shard_name, repo_type="dataset",
                revision=revision, cache_dir=str(CACHE_DIR),
            ))
        except Exception as exc:  # noqa: BLE001
            print(f"       download failed: {exc!r}", flush=True)
            continue

        try:
            pf = pq.ParquetFile(local)
            available = [c for c in PARQUET_COLUMNS if c in pf.schema_arrow.names]
            for batch in pf.iter_batches(columns=available, batch_size=1024):
                for row in batch.to_pylist():
                    me = row.get("main_entity") or {}
                    qid = me.get("identifier") if isinstance(me, dict) else None
                    if qid in targets:
                        found[qid] = {
                            "qid": qid,
                            "shard": shard_name,
                            "name": row.get("name"),
                            "url": row.get("url"),
                            "raw_infoboxes_column": row.get("infoboxes"),
                            "decoded_infoboxes": _decode_infoboxes(row.get("infoboxes")),
                        }
                        targets.discard(qid)
                        if not targets:
                            break
                if not targets:
                    break
        finally:
            # Free the shard regardless.
            try:
                real = local.resolve()
                if local.is_symlink():
                    local.unlink()
                if real.exists() and real.is_file():
                    real.unlink()
            except OSError:
                pass

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(found, indent=2, ensure_ascii=False) + "\n")
    print(f"[done] dumped {len(found)} target QIDs to {out_path}", flush=True)
    if targets:
        print(f"[warn] unmatched: {sorted(targets)}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
