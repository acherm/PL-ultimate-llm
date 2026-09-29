"""Build docs/m_swh_study.md (and optionally the PDF) from tools/m/report/*.md + analysis.json.

The prose lives in `tools/m/report/`; every number and table is substituted from
`data/derived/m_study/analysis.json` (placeholders look like ⟪NAME⟫), so the
report can be regenerated after any re-analysis and no figure is hand-copied.

    python3 -m tools.m.analysis && python3 -m tools.m.build_report --pdf
"""
import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SP = Path(__file__).parent / "report"
sys.path.insert(0, str(ROOT))
from tools.m import report_tables as RT  # noqa: E402

A = json.loads((ROOT / "data/derived/m_study/analysis.json").read_text())
RT.A = A

parts = ["header.md", "part1.md", "part2a.md", "part2b.md", "part2c.md", "part2d.md", "appendix_a.md", "appendix_bc.md"]
doc = "\n\n".join((SP / p).read_text().rstrip() for p in parts) + "\n"

cost = A["cost"]
j1 = cost["anthropic__claude-sonnet-4.6"]
j1i = cost["anthropic__claude-sonnet-4.6+ind"]
j2 = cost["google__gemini-3.8-flash"]
n = A["n"]
a = A["A_language"]
fc, rc = a["by_file_coarse"], a["by_repo_coarse"]
bf = A["B_what"]


def pc(d, k):
    return d.get(k, {}).get("pct", 0.0)


def tail_table():
    rows = defaultdict(lambda: {"U": 0, "R": 0, "ex": []})
    for x in A["I_tail"]["tail"]:
        g = rows[x["judge"]]
        g[x["frame"]] += 1
        if len(g["ex"]) < 3:
            o = (x["origin"] or "").replace("https://", "")
            g["ex"].append(f"`{x['name'][:28]}` ({o.split('/')[1] if '/' in o else o})")
    order = ["mathematica-wolfram", "mumps-m", "magma", "mercury", "c-or-cpp", "other-programming-language",
             "not-code", "unknown"]
    out = ["| language (judge) | by file (of 1,000) | by repo (of 1,000) | examples (repository owner) |",
           "|---|---:|---:|---|"]
    for k in order + [k for k in rows if k not in order]:
        if k in rows:
            g = rows[k]
            out.append(f"| {k} | {g['U']} | {g['R']} | {'; '.join(g['ex'])} |")
    return "\n".join(out)


D = A["D_octave"]
s2, g2, o2 = D["judge_x_lexical_v2"], D["judge2_x_lexical_v2"], D["ours_x_lexical_v2"]
nd = A["L_near_duplicates"]["main.m"]
pb = a["ppi_by_file"]
pr = a["ppi_by_repo"]


