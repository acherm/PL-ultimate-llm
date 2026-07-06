"""Render figures for the COBOL-in-SWH study report.

Reads the study artefacts (worklists + per-content reports + summaries) and
writes PNGs to docs/assets/cobol/. Reproducible:
    python3 -m tools.cobol.make_figures
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "cobol_study"
OUT = ROOT / "docs" / "assets" / "cobol"

UP = "#0b3d61"   # .CBL / Main
LO = "#d1731f"   # .cbl / LC
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": .3,
                     "axes.axisbelow": True, "figure.dpi": 140})


def verdicts(worklist: str, ext: str | None):
    """Yield judged verdict dicts for a worklist, optionally filtered by ext."""
    rows = list(csv.DictReader((STUDY / worklist).open()))
    out = []
    gated = 0
    for r in rows:
        if ext and not r["name"].endswith(ext):
            continue
        p = STUDY / "reports" / f"{r['sha1_git']}.json"
        if not p.exists():
            continue
        j = json.loads(p.read_text()).get("judge")
        if not isinstance(j, dict):
            continue
        if j.get("verdict"):
            out.append(j["verdict"])
        elif j.get("skipped"):
            gated += 1
    return out, gated


def pct(counter: Counter, keys: list[str], n: int) -> list[float]:
    return [100 * counter.get(k, 0) / n if n else 0 for k in keys]


def grouped_barh(fname, title, keys, a_vals, b_vals, a_lab, b_lab, xlabel="% of judged"):
    fig, ax = plt.subplots(figsize=(7.2, max(2.6, .52 * len(keys) + 1)))
    y = range(len(keys))
    h = .38
    ax.barh([i + h/2 for i in y], a_vals, height=h, color=UP, label=a_lab)
    ax.barh([i - h/2 for i in y], b_vals, height=h, color=LO, label=b_lab)
    ax.set_yticks(list(y)); ax.set_yticklabels(keys)
    ax.invert_yaxis(); ax.set_xlabel(xlabel); ax.set_title(title, fontweight="bold")
    for i in y:
        if a_vals[i] > 0.5:
            ax.text(a_vals[i] + .6, i + h/2, f"{a_vals[i]:.0f}", va="center", fontsize=8)
        if b_vals[i] > 0.5:
            ax.text(b_vals[i] + .6, i - h/2, f"{b_vals[i]:.0f}", va="center", fontsize=8)
    ax.legend(loc="lower right"); ax.set_xlim(0, max(a_vals + b_vals) * 1.18 + 2)
    fig.tight_layout(); fig.savefig(OUT / fname); plt.close(fig)
    print("wrote", fname)


def dist(verds, path):
    dom = Counter(v.get("purpose", {}).get("domain", "") for v in verds)
    fam = Counter(v.get("dialect", {}).get("family", "") for v in verds)
    mat = Counter(v.get("maturity", "") for v in verds)
    ptype = Counter(v.get("purpose", {}).get("program_type", "") for v in verds)
    return dom, fam, mat, ptype


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Clean extension-split: .CBL rows of the union sample vs .cbl-only sample.
    up_v, up_g = verdicts("worklist_scaled.csv", ".CBL")
    lo_v, lo_g = verdicts("worklist_lc.csv", ".cbl")
    nU, nL = len(up_v), len(lo_v)
    up_dom, up_fam, up_mat, up_pt = dist(up_v, None)
    lo_dom, lo_fam, lo_mat, lo_pt = dist(lo_v, None)
    A, B = f".CBL (n={nU})", f".cbl (n={nL})"

    # Fig 1 — domain (headline)
    dkeys = ["healthcare-medical", "education-tutorial", "demo-example",
             "retail-commerce", "banking-finance", "accounting-erp",
             "test-suite", "utility-tooling", "insurance", "manufacturing-logistics"]
    grouped_barh("fig_domain.png", "Business domain by extension casing",
                 dkeys, pct(up_dom, dkeys, nU), pct(lo_dom, dkeys, nL), A, B)

    # Fig 2 — dialect family
    fkeys = ["gnucobol", "ibm-mainframe", "micro-focus", "acucobol",
             "rm-cobol", "fujitsu-nec", "unknown"]
    grouped_barh("fig_dialect.png", "Dialect family by extension casing",
                 fkeys, pct(up_fam, fkeys, nU), pct(lo_fam, fkeys, nL), A, B)

    # Fig 3 — maturity
    mkeys = ["production-like", "student-exercise", "snippet", "toy-or-hello-world"]
    grouped_barh("fig_maturity.png", "Maturity by extension casing",
                 mkeys, pct(up_mat, mkeys, nU), pct(lo_mat, mkeys, nL), A, B)

    # Fig 4 — program type
    pkeys = ["batch", "online-cics", "subprogram", "demo", "test"]
    grouped_barh("fig_program_type.png", "Program type by extension casing",
                 pkeys, pct(up_pt, pkeys, nU), pct(lo_pt, pkeys, nL), A, B)

    # Fig 5 — feature prevalence (Main vs LC, from indicators CSVs, over text files)
    def feat(csvpath):
        rows = [r for r in csv.DictReader((STUDY / csvpath).open()) if r["is_text"] == "True"]
        n = len(rows)
        f = {
            "COPY": sum(int(r["copy_count"]) > 0 for r in rows),
            "CALL": sum(int(r["call_count"]) > 0 for r in rows),
            "EXEC CICS": sum(r["has_exec_cics"] == "True" for r in rows),
            "COMP-3": sum(int(r["comp3_count"]) > 0 for r in rows),
            "EXEC SQL": sum(r["has_exec_sql"] == "True" for r in rows),
        }
        return {k: 100 * v / n for k, v in f.items()}, n
    fm, nm = feat("indicators_scaled.csv")
    fl, nl = feat("indicators_lc.csv")
    fkeys2 = list(fm)
    grouped_barh("fig_features.png",
                 "Feature prevalence (mechanical, over text files)",
                 fkeys2, [fm[k] for k in fkeys2], [fl[k] for k in fkeys2],
                 f"Main (n={nm})", f".cbl (n={nl})", xlabel="% of text files")

    # Fig 6 — LOC distribution (log-x histogram)
    def loc(csvpath):
        return [max(1, int(r["code_lines"])) for r in csv.DictReader((STUDY / csvpath).open())
                if r["is_text"] == "True"]
    import numpy as np
    lm, ll = loc("indicators_scaled.csv"), loc("indicators_lc.csv")
    bins = np.logspace(0, np.log10(max(lm + ll) + 1), 26)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.hist(lm, bins=bins, alpha=.6, color=UP, label=f"Main (n={len(lm)}, med {int(np.median(lm))})")
    ax.hist(ll, bins=bins, alpha=.6, color=LO, label=f".cbl (n={len(ll)}, med {int(np.median(ll))})")
    ax.set_xscale("log"); ax.set_xlabel("code lines (log scale)"); ax.set_ylabel("files")
    ax.set_title("Program size distribution", fontweight="bold"); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "fig_loc.png"); plt.close(fig)
    print("wrote fig_loc.png")

    # Fig 7 — contamination / non-COBOL rate
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    labels = ["WBC_*_FOO synthetic\n(corpus-wide, of union)",
              ".cbl non-COBOL\n(gated in sample)",
              ".CBL non-COBOL\n(gated in sample)"]
    vals = [100 * 109999 / 276831, 100 * lo_g / (lo_g + nL), 100 * up_g / (up_g + nU)]
    cols = ["#888888", LO, UP]
    bars = ax.barh(labels, vals, color=cols)
    for b, v in zip(bars, vals):
        ax.text(v + .6, b.get_y() + b.get_height()/2, f"{v:.0f}%", va="center", fontsize=9)
    ax.set_xlabel("% non-COBOL / synthetic"); ax.invert_yaxis()
    ax.set_title("Contamination of the COBOL extension space", fontweight="bold")
    ax.set_xlim(0, max(vals) * 1.2)
    fig.tight_layout(); fig.savefig(OUT / "fig_contamination.png"); plt.close(fig)
    print("wrote fig_contamination.png")

    # Fig 8 — reclassifier vs division-gate (if the experiment has run)
    evalp = STUDY / "reclassify_eval.json"
    if evalp.exists():
        ev = json.loads(evalp.read_text())
        h, g = ev["heuristic_vs_oracle"], ev["division_gate_vs_oracle"]
        mkeys = ["precision", "recall", "f1", "accuracy"]
        fig, ax = plt.subplots(figsize=(7.2, 3.4))
        x = range(len(mkeys)); w = .38
        ax.bar([i - w/2 for i in x], [h[k] for k in mkeys], w, color=UP,
               label="reclassifier (content)")
        ax.bar([i + w/2 for i in x], [g[k] for k in mkeys], w, color="#999999",
               label="division-gate baseline")
        for i, k in enumerate(mkeys):
            ax.text(i - w/2, h[k] + .01, f"{h[k]:.2f}", ha="center", fontsize=8)
            ax.text(i + w/2, g[k] + .01, f"{g[k]:.2f}", ha="center", fontsize=8)
        ax.set_xticks(list(x)); ax.set_xticklabels(mkeys)
        ax.set_ylim(0, 1.15); ax.set_ylabel("score (vs LLM oracle)")
        ax.set_title(f"Reclassifier vs division-gate on is-COBOL (n={ev['n']})",
                     fontweight="bold")
        ax.legend(loc="lower left")
        fig.tight_layout(); fig.savefig(OUT / "fig_reclassify.png"); plt.close(fig)
        print("wrote fig_reclassify.png")

    # Fig 9 — archive-scale contamination (1K uniform random, content-based)
    est = STUDY / "corpus_estimate.jsonl"
    if est.exists():
        from .reclassify import COBOL_LABELS
        recs = [json.loads(l) for l in est.read_text().splitlines() if l.strip()]
        n = len(recs)
        cnt = Counter(r["label"] for r in recs)
        order = sorted(cnt, key=lambda k: (k not in COBOL_LABELS, -cnt[k]))
        vals = [100 * cnt[k] / n for k in order]
        cols = [UP if k in COBOL_LABELS else LO for k in order]
        n_non = sum(v for k, v in zip(order, vals) if k not in COBOL_LABELS)
        fig, ax = plt.subplots(figsize=(7.6, 3.8))
        bars = ax.barh(order, vals, color=cols)
        for b, v in zip(bars, vals):
            if v > 0.3:
                ax.text(v + .4, b.get_y() + b.get_height()/2, f"{v:.1f}%",
                        va="center", fontsize=8)
        ax.invert_yaxis(); ax.set_xlabel("% of contents")
        ax.set_xlim(0, max(vals) * 1.15 + 3)
        ax.set_title(f"What is in the .cbl/.CBL space? (n={n} uniform random)\n"
                     f"{n_non:.0f}% non-COBOL  ·  {100-n_non:.0f}% COBOL",
                     fontweight="bold", fontsize=11)
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=UP, label="COBOL"),
                           Patch(color=LO, label="non-COBOL / contamination")],
                  loc="lower right")
        fig.tight_layout(); fig.savefig(OUT / "fig_corpus_1k.png"); plt.close(fig)
        print("wrote fig_corpus_1k.png")

    print(f"\next-split: .CBL judged={nU} gated={up_g} | .cbl judged={nL} gated={lo_g}")


if __name__ == "__main__":
    main()
