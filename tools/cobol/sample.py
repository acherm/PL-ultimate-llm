"""Sample unique COBOL contents from the SWH-extracted CSVs.

Each CSV row is ``swh:1:cnt:<sha1_git>,/Filename``. The same content
(sha1_git) can appear many times under different filenames; we dedup by
sha1_git so the study spends its budget on *distinct* files.

Usage:
    python3 -m tools.cobol.sample --n 100 --seed 42 \
        --csv CBL_files.csv --csv cbl_files_lowercase.csv \
        --out data/derived/cobol_study/worklist.csv
"""

from __future__ import annotations

import argparse
import csv
import random
import re
from pathlib import Path

from .common import CSV_DIR, STUDY_DIR, ensure_dirs, sha1_git_of


def read_rows(csv_path: Path) -> list[tuple[str, str]]:
    """Return (swhid, filename) rows from a SWH-extracted CSV."""
    rows: list[tuple[str, str]] = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            rows.append((row[0].strip(), row[1].strip()))
    return rows


def dedup_by_content(rows: list[tuple[str, str]],
                     source: str) -> dict[str, dict]:
    """sha1_git -> {swhid, sha1_git, name, source_csv, n_filenames}.

    Keeps the first filename seen for each content and counts how many
    distinct filenames pointed at it (a small popularity signal).
    """
    out: dict[str, dict] = {}
    for swhid, name in rows:
        sha = sha1_git_of(swhid)
        if not sha:
            continue
        rec = out.get(sha)
        if rec is None:
            out[sha] = {
                "swhid": f"swh:1:cnt:{sha}",
                "sha1_git": sha,
                "name": name,
                "source_csv": source,
                "filenames": {name},
            }
        else:
            rec["filenames"].add(name)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Sample unique COBOL contents.")
    ap.add_argument("--n", type=int, default=100, help="number of samples")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed (reproducible)")
    ap.add_argument("--csv", action="append", default=None,
                    help="CSV filename under COBOL-SWH-extracted (repeatable)")
    ap.add_argument("--out", default=str(STUDY_DIR / "worklist.csv"))
    ap.add_argument("--exclude-name", default=None,
                    help="drop contents whose filename matches this regex "
                         "(e.g. 'WBC_.*_FOO' to skip synthetic placeholder files)")
    args = ap.parse_args()

    ensure_dirs()
    csv_names = args.csv or ["CBL_files.csv", "cbl_files_lowercase.csv"]
    exclude_re = re.compile(args.exclude_name) if args.exclude_name else None

    merged: dict[str, dict] = {}
    for name in csv_names:
        path = (CSV_DIR / name) if not Path(name).is_absolute() else Path(name)
        rows = read_rows(path)
        ded = dedup_by_content(rows, name)
        for sha, rec in ded.items():
            if sha in merged:
                merged[sha]["filenames"] |= rec["filenames"]
            else:
                merged[sha] = rec
        print(f"{name}: {len(rows)} rows -> {len(ded)} unique contents")

    print(f"merged unique contents across CSVs: {len(merged)}")

    if exclude_re is not None:
        before = len(merged)
        merged = {sha: rec for sha, rec in merged.items()
                  if not any(exclude_re.search(n) for n in rec["filenames"])}
        print(f"excluded {before - len(merged)} contents matching "
              f"/{args.exclude_name}/ -> {len(merged)} remain")

    keys = sorted(merged)  # deterministic order before seeding
    rng = random.Random(args.seed)
    pick = rng.sample(keys, min(args.n, len(keys)))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["swhid", "sha1_git", "name", "source_csv", "n_filenames"])
        for sha in pick:
            rec = merged[sha]
            w.writerow([rec["swhid"], rec["sha1_git"], rec["name"],
                        rec["source_csv"], len(rec["filenames"])])
    print(f"wrote {len(pick)} samples -> {out_path}")


if __name__ == "__main__":
    main()
