"""Export the `.rpgle` study to the common study-export format (tools/study_export.py).

Every number is recomputed from the per-content reports (data/derived/rpgle_study/
reports/*.json + worklist_all.csv) with the frame definitions of
tools/rpgle/analysis.py, so it reproduces docs/rpgle_swh_study.md (E1 n=996 judged,
E2 n=514, E1′ minus the three RPG-tooling repos, E1″ one content per (repo, file
name)); reclassifier metrics come from eval_split.json (v2, frozen → prospective)
and are recomputed on the same held-out split for v3 (in-sample).

    python3 -m tools.rpgle.export
    python3 tools/propagate_study.py --study rpgle            # plan; add --apply to merge
"""

from __future__ import annotations

import csv
import glob
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import study_export as SE  # noqa: E402
from tools.m.stats import wilson  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "rpgle_study"
CACHE = ROOT / ".cache" / "cobol"
CSV_POP = ROOT / "rpgle_files+origins.csv"
EXT = ".rpgle"
PL = "pl/rpgle"
REPORT = "docs/rpgle_swh_study.md"
TOOLING = {"https://github.com/smeup/jariko", "https://github.com/JCErasmus/antlr4-rpgle",
           "https://github.com/chrjorgensen/rpgleparser"}
# Judge verdicts carry no timestamp; review records use the study commit's time (fcea3d51)
# so propagated filenames are deterministic and re-running propagation never duplicates them.
JUDGED_AT = "2026-07-10T08:56:56Z"
# samples avoid parser/interpreter fixtures (incl. forks of the tooling repos) and generator output
SAMPLE_AVOID = ("jariko", "antlr4-rpgle", "rpgleparser", "generator")
JUDGE_MODEL = "anthropic/claude-sonnet-4.6"

TAIL_LABEL = {"data": "not-code:data", "docs": "not-code:docs", "binary": "not-code:binary",
              "generated": "not-code:generated", "other-language": "other-language", "ambiguous": "unknown"}
DISPLAY = {"rpgle": "RPG IV / ILE RPG", "not-code:data": "not code: data (tables, token lists, JSON)",
           "not-code:docs": "not code: docs (licence, ILEDocs metadata, plain text)",
           "not-code:binary": "not code: binary (EBCDIC)", "not-code:generated": "not code: generated",
           "other-language": "other notation (DDS, XSLT template)", "unknown": "unknown / ambiguous",
           "dialect:fully-free": "RPG IV — fully-free (**FREE)", "dialect:hybrid-free": "RPG IV — hybrid-free",
           "dialect:fixed-format": "RPG IV — fixed-format (column specs)",
           "unit:copy-member": "RPG IV — /COPY member (declarations only)"}
FRAME_METHOD = {
    "file": "judge (claude-sonnet-4.6, shown indicators), uniform by-file sample (E1)",
    "repo": "judge, one random content per repository — census of all 534 repositories (E2)",
    "file-filtered": "E1 subset: minus the 3 RPG-tooling repos (jariko, antlr4-rpgle, rpgleparser) (E1′)",
    "path": "E1 subset: one content per (repository, file name) — version history collapsed (E1″)",
}


