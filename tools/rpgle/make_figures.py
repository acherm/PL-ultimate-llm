"""Figures for the `.rpgle` study → docs/assets/rpgle/.

Provenance figures come from rpgle_files+origins.csv (ready any time); content
figures come from data/derived/rpgle_study/reports/ (need the judge run).

    python3 -m tools.rpgle.make_figures
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "rpgle_files+origins.csv"
STUDY = ROOT / "data" / "derived" / "rpgle_study"
OUT = ROOT / "docs" / "assets" / "rpgle"
BLUE, ORANGE, GREEN = "#0b3d61", "#d1731f", "#2e7d32"
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": .3,
                     "axes.axisbelow": True, "figure.dpi": 140})


def parse_origins():
    forge, origin, seen = Counter(), Counter(), set()
    if not CSV.exists():
        return forge, origin
    with CSV.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) < 3 or row[0] in seen:
                continue
            seen.add(row[0])
            o = (parse_qs(urlparse(row[2]).query).get("origin_url") or [None])[0]
            if o:
                origin[o] += 1
                forge[urlparse(o).netloc] += 1
    return forge, origin


def barh(fname, title, pairs, color=BLUE, log=True, xlabel="contents"):
    pairs = pairs[::-1]
    fig, ax = plt.subplots(figsize=(7.8, max(2.6, .44 * len(pairs) + 1)))
    ax.barh([k for k, _ in pairs], [v for _, v in pairs], color=color)
    for i, (_, v) in enumerate(pairs):
        ax.text(v, i, f" {v:,}", va="center", fontsize=8)
    if log:
        ax.set_xscale("log")
    ax.set_xlabel(xlabel + (" (log)" if log else ""))
    ax.set_title(title, fontweight="bold", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / fname); plt.close(fig)
    print("wrote", fname)


def V(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    forge, origin = parse_origins()
    ntot = sum(origin.values())

    if forge:
        barh("fig_rpgle_forges.png", f"Forge provenance — .rpgle ({ntot:,} contents)",
             forge.most_common(8))

        def short(u):
            u = u.rstrip("/").replace(".git", "")
            p = u.split("/")
            return "/".join(p[-2:]) if len(p) >= 2 else u
        tr = [(short(k), v) for k, v in origin.most_common(12)]
        t1 = origin.most_common(1)[0]
        barh("fig_rpgle_top_repos.png",
             f"Top repositories by .rpgle content count\n"
             f"({ntot:,} contents from {len(origin):,} repos; top = {round(100*t1[1]/ntot)}%)",
             tr, color=GREEN)

    A = json.loads((STUDY / "analysis.json").read_text()) if (STUDY / "analysis.json").exists() else None
    if not A:
        print("(run tools.rpgle.analysis first — content figures skipped)")
        return
    frames = A["frames"]
    nj = frames[1]["n_judged"]

    # --- dialect across sampling frames (the headline frame effect) ---
    dial = ["fully-free", "hybrid-free", "fixed-format"]
    short = ["E1 by-file\n(n=%d)" % frames[0]["n_judged"],
             "E2 by-repo census\n(n=%d)" % frames[1]["n_judged"],
             "E1' minus tooling\n(n=%d)" % frames[2]["n_judged"],
             "E1'' dedup versions\n(n=%d)" % frames[3]["n_judged"]]
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    x = range(len(short)); w = .26
    for i, (d, col) in enumerate(zip(dial, [GREEN, ORANGE, BLUE])):
        ax.bar([j + (i - 1) * w for j in x], [f["source_format"].get(d, 0) for f in frames],
               w, label=d, color=col)
        for j in x:
            v = frames[j]["source_format"].get(d, 0)
            ax.text(j + (i - 1) * w, v + 1, f"{v}", ha="center", fontsize=7.5)
    ax.set_xticks(list(x)); ax.set_xticklabels(short, fontsize=8)
    ax.set_ylabel("% of judged files"); ax.legend(fontsize=8, ncol=3)
    ax.set_title("The RPG dialect you measure depends on the sampling frame",
                 fontweight="bold", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / "fig_rpgle_frames.png"); plt.close(fig)
    print("wrote fig_rpgle_frames.png")

    # --- tooling confound ---
    t, r = A["tooling_confound"]["tooling"], A["tooling_confound"]["rest"]
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    labels = ["fixed-format", "snippet/toy", "production-like"]
    tv = [t["source_format"].get("fixed-format", 0),
          t["maturity"].get("snippet", 0) + t["maturity"].get("toy-or-hello-world", 0),
          t["maturity"].get("production-like", 0)]
    rv = [r["source_format"].get("fixed-format", 0),
          r["maturity"].get("snippet", 0) + r["maturity"].get("toy-or-hello-world", 0),
          r["maturity"].get("production-like", 0)]
    y = range(len(labels)); h = .36
    ax.barh([i + h/2 for i in y], tv, h, color=ORANGE,
            label=f"3 RPG-parser repos (n={t['n_judged']}, {A['version_inflation']['tooling_repo_share_pct']}% of corpus)")
    ax.barh([i - h/2 for i in y], rv, h, color=BLUE, label=f"all other repos (n={r['n_judged']})")
    for i in y:
        ax.text(tv[i] + 1, i + h/2, f"{tv[i]}%", va="center", fontsize=8)
        ax.text(rv[i] + 1, i - h/2, f"{rv[i]}%", va="center", fontsize=8)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels); ax.invert_yaxis()
    ax.set_xlabel("% of judged files"); ax.legend(fontsize=7.5, loc="lower right")
    ax.set_title("Three grammar/interpreter test corpora drive the fixed-format signal",
                 fontweight="bold", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / "fig_rpgle_tooling.png"); plt.close(fig)
    print("wrote fig_rpgle_tooling.png")

    # --- what .rpgle relates to (by-repo census) ---
    rel = frames[1]["related_languages"]
    barh("fig_rpgle_related_languages.png",
         f"What .rpgle content relates to (by-repo census, n={nj})",
         [(k, v) for k, v in list(rel.items())[:8]], color=ORANGE, log=False,
         xlabel="% of judged files")

    # --- unit kind, by-repo census ---
    uk = frames[1]["unit_kind"]
    barh("fig_rpgle_unit_kind.png", f"Compilation unit kind (by-repo census, n={nj})",
         [(k, v) for k, v in list(uk.items())[:6]], color=GREEN, log=False,
         xlabel="% of judged files")


if __name__ == "__main__":
    main()
