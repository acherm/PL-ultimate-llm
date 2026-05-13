#!/usr/bin/env python3
"""Re-classify everything under `samples/`, relocate to the right `<pl_id>/`.

Use after improving `tools/pl_classify.Classifier` (e.g., the pl_id consolidation
that collapsed `pl/zig` and `pl/zig-programming-language`). Existing sample
directories under `samples/unclassified/` get re-classified; metadata.json
gets updated to the new prediction.

This does NOT re-fetch bytes (cheap) or re-mine the SWH parquet (slow).
"""

from __future__ import annotations
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"

sys.path.insert(0, str(ROOT / "tools"))
from pl_classify import Classifier  # noqa: E402


def main() -> int:
    cls = Classifier()
    moved = updated = skipped = errors = 0
    for sha_dir in SAMPLES.glob("*/*/*"):
        if not sha_dir.is_dir():
            continue
        # samples/pl/<slug>/<sha>/ → parts ends with ('pl', '<slug>', '<sha>')
        # samples/unclassified/<sha>/ has only 2 levels deep — skip this 3-level glob.
        meta_path = sha_dir / "metadata.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            errors += 1
            continue
        filename = meta.get("filename") or ""
        code_path = sha_dir / filename
        if not code_path.exists():
            errors += 1
            continue
        ext = meta.get("ext") or ""
        if not ext:
            skipped += 1
            continue
        try:
            data = code_path.read_bytes()
        except Exception:
            errors += 1
            continue
        res = cls.classify_bytes(ext, data)
        new_pl_id = res.pl_id
        current_pl_id = meta.get("predicted_pl_id") or ""

        if not new_pl_id:
            skipped += 1
            continue
        if new_pl_id == current_pl_id:
            skipped += 1
            continue

        # Relocate: new dir at samples/<new_pl_id>/<sha>/
        target_parent = SAMPLES / new_pl_id
        target_dir = target_parent / sha_dir.name
        if target_dir.exists():
            print(f"  collision (target exists), skipping: {sha_dir} -> {target_dir}")
            skipped += 1
            continue
        target_parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(sha_dir), str(target_dir))

        # Update metadata in new location.
        new_meta_path = target_dir / "metadata.json"
        meta["predicted_pl_id"] = new_pl_id
        meta["predicted_via"] = res.via
        meta["predicted_confidence"] = res.confidence
        meta["predicted_heuristic_id"] = res.matched_heuristic_id
        meta["predicted_matches_claim"] = meta.get("predicted_matches_claim", "")
        new_meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        moved += 1
        if moved % 20 == 0:
            print(f"  moved {moved} so far…")

    # Also walk samples/unclassified/<sha>/ (2-deep) since glob('*/*/*') misses it.
    unclassified_dir = SAMPLES / "unclassified"
    if unclassified_dir.exists():
        for sha_dir in unclassified_dir.iterdir():
            if not sha_dir.is_dir():
                continue
            meta_path = sha_dir / "metadata.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                errors += 1
                continue
            filename = meta.get("filename") or ""
            code_path = sha_dir / filename
            if not code_path.exists() or not (ext := meta.get("ext")):
                skipped += 1
                continue
            try:
                data = code_path.read_bytes()
            except Exception:
                errors += 1
                continue
            res = cls.classify_bytes(ext, data)
            if not res.pl_id or res.pl_id == "unclassified":
                skipped += 1
                continue
            target_dir = SAMPLES / res.pl_id / sha_dir.name
            if target_dir.exists():
                skipped += 1
                continue
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(sha_dir), str(target_dir))
            meta["predicted_pl_id"] = res.pl_id
            meta["predicted_via"] = res.via
            meta["predicted_confidence"] = res.confidence
            meta["predicted_heuristic_id"] = res.matched_heuristic_id
            (target_dir / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            moved += 1

    # Clean empty unclassified dir if appropriate.
    if unclassified_dir.exists() and not any(unclassified_dir.iterdir()):
        unclassified_dir.rmdir()

    print(f"Done. moved={moved}, updated={updated}, skipped={skipped}, errors={errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
