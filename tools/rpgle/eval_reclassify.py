"""E3 — validate the zero-API mechanical layer against the LLM-judge oracle.

For `.cbl` the discriminating question was "is this even COBOL?" (46% was not).
For `.rpgle` the extension is clean, so a naive "always rpgle" classifier is
already ~98% accurate; that target is uninformative. The discriminating axes
here are *which RPG dialect* and *program vs copy member*, so those are what we
validate. The lesson: the validation target must follow the axis that actually
varies in the population.

    python3 -m tools.rpgle.eval_reclassify
"""

from __future__ import annotations

import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "rpgle_study"
RPGLE_LABELS = {"rpgle", "rpgle-copybook"}


def V(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return round(p, 3), round(r, 3), round(f, 3)


def binary(name, pairs):
    """pairs: list of (pred_bool, gold_bool)"""
    tp = sum(1 for p, g in pairs if p and g)
    fp = sum(1 for p, g in pairs if p and not g)
    fn = sum(1 for p, g in pairs if not p and g)
    tn = sum(1 for p, g in pairs if not p and not g)
    P, R, F = prf(tp, fp, fn)
    base = max(tp + fn, tn + fp) / len(pairs) if pairs else 0
    print(f"\n## {name}  (n={len(pairs)})")
    print(f"   TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"   precision={P}  recall={R}  F1={F}  accuracy={round((tp+tn)/len(pairs),3)}")
    print(f"   majority-class baseline accuracy={round(base,3)}")
    return {"n": len(pairs), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": P, "recall": R, "f1": F,
            "accuracy": round((tp + tn) / len(pairs), 3),
            "baseline_accuracy": round(base, 3)}


def multiclass(name, pairs, labels):
    """pairs: list of (pred, gold)"""
    conf = Counter(pairs)
    acc = sum(v for (p, g), v in conf.items() if p == g) / len(pairs)
    print(f"\n## {name}  (n={len(pairs)}, accuracy={round(acc,3)})")
    hdr = "pred\\gold".ljust(16) + "".join(l[:13].rjust(14) for l in labels)
    print("  " + hdr)
    for p in labels:
        print("  " + p[:15].ljust(16) + "".join(str(conf.get((p, g), 0)).rjust(14) for g in labels))
    per = {}
    f1s = []
    for l in labels:
        tp = conf.get((l, l), 0)
        fp = sum(v for (pp, g), v in conf.items() if pp == l and g != l)
        fn = sum(v for (pp, g), v in conf.items() if pp != l and g == l)
        P, R, F = prf(tp, fp, fn)
        per[l] = {"precision": P, "recall": R, "f1": F, "support": tp + fn}
        f1s.append(F)
        print(f"    {l:28} P={P:<6} R={R:<6} F1={F:<6} support={tp+fn}")
    macro = round(sum(f1s) / len(f1s), 3)
    base = max(Counter(g for _, g in pairs).values()) / len(pairs)
    print(f"   macro-F1={macro}   majority-class baseline accuracy={round(base,3)}")
    return {"n": len(pairs), "accuracy": round(acc, 3), "macro_f1": macro,
            "baseline_accuracy": round(base, 3), "per_class": per}


def main():
    reps = [json.loads(Path(p).read_text()) for p in glob.glob(str(STUDY / "reports" / "*.json"))]
    judged = [r for r in reps if V(r) and V(r).get("confidence") != "low"]
    print(f"oracle: {len(judged)} judged contents (of {len(reps)} fetched)")

    out = {}

    # --- T1: is-RPGLE (kept for comparability with the .cbl study) ---
    out["is_rpgle"] = binary("T1 · is-RPGLE  (mechanical looks_rpgle/copybook vs judge)", [
        (r["reclass"]["label"] in RPGLE_LABELS,
         bool(V(r).get("is_programming_language")) and
         V(r).get("content_type") in ("source-code", "copybook-or-header"))
        for r in judged])

    # --- T2: source format (the axis that actually varies) ---
    LBL = ["fully-free", "hybrid-free", "fixed-format"]
    pairs = [(r["indicators"]["source_format_guess"], V(r).get("source_format"))
             for r in judged
             if V(r).get("source_format") in LBL and r["indicators"]["source_format_guess"] in LBL]
    if pairs:
        out["source_format"] = multiclass("T2 · RPG source format (3-class)", pairs, LBL)

    # how often does the indicator abstain / disagree wildly?
    abst = sum(1 for r in judged if r["indicators"]["source_format_guess"] == "unknown")
    print(f"\n   indicator abstained ('unknown') on {abst}/{len(judged)} "
          f"({round(100*abst/max(len(judged),1))}%)")
    out["source_format_abstain_pct"] = round(100 * abst / max(len(judged), 1), 1)

    # --- T3: copy member vs compilable unit ---
    out["copybook"] = binary("T3 · /copy prototype-header member", [
        (bool(r["indicators"]["looks_copybook"]),
         V(r).get("unit_kind") == "copybook-prototype-header" or
         V(r).get("content_type") == "copybook-or-header")
        for r in judged])

    # --- error inspection ---
    print("\n## T3 false negatives (judge says copy member, indicators say no) — first 6")
    for r in judged:
        gold = (V(r).get("unit_kind") == "copybook-prototype-header" or
                V(r).get("content_type") == "copybook-or-header")
        if gold and not r["indicators"]["looks_copybook"]:
            i = r["indicators"]
            print(f"   {r['name'][:28]:30} dcl_pr={i['n_dcl_pr']} dcl_proc={i['n_dcl_proc']} "
                  f"cond={i['n_cond_directives']} fmt={i['source_format_guess']}")

    (STUDY / "eval_reclassify.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {STUDY / 'eval_reclassify.json'}")


if __name__ == "__main__":
    main()