# ---------------------------------------------------------------- data
def V(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def load_reports():
    reps = [json.loads(Path(p).read_text()) for p in glob.glob(str(STUDY / "reports" / "*.json"))]
    wl = {r["sha1_git"]: r for r in csv.DictReader((STUDY / "worklist_all.csv").open(encoding="utf-8"))}
    for r in reps:
        r["_wl"] = wl.get(r["sha1_git"], {})
    return reps


def frames(reps) -> dict[str, list[dict]]:
    uniform = [r for r in reps if r["_wl"].get("in_uniform") == "1"]
    diverse = [r for r in reps if r["_wl"].get("in_diverse") == "1"]
    no_tool = [r for r in uniform if r["origin"] not in TOOLING]
    seen, dedup = set(), []
    for r in sorted(uniform, key=lambda r: r["sha1_git"]):
        k = (r["origin"], r["name"])
        if k not in seen:
            seen.add(k)
            dedup.append(r)
    return {"file": uniform, "repo": diverse, "file-filtered": no_tool, "path": dedup}


def language_label(v) -> str:
    if v.get("is_programming_language") and v.get("content_type") in ("source-code", "copybook-or-header"):
        return "rpgle"
    return TAIL_LABEL.get(v.get("not_rpgle_label") or "", "unknown")


def pct(k, n):
    return round(100 * k / n, 2) if n else 0.0


def ci(k, n):
    _, lo, hi = wilson(k, n)
    return round(100 * lo, 1), round(100 * hi, 1)


# ---------------------------------------------------------------- evidence
def evidence_rows(reps):
    rows = []
    for frame, fr in frames(reps).items():
        j = [r for r in fr if V(r)]
        n = len(j)
        nontext = len(fr) - n
        note_n = f"{n} judged of {len(fr)} sampled ({nontext} non-text contents never judged)"

        def add(label, k, pl_id=PL, extra=""):
            lo, hi = ci(k, n)
            rows.append({"ext": EXT, "label": label, "display": DISPLAY.get(label, label), "pl_id": pl_id,
                         "frame": frame, "share_pct": pct(k, n), "ci_lo_pct": lo, "ci_hi_pct": hi,
                         "n_class": k, "n_frame": n, "method": FRAME_METHOD[frame],
                         "note": "; ".join(x for x in (extra, note_n) if x)})
        langs = Counter(language_label(V(r)) for r in j)
        for lab, k in langs.most_common():
            add(lab, k, PL if lab == "rpgle" else "")
        sf = Counter(V(r).get("source_format") for r in j)
        for d in ("fully-free", "hybrid-free", "fixed-format"):
            add(f"dialect:{d}", sf.get(d, 0),
                extra="share of all judged files; source_format per the judge (fully-free over-called vs the "
                      "**FREE directive, see heuristic_eval)" if d == "fully-free" else "share of all judged files")
        cm = sum(1 for r in j if V(r).get("content_type") == "copybook-or-header")
        add("unit:copy-member", cm, extra="content_type copybook-or-header (declaration-only /COPY member)")
    return rows


# ---------------------------------------------------------------- claims
def claim_rows(reps, samples):
    fr = frames(reps)
    share = {}
    for f in ("file", "repo"):
        j = [r for r in fr[f] if V(r)]
        share[f] = pct(sum(1 for r in j if language_label(V(r)) == "rpgle"), len(j))
    others = [c for c in SE.ext_claims() if not c["source"].startswith("swh_study:")]
    action = "observe" if (PL, EXT) in {(c["pl_id"], c["ext"]) for c in others} else "add"
    evid = "; ".join([REPORT] + [s["qualified_swhid"] for s in samples[:2]])
    return [{"ext": EXT, "pl_id": PL, "action": action, "strength": "primary" if action == "observe" else "proposed",
             "share_file_pct": round(share["file"], 1), "share_repo_pct": round(share["repo"], 1), "evidence": evid,
             "rationale": f"observed in SWH — {share['file']:.1f} % of judged files and {share['repo']:.1f} % of "
                          "repositories are RPG IV / ILE RPG source or /COPY members (a clean extension)",
             "status": "accepted"}]


# ---------------------------------------------------------------- samples
def origin_index() -> dict[str, list[dict]]:
    idx: dict[str, list[dict]] = {}
    with CSV_POP.open(encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        next(rd, None)
        for row in rd:
            if len(row) < 3:
                continue
            sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
            q = parse_qs(urlparse(row[2]).query)
            idx.setdefault(sha, []).append({
                "origin": (q.get("origin_url") or [""])[0], "path": (q.get("path") or [""])[0],
                "branch": (q.get("branch") or [""])[0], "ts": (q.get("timestamp") or [""])[0]})
    return idx


def pick_samples(reps):
    """Fully-free, hybrid-free and fixed-format programs plus a /COPY member: judge and
    reclassifier agree (and for the dialect, the indicator agrees too), confidence high,
    20–300 lines, distinct repositories, no parser fixtures or generator output."""
    oidx = origin_index()
    j = [r for r in reps if V(r) and V(r).get("confidence") == "high" and r["indicators"].get("is_text", True)]

    def ok_size(r, lo=20, hi=300):
        return (lo <= r["indicators"]["total_lines"] <= hi
                and not any(a in r["origin"].lower() for a in SAMPLE_AVOID))

    wants = [
        ("dialect:fully-free", lambda r: V(r)["source_format"] == "fully-free" and r["indicators"]["is_fully_free"]
         and r["reclass"]["label"] == "rpgle" and V(r)["content_type"] == "source-code"
         and V(r)["maturity"] in ("production-like", "library-quality") and ok_size(r), 2),
        ("dialect:hybrid-free", lambda r: V(r)["source_format"] == "hybrid-free"
         and r["indicators"]["source_format_guess"] == "hybrid-free" and r["reclass"]["label"] == "rpgle"
         and V(r)["content_type"] == "source-code" and V(r)["maturity"] in ("production-like", "library-quality")
         and ok_size(r), 1),
        ("dialect:fixed-format", lambda r: V(r)["source_format"] == "fixed-format"
         and r["indicators"]["source_format_guess"] == "fixed-format" and r["reclass"]["label"] == "rpgle"
         and V(r)["content_type"] == "source-code"
         and V(r)["maturity"] in ("production-like", "library-quality") and ok_size(r), 1),
        ("unit:copy-member", lambda r: V(r)["content_type"] == "copybook-or-header"
         and r["reclass"]["label"] == "rpgle-copybook" and r["indicators"].get("has_extproc")
         and r["name"] == "/SAX2.rpgle", 1),
    ]
    out, used_origins = [], set()
    for label, pred, k in wants:
        cands = sorted((r for r in j if pred(r)), key=lambda r: (abs(r["indicators"]["total_lines"] - 90),
                                                                r["sha1_git"]))
        got = 0
        for r in cands:
            if r["origin"] in used_origins:
                continue
            raw_p = CACHE / f"{r['sha1_git']}.bin"
            if not raw_p.exists() or SE.git_blob_sha1(raw_p.read_bytes()) != r["sha1_git"]:
                continue
            ctx = next((c for c in oidx.get(r["sha1_git"], []) if c["origin"] == r["origin"]),
                       (oidx.get(r["sha1_git"]) or [{}])[0])
            used_origins.add(r["origin"])
            v = V(r)
            out.append({"ext": EXT, "pl_id": PL, "label": label, "sha1_git": r["sha1_git"],
                        "filename": r["name"].lstrip("/"), "origin": ctx.get("origin") or r["origin"],
                        "path": ctx.get("path", ""), "branch": ctx.get("branch", ""), "visit_ts": ctx.get("ts", ""),
                        "qualified_swhid": SE.qualified_swhid(r["sha1_git"], ctx.get("origin") or r["origin"],
                                                              ctx.get("path")),
                        "verified_by": "judge:claude-sonnet-4.6; rules:rpgle-reclass"
                                       + ("; rules:**FREE-directive" if label == "dialect:fully-free" else ""),
                        "language_detail": f"{v.get('language', '')} · {v.get('source_format', '')} · {v.get('unit_kind', '')}",
                        "provenance_kind": v.get("maturity", ""),
                        "note": (v.get("purpose") or "")[:160]})
            got += 1
            if got >= k:
                break
    return out


# ---------------------------------------------------------------- heuristic evaluation
def heuristic_rows(reps):
    rows = []
    split = json.loads((STUDY / "eval_split.json").read_text())
    held = split["HELD-OUT (judged after freeze)"]
    tuning = split["TUNING (v1 errors inspected)"]
    ref_h = f"LLM judge (claude-sonnet-4.6), held-out split n={held['t1']['n']} (judged after the rules were frozen)"
    tool_v2 = "study rules rpgle-reclass v2 (frozen)"
    for target, key in (("T1:is-rpgle", "t1"), ("T3:copy-member", "t3")):
        for m in ("precision", "recall", "f1", "accuracy", "baseline_accuracy"):
            rows.append({"ext": EXT, "heuristic_id": "", "tool": tool_v2, "metric": f"{target}:{m}",
                         "value": held[key][m], "n": held[key]["n"], "reference": ref_h,
                         "note": "prospective (held-out)"})
            rows.append({"ext": EXT, "heuristic_id": "", "tool": tool_v2, "metric": f"{target}:{m}",
                         "value": tuning[key][m], "n": tuning[key]["n"],
                         "reference": f"LLM judge, tuning split n={tuning[key]['n']}",
                         "note": "tuning split (errors inspected to build v2 — in-sample)"})
    for m in ("accuracy", "macro_f1", "baseline_accuracy"):
        rows.append({"ext": EXT, "heuristic_id": "", "tool": tool_v2, "metric": f"T2:source-format:{m}",
                     "value": held["t2"][m], "n": held["t2"]["n"], "reference": ref_h,
                     "note": "prospective (held-out); 3-class fully/hybrid/fixed, judge as reference"})

    # v3 (current reports' indicators) on the same held-out split — in-sample: refined after these errors
    tune = set(json.loads((STUDY / "eval_tuning_set.json").read_text())["shas"])
    judged = [r for r in reps if V(r) and V(r).get("confidence") != "low" and r["sha1_git"] not in tune]

    def prf(pairs):
        tp = sum(1 for p, g in pairs if p and g)
        fp = sum(1 for p, g in pairs if p and not g)
        fn = sum(1 for p, g in pairs if not p and g)
        P = tp / (tp + fp) if tp + fp else 0.0
        R = tp / (tp + fn) if tp + fn else 0.0
        return round(P, 3), round(R, 3), round(2 * P * R / (P + R), 3) if P + R else 0.0
    t1 = [(r["reclass"]["label"] in ("rpgle", "rpgle-copybook"),
           bool(V(r).get("is_programming_language")) and V(r).get("content_type") in ("source-code", "copybook-or-header"))
          for r in judged]
    t3 = [(bool(r["indicators"]["looks_copybook"]),
           V(r).get("unit_kind") == "copybook-prototype-header" or V(r).get("content_type") == "copybook-or-header")
          for r in judged]
    for target, pairs in (("T1:is-rpgle", t1), ("T3:copy-member", t3)):
        for m, val in zip(("precision", "recall", "f1"), prf(pairs)):
            rows.append({"ext": EXT, "heuristic_id": "", "tool": "study rules rpgle-reclass v3", "metric": f"{target}:{m}",
                         "value": val, "n": len(pairs), "reference": ref_h,
                         "note": "IN-SAMPLE: v3 was refined after inspecting these held-out errors — an upper bound"})

    # the **FREE directive (lexical, decisive by definition) vs the judge's source_format
    fa = json.loads((STUDY / "analysis.json").read_text())["free_axis"]
    tool_free = "lexical rule: '**FREE' on line 1 (indicators.is_fully_free)"
    ref_f = f"judge source_format (fully/hybrid/fixed), n={fa['n']}"
    rows += [
        {"ext": EXT, "heuristic_id": "", "tool": tool_free, "metric": "agreement_with_judge",
         "value": round(fa["agree"] / fa["n"], 4), "n": fa["n"], "reference": ref_f,
         "note": "the directive defines fully-free; disagreements are judge errors, one-sided"},
        {"ext": EXT, "heuristic_id": "", "tool": tool_free, "metric": "judge_fully_free_without_directive",
         "value": fa["judge_says_fullyfree_without_directive"], "n": fa["n"], "reference": ref_f,
         "note": f"{fa['of_those_de_facto_col1']} of them do put code in columns 1-5 (free-form style, no directive)"},
        {"ext": EXT, "heuristic_id": "", "tool": tool_free, "metric": "judge_denies_fully_free_with_directive",
         "value": fa["judge_denies_fullyfree_with_directive"], "n": fa["n"], "reference": ref_f, "note": ""},
    ]

    # SWH Synid on the same judged files (tools/rpgle/run_synid.py), vs the judge's is-RPG
    syn_p = STUDY / "synid.jsonl"
    if syn_p.exists():
        syn = {d["sha1_git"]: d for d in map(json.loads, syn_p.read_text().splitlines())}
        jj = [r for r in reps if V(r) and r["sha1_git"] in syn]
        gold = {r["sha1_git"]: language_label(V(r)) == "rpgle" for r in jj}
        commit = next(iter(syn.values()))["synid_commit"]
        for cfg, tool in (("default", f"swh-synid {commit} (file mode, default strategies)"),
                          ("nocomment", f"swh-synid {commit} (file mode, without comment strategy)")):
            pred = {s: (syn[s].get(cfg) or []) for s in gold}
            answered = [s for s in gold if pred[s] and pred[s] != ["Text"] and len(pred[s]) == 1]
            correct = sum(1 for s in answered if (pred[s] == ["RPGLE"]) == gold[s])
            n_tail = sum(1 for s in gold if not gold[s])
            caught = sum(1 for s in gold if not gold[s] and pred[s] != ["RPGLE"])
            ref_s = f"judge (is RPG source/copy member), {len(gold)} judged files (all frames)"
            rows += [
                {"ext": EXT, "heuristic_id": "", "tool": tool, "metric": "accuracy_all",
                 "value": round(correct / len(gold), 4), "n": len(gold), "reference": ref_s, "note": ""},
                {"ext": EXT, "heuristic_id": "", "tool": tool, "metric": "abstain_rate",
                 "value": round(1 - len(answered) / len(gold), 4), "n": len(gold), "reference": ref_s, "note": ""},
                {"ext": EXT, "heuristic_id": "", "tool": tool, "metric": "recall:not-rpgle",
                 "value": round(caught / n_tail, 4) if n_tail else 0, "n": n_tail, "reference": ref_s,
                 "note": "one candidate for .rpgle (RPGLE): the extension decides; the non-RPG tail is never caught"},
            ]

    # Pygments: filename-driven lexer choice on every judged file
    import pygments
    from pygments.lexers import guess_lexer_for_filename
    from pygments.util import ClassNotFound
    jj = [r for r in reps if V(r) and (CACHE / f"{r['sha1_git']}.bin").exists()]
    abstain = 0
    for r in jj:
        try:
            guess_lexer_for_filename(r["name"].lstrip("/") or "x.rpgle",
                                     (CACHE / f"{r['sha1_git']}.bin").read_bytes().decode("utf-8", "replace"))
        except ClassNotFound:
            abstain += 1
    rows.append({"ext": EXT, "heuristic_id": "", "tool": f"pygments {pygments.__version__} guess_lexer_for_filename",
                 "metric": "abstain_rate", "value": round(abstain / len(jj), 4), "n": len(jj),
                 "reference": "judged files (all frames)", "note": "Pygments has no lexer claiming *.rpgle"})
    return rows


# ---------------------------------------------------------------- reviews hook
_BY_SHA = None


def study_reviews(s: dict) -> list[dict]:
    """Hook for tools/propagate_study.py: the judge's verdict on one propagated sample
    (kind=llm). The study has no human reviews (reviews_rpgle/ is empty)."""
    import reviewstore as RS  # tools/ is on sys.path when called from propagate_study
    global _BY_SHA
    if _BY_SHA is None:
        _BY_SHA = {r["sha1_git"]: r for r in load_reports()}
    r = _BY_SHA.get(s["sha1_git"])
    v = V(r) if r else None
    if not v or language_label(v) != "rpgle":
        return []
    subject = {"sha1_git": s["sha1_git"], "filename": s["filename"], "ext": s["ext"]}
    rev = RS.new_review(
        subject=subject,
        reviewer={"kind": "llm", "id": JUDGE_MODEL.replace("/", "-"), "version": r["judge"].get("schema"),
                  "runner": "tools/rpgle/judge.py",
                  "params": {"study": "rpgle", "mode": "bytes + filename + mechanical indicators", "temperature": 0}},
        label=PL, confidence=v.get("confidence") if v.get("confidence") in RS.CONFIDENCES else "medium",
        comment=f"{v.get('language', '')} · {v.get('source_format', '')} · {v.get('unit_kind', '')}",
        shown={"study": "rpgle"})
    rev["created_at"] = JUDGED_AT
    out = [rev]
    rdir = ROOT / "reviews_rpgle" / s["sha1_git"]
    for p in sorted(rdir.glob("*.json")) if rdir.is_dir() else []:
        h = json.loads(p.read_text())
        hu = h.get("human") or {}
        if hu.get("is_rpgle") != "yes":
            continue
        hr = RS.new_review(subject=subject, reviewer={"kind": "human", "id": h["reviewer"]["id"]},
                           label=PL, confidence="medium", comment=hu.get("notes"), shown={"study": "rpgle"})
        hr["created_at"] = h.get("created_at") or hr["created_at"]
        out.append(hr)
    return out


# ---------------------------------------------------------------- main
def main():
    reps = load_reports()
    pop = json.loads((STUDY / "population.json").read_text())
    samples = pick_samples(reps)
    tables = {"ext_evidence.csv": evidence_rows(reps), "samples.csv": samples,
              "claims.csv": claim_rows(reps, samples), "heuristic_eval.csv": heuristic_rows(reps)}
    judged = [r for r in reps if V(r)]
    spend = round(sum((r["judge"].get("usage") or {}).get("cost", 0) or 0 for r in judged), 2)
    meta = {"title": "What is actually in the .rpgle extension on Software Heritage?", "extensions": [EXT],
            "case_sensitive": True, "report": REPORT, "toolkit": "tools/rpgle/",
            "population": {"contents": pop["unique_contents"], "repositories": pop["unique_origins"],
                           "source": "rpgle_files+origins.csv (SWH graph-derived, maintainer export)"},
            "frames": {"file": "uniform over contents, n=1000 (996 judged)",
                       "repo": "census: one random content per repository, 534 repos (514 judged)",
                       "file-filtered": "E1 minus the 3 RPG-tooling repos (794 judged)",
                       "path": "E1 deduplicated to one content per (repository, file name) (923 judged)"},
            "judges": [f"{JUDGE_MODEL} (shown mechanical indicators; temperature 0)"],
            "human_reviews": 0, "judged": len(judged), "spend_usd": spend, "date": "2026-07-10"}
    SE.write_export("rpgle", meta, tables)


if __name__ == "__main__":
    main()
