"""Build docs/m_swh_study.md (and optionally the PDF) from tools/m/report/m_report.md.

The prose lives in `tools/m/report/m_report.md`; every number is resolved from the
study outputs at build time, so no figure is hand-copied:

  ⟪a:path/to/key|fmt⟫   a value in data/derived/m_study/analysis.json
  ⟪p:path|fmt⟫          … in population.json
  ⟪s:path|fmt⟫          … in population_signals.json
  ⟪T:name⟫              a table rendered by tools/m/report_tables.py (or tail_table below)
  ⟪X:name⟫              a derived value computed in `derived()` below

Paths use "/" (keys contain dots, e.g. `main.m`); `fmt` is a Python format spec
(default: the value as-is). The PDF follows the COBOL report's layout (US Letter,
contents page, shaded callouts).

    python3 -m tools.m.analysis && python3 -m tools.m.build_report --pdf
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from tools.m import report_tables as RT

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "m_study"
TEMPLATE = Path(__file__).parent / "report" / "m_report.md"
OUT = ROOT / "docs" / "m_swh_study.md"
PH = re.compile(r"⟪([apsTX]):([^|⟫]+)(?:\|([^⟫]+))?⟫")


def load():
    return {"a": json.loads((STUDY / "analysis.json").read_text()),
            "p": json.loads((STUDY / "population.json").read_text()),
            "s": json.loads((STUDY / "population_signals.json").read_text())}


def lookup(doc, path):
    for k in path.split("/"):
        doc = doc[k]
    return doc


def tail_table(A):
    rows = defaultdict(lambda: {"U": 0, "R": 0, "ex": []})
    for x in A["I_tail"]["tail"]:
        g = rows[x["judge"]]
        g[x["frame"]] += 1
        if len(g["ex"]) < 3:
            o = (x["origin"] or "").replace("https://", "")
            owner = o.split("/")[1] if "/" in o else o
            g["ex"].append(owner)
    order = ["mathematica-wolfram", "mumps-m", "magma", "mercury", "c-or-cpp", "other-programming-language",
             "not-code", "unknown"]
    out = ["| language (judge) | by file (of 1 000) | by repo (of 1 000) | e.g. repositories of |",
           "|---|---:|---:|---|"]
    for k in order + [k for k in rows if k not in order]:
        if k in rows:
            g = rows[k]
            out.append(f"| {k} | {g['U']} | {g['R']} | {', '.join(dict.fromkeys(g['ex']))} |")
    return "\n".join(out)


def octave3(A):
    d = A["D_octave"]
    cols = [d["judge_x_lexical_v2"], d["judge2_x_lexical_v2"], d["ours_x_lexical_v2"]]
    rows = ["| label × Octave-only syntax (comment/string-aware) | Sonnet 4.6 | Gemini 3.8 Flash | our rules v2 |",
            "|---|---:|---:|---:|"]
    for lab, key in (("`octave`, syntax present", "octave|lexical_octave=True"),
                     ("`octave`, **no** Octave-only syntax", "octave|lexical_octave=False"),
                     ("`matlab`, **with** Octave-only syntax", "matlab|lexical_octave=True")):
        rows.append(f"| {lab} | " + " | ".join(str(c.get(key, 0)) for c in cols) + " |")
    return "\n".join(rows)


def ppi_table(A):
    a = A["A_language"]

    def row(fr, name):
        c = fr["classes"]
        oc, ml = c["objective-c"], c["matlab-family"]
        return (f"| {name} | {fr['n_labelled']:,} + {fr['n_unlabelled']:,} | {oc['pct']:.1f} % "
                f"[{oc['ci'][0]:.1f}–{oc['ci'][1]:.1f}] | {oc['classical_ci'][0]:.1f}–{oc['classical_ci'][1]:.1f} | "
                f"{oc['width_ratio']:.2f} | {oc['lambda']:.2f} | {ml['pct']:.1f} % | {ml['width_ratio']:.2f} |")
    return "\n".join([
        "| frame | judged + free | Objective-C (PPI++) | judged-only CI | width ratio | λ | MATLAB (PPI++) | width ratio |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        row(a["ppi_by_file"], "by file (U)"), row(a["ppi_by_repo"], "by repo (R)")])


def derived(D):
    A = D["a"]
    a, b, c, fm = A["A_language"], A["B_what"], A["C_labellers"], A["C_labellers"]["failure_modes"]
    cost = A["cost"]
    pb, pr = a["ppi_by_file"]["classes"]["objective-c"], a["ppi_by_repo"]["classes"]["objective-c"]
    gain = 1 - (pb["width_ratio"] + pr["width_ratio"]) / 2
    port = A["D_octave"]["portability"]
    g = A["G_reclassifier"]
    oc_hand = lambda f: b[f]["per_language"]["objective-c"]["provenance_kind"]["hand-written"]["pct"]  # noqa: E731
    frac = lambda k: f"{fm[k]['k']} / {fm[k]['n']:,} ({100 * fm[k]['k'] / fm[k]['n']:.1f} %)"  # noqa: E731
    parsed = sum(v["parsed"] for v in cost.values() if isinstance(v, dict))
    j1, j2, ji = (cost["anthropic__claude-sonnet-4.6"], cost["google__gemini-3.8-flash"],
                  cost["anthropic__claude-sonnet-4.6+ind"])
    return {
        "tail_pct": f"{100 - a['by_file_coarse']['objective-c']['pct'] - a['by_file_coarse']['matlab-family']['pct']:.1f}",
        "oc_nonhand_file": f"{100 - oc_hand('by_file'):.0f}",
        "oc_nonhand_repo": f"{100 - oc_hand('by_repo'):.0f}",
        "spend": (f"Sonnet ${j1['usd']:.2f} ({j1['calls']:,} calls), Gemini ${j2['usd']:.2f} ({j2['calls']:,}, "
                  f"{j2['failed_retried']} empty responses retried), anchoring ablation ${ji['usd']:.2f} "
                  f"({ji['calls']}) — **${cost['total_usd']:.2f}** for {parsed:,} verdicts"),
        "spend_short": f"${cost['total_usd']:.2f} for {parsed:,} LLM verdicts; everything else ran locally",
        "pyg": frac("pygments_matlab_as_objc") + " of MATLAB files",
        "ling": frac("linguist_abstain_on_matlab") + " of MATLAB files",
        "synid_text": frac("synid_text_on_objc"),
        "synid_nc": frac("synid_nc_text_on_objc"),
        "retest_lang": f"{100 * A['E_anchoring']['self_agreement_by_field']['language']:.1f}",
        "retest_mat": f"{100 * A['E_anchoring']['self_agreement_by_field']['maturity']:.1f}",
        "port_s": f"{100 * port['judge'].get('matlab-specific', 0) / port['n_by_file']:.0f}",
        "port_g": f"{100 * port['judge2'].get('portable-matlab-octave', 0) / port['n_by_file']:.0f}",
        "port_lex": f"{100 * port['lexical_matlab_only_features'] / port['n_by_file']:.0f}",
        "v1_heldout": f"{100 * g['v1_judge']['coarse_accuracy']:.1f}",
        "v2_gain": f"{100 * (g['v2_judge']['coarse_accuracy'] - g['v1_judge']['coarse_accuracy']):.1f}",
        "ppi_table": ppi_table(A),
        "ppi_lambda": f"{(pb['lambda'] + pr['lambda']) / 2:.1f}",
        "ppi_gain": f"{100 * gain:.0f}",
        "ppi_eff": f"{1 / (1 - gain) ** 2:.1f}",
        "t_nonhand": f"{A['I_tail']['top_mostly_not_hand_written']}",
        **prereg(A),
    }


def prereg(A):
    a, fm, f = A["A_language"], A["C_labellers"]["failure_modes"], A["F_intermodel"]
    big = a["by_file_coarse"]["objective-c"]["pct"] + a["by_file_coarse"]["matlab-family"]["pct"]
    tail_langs = [l for l in ("mathematica-wolfram", "mumps-m", "magma", "mercury", "c-or-cpp",
                              "other-programming-language", "not-code") if a["by_file"].get(l) or a["by_repo"].get(l)]
    oc_hand = A["B_what"]["by_file"]["per_language"]["objective-c"]["provenance_kind"]["hand-written"]["pct"]
    pc = lambda k: 100 * fm[k]["k"] / fm[k]["n"]  # noqa: E731
    st = 100 * (fm["synid_text_all"]["k"] + fm["synid_unresolved_all"]["k"]) / fm["synid_text_all"]["n"]
    d = A["D_octave"]
    r1, r2 = d["judge_x_lexical"], d["judge_x_lexical_v2"]
    g2 = d["judge2_x_lexical_v2"]
    e = A["E_anchoring"]
    return {
        "h1": f"{big:.1f} %; rest spans {len(tail_langs)}",
        "h2": f"{a['by_file_coarse']['objective-c']['pct']:.1f} % vs {a['by_repo_coarse']['objective-c']['pct']:.1f} %",
        "h3": f"{100 - oc_hand:.1f} %",
        "h4": f"{pc('linguist_abstain_all'):.1f} % · {pc('pygments_matlab_as_objc'):.1f} % · {st:.1f} %",
        "h5": (f"regex: {r1.get('octave|lexical_octave=False', 0)} vs {r1.get('matlab|lexical_octave=True', 0)}; "
               f"lexer: {r2.get('octave|lexical_octave=False', 0)} vs {r2.get('matlab|lexical_octave=True', 0)} "
               f"(Gemini {g2.get('octave|lexical_octave=False', 0)} vs {g2.get('matlab|lexical_octave=True', 0)})"),
        "h6": f"{e['agree_with_ours_blind']} % blind vs {e['agree_with_ours_shown']} % shown",
        "h7": (f"κ {f['language']['kappa']:.2f} · {f['provenance_kind']['kappa']:.2f} · "
               f"{f['maturity']['kappa']:.2f}"),
    }


def render(D):
    RT.A = D["a"]
    X = derived(D)
    tables = {"tail": lambda: tail_table(D["a"]), "octave3": lambda: octave3(D["a"])}

    def sub(m):
        src, key, fmt = m.group(1), m.group(2), m.group(3)
        if src == "X":
            return X[key]
        if src == "T":
            return tables[key]() if key in tables else getattr(RT, key)()
        v = lookup(D[src], key)
        return format(v, fmt) if fmt else str(v)
    doc = PH.sub(sub, TEMPLATE.read_text(encoding="utf-8"))
    left = sorted(set(re.findall(r"⟪[^⟫]*⟫", doc)))
    if left:
        raise SystemExit(f"unresolved placeholders: {left}")
    return doc


def pdf():
    subprocess.run(["pandoc", OUT.name, "-o", OUT.with_suffix(".pdf").name, "--pdf-engine=lualatex", "--toc",
                    "--toc-depth=2", "-H", "assets/callout.tex", "-H", "assets/m/pdf_header.tex",
                    "--resource-path=.", "-V", "papersize=letter", "-V", "geometry:margin=1in",
                    "-V", "colorlinks=true", "-V", "linkcolor=black", "-V", "urlcolor=blue"],
                   cwd=OUT.parent, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true", help="also build docs/m_swh_study.pdf (pandoc + lualatex)")
    args = ap.parse_args()
    OUT.write_text(render(load()), encoding="utf-8")
    print(f"wrote {OUT} ({len(OUT.read_text().splitlines())} lines)")
    if args.pdf:
        pdf()
        print(f"wrote {OUT.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
