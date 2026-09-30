"""Every number quoted in the `.m` report — writes data/derived/m_study/analysis.json.

  A  language by frame: by-file (U), by-repo (R), by-path (U re-weighted by
     1/path_versions), and prediction-powered (PPI) versions of U and R that
     combine the frozen v1 reclassifier on all fetched contents with the judge
     on the judged subset
  B  what the files are: content type, provenance kind, unit, maturity, domain
  C  labeller agreement: pairwise agreement and κ, accuracy against the
     two-judge consensus, abstention, and Dawid–Skene accuracy with no oracle
  D  E3 lexical vs semantic — the Octave definition (H5)
  E  E5 anchoring ablation (H6)
  F  E4 inter-model agreement per field (H7)
  G  reclassifier v1 prospective evaluation (held-out = all but U ranks 1–300)
  H  mapping stress-test: what ext_claim.csv says `.m` is vs what it is
  I  the tail catalogue and frame T (the 25 largest repositories)

    python3 -m tools.m.analysis
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from tools.m import stats as S
from tools.m import taxonomy as tax
from tools.m.data import J1, J2, J1_IND, STUDY, load

ROOT = Path(__file__).resolve().parents[2]
OUT = STUDY / "analysis.json"
N_JUDGED = 1000          # judged rank prefix in each of U and R
PPI_MAX_RANK = 2000      # PPI unlabelled pool = ranks N_JUDGED+1 .. PPI_MAX_RANK in each frame
TUNING_MAX_RANK = 300    # U ranks 1..300 = tuning split for reclassifier revisions

MAIN_LANGS = ["objective-c", "matlab", "octave", "mathematica-wolfram", "mercury", "mumps-m",
              "magma", "maple", "scilab", "limbo", "muf", "mason", "c-or-cpp",
              "other-programming-language", "not-code", "unknown"]
ABSTAIN = {"unknown", "unresolved", None}


def coarse(l):
    if l in ("matlab", "octave"):
        return "matlab-family"
    if l in ("objective-c", "mathematica-wolfram", "not-code"):
        return l
    if l in ABSTAIN:
        return "unknown"
    return "other-code"


COARSE = ["objective-c", "matlab-family", "mathematica-wolfram", "other-code", "not-code"]


def pct(x):
    return round(100 * x, 1)


def dist(values, keys=None, n=None):
    c = Counter(values)
    n = n or sum(c.values()) or 1
    items = [(k, c.get(k, 0)) for k in keys] if keys else c.most_common()
    return {k: {"n": v, "pct": pct(v / n), "ci": [pct(x) for x in S.wilson(v, n)[1:]]} for k, v in items if v}


def frames(recs):
    # binary contents are never sent to a judge; they count as "not-code" (see data.Rec.lang)
    judged = lambda r: r.v("judge") is not None or (r.labels is not None and not r.ind.get("is_text", True))  # noqa: E731
    U = [r for r in recs.values() if r.in_frame("U", N_JUDGED) and judged(r)]
    R = [r for r in recs.values() if r.in_frame("R", N_JUDGED) and judged(r)]
    T = [r for r in recs.values() if r.in_frame("T") and judged(r)]
    Uall = [r for r in recs.values() if r.in_frame("U") and r.labels]
    Rall = [r for r in recs.values() if r.in_frame("R") and r.labels]
    return U, R, T, Uall, Rall


# ---------------------------------------------------------------- A: language by frame
def section_a(U, R, Uall, Rall):
    out = {}
    L = lambda r: r.lang("judge")  # noqa: E731
    out["by_file"] = dist([L(r) for r in U])
    out["by_repo"] = dist([L(r) for r in R])
    out["by_file_coarse"] = dist([coarse(L(r)) for r in U], COARSE)
    out["by_repo_coarse"] = dist([coarse(L(r)) for r in R], COARSE)
    # by-path: one content per (origin, path) ⇔ weight 1/path_versions
    w = [1 / max(1, int(r.row["path_versions"] or 1)) for r in U]
    out["by_path_coarse"] = {}
    for c in COARSE:
        p, lo, hi, neff = S.weighted_prop([int(coarse(L(r)) == c) for r in U], w)
        out["by_path_coarse"][c] = {"pct": pct(p), "ci": [pct(lo), pct(hi)], "n_eff": round(neff)}
    # by-repo via re-weighting the by-file sample (1/repo_n) — a cross-check on R
    w2 = [1 / max(1, int(r.row["repo_n"] or 1)) for r in U]
    out["by_repo_reweighted_coarse"] = {}
    for c in COARSE:
        p, lo, hi, neff = S.weighted_prop([int(coarse(L(r)) == c) for r in U], w2)
        out["by_repo_reweighted_coarse"][c] = {"pct": pct(p), "ci": [pct(lo), pct(hi)], "n_eff": round(neff)}
    # PPI: cheap = frozen v1 reclassifier (never tuned on judged data), gold = judge
    for name, lab, allf, frame in (("ppi_by_file", U, Uall, "U"), ("ppi_by_repo", R, Rall, "R")):
        labelled = {r.sha for r in lab}
        unl = [r for r in allf if r.sha not in labelled
               and N_JUDGED < (r.u_rank if frame == "U" else r.d_rank) <= PPI_MAX_RANK]
        res = {}
        for c in COARSE:
            gold = [int(coarse(L(r)) == c) for r in lab]
            fl = [int(coarse(r.labels["ours_v1"]["lang"]) == c) for r in lab]
            fu = [int(coarse(r.labels["ours_v1"]["lang"]) == c) for r in unl]
            th, lo, hi, lam, cw, pw = S.ppi_pp_prop(gold, fl, fu)
            k = sum(gold)
            _, clo, chi = S.wilson(k, len(gold))
            res[c] = {"pct": pct(th), "ci": [pct(lo), pct(hi)], "lambda": round(lam, 3),
                      "classical_ci": [pct(clo), pct(chi)],
                      "width_ratio": round(pw / cw, 2) if cw > 0 else None}
        out[name] = {"n_labelled": len(lab), "n_unlabelled": len(unl), "classes": res}
    return out


# ---------------------------------------------------------------- B: what the files are
def section_b(U, R):
    out = {}
    for fname, fr in (("by_file", U), ("by_repo", R)):
        fr = [r for r in fr if r.v("judge")]
        V = [r.v("judge") for r in fr]
        lines = [r.ind.get("total_lines", 0) for r in fr]
        d = {k: dist([v.get(k) for v in V]) for k in
             ("content_type", "provenance_kind", "unit_kind", "maturity", "domain", "matlab_dialect")}
        d["median_lines"] = statistics.median(lines) if lines else 0
        d["is_pl_pct"] = pct(sum(bool(v.get("is_programming_language")) for v in V) / max(len(V), 1))
        per_lang = {}
        for lang in ("objective-c", "matlab"):
            sub = [r for r in fr if coarse(r.lang("judge")) == coarse(lang)]
            per_lang[lang] = {
                "n": len(sub),
                "median_lines": statistics.median([r.ind.get("total_lines", 0) for r in sub]) if sub else 0,
                **{k: dist([r.v("judge").get(k) for r in sub]) for k in
                   ("provenance_kind", "maturity", "domain", "unit_kind")},
            }
        d["per_language"] = per_lang
        rel = Counter()
        for v in V:
            for l in {x.strip() for x in (v.get("related_languages") or [])}:
                rel[l] += 1
        d["related_languages"] = {k: {"n": c, "pct": pct(c / max(len(V), 1))} for k, c in rel.most_common(20)}
        out[fname] = d
    return out


# ---------------------------------------------------------------- C: labeller agreement
LABS = ["judge", "judge2", "ours", "linguist", "pygments", "synid", "synid_nc"]
LABS_EVAL = LABS + ["ours_v1"]


def section_c(recs_j):
    out = {}
    fine = lambda r, l: r.lang(l)  # noqa: E731
    crs = lambda r, l: None if r.lang(l) is None else coarse(r.lang(l))  # noqa: E731
    out["pairwise_fine"] = S.pairwise(recs_j, LABS, fine)
    out["pairwise_coarse"] = S.pairwise(recs_j, LABS, crs)
    # consensus = the two independent LLMs agree (coarse)
    cons = [r for r in recs_j if r.lang("judge2") and coarse(r.lang("judge")) == coarse(r.lang("judge2"))]
    out["consensus_n"] = len(cons)
    out["consensus_of"] = sum(1 for r in recs_j if r.lang("judge2"))
    acc = {}
    for lab in LABS_EVAL:
        xs = [(coarse(r.lang("judge")), r.lang(lab)) for r in cons if r.lang(lab) is not None]
        if not xs:
            continue
        abst = sum(1 for _, y in xs if y in ABSTAIN)
        answered = [(g, y) for g, y in xs if y not in ABSTAIN]
        correct = sum(1 for g, y in answered if coarse(y) == g)
        per = {}
        for c in COARSE:
            tp = sum(1 for g, y in answered if g == c and coarse(y) == c)
            fn = sum(1 for g, y in xs if g == c and (y in ABSTAIN or coarse(y) != c))
            fp = sum(1 for g, y in answered if g != c and coarse(y) == c)
            per[c] = {"support": tp + fn, "recall": round(tp / max(tp + fn, 1), 3),
                      "precision": round(tp / max(tp + fp, 1), 3) if tp + fp else None}
        acc[lab] = {"n": len(xs), "abstain_pct": pct(abst / len(xs)),
                    "accuracy_answered": round(correct / max(len(answered), 1), 4),
                    "accuracy_all": round(correct / len(xs), 4), "per_class": per}
    out["vs_consensus"] = acc
    # specific failure modes
    ml = [r for r in cons if coarse(r.lang("judge")) == "matlab-family"]
    oc = [r for r in cons if coarse(r.lang("judge")) == "objective-c"]
    out["failure_modes"] = {
        "pygments_matlab_as_objc": {"k": sum(r.lang("pygments") == "objective-c" for r in ml), "n": len(ml)},
        "linguist_abstain_on_matlab": {"k": sum(r.lang("linguist") in ABSTAIN for r in ml), "n": len(ml)},
        "synid_text_on_objc": {"k": sum(r.lang("synid") == "unknown" for r in oc), "n": len(oc)},
        "synid_nc_text_on_objc": {"k": sum(r.lang("synid_nc") == "unknown" for r in oc), "n": len(oc)},
        "synid_unresolved_all": {"k": sum(r.lang("synid") == "unresolved" for r in cons), "n": len(cons)},
        "synid_text_all": {"k": sum(r.lang("synid") == "unknown" for r in cons), "n": len(cons)},
        "linguist_abstain_all": {"k": sum(r.lang("linguist") in ABSTAIN for r in cons), "n": len(cons)},
    }
    # Synid's "unresolved" (full candidate set) vs UTF-8 validity of the bytes
    from tools.cobol.common import CACHE_DIR

    def utf8(r):
        try:
            (CACHE_DIR / f"{r.sha}.bin").read_bytes().decode("utf-8")
            return True
        except (UnicodeDecodeError, FileNotFoundError):
            return False
    txt = [r for r in recs_j if r.ind.get("is_text", True)]
    unres = [r for r in txt if r.lang("synid") == "unresolved"]
    res_ = [r for r in txt if r.lang("synid") not in ("unresolved", None)]
    out["synid_utf8"] = {"unresolved_text": len(unres), "unresolved_non_utf8": sum(not utf8(r) for r in unres),
                         "unresolved_matlab": sum(r.lang("judge") == "matlab" for r in unres),
                         "unresolved_matlab_with_pct_comment": sum(r.lang("judge") == "matlab" and
                                                                   r.ind.get("ml_pct_comments", 0) > 0 for r in unres),
                         "resolved_text": len(res_), "resolved_non_utf8": sum(not utf8(r) for r in res_)}
    # Dawid–Skene, coarse classes, abstentions as missing, NO labeller privileged
    items = {}
    for r in recs_j:
        d = {}
        for lab in LABS:
            y = r.lang(lab)
            if y is not None and y not in ABSTAIN:
                d[lab] = coarse(y)
        if d:
            items[r.sha] = d
    post, conf, prior = S.dawid_skene(items, COARSE)
    out["dawid_skene"] = {"n_items": len(items), "prior": dict(zip(COARSE, [round(p, 4) for p in prior])),
                          "accuracy": {k: round(v, 4) for k, v in S.ds_accuracy(conf, prior).items()},
                          "note": "abstentions treated as missing; assumes conditional independence "
                                  "(violated: synid embeds the Linguist rules and Pygments scorers)"}
    ds_label = {it: COARSE[max(range(len(COARSE)), key=lambda k: p[k])] for it, p in post.items()}
    out["dawid_skene"]["agrees_with_judge_pct"] = pct(
        sum(ds_label[r.sha] == coarse(r.lang("judge")) for r in recs_j if r.sha in ds_label) / max(len(ds_label), 1))
    return out


# ---------------------------------------------------------------- D: Octave, lexical vs semantic
def section_d(recs_j):
    ml = [r for r in recs_j if coarse(r.lang("judge")) == "matlab-family"]

    def lexical_octave(r):
        i = r.ind
        return (i.get("oct_block_ends", 0) + i.get("oct_hash_comments", 0) + i.get("oct_printf", 0)
                + i.get("oct_ne", 0) + int(bool(i.get("oct_script_marker")))) > 0

    def lexical_v2(r):
        return r.ind.get("octave_syntax_v2", 0) > 0

    tab_v2 = Counter((r.lang("judge"), lexical_v2(r)) for r in ml)
    j2_v2 = Counter((r.lang("judge2"), lexical_v2(r)) for r in ml if r.lang("judge2"))
    ours_v2 = Counter((r.lang("ours"), lexical_v2(r)) for r in ml)
    ecosystem = Counter((r.lang("judge"), bool(r.ind.get("oct_ecosystem")), lexical_v2(r)) for r in ml
                        if r.lang("judge") == "octave")
    tab = Counter((r.lang("judge"), lexical_octave(r)) for r in ml)
    tab2 = Counter((r.v("judge").get("matlab_dialect"), lexical_octave(r)) for r in ml)
    j2 = Counter((r.lang("judge2"), lexical_octave(r)) for r in ml if r.lang("judge2"))
    ex = [{"sha": r.sha, "name": r.row["name"], "judge": r.lang("judge"),
           "markers": {k: r.ind.get(k) for k in ("oct_block_ends", "oct_hash_comments", "oct_printf",
                                                  "oct_ne", "oct_script_marker") if r.ind.get(k)}}
          for r in ml if (r.lang("judge") == "octave") != lexical_octave(r)][:40]
    ex2 = [{"sha": r.sha, "name": r.row["name"], "judge": r.lang("judge"), "judge2": r.lang("judge2"),
            "path": r.row.get("path"), "ecosystem": r.ind.get("oct_ecosystem"),
            "v2": {k: r.ind.get(k) for k in ("oct_block_ends", "oct_hash_comments", "oct_code_printf",
                                             "oct_code_ne", "oct_code_incr") if r.ind.get(k)}}
           for r in ml if (r.lang("judge") == "octave") != lexical_v2(r)]
    ml_u = [r for r in ml if r.in_frame("U", N_JUDGED)]
    ml_only = sum(1 for r in ml_u if r.ind.get("ml_classdef") or r.ind.get("ml_arguments_block")
                  or r.ind.get("ml_matlab_ns") or r.ind.get("ml_guide"))
    portability = {
        "n_by_file": len(ml_u),
        "judge": dict(Counter(r.v("judge").get("matlab_dialect") for r in ml_u).most_common()),
        "judge2": dict(Counter(r.v("judge2").get("matlab_dialect") for r in ml_u if r.v("judge2")).most_common()),
        "lexical_matlab_only_features": ml_only,
    }
    return {"n_matlab_family": len(ml), "portability": portability,
            "judge_x_lexical_v2": {f"{a}|lexical_octave={b}": c for (a, b), c in tab_v2.items()},
            "judge2_x_lexical_v2": {f"{a}|lexical_octave={b}": c for (a, b), c in j2_v2.items()},
            "ours_x_lexical_v2": {f"{a}|lexical_octave={b}": c for (a, b), c in ours_v2.items()},
            "judge_octave_by_ecosystem_marker": {f"ecosystem={b}|syntax={c}": n for (_, b, c), n in ecosystem.items()},
            "disagreements_v2": ex2,
            "judge_x_lexical": {f"{a}|lexical_octave={b}": c for (a, b), c in tab.items()},
            "dialect_x_lexical": {f"{a}|lexical_octave={b}": c for (a, b), c in tab2.items()},
            "judge2_x_lexical": {f"{a}|lexical_octave={b}": c for (a, b), c in j2.items()},
            "disagreements": ex}


# ---------------------------------------------------------------- E: anchoring ablation
def section_e(recs):
    both = [r for r in recs.values() if r.v("judge") and r.v("judge_ind")]
    if not both:
        return {"n": 0}
    a_blind = sum(r.lang("judge") == r.labels["ours"]["lang"] for r in both) / len(both)
    a_ind = sum(r.lang("judge_ind") == r.labels["ours"]["lang"] for r in both) / len(both)
    flips = [r for r in both if r.lang("judge") != r.lang("judge_ind")]
    toward = sum(r.lang("judge_ind") == r.labels["ours"]["lang"] for r in flips)
    fields = {}
    for k in ("language", "content_type", "provenance_kind", "unit_kind", "matlab_dialect", "maturity", "domain"):
        fields[k] = round(sum(r.v("judge").get(k) == r.v("judge_ind").get(k) for r in both) / len(both), 3)
    return {"n": len(both), "agree_with_ours_blind": pct(a_blind), "agree_with_ours_shown": pct(a_ind),
            "language_flips": len(flips), "flips_toward_ours": toward,
            "self_agreement_by_field": fields,
            "flip_examples": [{"name": r.row["name"], "blind": r.lang("judge"), "shown": r.lang("judge_ind"),
                               "ours": r.labels["ours"]["lang"]} for r in flips[:20]]}


# ---------------------------------------------------------------- F: inter-model agreement
def section_f(recs_j):
    both = [r for r in recs_j if r.v("judge2")]
    out = {"n": len(both)}
    for k in ("language", "content_type", "is_programming_language", "provenance_kind", "unit_kind",
              "matlab_dialect", "maturity", "domain", "confidence"):
        a = [str(r.v("judge").get(k)) for r in both]
        b = [str(r.v("judge2").get(k)) for r in both]
        out[k] = {"agree": round(sum(x == y for x, y in zip(a, b)) / max(len(both), 1), 3),
                  "kappa": round(S.cohen_kappa(a, b), 3)}
    out["language_coarse"] = {
        "agree": round(sum(coarse(r.lang("judge")) == coarse(r.lang("judge2")) for r in both) / max(len(both), 1), 4),
        "kappa": round(S.cohen_kappa([coarse(r.lang("judge")) for r in both],
                                     [coarse(r.lang("judge2")) for r in both]), 3)}
    conf = Counter((r.lang("judge"), r.lang("judge2")) for r in both if r.lang("judge") != r.lang("judge2"))
    out["language_disagreements"] = {f"{a} vs {b}": c for (a, b), c in conf.most_common(20)}
    pk = Counter((r.v("judge").get("provenance_kind"), r.v("judge2").get("provenance_kind"))
                 for r in both if r.v("judge").get("provenance_kind") != r.v("judge2").get("provenance_kind"))
    out["provenance_disagreements"] = {f"{a} vs {b}": c for (a, b), c in pk.most_common(12)}
    return out


# ---------------------------------------------------------------- G: reclassifier evaluation
def section_g(recs_j):
    held = [r for r in recs_j if not (r.u_rank and r.u_rank <= TUNING_MAX_RANK)]
    tune = [r for r in recs_j if r.u_rank and r.u_rank <= TUNING_MAX_RANK]
    out = {"n_heldout": len(held), "n_tuning": len(tune)}
    for ver, ref, pool in (("v1", "judge", held), ("v1", "consensus", held), ("v2", "judge", held),
                           ("v2", "consensus", held), ("v1", "judge_tuning", tune), ("v2", "judge_tuning", tune)):
        key = "ours_v1" if ver == "v1" else "ours"
        xs = []
        for r in pool:
            if ref == "consensus":
                if not r.lang("judge2") or coarse(r.lang("judge")) != coarse(r.lang("judge2")):
                    continue
            xs.append((r.lang("judge"), r.labels[key]["lang"]))
        fine_acc = sum(g == y for g, y in xs) / max(len(xs), 1)
        coarse_acc = sum(coarse(g) == coarse(y) for g, y in xs) / max(len(xs), 1)
        per = {}
        for c in COARSE:
            tp = sum(1 for g, y in xs if coarse(g) == c and coarse(y) == c)
            fn = sum(1 for g, y in xs if coarse(g) == c and coarse(y) != c)
            fp = sum(1 for g, y in xs if coarse(g) != c and coarse(y) == c)
            p = tp / (tp + fp) if tp + fp else None
            rr = tp / (tp + fn) if tp + fn else None
            f1 = 2 * p * rr / (p + rr) if p and rr else None
            per[c] = {"support": tp + fn, "precision": p and round(p, 3), "recall": rr and round(rr, 3),
                      "f1": f1 and round(f1, 3)}
        errs = Counter((g, y) for g, y in xs if coarse(g) != coarse(y))
        out[f"{ver}_{ref}"] = {"n": len(xs), "fine_accuracy": round(fine_acc, 4),
                               "coarse_accuracy": round(coarse_acc, 4), "per_class": per,
                               "errors": {f"{g} → {y}": c for (g, y), c in errs.most_common(15)}}
    return out


# ---------------------------------------------------------------- H: mapping stress test
def section_h(U, R):
    claims = defaultdict(list)
    p = ROOT / "data" / "derived" / "pl_taxonomy" / "ext_claim.csv"
    for row in csv.DictReader(p.open(encoding="utf-8")):
        if row["ext"] in (".m", ".M"):
            claims[row["pl_id"]].append(f"{row['source']}:{row['strength']}")
    lang_to_pl = dict(tax.MAPPING_CLAIMS)
    obsU = Counter(r.lang("judge") for r in U)
    obsR = Counter(r.lang("judge") for r in R)
    rows = []
    for lang in MAIN_LANGS:
        pl = lang_to_pl.get(lang)
        rows.append({"language": lang, "pl_id": pl, "claimed_by": claims.get(pl, []) if pl else [],
                     "by_file_n": obsU.get(lang, 0), "by_file_pct": pct(obsU.get(lang, 0) / max(len(U), 1)),
                     "by_repo_n": obsR.get(lang, 0), "by_repo_pct": pct(obsR.get(lang, 0) / max(len(R), 1))})
    spurious = [pl for pl in claims if pl not in lang_to_pl.values()]
    return {"claims": {k: v for k, v in claims.items()}, "rows": rows,
            "claims_without_language_in_taxonomy": spurious}


# ---------------------------------------------------------------- I: tail + frame T
def section_i(recs, U, R, T):
    tail = []
    for r in {x.sha: x for x in U + R}.values():
        if coarse(r.lang("judge")) in ("objective-c", "matlab-family"):
            continue
        v = r.v("judge") or {"language_detail": "binary (not sent to the judges)", "content_type": "binary"}
        tail.append({"sha": r.sha, "frame": "U" if r in U else "R", "name": r.row["name"],
                     "origin": r.row["origin"], "judge": r.lang("judge"), "detail": v.get("language_detail"),
                     "judge2": r.lang("judge2"), "ours": r.labels["ours"]["lang"], "synid": r.lang("synid"),
                     "content_type": v.get("content_type"), "provenance": v.get("provenance_detail")})
    top = defaultdict(list)
    for r in T:
        v = r.v("judge") or {"content_type": "binary", "provenance_kind": "unknown", "language_detail": "binary"}
        top[r.row["origin"]].append({"name": r.row["name"], "language": r.lang("judge"),
                                     "content_type": v.get("content_type"),
                                     "provenance_kind": v.get("provenance_kind"),
                                     "detail": v.get("provenance_detail") or v.get("language_detail")})
    pop = json.loads((STUDY / "population.json").read_text())
    top_rows = []
    for t in pop["top_repos"]:
        top_rows.append({**t, "sampled": top.get(t["origin"], [])})
    mostly_not_hand = sum(1 for rows in top.values()
                          if sum(1 for x in rows if x["provenance_kind"] != "hand-written") >= 3)
    return {"tail": sorted(tail, key=lambda x: (x["judge"] or "", x["name"])), "top_repos": top_rows,
            "top_mostly_not_hand_written": mostly_not_hand, "top_n_repos": len(top)}


# ---------------------------------------------------------------- J: duplication signals
def section_j(U, R):
    pop_path = STUDY / "name_popularity.json"
    npop = json.loads(pop_path.read_text()) if pop_path.exists() else {}
    out = {}
    for fname, fr in (("by_file", U), ("by_repo", R)):
        fr = [r for r in fr if r.v("judge")]
        by_prov = defaultdict(list)
        for r in fr:
            nm = npop.get(r.row["name"], {})
            by_prov[r.v("judge").get("provenance_kind")].append(nm.get("repos", 0))
        out[fname] = {k: {"n": len(v), "median_name_repos": statistics.median(v) if v else 0,
                          "quartiles": statistics.quantiles(v, n=4) if len(v) >= 4 else None}
                      for k, v in by_prov.items()}
        vers = [int(r.row["path_versions"] or 1) for r in fr]
        out[fname]["path_versions_median"] = statistics.median(vers) if vers else 0
    return out


# ---------------------------------------------------------------- L: near-duplicate templates
def section_l(recs):
    """Distinct contents vs distinct after stripping `//` comment lines, for Xcode template names."""
    import hashlib
    from tools.cobol.common import CACHE_DIR
    groups = defaultdict(list)
    for r in recs.values():
        in_scope = r.in_frame("U", PPI_MAX_RANK) or r.in_frame("R", PPI_MAX_RANK)
        if r.row["name"] in ("main.m", "AppDelegate.m", "ViewController.m", "SceneDelegate.m") and r.labels and in_scope:
            p = CACHE_DIR / f"{r.sha}.bin"
            if p.exists():
                groups[r.row["name"]].append(p.read_bytes().decode("utf-8", "replace"))
    out = {}
    for name, texts in groups.items():
        c = Counter(hashlib.md5("\n".join(l.rstrip() for l in t.split("\n")
                                           if l.strip() and not l.strip().startswith("//")).encode()).hexdigest()
                    for t in texts)
        out[name] = {"distinct_contents": len(texts), "distinct_without_comments": len(c),
                     "largest_cluster": c.most_common(1)[0][1] if c else 0}
    return out


# ---------------------------------------------------------------- K: pre-registration scorecard
def section_k(res, U, R, recs_j):
    a, b, c, d, e, f = (res["A_language"], res["B_what"], res["C_labellers"], res["D_octave"],
                        res["E_anchoring"], res["F_intermodel"])
    out = {}
    big = a["by_file_coarse"].get("objective-c", {}).get("pct", 0) + a["by_file_coarse"].get("matlab-family", {}).get("pct", 0)
    tail_langs = sorted({r.lang("judge") for r in recs_j} - {"objective-c", "matlab", "octave", "unknown", None})
    out["H1"] = {"claim": "by file, Objective-C + MATLAB-family >= 95%; remainder <= 5% spanning >= 6 languages/formats",
                 "observed": f"{big:.1f}% ; remainder {100 - big:.1f}% ; {len(tail_langs)} distinct: {', '.join(tail_langs)}",
                 "verdict": "supported" if big >= 95 and len(tail_langs) >= 6 else "not supported"}
    oc_f = a["by_file_coarse"].get("objective-c", {}).get("pct", 0)
    oc_r = a["by_repo_coarse"].get("objective-c", {}).get("pct", 0)
    out["H2"] = {"claim": "Objective-C share differs by >= 10 points between by-file and by-repo (weak guess: higher by file)",
                 "observed": f"by file {oc_f:.1f}% vs by repo {oc_r:.1f}% (diff {oc_r - oc_f:+.1f})",
                 "verdict": ("supported" if abs(oc_r - oc_f) >= 10 else "not supported")
                 + ("; direction guess wrong" if oc_r > oc_f else "; direction guess right")}
    pk = b["by_file"]["per_language"]["objective-c"]["provenance_kind"]
    nonhand = 100 - pk.get("hand-written", {}).get("pct", 0)
    out["H3"] = {"claim": "by file, >= 15% of Objective-C files are not hand-written",
                 "observed": f"{nonhand:.1f}% not hand-written",
                 "verdict": "supported" if nonhand >= 15 else "not supported"}
    fm = c["failure_modes"]
    la = 100 * fm["linguist_abstain_all"]["k"] / max(fm["linguist_abstain_all"]["n"], 1)
    pm = 100 * fm["pygments_matlab_as_objc"]["k"] / max(fm["pygments_matlab_as_objc"]["n"], 1)
    st = 100 * (fm["synid_text_all"]["k"] + fm["synid_unresolved_all"]["k"]) / max(fm["synid_text_all"]["n"], 1)
    out["H4"] = {"claim": "Linguist abstains >= 5%; Pygments MATLAB->ObjC >= 5% of MATLAB; Synid Text/unresolved >= 10% "
                          "(descriptive: glimpsed during calibration)",
                 "observed": f"Linguist abstains {la:.1f}%; Pygments {pm:.1f}%; Synid {st:.1f}%",
                 "verdict": ("consistent" if la >= 5 and pm >= 5 and st >= 10 else "partly consistent")}
    jl = d["judge_x_lexical"]
    oct_nolex = jl.get("octave|lexical_octave=False", 0)
    mat_lex = jl.get("matlab|lexical_octave=True", 0)
    one_sided = max(oct_nolex, mat_lex) >= 5 and max(oct_nolex, mat_lex) >= 3 * max(1, min(oct_nolex, mat_lex))
    j2 = d.get("judge_x_lexical_v2", {})
    o2, m2 = j2.get("octave|lexical_octave=False", 0), j2.get("matlab|lexical_octave=True", 0)
    one_sided_v2 = max(o2, m2) >= 5 and max(o2, m2) >= 3 * max(1, min(o2, m2))
    g2 = d.get("judge2_x_lexical_v2", {})
    out["H5"] = {"claim": "judge's octave label disagrees with the lexical definition, one-sidedly",
                 "observed": (f"as registered (regex markers): octave-without-syntax {oct_nolex} vs matlab-with-syntax "
                              f"{mat_lex}; post-hoc, comment/string-aware markers: {o2} vs {m2} "
                              f"(judge 2: {g2.get('octave|lexical_octave=False', 0)} vs "
                              f"{g2.get('matlab|lexical_octave=True', 0)})"),
                 "verdict": ("supported" if one_sided else "not supported as registered")
                 + ("; supported post-hoc for judge 1 only" if one_sided_v2 and not one_sided else "")}
    if e.get("n"):
        toward = e["flips_toward_ours"]
        away = e["language_flips"] - toward
        out["H6"] = {"claim": "shown the indicators, the judge agrees more with our reclassifier",
                     "observed": f"blind {e['agree_with_ours_blind']}% vs shown {e['agree_with_ours_shown']}% "
                                 f"(n={e['n']}; {toward} flips toward ours, {away} away)",
                     "verdict": "supported" if e["agree_with_ours_shown"] > e["agree_with_ours_blind"] + 1 else "not supported"}
    if f.get("n"):
        kl, kp, km = f["language"]["kappa"], f["provenance_kind"]["kappa"], f["maturity"]["kappa"]
        out["H7"] = {"claim": "kappa(language) >= 0.9; kappa(provenance_kind) < 0.7 and kappa(maturity) < 0.7",
                     "observed": f"language {kl:.2f}; provenance_kind {kp:.2f}; maturity {km:.2f}",
                     "verdict": ("supported" if kl >= .9 and kp < .7 and km < .7 else
                                 "partly supported" if kl >= .9 else "not supported")}
    return out


def judge_costs() -> dict:
    """Everything paid, per judge layer — including failed calls kept under _failed/."""
    from tools.m.data import JUDGE
    out = {}
    for d in sorted(JUDGE.glob("*")) if JUDGE.exists() else []:
        files = list(d.glob("*.json")) + list(d.glob("_failed/*.json"))
        cost = sum((json.loads(p.read_text()).get("usage") or {}).get("cost", 0) or 0 for p in files)
        ok = sum(1 for p in d.glob("*.json") if json.loads(p.read_text()).get("parse_ok"))
        out[d.name] = {"calls": len(files), "parsed": ok, "failed_retried": len(list(d.glob("_failed/*.json"))),
                       "usd": round(cost, 2)}
    out["total_usd"] = round(sum(v["usd"] for v in out.values() if isinstance(v, dict)), 2)
    return out


def main():
    recs = load()
    U, R, T, Uall, Rall = frames(recs)
    recs_j = list({r.sha: r for r in U + R}.values())
    res = {
        "n": {"U_judged": len(U), "R_judged": len(R), "T_judged": len(T),
              "U_labelled": len(Uall), "R_labelled": len(Rall),
              "U_used": sum(1 for r in Uall if r.u_rank <= PPI_MAX_RANK),
              "R_used": sum(1 for r in Rall if r.d_rank <= PPI_MAX_RANK),
              "judge2": sum(1 for r in recs_j if r.v("judge2")),
              "judge_ind": sum(1 for r in recs.values() if r.v("judge_ind"))},
        "cost": judge_costs(),
        "A_language": section_a(U, R, Uall, Rall),
        "B_what": section_b(U, R),
        "C_labellers": section_c(recs_j),
        "D_octave": section_d(recs_j),
        "E_anchoring": section_e(recs),
        "F_intermodel": section_f(recs_j),
        "G_reclassifier": section_g(recs_j),
        "H_mapping": section_h(U, R),
        "I_tail": section_i(recs, U, R, T),
        "J_duplication": section_j(U, R),
        "L_near_duplicates": section_l(recs),
    }
    res["K_prereg"] = section_k(res, U, R, recs_j)
    OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    a = res["A_language"]
    print("n:", res["n"], "cost:", res["cost"])
    for k in ("by_file_coarse", "by_repo_coarse", "by_path_coarse", "by_repo_reweighted_coarse"):
        print(f"{k:28}", {c: v["pct"] for c, v in a[k].items()})
    for k in ("ppi_by_file", "ppi_by_repo"):
        print(f"{k:28}", {c: (v["pct"], v["width_ratio"]) for c, v in a[k]["classes"].items()})
    print("vs consensus:", {k: (v["accuracy_all"], v["abstain_pct"]) for k, v in res["C_labellers"]["vs_consensus"].items()})
    print("DS accuracy:", res["C_labellers"]["dawid_skene"]["accuracy"])
    print("failure modes:", res["C_labellers"]["failure_modes"])
    print("octave:", res["D_octave"]["judge_x_lexical"])
    print("anchoring:", {k: v for k, v in res["E_anchoring"].items() if k not in ("flip_examples",)})
    print("intermodel:", {k: v for k, v in res["F_intermodel"].items() if isinstance(v, dict) and "kappa" in v})
    print("reclass:", {k: (v["fine_accuracy"], v["coarse_accuracy"], v["n"]) for k, v in res["G_reclassifier"].items()
                       if isinstance(v, dict)})
    for h, v in res["K_prereg"].items():
        print(f"{h}: {v['verdict']:28} | {v['observed']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
