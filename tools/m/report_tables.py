"""Render the `.m` report's tables from analysis.json (so no number is hand-copied).

    python3 -m tools.m.report_tables            # prints every table as Markdown
    python3 -m tools.m.report_tables frames     # one table
"""

from __future__ import annotations

import json
import sys

from tools.m.data import STUDY

A = None
COARSE = ["objective-c", "matlab-family", "mathematica-wolfram", "other-code", "not-code"]
NAMES = {"objective-c": "Objective-C", "matlab-family": "MATLAB / Octave", "mathematica-wolfram": "Wolfram",
         "other-code": "other code", "not-code": "not code"}
LAB = {"judge": "Sonnet 4.6 (judge)", "judge2": "Gemini 3.8 Flash (judge)",
       "ours": "our rules v2", "ours_v1": "our rules v1 (frozen)",
       "linguist": "Linguist heuristics", "pygments": "Pygments",
       "synid": "SWH Synid (default)", "synid_nc": "SWH Synid (no `comment`)"}


def ci(v):
    return f"{v['pct']:.1f}% [{v['ci'][0]:.1f}–{v['ci'][1]:.1f}]"


def frames():
    a = A["A_language"]
    cols = [("by file (U, judged)", a["by_file_coarse"], A["n"]["U_judged"]),
            ("by file, PPI", a["ppi_by_file"]["classes"], f"{a['ppi_by_file']['n_labelled']}+{a['ppi_by_file']['n_unlabelled']}"),
            ("by path (U reweighted)", a["by_path_coarse"], "n_eff"),
            ("by repo (U reweighted)", a["by_repo_reweighted_coarse"], "n_eff"),
            ("by repo (R, judged)", a["by_repo_coarse"], A["n"]["R_judged"]),
            ("by repo, PPI", a["ppi_by_repo"]["classes"], f"{a['ppi_by_repo']['n_labelled']}+{a['ppi_by_repo']['n_unlabelled']}")]
    out = ["| language | " + " | ".join(c[0] for c in cols) + " |", "|---|" + "---:|" * len(cols)]
    for c in COARSE:
        cells = []
        for _, d, _n in cols:
            v = d.get(c)
            cells.append(ci(v) if v and v.get("pct") == v.get("pct") else "0")
        out.append(f"| {NAMES[c]} | " + " | ".join(cells) + " |")
    ns = []
    for name, d, n in cols:
        if n == "n_eff":
            n = f"n_eff≈{next(iter(d.values()))['n_eff']}"
        ns.append(str(n))
    out.append("| *n* | " + " | ".join(ns) + " |")
    return "\n".join(out)


def fine(frame="by_file"):
    d = A["A_language"][frame]
    return "\n".join(["| language (judge) | n | % [95% CI] |", "|---|---:|---:|"] +
                     [f"| {k} | {v['n']} | {ci(v)} |" for k, v in d.items()])


def labellers():
    acc = A["C_labellers"]["vs_consensus"]
    ds = A["C_labellers"]["dawid_skene"]["accuracy"]
    out = ["| labeller | agrees | disagrees | abstains | accuracy when it answers | Dawid–Skene accuracy |",
           "|---|---:|---:|---:|---:|---:|"]
    for k in ("judge", "judge2", "ours", "ours_v1", "linguist", "synid_nc", "synid", "pygments"):
        if k not in acc:
            continue
        v = acc[k]
        if k in ("judge", "judge2"):
            out.append(f"| {LAB[k]} | *defines the consensus* | | | | {100 * ds[k]:.1f}% |")
            continue
        ok = 100 * v["accuracy_all"]
        bad = max(0.0, 100 - ok - v["abstain_pct"])
        out.append(f"| {LAB[k]} | {ok:.1f}% | {bad:.1f}% | {v['abstain_pct']:.1f}% | "
                   f"{100 * v['accuracy_answered']:.1f}% | {100 * ds[k]:.1f}% |" if k in ds else
                   f"| {LAB[k]} | {ok:.1f}% | {bad:.1f}% | {v['abstain_pct']:.1f}% | {100 * v['accuracy_answered']:.1f}% | — |")
    return "\n".join(out)


def per_class():
    acc = A["C_labellers"]["vs_consensus"]
    out = ["| labeller | " + " | ".join(f"{NAMES[c]} R" for c in COARSE[:3]) + " | other-code R | not-code R |",
           "|---|" + "---:|" * 5]
    for k in ("ours", "ours_v1", "linguist", "synid_nc", "synid", "pygments"):
        if k not in acc:
            continue
        pc = acc[k]["per_class"]
        out.append(f"| {LAB[k]} | " + " | ".join(
            f"{pc[c]['recall']:.2f} ({pc[c]['support']})" for c in COARSE) + " |")
    return "\n".join(out)


def intermodel():
    f = A["F_intermodel"]
    rows = ["| field | agreement | Cohen's κ |", "|---|---:|---:|"]
    for k in ("language_coarse", "language", "is_programming_language", "content_type", "unit_kind",
              "provenance_kind", "matlab_dialect", "domain", "maturity", "confidence"):
        if k in f:
            rows.append(f"| `{k}` | {100 * f[k]['agree']:.1f}% | {f[k]['kappa']:.2f} |")
    return "\n".join(rows)


