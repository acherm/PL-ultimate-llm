"""Descriptive statistics of the `.rpgle` population (rpgle_files+origins.csv).

Establishes what we are sampling FROM, so the representativeness of each frame
can be judged. Writes data/derived/rpgle_study/population.json.

    python3 -m tools.rpgle.population
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "rpgle_files+origins.csv"
OUT = ROOT / "data" / "derived" / "rpgle_study" / "population.json"


def main():
    rows = 0
    by_sha: dict[str, dict] = {}
    with CSV.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) < 3:
                continue
            rows += 1
            sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
            origin = (parse_qs(urlparse(row[2]).query).get("origin_url") or [None])[0]
            if sha and sha not in by_sha:
                by_sha[sha] = {"name": row[1], "origin": origin}

    with_origin = {s: r for s, r in by_sha.items() if r["origin"]}
    by_origin: dict[str, list] = defaultdict(list)
    for s, r in with_origin.items():
        by_origin[r["origin"]].append(s)

    sizes = sorted((len(v) for v in by_origin.values()), reverse=True)
    n = sum(sizes)
    cum, r80 = 0, 0
    for i, s in enumerate(sizes, 1):
        cum += s
        if cum >= 0.8 * n:
            r80 = i
            break

    top = sorted(by_origin.items(), key=lambda kv: -len(kv[1]))[:10]
    forges = Counter(urlparse(o).netloc for o in by_origin)
    forge_contents = Counter()
    for o, v in by_origin.items():
        forge_contents[urlparse(o).netloc] += len(v)
    names = Counter(r["name"] for r in by_sha.values())

    pop = {
        "csv_rows": rows,
        "unique_contents": len(by_sha),
        "unique_filenames": len(names),
        "contents_with_origin": len(with_origin),
        "unique_origins": len(by_origin),
        "contents_per_repo": {
            "median": statistics.median(sizes), "mean": round(n / len(sizes), 1),
            "max": sizes[0], "p90": sizes[int(.1 * len(sizes))],
            "repos_with_1": sum(1 for s in sizes if s == 1),
        },
        "concentration": {
            "top1_pct": round(100 * sizes[0] / n, 1),
            "top10_pct": round(100 * sum(sizes[:10]) / n, 1),
            "repos_for_80pct": r80,
            "repos_for_80pct_share": round(100 * r80 / len(sizes), 1),
        },
        "top_repos": [{"origin": o, "contents": len(v),
                       "pct": round(100 * len(v) / n, 1)} for o, v in top],
        "forges_by_repo": dict(forges.most_common(8)),
        "forges_by_content": dict(forge_contents.most_common(8)),
        "top_filenames": [{"name": k, "n": v} for k, v in names.most_common(12)],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pop, indent=2), encoding="utf-8")
    print(json.dumps(pop, indent=2)[:2200])
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
