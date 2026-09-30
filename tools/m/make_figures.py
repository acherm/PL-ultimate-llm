"""Figures for the `.m` study → docs/assets/m/.

Reads data/derived/m_study/{analysis.json, population.json, name_popularity.json}
and the Parquet population for the concentration curve (optional: skipped if
DuckDB is unavailable in this interpreter).

Colour follows the entity, in the fixed order of the reference categorical palette
(validated: adjacent CVD ΔE ≥ 9.1; slots 3–5 are < 3:1 on the surface, so every
figure carries direct labels).

    python3 -m tools.m.make_figures
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "m_study"
OUT = ROOT / "docs" / "assets" / "m"

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = {"objective-c": "#2a78d6", "matlab-family": "#eb6834", "mathematica-wolfram": "#1baf7a",
          "other-code": "#eda100", "not-code": "#e87ba4"}
NEUTRAL = "#b9b8b3"
LABEL = {"objective-c": "Objective-C", "matlab-family": "MATLAB / Octave",
         "mathematica-wolfram": "Wolfram", "other-code": "other code", "not-code": "not code"}

plt.rcParams.update({
    "font.size": 9.5, "font.family": "sans-serif", "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": .6,
    "axes.axisbelow": True, "figure.dpi": 150, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 10.5, "axes.titlelocation": "left",
})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig_frames(a):
    """Share of the two big languages, per sampling frame, with 95% CIs."""
    A = a["A_language"]
    frames = [
        ("by file (U, judged)", A["by_file_coarse"], "ci"),
        ("by file, PPI (U ≤ 2000)", A["ppi_by_file"]["classes"], "ci"),
        ("by path (U re-weighted)", A["by_path_coarse"], "ci"),
        ("by repo (U re-weighted)", A["by_repo_reweighted_coarse"], "ci"),
        ("by repo (R, judged)", A["by_repo_coarse"], "ci"),
        ("by repo, PPI (R ≤ 2000)", A["ppi_by_repo"]["classes"], "ci"),
    ]
    fig, ax = plt.subplots(figsize=(7.6, 3.5))
    for off, cls in ((-.14, "objective-c"), (.14, "matlab-family")):
        for i, (_, d, _k) in enumerate(frames):
            v = d.get(cls)
            if not v or v.get("pct") != v.get("pct"):
                continue
            y = len(frames) - 1 - i + off
            lo, hi = v["ci"]
            ax.plot([lo, hi], [y, y], color=SERIES[cls], lw=2, solid_capstyle="round")
            ax.plot(v["pct"], y, "o", ms=6.5, color=SERIES[cls], mec=SURFACE, mew=1.5)
            ax.text(hi + 1, y, f"{v['pct']:.0f}%", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(frames)))
    ax.set_yticklabels([f[0] for f in frames][::-1])
    ax.set_xlim(0, 100)
    ax.set_xlabel("share of the frame (%)  ·  dot = estimate, line = 95% CI")
    ax.grid(axis="y", visible=False)
    ax.set_title("Which language is a .m file? It depends on what you count")
    for cls in ("objective-c", "matlab-family"):
        ax.plot([], [], "o-", color=SERIES[cls], label=LABEL[cls])
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False, fontsize=8.5)
    ax.set_title("Which language is a .m file? It depends on what you count")
    save(fig, "fig_m_frames.png")


def fig_labellers(a):
    """Each labeller vs the two-judge consensus: correct / wrong / abstain."""
    acc = a["C_labellers"]["vs_consensus"]
    order = ["judge", "judge2", "ours", "linguist", "synid_nc", "synid", "pygments"]
    names = {"judge": "LLM judge (Sonnet 4.6)*", "judge2": "LLM judge 2 (Gemini 3.8 Flash)*",
             "ours": "our reclassifier v2", "linguist": "Linguist .m heuristics",
             "synid": "SWH Synid (default)", "synid_nc": "SWH Synid (no comment strategy)",
             "pygments": "Pygments guess_lexer"}
    rows = [(k, acc[k]) for k in order if k in acc]
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    for i, (k, v) in enumerate(rows[::-1]):
        n = v["n"]
        ok = 100 * v["accuracy_all"]
        ab = v["abstain_pct"]
        bad = max(0.0, 100 - ok - ab)
        left = 0
        for w, col, lab in ((ok, SERIES["objective-c"], "agrees"), (bad, SERIES["matlab-family"], "disagrees"),
                            (ab, NEUTRAL, "abstains / 'Text'")):
            if w > 0:
                ax.barh(i, w, left=left, color=col, height=.62, edgecolor=SURFACE, linewidth=1.2)
            left += w
        ax.text(101, i, f"{ok:.1f}% · {bad:.1f}% · {ab:.1f}%", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([names[k] for k, _ in rows[::-1]])
    ax.set_xlim(0, 128)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("% of consensus items (coarse language)   *consensus = the two judges agree")
    ax.grid(axis="y", visible=False)
    ax.set_title("Seven labellers against the two-judge consensus")
    ax.legend(handles=[Patch(color=SERIES["objective-c"], label="agrees"),
                       Patch(color=SERIES["matlab-family"], label="disagrees"),
                       Patch(color=NEUTRAL, label="abstains / answers 'Text'")],
              loc="upper center", frameon=False, fontsize=8, ncol=3, bbox_to_anchor=(.45, -0.22))
    save(fig, "fig_m_labellers.png")


def fig_kappa(a):
    pw = a["C_labellers"]["pairwise_coarse"]
    labs = ["judge", "judge2", "ours", "linguist", "synid_nc", "synid", "pygments"]
    labs = [l for l in labs if l in pw]
    M = [[pw[x].get(y, {}).get("kappa", float("nan")) for y in labs] for x in labs]
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("blue", ["#cde2fb", "#6da7ec", "#2a78d6", "#184f95", "#0d366b"])
    im = ax.imshow(M, cmap=cmap, vmin=0.6, vmax=1.0)
    for i in range(len(labs)):
        for j in range(len(labs)):
            v = M[i][j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color="#ffffff" if v >= .74 else INK)
    ax.set_xticks(range(len(labs)))
    ax.set_yticks(range(len(labs)))
    ax.set_xticklabels(labs, rotation=40, ha="right")
    ax.set_yticklabels(labs)
    ax.grid(False)
    ax.set_title("Pairwise Cohen's κ (coarse language, abstention = its own label)")
    fig.colorbar(im, ax=ax, fraction=.046, pad=.04)
    save(fig, "fig_m_kappa.png")


def fig_provenance(a):
    B = a["B_what"]
    kinds = ["hand-written", "ide-or-framework-template", "vendored-third-party", "tool-generated",
             "decompiled-or-dumped"]
    kl = {"hand-written": "hand-written", "ide-or-framework-template": "IDE / framework template",
          "vendored-third-party": "vendored library", "tool-generated": "tool-generated",
          "decompiled-or-dumped": "decompiled / dumped"}
    groups = [("Objective-C · by file", B["by_file"]["per_language"]["objective-c"]),
              ("Objective-C · by repo", B["by_repo"]["per_language"]["objective-c"]),
              ("MATLAB · by file", B["by_file"]["per_language"]["matlab"]),
              ("MATLAB · by repo", B["by_repo"]["per_language"]["matlab"])]
    cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
    fig, ax = plt.subplots(figsize=(7.6, 2.9))
    for i, (g, d) in enumerate(groups[::-1]):
        left = 0
        pk = d["provenance_kind"]
        for k, c in zip(kinds, cols):
            w = pk.get(k, {}).get("pct", 0)
            if w:
                ax.barh(i, w, left=left, color=c, height=.62, edgecolor=SURFACE, linewidth=1.2)
                if w >= 7:
                    ax.text(left + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=7.5,
                            color="#ffffff" if c in ("#2a78d6",) else INK)
            left += w
        ax.text(101, i, f"n={d['n']}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels([g for g, _ in groups[::-1]])
    ax.set_xlim(0, 110)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("% of files of that language (judge)")
    ax.set_title("How the file came to exist")
    ax.legend(handles=[Patch(color=c, label=kl[k]) for k, c in zip(kinds, cols)],
              loc="upper center", bbox_to_anchor=(.45, -0.3), ncol=5, frameon=False, fontsize=7.5)
    save(fig, "fig_m_provenance.png")


def fig_names():
    npop = json.loads((STUDY / "name_popularity.json").read_text())
    top = sorted(npop.items(), key=lambda kv: -kv[1]["repos"])[:16]
    objc = {"AppDelegate.m", "main.m", "ViewController.m", "MainViewController.m", "LoginViewController.m",
            "DetailViewController.m", "Tests.m", "SceneDelegate.m", "RootViewController.m",
            "HomeViewController.m", "MasterViewController.m", "GeneratedPluginRegistrant.m"}
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    for i, (n, d) in enumerate(top[::-1]):
        cls = "objective-c" if n in objc else ("matlab-family" if n != "test.m" else "other-code")
        ax.barh(i, d["repos"], color=SERIES[cls], height=.62)
        ax.text(d["repos"] * 1.08, i, f"{d['repos']:,} repos", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels([n for n, _ in top[::-1]], fontsize=8)
    ax.set_xscale("log")
    ax.set_xlim(1e4, 3e6)
    ax.set_xlabel("distinct repositories containing a file of that name (log)")
    ax.grid(axis="y", visible=False)
    ax.set_title("The most replicated .m file names in Software Heritage")
    ax.legend(handles=[Patch(color=SERIES["objective-c"], label="Xcode template / iOS"),
                       Patch(color=SERIES["matlab-family"], label="Coursera ML course exercise"),
                       Patch(color=SERIES["other-code"], label="generic name")],
              loc="lower right", frameon=False, fontsize=8)
    save(fig, "fig_m_names.png")


def fig_concentration():
    sig = json.loads((STUDY / "population_signals.json").read_text())
    pts = sig["lorenz"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(xs, ys, color=SERIES["objective-c"], lw=2)
    ax.plot([0, 100], [0, 100], color=GRID, lw=1, ls="--")
    for p in (1, 10):
        v = min(pts, key=lambda q: abs(q[0] - p))[1]
        ax.plot(p, v, "o", ms=6, color=SERIES["objective-c"], mec=SURFACE, mew=1.5)
        ax.text(p * 1.3, v - 7, f"top {p}% of repos → {v:.0f}% of contents", fontsize=8, color=INK2)
    ax.set_xscale("log")
    ax.set_xlim(min(x for x in xs if x > 0), 100)
    ax.set_ylim(0, 100)
    ticks = [t for t in (0.001, 0.01, 0.1, 1, 10, 100) if t >= min(x for x in xs if x > 0)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}%" for t in ticks])
    ax.set_xlabel("% of repositories, largest first (log)")
    ax.set_ylabel("% of .m contents")
    ax.set_title(f"{sig['repos']:,} repositories; the largest holds {sig['largest_repo_pct']:.2f}% of .m contents")
    save(fig, "fig_m_concentration.png")


FRAME_COL = {"by_file": "#4a3aa7", "by_repo": "#1baf7a"}   # frames, distinct from the language colours


def fig_languages(a):
    """Every language/format under .m, by file and by repo, on a log scale (the polysemy picture)."""
    A = a["A_language"]
    order = ["objective-c", "matlab", "octave", "mathematica-wolfram", "mumps-m", "magma", "mercury",
             "c-or-cpp", "other-programming-language", "not-code", "limbo", "muf"]
    names = {"objective-c": "Objective-C", "matlab": "MATLAB", "octave": "Octave (Octave-only syntax)",
             "mathematica-wolfram": "Wolfram / Mathematica", "mumps-m": "MUMPS (M)", "magma": "Magma*",
             "mercury": "Mercury", "c-or-cpp": "C*", "other-programming-language": "other languages*",
             "not-code": "not code*", "limbo": "Limbo", "muf": "MUF"}
    fig, ax = plt.subplots(figsize=(7.6, 4.1))
    NONE_X = 0.045
    for off, key, lab in ((-.17, "by_file", "by file (U, n = 1,000)"), (.17, "by_repo", "by repo (R, n = 1,000)")):
        d, col = A[key], FRAME_COL[key]
        for i, lang in enumerate(order):
            y = len(order) - 1 - i + off
            v = d.get(lang)
            if not v or not v["n"]:
                ax.plot(NONE_X, y, marker="x", ms=5, mew=1.4, color=col)
                continue
            lo, hi = max(v["ci"][0], 0.06), v["ci"][1]
            ax.plot([lo, hi], [y, y], color=col, lw=1.6, alpha=.5, solid_capstyle="round")
            ax.plot(v["pct"], y, "o", ms=6, color=col, mec=SURFACE, mew=1.2)
            ax.text(hi * 1.15, y, f"{v['n']}", va="center", fontsize=7, color=INK2)
        ax.plot([], [], "o-", color=col, label=lab)
    ax.plot([], [], "x", color=INK2, label="none observed")
    ax.axvline(0.07, color=GRID, lw=.8)
    ax.set_xscale("log")
    ax.set_xlim(0.035, 150)
    ax.set_xticks([0.1, 1, 10, 100])
    ax.set_xticklabels(["0.1%", "1%", "10%", "100%"])
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([names[l] for l in order][::-1])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("share of judged files (log) · line = 95% CI · number = files")
    ax.set_title("What is in the .m space? Two languages and a long tail")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.text(0.01, -0.02, "* claimed by no source in our extension→language mapping", fontsize=7.5, color=INK2)
    save(fig, "fig_m_languages.png")


def main():
    a = json.loads((STUDY / "analysis.json").read_text())
    fig_languages(a)
    fig_frames(a)
    fig_labellers(a)
    fig_kappa(a)
    fig_provenance(a)
    fig_names()
    fig_concentration()


if __name__ == "__main__":
    main()
