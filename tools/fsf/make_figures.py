"""Figures for the .fsf study → docs/assets/fsf/.

Provenance figures come from fsf_files+origin.csv (ready any time); content
figures come from data/derived/fsf_study/reports/ (need the judge run).

    python3 -m tools.fsf.make_figures
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
CSV = ROOT / "fsf_files+origin.csv"
STUDY = ROOT / "data" / "derived" / "fsf_study"
OUT = ROOT / "docs" / "assets" / "fsf"
BLUE, ORANGE, PURPLE = "#0b3d61", "#d1731f", "#5b3ea8"
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": .3,
                     "axes.axisbelow": True, "figure.dpi": 140})


def parse_origins():
    forge, origin = Counter(), Counter()
    if not CSV.exists():
        return forge, origin
    with CSV.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        seen = set()
        for row in r:
            if len(row) < 3 or row[0] in seen:
                continue
            seen.add(row[0])
            o = (parse_qs(urlparse(row[2]).query).get("origin_url") or [None])[0]
            if o:
                origin[o] += 1
                forge[urlparse(o).netloc] += 1
    return forge, origin


def load_verdicts():
    reps = [json.loads(open(p).read()) for p in glob.glob(str(STUDY / "reports" / "*.json"))]
    return reps


def barh(fname, title, pairs, color=BLUE, log=True, xlabel="contents"):
    pairs = pairs[::-1]
    fig, ax = plt.subplots(figsize=(7.6, max(2.6, .42 * len(pairs) + 1)))
    cols = color if isinstance(color, str) else color
    ax.barh([k for k, _ in pairs], [v for _, v in pairs],
            color=cols if isinstance(cols, str) else cols)
    for i, (_, v) in enumerate(pairs):
        ax.text(v, i, f" {v:,}", va="center", fontsize=8)
    if log:
        ax.set_xscale("log")
    ax.set_xlabel(xlabel + (" (log)" if log else "")); ax.set_title(title, fontweight="bold")
    fig.tight_layout(); fig.savefig(OUT / fname); plt.close(fig)
    print("wrote", fname)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    forge, origin = parse_origins()
    ntot = sum(origin.values())

    if forge:
        barh("fig_fsf_forges.png",
             f"Forge provenance — .fsf ({ntot:,} contents)", forge.most_common(9))

        def short(u):
            u = u.rstrip("/").replace(".git", "")
            p = u.split("/")
            return "/".join(p[-2:]) if len(p) >= 2 else u
        top = [(short(k), v) for k, v in origin.most_common(12)]
        fig, ax = plt.subplots(figsize=(8.2, 4.4))
        top_r = top[::-1]
        ax.barh([k for k, _ in top_r], [v for _, v in top_r], color=PURPLE)
        for i, (_, v) in enumerate(top_r):
            ax.text(v, i, f" {v:,}", va="center", fontsize=8)
        ax.set_xscale("log"); ax.set_xlabel("contents (log)")
        t1 = origin.most_common(1)[0]
        ax.set_title(f"Top repositories by .fsf content count\n"
                     f"({ntot:,} contents from {len(origin):,} repos; top = {round(100*t1[1]/ntot)}%)",
                     fontweight="bold", fontsize=10)
        fig.tight_layout(); fig.savefig(OUT / "fig_fsf_top_repos.png"); plt.close(fig)
        print("wrote fig_fsf_top_repos.png")

    # ---- content figures (need the judge run) ----
    reps = load_verdicts()
    V = lambda r: (r.get("judge") or {}).get("verdict") if isinstance(r.get("judge"), dict) else None
    judged = [r for r in reps if V(r)]
    if not judged:
        print("(no judged reports yet — content figures skipped)")
        return

    ct = Counter(V(r).get("content_type", "") for r in judged)
    barh("fig_fsf_content_type.png",
         f"Content type of .fsf files (n={len(judged)})",
         ct.most_common(8), color=BLUE, log=False, xlabel="contents")

    rel = Counter()
    for r in judged:
        for l in (V(r).get("related_languages") or []):
            rel[l.strip()] += 1
    barh("fig_fsf_related_languages.png",
         f"What .fsf relates to — related_languages (n={len(judged)} judged)",
         rel.most_common(10), color=ORANGE, log=True, xlabel="mentions")

    # FEAT sub-types (only the FEAT ones)
    feat = [r for r in judged if V(r).get("artifact_kind", "").startswith("fsl-")]
    if feat:
        lvl = Counter(V(r).get("feat_level", "") for r in feat)
        at = Counter(V(r).get("analysis_type", "") for r in feat)
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
        for ax, (title, c) in zip(axes, [("FEAT level", lvl), ("analysis type", at)]):
            items = c.most_common(6)[::-1]
            ax.barh([k for k, _ in items], [v for _, v in items], color=PURPLE)
            ax.set_title(title, fontweight="bold"); ax.set_xlabel("FEAT files")
        fig.suptitle(f"FSL FEAT sub-types (n={len(feat)})", fontweight="bold")
        fig.tight_layout(); fig.savefig(OUT / "fig_fsf_feat.png"); plt.close(fig)
        print("wrote fig_fsf_feat.png")

    # by-file (uniform) vs by-repo (diverse)
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
        keys = [k for k, _ in ct.most_common(6)]
        fig, ax = plt.subplots(figsize=(7.6, 4))
        y = range(len(keys)); h = .38
        for si, (fr, col, lab) in enumerate([("uniform", BLUE, "by-file (uniform)"),
                                             ("diverse", ORANGE, "by-repo (diverse)")]):
            c = Counter(V(r).get("content_type", "") for r in frames[fr])
            n = sum(c.values()) or 1
            off = (h/2) if si == 0 else -(h/2)
            ax.barh([i + off for i in y], [100 * c.get(k, 0) / n for k in keys], h,
                    color=col, label=f"{lab} (n={len(frames[fr])})")
        ax.set_yticks(list(y)); ax.set_yticklabels(keys, fontsize=8)
        ax.invert_yaxis(); ax.set_xlabel("% of judged"); ax.legend(fontsize=8)
        ax.set_title("Content type: by-file vs by-repo", fontweight="bold")
        fig.tight_layout(); fig.savefig(OUT / "fig_fsf_frames.png"); plt.close(fig)
        print("wrote fig_fsf_frames.png")


if __name__ == "__main__":
    main()
