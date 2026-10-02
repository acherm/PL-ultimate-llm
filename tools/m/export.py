"""Export the `.m` study to the common study-export format (tools/study_export.py).

Everything comes from data/derived/m_study/analysis.json and the label layers,
so the export can be regenerated after any re-analysis:

    python3 -m tools.m.analysis && python3 -m tools.m.export
    python3 tools/propagate_study.py --study m            # plan; add --apply to merge
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import study_export as SE  # noqa: E402
from tools.m.analysis import LABS, coarse  # noqa: E402
from tools.m.data import STUDY, load  # noqa: E402

EXT = ".m"
REPORT = "docs/m_swh_study.md"
PL = {"objective-c": "pl/objective-c", "matlab": "pl/matlab", "octave": "pl/octave",
      "mathematica-wolfram": "pl/wolfram-language", "mercury": "pl/mercury", "mumps-m": "pl/m",
      "magma": "pl/magma", "limbo": "pl/limbo", "muf": "pl/muf", "maple": "pl/maple", "scilab": "pl/scilab",
      "c-or-cpp": "pl/c", "matlab-family": "pl/matlab"}
# languages for which .m is a *conventional* extension → eligible for observe/add claims
CONVENTIONAL = {"objective-c", "matlab", "octave", "mathematica-wolfram", "mercury", "mumps-m", "magma",
                "limbo", "muf", "mason"}
NOTE_LABEL = {"other-programming-language": "other-language", "not-code": "not-code", "unknown": "unknown",
              "c-or-cpp": "misnamed:c"}
DISPLAY = {"objective-c": "Objective-C", "matlab": "MATLAB", "matlab-family": "MATLAB + Octave (family)",
           "octave": "GNU Octave (Octave-only syntax)", "mathematica-wolfram": "Wolfram Language / Mathematica",
           "mercury": "Mercury", "mumps-m": "MUMPS (M)", "magma": "Magma", "limbo": "Limbo", "muf": "MUF",
           "maple": "Maple", "scilab": "Scilab", "mason": "Mason (Perl templates)", "c-or-cpp": "C (misnamed .m)",
           "other-programming-language": "other languages", "not-code": "not code (XML, data, text, binary)",
           "unknown": "unknown"}
LINGUIST_RULE = {"objective-c": 0, "mercury": 1, "muf": 2, "mumps-m": 3, "mathematica-wolfram": 4,
                 "matlab": 5, "limbo": 6}


def r1(x):
    return round(float(x), 2)


def evidence_rows(A):
    rows = []
    a = A["A_language"]
    for frame, key, method in (("file", "by_file", "judge, uniform by-file sample"),
                               ("repo", "by_repo", "judge, one file per repository")):
        n = A["n"]["U_judged" if frame == "file" else "R_judged"]
        for lab, v in a[key].items():
            rows.append({"ext": EXT, "label": NOTE_LABEL.get(lab, lab), "display": DISPLAY.get(lab, lab),
                         "pl_id": PL.get(lab, ""), "frame": frame, "share_pct": r1(v["pct"]), "ci_lo_pct": r1(v["ci"][0]),
                         "ci_hi_pct": r1(v["ci"][1]), "n_class": v["n"], "n_frame": n, "method": method,
                         "note": "Sonnet 4.6, blind; 2nd judge agrees on 99.7 %" if lab in ("objective-c", "matlab") else ""})
    for frame, key in (("path", "by_path_coarse"), ("repo-reweighted", "by_repo_reweighted_coarse")):
        for lab, v in a[key].items():
            if lab not in ("objective-c", "matlab-family"):
                continue
            rows.append({"ext": EXT, "label": lab, "display": DISPLAY.get(lab, lab), "pl_id": PL.get(lab, ""),
                         "frame": frame, "share_pct": r1(v["pct"]), "ci_lo_pct": r1(v["ci"][0]), "ci_hi_pct": r1(v["ci"][1]),
                         "n_class": "", "n_frame": v["n_eff"], "method": "by-file sample re-weighted by exact population weights (Kish n_eff)",
                         "note": "matlab-family = MATLAB + Octave" if lab == "matlab-family" else ""})
    for frame, key in (("file-ppi", "ppi_by_file"), ("repo-ppi", "ppi_by_repo")):
        d = a[key]
        for lab in ("objective-c", "matlab-family"):
            v = d["classes"][lab]
            rows.append({"ext": EXT, "label": lab, "display": DISPLAY.get(lab, lab), "pl_id": PL[lab],
                         "frame": frame, "share_pct": r1(v["pct"]),
                         "ci_lo_pct": r1(v["ci"][0]), "ci_hi_pct": r1(v["ci"][1]), "n_class": "",
                         "n_frame": d["n_labelled"] + d["n_unlabelled"],
                         "method": f"PPI++ (λ={v['lambda']}): {d['n_labelled']} judged + {d['n_unlabelled']} rule-labelled",
                         "note": "matlab-family = MATLAB + Octave" if lab == "matlab-family" else ""})
    M = A["M_tail_census"]
    claimed = {c["pl_id"] for c in SE.ext_claims() if c["ext"] == EXT and not c["source"].startswith("swh_study:")}
    for frame, fr in (("file-census", "U"), ("repo-census", "R")):
        for lab, v in M[fr]["estimates"].items():
            if lab in ("objective-c", "matlab-family"):
                continue
            n = v["files_in_tail_census"] + v["files_in_main_subsample"]
            n_any = sum(M[f]["estimates"][lab]["files_in_tail_census"] + M[f]["estimates"][lab]["files_in_main_subsample"]
                        for f in ("U", "R"))
            if n_any == 0 and PL.get(lab) not in claimed:
                continue        # zero rows only matter for a claimed language ("claimed, never seen")
            rows.append({"ext": EXT, "label": NOTE_LABEL.get(lab, lab), "display": DISPLAY.get(lab, lab),
                         "pl_id": PL.get(lab, ""), "frame": frame,
                         "share_pct": fmt_share(v.get("pct_exact", v["pct"])), "ci_lo_pct": r1(v["ci"][0]),
                         "ci_hi_pct": r1(v["ci"][1]),
                         "n_class": n, "n_frame": M[fr]["phase1_n"],
                         "method": "two-phase stratified: tail stratum judged in full + judged main subsample",
                         "note": "conservative interval"})
    return rows


def fmt_share(x: float) -> float:
    """1 decimal from 1 % up, 2 below (so 0.01 % — one file in 10 000 — stays visible)."""
    return round(x, 1) if x >= 1 else round(x, 2)


def best_share(A, lab):
    """(file %, repo %) — census for the tail, judged frames for the two big languages."""
    M = A["M_tail_census"]
    if lab in M["U"]["estimates"]:
        u, r = M["U"]["estimates"][lab], M["R"]["estimates"][lab]
        return fmt_share(u.get("pct_exact", u["pct"])), fmt_share(r.get("pct_exact", r["pct"]))
    a = A["A_language"]
    return a["by_file"].get(lab, {}).get("pct", 0.0), a["by_repo"].get(lab, {}).get("pct", 0.0)


def claim_rows(A, samples):
    # what the *other* sources claim — the study's own rows (after a previous propagation) don't count
    others = [c for c in SE.ext_claims() if not c["source"].startswith("swh_study:")]
    existing = {(c["pl_id"], c["ext"]) for c in others}
    claimed_here = {c["pl_id"]: c["source"] for c in others if c["ext"] == EXT}
    ex = {}
    for s in samples:
        ex.setdefault(s["pl_id"], []).append(s["qualified_swhid"])
    rows = []
    for lab in sorted(CONVENTIONAL):
        pid = PL.get(lab)
        if not pid:
            continue
        f, r = best_share(A, lab)
        n_obs = (A["M_tail_census"]["U"]["estimates"].get(lab, {}).get("files_in_tail_census", 0)
                 + A["M_tail_census"]["R"]["estimates"].get(lab, {}).get("files_in_tail_census", 0)
                 + A["A_language"]["by_file"].get(lab, {}).get("n", 0) + A["A_language"]["by_repo"].get(lab, {}).get("n", 0))
        evid = "; ".join([REPORT] + ex.get(pid, [])[:2])
        if n_obs == 0:
            if pid in claimed_here:
                rows.append({"ext": EXT, "pl_id": pid, "action": "unobserved", "strength": "",
                             "share_file_pct": 0, "share_repo_pct": 0, "evidence": REPORT,
                             "rationale": f"claimed by {claimed_here[pid]}; never observed among 13 000 sampled "
                                          "contents (judged samples + tail census)", "status": "accepted"})
            continue
        strength = "primary" if max(f, r) >= 10 else "secondary"
        action = "observe" if (pid, EXT) in existing else "add"
        rows.append({"ext": EXT, "pl_id": pid, "action": action, "strength": strength if action == "observe" else "proposed",
                     "share_file_pct": f, "share_repo_pct": r, "evidence": evid,
                     "rationale": ("observed in SWH" if action == "observe" else
                                   "observed in SWH, conventional .m extension of this language, claimed by no source")
                                  + f" — {f} % of files, {r} % of repositories", "status": "accepted"})
    # claimants never seen and not in CONVENTIONAL (e.g. A+ via Wikipedia)
    seen = {r["pl_id"] for r in rows}
    for pid, src in claimed_here.items():
        if pid in seen or pid in ("pl/m4", "pl/monkey-c", "pl/win32-message-file"):
            continue
        rows.append({"ext": EXT, "pl_id": pid, "action": "unobserved", "strength": "", "share_file_pct": 0,
                     "share_repo_pct": 0, "evidence": REPORT,
                     "rationale": f"claimed by {src}; never observed among 13 000 sampled contents", "status": "accepted"})
    for pid in ("pl/m4", "pl/monkey-c", "pl/win32-message-file"):
        rows.append({"ext": EXT, "pl_id": pid, "action": "dispute", "strength": "disputed",
                     "source_disputed": "pygments", "share_file_pct": 0, "share_repo_pct": 0,
                     "evidence": f"{REPORT} §4.1; data/derived/m_study/mapping_pygments_ext_fallback.json",
                     "rationale": "inherited from Pygments' Mason lexer through an extension-overlap join "
                                  "(master_inventory.match_pygments_name: shared .mc); never observed",
                     "status": "accepted"})
    return rows


def pick_samples(recs, A):
    """Exemplars per conventional language: both judges agree, text, 15–400 lines,
    hand-written or library code, distinct repositories. Files a human reviewer
    confirmed are always kept and rank first; judge-only picks are capped at 3
    (2 for Objective-C and MATLAB)."""
    out, by_lab = [], {}
    for r in recs.values():
        j, j2 = r.lang("judge"), r.lang("judge2")
        if not j or j != j2 or j not in CONVENTIONAL:
            continue
        v = r.v("judge")
        lines = r.ind.get("total_lines", 0)
        if not (15 <= lines <= 400) or v.get("provenance_kind") not in ("hand-written", "vendored-third-party", "tool-generated"):
            continue
        if j == "octave" and not r.ind.get("octave_syntax_v2"):
            continue                      # an Octave exemplar must show Octave-only syntax
        h = r.human()
        human_ok = bool(h and not h.get("_rule") and h.get("language") == j)
        by_lab.setdefault(j, []).append((not human_ok, v.get("provenance_kind") != "hand-written",
                                         abs(lines - 80), r.sha, r, human_ok))
    # rare languages: if the filters left nothing, take any file both judges agree on
    for r in recs.values():
        j = r.lang("judge")
        if j in CONVENTIONAL and j == r.lang("judge2") and j not in by_lab and r.ind.get("is_text", True):
            by_lab.setdefault(j, []).append((True, True, 0, r.sha, r, False))
    for lab, cands in by_lab.items():
        seen_origins, n_judge_only = set(), 0
        for *_k, r, human_ok in sorted(cands, key=lambda c: c[:4]):
            # distinct repositories and the cap shape the judge-only picks; a file a
            # human confirmed is always kept, even next to another from its repository
            if not human_ok and r.row.get("origin") in seen_origins:
                continue
            if not human_ok and n_judge_only >= (3 if lab not in ("objective-c", "matlab") else 2):
                continue
            raw = SE.content_bytes("m", r.sha)
            if raw is None:
                continue
            seen_origins.add(r.row.get("origin"))
            v = r.v("judge")
            out.append({"ext": EXT, "pl_id": PL[lab], "label": lab, "sha1_git": r.sha,
                        "filename": r.row["name"], "origin": r.row.get("origin", ""), "path": r.row.get("path", ""),
                        "branch": r.row.get("branch", ""), "visit_ts": r.row.get("ts", ""),
                        "qualified_swhid": SE.qualified_swhid(r.sha, r.row.get("origin"), r.row.get("path")),
                        "verified_by": "judge:claude-sonnet-4.6; judge:gemini-3.8-flash"
                                       + "".join(f"; human:{rid}" for rid in (r.human_reviewers() if human_ok else [])),
                        "language_detail": v.get("language_detail", ""), "provenance_kind": v.get("provenance_kind", ""),
                        "note": (v.get("purpose") or "")[:160]})
            n_judge_only += not human_ok
    return out


def heuristic_rows(recs, A):
    rows = []
    cons = [r for r in recs.values() if (r.in_frame("U", 1000) or r.in_frame("R", 1000)) and r.lang("judge2")
            and coarse(r.lang("judge")) == coarse(r.lang("judge2"))]
    ref = f"two-judge consensus, {len(cons)} files (U+R ranks ≤ 1000)"
    for lab, i in LINGUIST_RULE.items():
        fired = [r for r in cons if r.lang("linguist") == lab]
        ok = sum(1 for r in fired if coarse(r.lang("judge")) == coarse(lab))
        rows.append({"ext": EXT, "heuristic_id": f"h/linguist/.m/{i}", "tool": "linguist-heuristics",
                     "metric": "fires", "value": len(fired), "n": len(cons), "reference": ref, "note": ""})
        if fired:
            rows.append({"ext": EXT, "heuristic_id": f"h/linguist/.m/{i}", "tool": "linguist-heuristics",
                         "metric": "precision", "value": round(ok / len(fired), 4), "n": len(fired),
                         "reference": ref, "note": ""})
    acc = A["C_labellers"]["vs_consensus"]
    tools = {"linguist": "linguist-heuristics (first match, else abstain)", "pygments": "pygments guess_lexer_for_filename",
             "synid": "swh-synid 9bc1c32 (file mode, default strategies)",
             "synid_nc": "swh-synid 9bc1c32 (file mode, without comment strategy)",
             "ours_v1": "study rules m-reclass/1 (frozen before judging)", "ours": "study rules m-reclass/2"}
    for lab, tool in tools.items():
        if lab not in acc:
            continue
        v = acc[lab]
        for metric, val in (("accuracy_all", v["accuracy_all"]), ("accuracy_when_answering", v["accuracy_answered"]),
                            ("abstain_rate", round(v["abstain_pct"] / 100, 4))):
            rows.append({"ext": EXT, "heuristic_id": "", "tool": tool, "metric": metric, "value": val, "n": v["n"],
                         "reference": ref, "note": ""})
        for cls, pc in v["per_class"].items():
            rows.append({"ext": EXT, "heuristic_id": "", "tool": tool, "metric": f"recall:{cls}",
                         "value": pc["recall"], "n": pc["support"], "reference": ref, "note": ""})
    fm = A["C_labellers"]["failure_modes"]
    for key, tool, note in (("pygments_matlab_as_objc", tools["pygments"], "ObjectiveCLexer.analyse_text matches MATLAB matrix literals"),
                            ("linguist_abstain_on_matlab", tools["linguist"], "MATLAB rule is ^\\s*% — no comment line, no decision"),
                            ("synid_text_on_objc", tools["synid"], "comment strategy counts '%' inside @\"%@\" and drops Objective-C"),
                            ("synid_nc_text_on_objc", tools["synid_nc"], "")):
        v = fm[key]
        rows.append({"ext": EXT, "heuristic_id": "", "tool": tool, "metric": f"failure:{key}",
                     "value": round(v["k"] / max(v["n"], 1), 4), "n": v["n"], "reference": ref, "note": note})
    su = A["C_labellers"]["synid_utf8"]
    rows.append({"ext": EXT, "heuristic_id": "", "tool": tools["synid"], "metric": "failure:unresolved_non_utf8",
                 "value": round(su["unresolved_non_utf8"] / max(su["unresolved_text"], 1), 4), "n": su["unresolved_text"],
                 "reference": "bytes", "note": "file/SquashFS hosts read strictly as UTF-8; content strategies skipped"})
    return rows


# ---------------------------------------------------------------- online review (review page)
# The audit queue, published as review items for the static review page
# (/review/study/m/, web/build_site.py). Reviews come back as GitHub issues and
# are ingested by tools/ingest_reviews.py, which calls the hooks below.
SWH = "https://archive.softwareheritage.org"
HUMAN_FIELDS = ("language", "content_type", "provenance_kind", "matlab_dialect", "confidence", "notes")
OCTAVE_RULE = ("Same rule as the judges: <b>matlab</b> = MATLAB-family code MATLAB accepts (portable code too); "
               "<b>octave</b> only if the file uses syntax MATLAB rejects (<code>#</code> comments, "
               "<code>endfunction</code>/<code>endif</code>, <code>printf</code>, <code>++</code>, <code>!=</code>). "
               "Record portability in the MATLAB-dialect field.")
# study label → encyclopedia review label (docs/reviews.md vocabulary); the exact
# study answer is kept in the record's `study` block
NOT_CODE_LABEL = {"markup-or-xml": "data:xml-like", "docs-or-text": "docs", "binary": "binary:other",
                  "config": "data:config", "data-or-expression": "data:domain", "empty-or-trivial": "noise"}


def _forge_url(row: dict) -> str:
    from urllib.parse import quote
    o, br, p = row.get("origin") or "", row.get("branch") or "", (row.get("path") or "").lstrip("/")
    b = br.replace("refs/heads/", "").replace("refs/tags/", "")
    if not (o and b and p):
        return o
    if "github.com" in o:
        return f"{o}/blob/{quote(b)}/{quote(p)}"
    if "gitlab" in o:
        return f"{o.removesuffix('.git')}/-/blob/{quote(b)}/{quote(p)}"
    if "bitbucket.org" in o:
        return f"{o}/src/{quote(b)}/{quote(p)}"
    return o


def _swh_browse_url(row: dict) -> str:
    from urllib.parse import urlencode
    q = {k: v for k, v in (("branch", row.get("branch")), ("origin_url", row.get("origin")),
                           ("path", row.get("path")), ("timestamp", row.get("ts"))) if v}
    return f"{SWH}/browse/origin/directory/?{urlencode(q)}" if row.get("origin") else ""


def review_spec(recs=None) -> dict:
    """Review items for the online page: the blind audit queue, with provenance and
    population context only — no machine label, stratum or weight (they would hint)."""
    from tools.m import audit as audit_mod
    from tools.m import taxonomy as tax
    recs = recs if recs is not None else load()
    npop = json.loads((STUDY / "name_popularity.json").read_text()) if (STUDY / "name_popularity.json").exists() else {}
    items = []
    for d in audit_mod.queue():
        r = recs.get(d["sha1_git"])
        if r is None:
            continue
        row, np_ = r.row, npop.get(r.row.get("name", ""), {})
        items.append({
            "sha1_git": r.sha, "filename": row.get("name", ""), "origin": row.get("origin", ""),
            "branch": row.get("branch", ""), "path": row.get("path", ""), "visit_ts": row.get("ts", ""),
            "forge_url": _forge_url(row), "swh_browse_url": _swh_browse_url(row),
            "qualified_swhid": SE.qualified_swhid(r.sha, row.get("origin"), row.get("path")),
            "repo_contents": row.get("repo_n", ""), "path_versions": row.get("path_versions", ""),
            "name_repos": np_.get("repos", ""), "name_contents": np_.get("contents", ""),
            "reviewed_by": sorted({(rv.get("reviewer") or {}).get("id") for rv in r.human_latest()}),
        })
    opt = lambda vals, disp=None: [{"value": v, "label": (disp or {}).get(v, v)} for v in vals]  # noqa: E731
    return {
        "schema": "review-items/1", "study": "m", "ext": EXT,
        "title": "Which language is this .m file written in?",
        "queue": "audit",
        "queue_note": ("A stratified random sample of the study's files (the blind audit). The page shows no "
                       "machine label; after you submit, the bot replies with how the two LLM judges labelled "
                       "the same files."),
        "fields": [
            {"id": "language", "label": "Language", "required": True,
             "options": opt(tax.LANGUAGES + ["unsure"], {**DISPLAY, "unsure": "unsure (skip in the estimate)"}),
             "help": OCTAVE_RULE},
            {"id": "content_type", "label": "Content type", "options": opt(tax.CONTENT_TYPES)},
            {"id": "provenance_kind", "label": "Provenance kind", "options": opt(tax.PROVENANCE_KINDS)},
            {"id": "matlab_dialect", "label": "MATLAB dialect (if MATLAB-family)", "options": opt(tax.MATLAB_DIALECTS)},
            {"id": "confidence", "label": "Your confidence", "required": True, "options": opt(tax.CONFIDENCES)},
            {"id": "notes", "label": "Notes", "type": "text"},
        ],
        "expertise": {"topics": ["MATLAB", "GNU Octave", "Objective-C", "Wolfram / Mathematica", "MUMPS",
                                 "Mercury", "Magma"],
                      "levels": ["none", "some", "expert"]},
        "items": items,
    }


def review_label(human: dict) -> str:
    """Encyclopedia label (docs/reviews.md) for a study answer."""
    lang = human.get("language") or ""
    if lang in PL:
        return PL[lang]
    if lang == "mason":
        return "pl/new:mason"
    if lang == "not-code":
        return NOT_CODE_LABEL.get(human.get("content_type") or "", "unknown")
    return "unknown"                       # other-programming-language, unknown, unsure


def judge_labels(shas: list[str]) -> dict[str, dict[str, str | None]]:
    """The two blind judges' labels (study vocabulary, normalised as in the report),
    for the reveal the ingest bot posts after a reviewer submits."""
    recs = load(with_reviews=False)
    out = {}
    for sha in shas:
        r = recs.get(sha)
        out[sha] = ({"claude-sonnet-4.6": r.lang("judge"), "gemini-3.8-flash": r.lang("judge2")}
                    if r else {})
    return out


_RECS = None


def study_reviews(s: dict) -> list[dict]:
    """Hook for tools/propagate_study.py: both blind judges (kind=llm) and the human
    audit reviews (kind=human) for one propagated sample, as reviewstore records."""
    import reviewstore as RS  # tools/ is on sys.path when called from propagate_study
    from tools.m.data import J1, J2
    global _RECS
    if _RECS is None:
        _RECS = load()
    r = _RECS.get(s["sha1_git"])
    if r is None:
        return []
    subject = {"sha1_git": s["sha1_git"], "filename": s["filename"], "ext": s["ext"]}
    out = []
    for layer, model in (("judge", J1), ("judge2", J2)):
        v, meta = r.v(layer), r.judge_meta.get(model, {})
        lab = r.lang(layer)
        if not v or lab not in PL:
            continue
        rev = RS.new_review(
            subject=subject,
            reviewer={"kind": "llm", "id": meta.get("model", model).replace("/", "-"),
                      "version": meta.get("schema"), "runner": "tools/m/judge.py",
                      "params": {"study": "m", "mode": "blind: bytes + filename + path + repository",
                                 "temperature": 0}},
            label=PL[lab], confidence=v.get("confidence") if v.get("confidence") in RS.CONFIDENCES else "medium",
            comment=v.get("language_detail"), shown={"study": "m"})
        rev["created_at"] = meta.get("judged_at") or rev["created_at"]
        out.append(rev)
    for h in r.reviews:
        hu = h.get("human") or {}
        if hu.get("language") not in PL or h.get("online"):
            continue                      # online reviews already live in reviews/ (tools/ingest_reviews.py)
        rev = RS.new_review(
            subject=subject, reviewer={"kind": "human", "id": h["reviewer"]["id"]},
            label=PL[hu["language"]],
            confidence=hu.get("confidence") if hu.get("confidence") in RS.CONFIDENCES else "medium",
            comment=hu.get("notes"),
            shown={"study": "m", "blind": bool(h.get("blind")), "audit": bool(h.get("audit"))})
        rev["created_at"] = h.get("created_at") or rev["created_at"]
        out.append(rev)
    return out


def main():
    A = json.loads((STUDY / "analysis.json").read_text())
    pop = json.loads((STUDY / "population.json").read_text())
    recs = load()
    samples = pick_samples(recs, A)
    tables = {"ext_evidence.csv": evidence_rows(A), "samples.csv": samples,
              "claims.csv": claim_rows(A, samples), "heuristic_eval.csv": heuristic_rows(recs, A)}
    SE.write_review_items("m", review_spec(recs), raw=lambda sha: SE.content_bytes("m", sha))
    meta = {"title": "What is actually in the .m extension on Software Heritage?", "extensions": [EXT],
            "case_sensitive": True, "report": REPORT, "toolkit": "tools/m/",
            "population": {"contents": pop["unique_contents"], "repositories": pop["unique_origins"],
                           "source": "SWH-m-files.zip (swh-provenance on CINES, 2026-09)"},
            "frames": {
                "file": (f"{A['n']['U_labelled']:,} .m files drawn uniformly at random; "
                         f"{A['n']['U_judged']:,} read by both LLM judges, all labelled by the study's rules, "
                         f"and all {A['M_tail_census']['U']['judged']['tail']} rare-language candidates judged"),
                "repo": (f"{A['n']['R_labelled']:,} repositories drawn uniformly at random, one random .m file each; "
                         f"{A['n']['R_judged']:,} judged, all labelled by the study's rules, "
                         f"and all {A['M_tail_census']['R']['judged']['tail']} rare-language candidates judged"),
            },
            "judges": ["anthropic/claude-sonnet-4.6 (blind)", "google/gemini-3.8-flash (blind)"],
            "human_reviews": sum(1 for r in recs.values() if r.reviews),
            "preregistration": "data/derived/m_study/PREREGISTRATION.md (eb988475)",
            "spend_usd": A["cost"]["total_usd"], "date": "2026-10-01"}
    SE.write_export("m", meta, tables)


if __name__ == "__main__":
    main()