def reclass():
    g = A["G_reclassifier"]
    rows = ["| rules | scored on | n | fine accuracy | coarse accuracy |", "|---|---|---:|---:|---:|"]
    for k, lab in (("v1_judge_tuning", "v1 · tuning split vs judge"), ("v2_judge_tuning", "v2 · tuning split vs judge (in-sample)"),
                   ("v1_judge", "v1 · held-out vs judge (prospective)"), ("v2_judge", "v2 · held-out vs judge"),
                   ("v1_consensus", "v1 · held-out vs consensus"), ("v2_consensus", "v2 · held-out vs consensus")):
        if k in g:
            v = g[k]
            rows.append(f"| {lab.split(' · ')[0]} | {lab.split(' · ')[1]} | {v['n']} | {100 * v['fine_accuracy']:.1f}% | {100 * v['coarse_accuracy']:.1f}% |")
    return "\n".join(rows)


def provenance():
    b = A["B_what"]
    kinds = ["hand-written", "ide-or-framework-template", "vendored-third-party", "tool-generated",
             "decompiled-or-dumped", "unknown"]
    rows = ["| provenance kind | by file | by repo | Objective-C by file | Objective-C by repo | MATLAB by file | MATLAB by repo |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    for k in kinds:
        cells = [b["by_file"]["provenance_kind"].get(k), b["by_repo"]["provenance_kind"].get(k),
                 b["by_file"]["per_language"]["objective-c"]["provenance_kind"].get(k),
                 b["by_repo"]["per_language"]["objective-c"]["provenance_kind"].get(k),
                 b["by_file"]["per_language"]["matlab"]["provenance_kind"].get(k),
                 b["by_repo"]["per_language"]["matlab"]["provenance_kind"].get(k)]
        if not any(cells):
            continue
        rows.append(f"| {k} | " + " | ".join(f"{c['pct']:.1f}%" if c else "—" for c in cells) + " |")
    return "\n".join(rows)


def what(field):
    b = A["B_what"]
    keys = list(dict.fromkeys(list(b["by_file"][field]) + list(b["by_repo"][field])))
    rows = [f"| `{field}` | by file | by repo |", "|---|---:|---:|"]
    for k in keys:
        f, r = b["by_file"][field].get(k), b["by_repo"][field].get(k)
        rows.append(f"| {k} | {ci(f) if f else '—'} | {ci(r) if r else '—'} |")
    return "\n".join(rows)


def mapping():
    h = A["H_mapping"]
    rows = ["| language | claimed in `ext_claim.csv` by | by file | by repo |", "|---|---|---:|---:|"]
    for r in h["rows"]:
        if not r["claimed_by"] and r["by_file_n"] == 0 and r["by_repo_n"] == 0:
            continue
        cb = ", ".join(sorted(set(x.split(":")[0] for x in r["claimed_by"]))) or "**— (unclaimed)**"
        rows.append(f"| {r['language']} | {cb} | {r['by_file_n']} ({r['by_file_pct']}%) | {r['by_repo_n']} ({r['by_repo_pct']}%) |")
    return "\n".join(rows)


def tail():
    t = A["I_tail"]["tail"]
    rows = ["| frame | file | judge | detail | judge 2 | ours v2 | origin |", "|---|---|---|---|---|---|---|"]
    for x in t:
        o = (x["origin"] or "").replace("https://", "")
        rows.append(f"| {x['frame']} | `{x['name'][:34]}` | {x['judge']} | {(x['detail'] or '')[:60]} | "
                    f"{x['judge2'] or '—'} | {x['ours']} | {o[:48]} |")
    return "\n".join(rows)


def top():
    rows = ["| repository | `.m` contents | % | what the 4 sampled files are (judge) |", "|---|---:|---:|---|"]
    for t in A["I_tail"]["top_repos"]:
        s = t["sampled"]
        desc = "; ".join(sorted({f"{x['language']}/{x['provenance_kind']}" for x in s})) if s else "—"
        det = s[0]["detail"] if s else ""
        if len(det) > 72:
            det = det[:72].rsplit(" ", 1)[0] + "…"
        rows.append(f"| {t['origin'].replace('https://', '')} | {t['contents']:,} | {t['pct']} | {desc} — {det} |")
    return "\n".join(rows)


def octave():
    d = A["D_octave"]
    return "\n".join(["| judge × lexical Octave markers | files |", "|---|---:|"] +
                     [f"| {k.replace('|', ' · ')} | {v} |" for k, v in sorted(d["judge_x_lexical"].items())])


def main():
    global A
    A = json.loads((STUDY / "analysis.json").read_text())
    which = sys.argv[1:] or ["frames", "fine", "labellers", "per_class", "intermodel", "reclass",
                             "provenance", "mapping", "octave", "top", "tail"]
    for w in which:
        print(f"\n<!-- {w} -->")
        print(globals()[w]())


if __name__ == "__main__":
    main()


def _p(d, *keys):
    for k in keys:
        d = (d or {}).get(k)
    return d


def composition():
    """Q2 comparison table, by frame (COBOL-report style)."""
    b = A["B_what"]
    kappa = A["F_intermodel"]

    def row(label, field, keys, note=""):
        cells = []
        for fr in ("by_file", "by_repo"):
            v = sum((_p(b, fr, field, k, "pct") or 0) for k in keys)
            cells.append(("<1%" if v < 1 else f"{v:.0f}%") if v else "—")
        return f"| {label}{note} | {cells[0]} | {cells[1]} |"

    rows = ["| | **by file (U)** | **by repo (R)** |", "|---|---:|---:|",
            row("hand-written", "provenance_kind", ["hand-written"]),
            row("IDE / framework template", "provenance_kind", ["ide-or-framework-template"]),
            row("tool-generated", "provenance_kind", ["tool-generated"]),
            row("vendored third-party library", "provenance_kind", ["vendored-third-party"]),
            row("decompiled / dumped", "provenance_kind", ["decompiled-or-dumped"]),
            row("class implementation (ObjC / `classdef`)", "unit_kind", ["class-implementation"]),
            row("MATLAB function file", "unit_kind", ["function-file"]),
            row("script", "unit_kind", ["script"]),
            row("test", "unit_kind", ["test"]),
            row("domain: iOS/macOS app or library", "domain", ["mobile-desktop-app", "mobile-library-framework"]),
            row("domain: numerical / signal / ML / control / engineering", "domain",
                ["numerical-scientific", "signal-image-processing", "machine-learning-data", "control-robotics",
                 "engineering-simulation"]),
            row("maturity: research code", "maturity", ["research-code"], "†"),
            row("maturity: student exercise", "maturity", ["student-exercise"], "†"),
            row("maturity: toy or snippet", "maturity", ["toy-or-hello-world", "snippet"], "†"),
            f"| median lines | {b['by_file']['median_lines']:.0f} | {b['by_repo']['median_lines']:.0f} |"]
    return "\n".join(rows) + (f"\n\n*† `maturity` is the least reliable field (two-judge κ "
                              f"{kappa['maturity']['kappa']:.2f}, §4.4); read it as indicative.*")


def per_language():
    b = A["B_what"]
    cols = [("Objective-C", "by_file", "objective-c"), ("Objective-C", "by_repo", "objective-c"),
            ("MATLAB/Octave", "by_file", "matlab"), ("MATLAB/Octave", "by_repo", "matlab")]
    head = "| | " + " | ".join(f"{l} · {'file' if f == 'by_file' else 'repo'}" for l, f, _ in cols) + " |"
    rows = [head, "|---|" + "---:|" * len(cols)]

    def cell(f, lang, field, keys):
        d = b[f]["per_language"][lang][field]
        v = sum((d.get(k) or {}).get("pct", 0) for k in keys)
        return ("<1%" if v < 1 else f"{v:.0f}%") if v else "—"
    for label, field, keys in (("hand-written", "provenance_kind", ["hand-written"]),
                               ("IDE / framework template", "provenance_kind", ["ide-or-framework-template"]),
                               ("vendored + generated + dumped", "provenance_kind",
                                ["vendored-third-party", "tool-generated", "decompiled-or-dumped"]),
                               ("research code†", "maturity", ["research-code"]),
                               ("student exercise†", "maturity", ["student-exercise"]),
                               ("production-like†", "maturity", ["production-like"])):
        rows.append(f"| {label} | " + " | ".join(cell(f, l, field, keys) for _, f, l in cols) + " |")
    rows.append("| median lines | " + " | ".join(f"{b[f]['per_language'][l]['median_lines']:.0f}" for _, f, l in cols) + " |")
    rows.append("| *n* | " + " | ".join(str(b[f]['per_language'][l]['n']) for _, f, l in cols) + " |")
    return "\n".join(rows)


def top12():
    rows = ["| repository | `.m` contents | what the sampled files are (judge) |", "|---|---:|---|"]
    for t in A["I_tail"]["top_repos"][:12]:
        s = t["sampled"]
        kinds = sorted({f"{x['language']} / {x['provenance_kind']}" for x in s})
        det = s[0]["detail"] if s else ""
        if len(det) > 64:
            det = det[:64].rsplit(" ", 1)[0] + "…"
        rows.append(f"| {t['origin'].replace('https://', '')} | {t['contents']:,} | {'; '.join(kinds)} — *{det}* |")
    return "\n".join(rows)


def top10():
    rows = ["| repository | `.m` contents | 4 sampled files (judge) |", "|---|---:|---|"]
    for t in A["I_tail"]["top_repos"][:10]:
        kinds = sorted({f"{x['language']}, {x['provenance_kind']}" for x in t["sampled"]})
        rows.append(f"| {t['origin'].replace('https://github.com/', '').replace('https://', '')} | "
                    f"{t['contents']:,} | {'; '.join(kinds)} |")
    return "\n".join(rows)
