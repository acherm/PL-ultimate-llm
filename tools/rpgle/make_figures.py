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

    reps = [json.loads(open(p).read()) for p in glob.glob(str(STUDY / "reports" / "*.json"))]
    judged = [r for r in reps if V(r)]
    if not judged:
        print("(no judged reports yet — content figures skipped)")
        return

    # source format — the RPG dialect axis
    sf = Counter(V(r).get("source_format", "") for r in judged)
    barh("fig_rpgle_source_format.png",
         f"RPG source format (n={len(judged)} judged)",
         sf.most_common(6), color=BLUE, log=False, xlabel="files")

    # what it relates to
    rel = Counter()
    for r in judged:
        for l in (V(r).get("related_languages") or []):
            rel[l.strip()] += 1
    barh("fig_rpgle_related_languages.png",
         f"What .rpgle relates to — related_languages (n={len(judged)})",
         rel.most_common(10), color=ORANGE, log=True, xlabel="mentions")

    # unit kind
    uk = Counter(V(r).get("unit_kind", "") for r in judged)
    barh("fig_rpgle_unit_kind.png", f"Compilation unit kind (n={len(judged)})",
         uk.most_common(7), color=GREEN, log=False, xlabel="files")

    # by-file (uniform) vs by-repo (census)
    wl = {r["sha1_git"]: r for r in csv.DictReader((STUDY / "worklist_all.csv").open())}
    frames = defaultdict(list)
    for r in judged:
        row = wl.get(r["sha1_git"])
        if not row:
            continue
        if row.get("in_uniform") == "1":
            frames["uniform"].append(r)
        if row.get("in_diverse") == "1":
            frames["diverse"].append(r)
    if frames.get("uniform") and frames.get("diverse"):
        fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
        for ax, (title, key, keys) in zip(axes, [
            ("Unit kind", "unit_kind",
             ["program", "copybook-prototype-header", "procedure-or-service-program",
              "module", "test"]),
            ("Maturity", "maturity",
             ["production-like", "library-quality", "student-exercise",
              "toy-or-hello-world", "snippet"])]):
            y = range(len(keys)); h = .38
            for si, (fr, col, lab) in enumerate([("uniform", BLUE, "by-file"),
                                                 ("diverse", ORANGE, "by-repo (census)")]):
                c = Counter(V(r).get(key, "") for r in frames[fr])
                n = sum(c.values()) or 1
                off = (h/2) if si == 0 else -(h/2)
                ax.barh([i + off for i in y], [100 * c.get(k, 0) / n for k in keys], h,
                        color=col, label=f"{lab} (n={len(frames[fr])})")
            ax.set_yticks(list(y)); ax.set_yticklabels(keys, fontsize=7)
            ax.invert_yaxis(); ax.set_xlabel("% of judged"); ax.legend(fontsize=7)
            ax.set_title(title, fontweight="bold")
        fig.suptitle("File-level vs project-level (.rpgle)", fontweight="bold")
        fig.tight_layout(); fig.savefig(OUT / "fig_rpgle_frames.png"); plt.close(fig)
        print("wrote fig_rpgle_frames.png")


if __name__ == "__main__":
    main()
