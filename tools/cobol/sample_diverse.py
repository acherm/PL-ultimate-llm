"""Origin-diverse sample across .cbl + .CBL: at most ONE content per origin
repo, so no single project (e.g. the 110k-file WBC GitLab fixture, or ORCA)
dominates. Maximises repository / provenance coverage.

Uses the graph-derived origin CSVs (cbl_file+origin.csv, CBL_files+origins.csv).
Output worklist matches run_study's schema (+ origin/forge/corpus columns):
    python3 -m tools.cobol.sample_diverse --n 1000 --seed 5
"""

from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .common import STUDY_DIR
from .origins import CSV_FILES, _parse_browse_url


def load_pool() -> dict[str, list[dict]]:
    """origin_url -> [{sha, name, corpus, forge, path}] across both CSVs."""
    by_origin: dict[str, list[dict]] = defaultdict(list)
    seen_sha: set[str] = set()
    for path in CSV_FILES:
        if not path.exists():
            continue
        corpus = ".CBL" if "CBL_files" in path.name else ".cbl"
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 3:
                    continue
                sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
                rec = _parse_browse_url(row[2])
                if not sha or not rec or sha in seen_sha:
                    continue
                seen_sha.add(sha)
                by_origin[rec["origin"]].append({
                    "sha": sha, "name": row[1], "corpus": corpus,
                    "origin": rec["origin"], "forge": rec["forge"],
                    "path": rec.get("path")})
    return by_origin


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--out", default=str(STUDY_DIR / "worklist_div.csv"))
    args = ap.parse_args()

    by_origin = load_pool()
    origins = sorted(by_origin)
    print(f"pool: {sum(len(v) for v in by_origin.values())} unique contents "
          f"across {len(origins)} distinct origins")

    rng = random.Random(args.seed)
    rng.shuffle(origins)
    picks = []
    for origin in origins:
        if len(picks) >= args.n:
            break
        cand = by_origin[origin]
        picks.append(rng.choice(cand))  # one content from this origin

    from collections import Counter
    corp = Counter(p["corpus"] for p in picks)
    forge = Counter(p["forge"] for p in picks)
    print(f"sampled {len(picks)} contents from {len(picks)} distinct origins")
    print(f"  corpus: {dict(corp)}")
    print(f"  forges: {dict(forge.most_common(8))}")

    out = Path(args.out)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["swhid", "sha1_git", "name", "source_csv",
                    "n_filenames", "origin", "forge"])
        for p in picks:
            w.writerow([f"swh:1:cnt:{p['sha']}", p["sha"], p["name"],
                        p["corpus"], 1, p["origin"], p["forge"]])
    print(f"wrote {len(picks)} -> {out}")


if __name__ == "__main__":
    main()
