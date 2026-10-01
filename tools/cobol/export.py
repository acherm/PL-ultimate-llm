"""Export the COBOL `.cbl`/`.CBL` study to the common study-export format (tools/study_export.py).

Every number is recomputed from the study's data files:

  file frame   data/derived/cobol_study/corpus_estimate.jsonl — the uniform 1 000-content
               sample of the full `.cbl` ∪ `.CBL` union, labelled by the content
               reclassifier (precision 1.00 / recall 0.79 vs the LLM judge)
  repo frame   worklist_div.csv — 1 000 of the 6 278 repositories, one random content
               each — re-labelled here with the same reclassifier (bytes from cache)
  samples      reports/*.json (judge verdicts) + tools/cobol/origins.py (graph origins)
  heuristics   reclassify_eval.json, and synid.jsonl (tools/cobol/run_synid.py)

Case: `ext_claim` is case-folded, and so is the site's per-extension page; the study's
headline frames sample the *union* of both casings. Union rows are therefore written
under `.cbl` (note: "case-folded union"); exact-case rows are written for `.CBL`;
lowercase-exact shares go to study.json (`case_split`), since a `.cbl` row would
collide with the union row of the same frame.

    python3 -m tools.cobol.run_synid      # optional, for the Synid evaluation
    python3 -m tools.cobol.export
    python3 tools/propagate_study.py --study cobol            # plan; --apply to merge
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import study_export as SE  # noqa: E402
from tools.cobol import reclassify as rc  # noqa: E402
from tools.cobol.common import CACHE_DIR  # noqa: E402
from tools.cobol.origins import graph_origins  # noqa: E402
from tools.cobol.run_study import canonical_view  # noqa: E402
from tools.m.stats import wilson  # noqa: E402

STUDY = ROOT / "data" / "derived" / "cobol_study"
REVIEWS = ROOT / "reviews_cobol"
REPORT = "docs/cobol_swh_study.md"
POP = {"contents": 276831, "contents_lowercase": 81446, "contents_uppercase": 196228,
       "contents_with_origin": 276600, "repositories": 6278}     # recomputed from COBOL-SWH-extracted/ + origins

# reclassifier label → (evidence label, display, pl_id)
BUCKET = {
    "cobol": ("cobol", "COBOL (programs, copybooks, generated)", "pl/cobol"),
    "cobol-copybook": ("cobol", "COBOL (programs, copybooks, generated)", "pl/cobol"),
    "cobol-generated": ("cobol", "COBOL (programs, copybooks, generated)", "pl/cobol"),
    "synthetic-placeholder": ("not-code:synthetic-fixture",
                              "synthetic test fixture (WBC_*_FOO.CBL, one GitLab repository)", ""),
    "comic-book-list": ("not-code:calibre-comic-list", "Calibre/ComicRack comic-book reading lists", ""),
    "other": ("other", "other text (foreign source, data, docs)", ""),
    "binary-data": ("not-code:binary", "binary data", ""),
}
# reviewer ids in reviews_cobol/ → the id the encyclopedia's review store uses for that person
REVIEWER_ID = {"mathieuacher": "mathieu-acher", "mathieu": "mathieu-acher"}
ORDER = ["cobol", "not-code:synthetic-fixture", "not-code:calibre-comic-list", "other", "not-code:binary"]


def ext_of(name: str) -> str:
    return ".CBL" if name.endswith(".CBL") else ".cbl" if name.endswith(".cbl") else name.rsplit(".", 1)[-1]


# ------------------------------------------------------------------ frames
def file_frame() -> list[dict]:
    """[{sha, name, label, ext}] — the uniform 1k content-classified sample."""
    out = []
    for line in (STUDY / "corpus_estimate.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out.append({"sha": r["sha1_git"], "name": r["name"], "label": r["label"], "ext": ext_of(r["name"])})
    return out


def repo_frame() -> list[dict]:
    """[{sha, name, label, ext}] — the by-repo sample, reclassified from cached bytes."""
    out = []
    for r in csv.DictReader((STUDY / "worklist_div.csv").open(encoding="utf-8")):
        raw = (CACHE_DIR / f"{r['sha1_git']}.bin").read_bytes()
        out.append({"sha": r["sha1_git"], "name": r["name"], "label": rc.classify(r["name"], raw)["label"],
                    "ext": r.get("source_csv") or ext_of(r["name"])})
    return out


def shares(items: list[dict]) -> dict:
    n = len(items)
    c = Counter(BUCKET[i["label"]][0] for i in items)
    sub = Counter(i["label"] for i in items if BUCKET[i["label"]][0] == "cobol")
    out = {}
    for lab in ORDER:
        k = c.get(lab, 0)
        if not k:
            continue
        p, lo, hi = wilson(k, n)
        out[lab] = {"k": k, "n": n, "pct": round(100 * p, 1), "lo": round(100 * lo, 1), "hi": round(100 * hi, 1)}
    out["_cobol_parts"] = dict(sub)
    return out


def evidence_rows(F, R) -> tuple[list[dict], dict]:
    rows, case_split = [], {}
    frames = (("file", F, "content reclassifier over a uniform random 1 000 of the 276 831 contents "
                          "(precision 1.00 / recall 0.79 vs the LLM judge → COBOL is a lower bound)"),
              ("repo", R, "1 000 of the 6 278 repositories, one random content each, content reclassifier"))
    for frame, items, method in frames:
        for ext, scope, sel in ((".cbl", "case-folded union of .cbl and .CBL (the study's headline frame)",
                                 items),
                                (".CBL", "uppercase .CBL only", [i for i in items if i["ext"] == ".CBL"])):
            s = shares(sel)
            for lab in ORDER:
                if lab not in s:
                    continue
                v = s[lab]
                note = scope
                if lab == "cobol":
                    parts = s["_cobol_parts"]
                    note += (f"; of which programs {parts.get('cobol', 0)}, copybooks/fragments "
                             f"{parts.get('cobol-copybook', 0)}, machine-generated {parts.get('cobol-generated', 0)}")
                rows.append({"ext": ext, "label": lab, "display": BUCKET_DISPLAY[lab], "pl_id": BUCKET_PL[lab],
                             "frame": frame, "share_pct": v["pct"], "ci_lo_pct": v["lo"], "ci_hi_pct": v["hi"],
                             "n_class": v["k"], "n_frame": v["n"], "method": method, "note": note})
        lower = shares([i for i in items if i["ext"] == ".cbl"])
        case_split[frame] = {"lowercase .cbl only": {k: v for k, v in lower.items() if not k.startswith("_")},
                             "n": sum(1 for i in items if i["ext"] == ".cbl")}
    return rows, case_split


BUCKET_DISPLAY = {v[0]: v[1] for v in BUCKET.values()}
BUCKET_PL = {v[0]: v[2] for v in BUCKET.values()}


# ------------------------------------------------------------------ samples
def load_reports() -> dict[str, dict]:
    out = {}
    for p in (STUDY / "reports").glob("*.json"):
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return out


def human_reviews(sha: str) -> list[dict]:
    d = REVIEWS / sha
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))] if d.is_dir() else []


def _cached_ok(sha: str) -> bytes | None:
    p = CACHE_DIR / f"{sha}.bin"
    if not p.exists():
        return None
    raw = p.read_bytes()
    return raw if SE.git_blob_sha1(raw) == sha else None


def pick_samples(reports: dict[str, dict]) -> list[dict]:
    """A deliberate mix (distinct origins): a GnuCOBOL learner program, an ORCA (jma-receipt)
    production program, an IBM-mainframe CICS program, a copybook, a Micro Focus OO generated
    unit, plus the one human-reviewed file. Each: judge says COBOL (or a human did), the
    reclassifier agrees, bytes re-hash to the sha1_git, and the graph knows its origin."""
    graph = graph_origins()
    div = {r["sha1_git"] for r in csv.DictReader((STUDY / "worklist_div.csv").open(encoding="utf-8"))}
    cands = []
    for sha, rep in reports.items():
        v = canonical_view(((rep.get("judge") or {}).get("verdict")))
        if not v or v["cobol_confirmed"] != "true" or sha not in graph:
            continue
        raw = _cached_ok(sha)
        if raw is None:
            continue
        rl = rc.classify(rep["sample"]["filename"], raw)
        if not rl["is_cobol"]:
            continue
        lines = (rep.get("indicators") or {}).get("total_lines", 0)
        cands.append({"sha": sha, "rep": rep, "v": v, "reclass": rl["label"], "lines": lines,
                      "origin": graph[sha]["origin"], "in_div": sha in div})
    kinds = [
        ("gnucobol learner program", 80,
         lambda c: c["v"]["family"] == "gnucobol" and c["v"]["maturity"] == "student-exercise"
         and 20 <= c["lines"] <= 200 and c["in_div"]),
        ("ORCA (jma-receipt) production program", 300,
         lambda c: "jma-receipt" in c["origin"] and c["v"]["maturity"] == "production-like" and c["lines"] <= 600),
        ("IBM-mainframe online CICS program", 150,
         lambda c: c["v"]["family"] == "ibm-mainframe" and c["v"]["program_type"] == "online-cics"
         and c["lines"] <= 400),
        ("copybook / fragment", 40, lambda c: c["reclass"] == "cobol-copybook" or c["v"]["program_type"] == "copybook"),
        ("Micro Focus OO generated unit", 80, lambda c: c["reclass"] == "cobol-generated"),
    ]
    picked, origins = [], set()
    for kind, target, pred in kinds:
        pool = sorted((c for c in cands if pred(c) and c["origin"] not in origins),
                      key=lambda c: (abs(c["lines"] - target), c["sha"]))
        if pool:
            c = pool[0]
            origins.add(c["origin"])
            picked.append(sample_row(c["sha"], c["rep"]["sample"]["filename"], graph[c["sha"]], kind,
                                     verdict=c["v"], reclass=c["reclass"],
                                     judge_schema=(c["rep"].get("judge") or {}).get("schema")))
    # the human-reviewed file(s), if COBOL and verifiable
    for d in sorted(p for p in REVIEWS.iterdir() if p.is_dir()) if REVIEWS.exists() else []:
        hs = human_reviews(d.name)
        if not hs or (hs[-1].get("human") or {}).get("is_cobol") != "yes":
            continue
        raw = _cached_ok(d.name)
        if raw is None or d.name not in graph or graph[d.name]["origin"] in origins:
            continue
        rl = rc.classify(hs[-1]["subject"].get("filename", ""), raw)
        origins.add(graph[d.name]["origin"])
        rep = reports.get(d.name) or {}
        picked.append(sample_row(d.name, hs[-1]["subject"].get("filename", ""), graph[d.name],
                                 "human-reviewed (" + ((hs[-1].get("human") or {}).get("domain") or "") + ")",
                                 verdict=canonical_view((rep.get("judge") or {}).get("verdict")),
                                 reclass=rl["label"], judge_schema=(rep.get("judge") or {}).get("schema"),
                                 human=REVIEWER_ID.get(hs[-1]["reviewer"]["id"], hs[-1]["reviewer"]["id"])))
    return picked


def sample_row(sha, filename, g, kind, *, verdict, reclass, judge_schema, human=None) -> dict:
    name = Path(filename).name
    path = g.get("path") or filename
    vb = []
    if verdict:
        vb.append(f"judge:claude-sonnet-4.6 ({judge_schema}, shown indicators)")
    vb.append(f"reclassifier:{reclass}")
    if human:
        vb.append(f"human:{human}")
    detail = (f"COBOL — {verdict['family']}, {verdict['standard']}, {verdict['source_format']} format"
              if verdict else "COBOL (not judged: below the division gate)")
    note = kind
    if verdict:
        note += f"; {verdict['program_type']}, {verdict['domain']}"
    return {"ext": ".CBL" if name.endswith(".CBL") else ".cbl", "pl_id": "pl/cobol", "label": "cobol",
            "sha1_git": sha, "filename": name, "origin": g.get("origin", ""), "path": path,
            "branch": g.get("branch") or "", "visit_ts": g.get("timestamp") or "",
            "qualified_swhid": SE.qualified_swhid(sha, g.get("origin"), path), "verified_by": "; ".join(vb),
            "language_detail": detail, "provenance_kind": (verdict or {}).get("maturity", "") or "", "note": note}


# ------------------------------------------------------------------ claims
def claim_rows(F_shares, R_shares, samples) -> list[dict]:
    f, r = F_shares["cobol"]["pct"], R_shares["cobol"]["pct"]
    evid = "; ".join([REPORT] + [s["qualified_swhid"] for s in samples[:2]])
    return [{"ext": ".cbl", "pl_id": "pl/cobol", "action": "observe", "strength": "primary",
             "share_file_pct": f, "share_repo_pct": r, "evidence": evid,
             "rationale": (f"observed in SWH — COBOL is {f} % of .cbl/.CBL files (lower bound; {F_shares['not-code:synthetic-fixture']['pct']} % of files are "
                           f"one synthetic fixture) and the sampled file of {r} % of repositories"),
             "status": "accepted"}]


# ------------------------------------------------------------------ heuristics
def heuristic_rows(F, R) -> list[dict]:
    ev = json.loads((STUDY / "reclassify_eval.json").read_text())
    ref = (f"LLM oracle (claude-sonnet-4.6) on {ev['n']} files: {ev['groups']['tail']} non-COBOL-tail, "
           f"{ev['groups']['wbc']} synthetic, {ev['groups']['control']} controls")
    rows = []
    for tool, key, note in (("study rules: cobol content reclassifier", "heuristic_vs_oracle",
                             "in-sample: the rules were distilled from these oracle labels"),
                            ("division gate (n_divisions ≥ 2)", "division_gate_vs_oracle",
                             "the study's cost gate, used as a baseline classifier")):
        m = ev[key]
        for metric in ("precision", "recall", "f1", "accuracy"):
            rows.append({"ext": ".cbl", "heuristic_id": "", "tool": tool, "metric": f"{metric}:is-cobol",
                         "value": m[metric], "n": ev["n"], "reference": ref, "note": note})
    rows.append({"ext": ".cbl", "heuristic_id": "", "tool": "linguist-heuristics", "metric": "disambiguation_rules",
                 "value": 0, "n": "", "reference": "data/derived/pl_taxonomy/heuristic.csv",
                 "note": "no .cbl disambiguation block: Linguist maps every .cbl to COBOL by extension"})
    syn_path = STUDY / "synid.jsonl"
    if syn_path.exists():
        syn = {}
        for line in syn_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                d = json.loads(line)
                syn[d["sha1_git"]] = d
        tool = "swh-synid " + next(iter(syn.values()))["synid_commit"] + " (file mode, default strategies)"
        for frame, items, ref2 in (("file", F, "content reclassifier labels, uniform 1k by-file"),
                                   ("repo", R, "content reclassifier labels, 1k by-repo")):
            for ext, sel in ((".cbl", items), (".CBL", [i for i in items if i["ext"] == ".CBL"])):
                xs = [i for i in sel if i["sha"] in syn]
                said_cobol = [i for i in xs if (syn[i["sha"]]["default"] or []) == ["COBOL"]]
                truth = [i for i in xs if BUCKET[i["label"]][0] == "cobol"]
                ok = sum(1 for i in xs if ((syn[i["sha"]]["default"] or []) == ["COBOL"]) == (BUCKET[i["label"]][0] == "cobol"))
                abst = sum(1 for i in xs if not syn[i["sha"]]["default"] or syn[i["sha"]]["default"] == ["Text"])
                scope = "union .cbl ∪ .CBL" if ext == ".cbl" else "uppercase .CBL only"
                for metric, val in (("accuracy_all", ok / len(xs)), ("abstain_rate", abst / len(xs)),
                                    ("says_cobol_rate", len(said_cobol) / len(xs)),
                                    ("precision:cobol", len(truth) / max(len(said_cobol), 1))):
                    rows.append({"ext": ext, "heuristic_id": "", "tool": tool, "metric": f"{metric}@{frame}",
                                 "value": round(val, 4), "n": len(xs), "reference": f"{ref2} ({scope})",
                                 "note": "extension-only verdict: synthetic stubs, comic-book lists and binaries "
                                         "are all called COBOL; .CBL is handled like .cbl"})
    return rows


# ------------------------------------------------------------------ reviews hook
_REPORTS = None


def study_reviews(s: dict) -> list[dict]:
    """Hook for tools/propagate_study.py: the judge verdict (kind=llm) and any human review
    (kind=human) for one propagated sample, as reviewstore records."""
    import reviewstore as RS  # tools/ is on sys.path when called from propagate_study
    global _REPORTS
    if _REPORTS is None:
        _REPORTS = load_reports()
    sha = s["sha1_git"]
    subject = {"sha1_git": sha, "filename": s["filename"], "ext": s["ext"]}
    out = []
    rep = _REPORTS.get(sha) or {}
    j = rep.get("judge") or {}
    v = canonical_view(j.get("verdict"))
    if v and v["cobol_confirmed"] == "true":
        conf = v["confidence"] if v["confidence"] in RS.CONFIDENCES else "medium"
        rev = RS.new_review(
            subject=subject,
            reviewer={"kind": "llm", "id": (j.get("model") or "anthropic/claude-sonnet-4.6").replace("/", "-"),
                      "version": j.get("schema"), "runner": "tools/cobol/judge.py",
                      "params": {"study": "cobol", "mode": "bytes + filename + mechanical indicators "
                                                           "(pre-revision protocol, not blind)", "temperature": 0}},
            label="pl/cobol", confidence=conf,
            comment=(f"{v['family']}, {v['standard']}, {v['source_format']}; {v['program_type']}, {v['domain']}"),
            shown={"study": "cobol"})
        rev["created_at"] = rep.get("generated_at") or rev["created_at"]
        out.append(rev)
    for h in human_reviews(sha):
        hu = h.get("human") or {}
        if hu.get("is_cobol") != "yes":
            continue
        rev = RS.new_review(
            subject=subject, reviewer={"kind": "human", "id": REVIEWER_ID.get(h["reviewer"]["id"], h["reviewer"]["id"])},
            label="pl/cobol", confidence="medium",               # the COBOL review form has no confidence field
            comment="; ".join(x for x in (hu.get("domain"), hu.get("dialect_family"), hu.get("notes")) if x) or None,
            shown={"study": "cobol", "tool": "tools/cobol/review_app.py"})
        rev["created_at"] = h.get("created_at") or rev["created_at"]
        out.append(rev)
    return out


# ------------------------------------------------------------------ main
def main():
    F, R = file_frame(), repo_frame()
    evidence, case_split = evidence_rows(F, R)
    reports = load_reports()
    samples = pick_samples(reports)
    tables = {"ext_evidence.csv": evidence, "samples.csv": samples,
              "claims.csv": claim_rows(shares(F), shares(R), samples),
              "heuristic_eval.csv": heuristic_rows(F, R)}
    judged = sum(1 for r in reports.values() if canonical_view((r.get("judge") or {}).get("verdict")))
    meta = {"title": "What is actually in the COBOL extensions on Software Heritage?",
            "extensions": [".cbl", ".CBL"], "case_sensitive": True, "report": REPORT, "toolkit": "tools/cobol/",
            "population": {**POP, "source": "COBOL-SWH-extracted/{cbl_files_lowercase,CBL_files}.csv + "
                                            "cbl_file+origin.csv + CBL_files+origins.csv"},
            "frames": {"file": "uniform 1 000 contents of the .cbl ∪ .CBL union, content-classified "
                               "(corpus_estimate.jsonl)",
                       "repo": "1 000 of 6 278 repositories, one random content each (worklist_div.csv), "
                               "content-classified"},
            "case_note": ("ext_claim and the site's per-extension pages are case-folded: union rows are filed "
                          "under .cbl; exact-case rows under .CBL; lowercase-only shares are in case_split"),
            "case_split": case_split,
            "judges": ["anthropic/claude-sonnet-4.6 (cobol-judge/1 and /2; shown the mechanical indicators)"],
            "judged_contents": judged,
            "human_reviews": sum(1 for p in REVIEWS.iterdir() if p.is_dir()) if REVIEWS.exists() else 0,
            "human_group_rules": "reviews_cobol/_rules.jsonl (the WBC fixture origin → not-cobol:synthetic)",
            "spend_usd_approx": 45, "spend_note": "approximate total across experiments, per the report",
            "study_dates": "2026-06-16 – 2026-07-08", "date": "2026-10-01"}
    SE.write_export("cobol", meta, tables)


if __name__ == "__main__":
    main()