def ppi_text():
    def row(fr, name):
        c = fr["classes"]
        return (f"| {name} | {fr['n_labelled']} + {fr['n_unlabelled']} | "
                f"{c['objective-c']['pct']:.1f}% [{c['objective-c']['ci'][0]:.1f}–{c['objective-c']['ci'][1]:.1f}] | "
                f"{c['objective-c']['classical_ci'][0]:.1f}–{c['objective-c']['classical_ci'][1]:.1f} | "
                f"{c['objective-c']['width_ratio']:.2f} | {c['objective-c']['lambda']:.2f} | "
                f"{c['matlab-family']['pct']:.1f}% | {c['matlab-family']['width_ratio']:.2f} |")
    return "\n".join([
        "| frame | judged + cheap-only | Objective-C (PPI++) | judged-only 95% CI | width ratio | λ | MATLAB (PPI++) | width ratio |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        row(pb, "by file (U)"), row(pr, "by repo (R)")])


gain = 1 - (pb["classes"]["objective-c"]["width_ratio"] + pr["classes"]["objective-c"]["width_ratio"]) / 2
K = A["K_prereg"]
subs = {
    "⟪BOTTOM⟫": (SP / "bottom.md").read_text().strip(),
    "⟪U_FETCHED⟫": f"{n['U_used']:,} of 10,000 drawn", "⟪R_FETCHED⟫": f"{n['R_used']:,} of 3,000 drawn",
    "⟪J1_COST⟫": f"${j1['usd']:.2f} for {j1['calls']:,} calls",
    "⟪J2_COST⟫": f"${j2['usd']:.2f} for {j2['calls']:,} calls",
    "⟪SPEND⟫": (f"Primary judge ${j1['usd']:.2f} ({j1['calls']:,} calls, incl. frame T), anchoring ablation "
                f"${j1i['usd']:.2f} ({j1i['calls']} calls), second judge ${j2['usd']:.2f} ({j2['calls']:,} calls, "
                f"{j2['failed_retried']} empty responses retried once) — **${cost['total_usd']:.2f} in total**, "
                f"{sum(v['parsed'] for k, v in cost.items() if isinstance(v, dict)):,} parsed verdicts. "
                f"Everything else ran locally for free."),
    "⟪FRAMES_TABLE⟫": RT.frames(), "⟪TAIL_TABLE⟫": tail_table(), "⟪PROVENANCE_TABLE⟫": RT.provenance(),
    "⟪NEARDUP⟫": (f"in our sample, {nd['distinct_contents']} distinct `main.m` contents collapse to "
                  f"{nd['distinct_without_comments']} once `//` comment lines are removed"),
    "⟪ND_MAIN_N⟫": str(nd["distinct_contents"]), "⟪ND_MAIN_K⟫": str(nd["distinct_without_comments"]),
    "⟪ND_MAIN_C⟫": f"{nd['largest_cluster']} ({100 * nd['largest_cluster'] / nd['distinct_contents']:.0f}%)",
    "⟪ND_APP_C⟫": str(A["L_near_duplicates"]["AppDelegate.m"]["largest_cluster"]),
    "⟪ND_APP_N⟫": str(A["L_near_duplicates"]["AppDelegate.m"]["distinct_contents"]),
    "⟪TOP_TABLE⟫": RT.top(), "⟪LABELLERS_TABLE⟫": RT.labellers(), "⟪PERCLASS_TABLE⟫": RT.per_class(),
    "⟪OCT_S_TT⟫": str(s2.get("octave|lexical_octave=True", 0)), "⟪OCT_S_TF⟫": str(s2.get("octave|lexical_octave=False", 0)),
    "⟪OCT_S_FT⟫": str(s2.get("matlab|lexical_octave=True", 0)),
    "⟪OCT_G_TT⟫": str(g2.get("octave|lexical_octave=True", 0)), "⟪OCT_G_TF⟫": str(g2.get("octave|lexical_octave=False", 0)),
    "⟪OCT_G_FT⟫": str(g2.get("matlab|lexical_octave=True", 0)),
    "⟪OCT_O_TT⟫": str(o2.get("octave|lexical_octave=True", 0)), "⟪OCT_O_TF⟫": str(o2.get("octave|lexical_octave=False", 0)),
    "⟪OCT_O_FT⟫": str(o2.get("matlab|lexical_octave=True", 0)),
    "⟪INTERMODEL_TABLE⟫": RT.intermodel(), "⟪RECLASS_TABLE⟫": RT.reclass(),
    "⟪POOL⟫": f"{pb['n_unlabelled']:,} by file, {pr['n_unlabelled']:,} by repo",
    "⟪PPI_TEXT⟫": ppi_text(), "⟪PPI_GAIN⟫": f"about {100 * gain:.0f}%",
    "⟪PPI_LAMBDA⟫": f"{(pb['classes']['objective-c']['lambda'] + pr['classes']['objective-c']['lambda']) / 2:.1f}",
    "⟪PPI_EFF⟫": f"{1 / (1 - gain) ** 2:.1f}",
    "⟪MAPPING_TABLE⟫": RT.mapping(),
    **{f"⟪{h}⟫": K[h]["observed"] for h in K},
}
for k, v in subs.items():
    doc = doc.replace(k, v)
left = sorted({doc[i:doc.index("⟫", i) + 1] for i in range(len(doc)) if doc.startswith("⟪", i)})
if left:
    print("UNFILLED:", left)
(ROOT / "docs/m_swh_study.md").write_text(doc, encoding="utf-8")
print("wrote docs/m_swh_study.md", len(doc.splitlines()), "lines")

ap = argparse.ArgumentParser()
ap.add_argument("--pdf", action="store_true", help="also build docs/m_swh_study.pdf (pandoc + xelatex)")
if ap.parse_args().pdf:
    subprocess.run(["pandoc", "m_swh_study.md", "-o", "m_swh_study.pdf", "--pdf-engine=xelatex",
                    "-H", "assets/callout.tex", "-H", "assets/m/tables.tex", "--resource-path=.",
                    "-V", "geometry:margin=2cm", "-V", "fontsize=10pt", "-V", "colorlinks=true",
                    "-V", "mainfont=STIXGeneral", "-V", "monofont=Menlo", "-V", "monofontoptions=Scale=0.82"],
                   cwd=ROOT / "docs", check=True)
    print("wrote docs/m_swh_study.pdf")
