"""Experiment: does the cheap reclassifier match the LLM judge on the tail?

Builds an evaluation set of three groups:
  - **tail**    : files the division-gate skipped (the suspected non-COBOL);
  - **wbc**     : `WBC_*_FOO` synthetic placeholders (from the pilot cache);
  - **control** : files the judge already confirmed as COBOL.

Ground truth = the LLM judge's `cobol_confirmed` (oracle). We then score two
cheap binary classifiers against it — the deterministic **reclassifier**
(`reclassify.classify`) and the **division-gate** baseline (`n_divisions>=2`,
what run_study used) — on the task "is this COBOL?". Oracle verdicts are
cached to disk so re-runs are free.

Run (needs OPENROUTER_API_KEY):
    python3 -m tools.cobol.eval_reclassify --tail-all --wbc 20 --controls 50
Output: data/derived/cobol_study/reclassify_eval.json  (+ printed metrics)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from . import indicators as ind_mod
from . import judge as judge_mod
from . import reclassify as rc
from .common import CACHE_DIR, STUDY_DIR

REPORTS = STUDY_DIR / "reports"
ORACLE_CACHE = STUDY_DIR / "reclassify_oracle_cache.json"
OUT = STUDY_DIR / "reclassify_eval.json"


def cached_raw(sha: str) -> bytes | None:
    p = CACHE_DIR / f"{sha}.bin"
    return p.read_bytes() if p.exists() else None


def load_report(sha: str) -> dict | None:
    p = REPORTS / f"{sha}.json"
    return json.loads(p.read_text()) if p.exists() else None


def worklist(name: str):
    return list(csv.DictReader((STUDY_DIR / name).open()))


def build_items(tail_all: bool, n_wbc: int, n_controls: int) -> list[dict]:
    items, seen = [], set()

    def add(sha, name, group):
        if sha in seen or not (CACHE_DIR / f"{sha}.bin").exists():
            return
        seen.add(sha)
        items.append({"sha1_git": sha, "filename": name, "group": group})

    # tail = gated files across both studies
    tail = 0
    for wl in ("worklist_scaled.csv", "worklist_lc.csv"):
        for r in worklist(wl):
            rep = load_report(r["sha1_git"])
            j = rep and rep.get("judge")
            if isinstance(j, dict) and j.get("skipped"):
                add(r["sha1_git"], r["name"], "tail"); tail += 1
                if not tail_all and tail >= 60:
                    break

    # wbc synthetic from the pilot (seed-42) worklist
    w = 0
    for r in worklist("worklist.csv"):
        if "_FOO" in r["name"] and w < n_wbc:
            before = len(items); add(r["sha1_git"], r["name"], "wbc")
            if len(items) > before:
                w += 1

    # controls = judge-confirmed COBOL
    c = 0
    for r in worklist("worklist_scaled.csv"):
        if c >= n_controls:
            break
        rep = load_report(r["sha1_git"])
        j = rep and rep.get("judge")
        v = j.get("verdict") if isinstance(j, dict) else None
        if v and str(v.get("cobol_confirmed")).lower() == "true":
            before = len(items); add(r["sha1_git"], r["name"], "control")
            if len(items) > before:
                c += 1
    return items


def oracle_label(sha: str, name: str, cache: dict) -> dict:
    """LLM ground truth: {is_cobol, not_cobol_label}. Cached to disk."""
    if sha in cache:
        return cache[sha]
    raw = cached_raw(sha)
    text = raw.decode("utf-8", "replace")
    ind = ind_mod.compute(text)
    out = judge_mod.judge(name, ind.to_dict(), text)
    v = out.get("verdict") or {}
    res = {"is_cobol": str(v.get("cobol_confirmed")).lower() == "true",
           "not_cobol_label": v.get("not_cobol_label", ""),
           "cost": (out.get("usage") or {}).get("cost", 0)}
    cache[sha] = res
    ORACLE_CACHE.write_text(json.dumps(cache, indent=2))
    return res


def metrics(pred, truth):
    """Binary metrics with positive class = is-COBOL."""
    tp = sum(p and t for p, t in zip(pred, truth))
    fp = sum(p and not t for p, t in zip(pred, truth))
    fn = sum((not p) and t for p, t in zip(pred, truth))
    tn = sum((not p) and (not t) for p, t in zip(pred, truth))
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = (tp + tn) / len(pred) if pred else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(prec, 3), "recall": round(rec, 3),
            "f1": round(f1, 3), "accuracy": round(acc, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tail-all", action="store_true")
    ap.add_argument("--wbc", type=int, default=20)
    ap.add_argument("--controls", type=int, default=50)
    args = ap.parse_args()

    cache = json.loads(ORACLE_CACHE.read_text()) if ORACLE_CACHE.exists() else {}
    items = build_items(args.tail_all, args.wbc, args.controls)
    from collections import Counter
    print("eval set:", dict(Counter(i["group"] for i in items)), "total", len(items))

    rows, oracle_cost = [], 0.0
    for i, it in enumerate(items, 1):
        sha, name, grp = it["sha1_git"], it["filename"], it["group"]
        raw = cached_raw(sha)
        rep = load_report(sha)
        n_div = (rep or {}).get("indicators", {}).get("n_divisions", 0)
        # oracle
        if grp == "control":
            oracle = {"is_cobol": True, "not_cobol_label": "none"}
        else:
            oracle = oracle_label(sha, name, cache)
            oracle_cost += oracle.get("cost", 0) or 0
        # systems under test
        h = rc.classify(name, raw)
        rows.append({**it, "n_divisions": n_div,
                     "oracle_is_cobol": oracle["is_cobol"],
                     "oracle_not_cobol_label": oracle.get("not_cobol_label", ""),
                     "heuristic_label": h["label"],
                     "heuristic_is_cobol": h["is_cobol"],
                     "gate_is_cobol": n_div >= 2})
        if i % 20 == 0:
            print(f"  {i}/{len(items)} …")

    truth = [r["oracle_is_cobol"] for r in rows]
    m_heur = metrics([r["heuristic_is_cobol"] for r in rows], truth)
    m_gate = metrics([r["gate_is_cobol"] for r in rows], truth)

    # fine-label breakdown of what the heuristic calls non-COBOL
    fine = Counter(r["heuristic_label"] for r in rows if not r["heuristic_is_cobol"])
    # disagreements heuristic vs oracle
    disagree = [{"filename": r["filename"], "heuristic": r["heuristic_label"],
                 "oracle_is_cobol": r["oracle_is_cobol"],
                 "oracle_label": r["oracle_not_cobol_label"]}
                for r in rows if r["heuristic_is_cobol"] != r["oracle_is_cobol"]]

    result = {
        "n": len(rows), "groups": dict(Counter(r["group"] for r in rows)),
        "oracle_cost_usd": round(oracle_cost, 4),
        "heuristic_vs_oracle": m_heur,
        "division_gate_vs_oracle": m_gate,
        "heuristic_noncobol_labels": dict(fine),
        "n_disagreements": len(disagree),
        "disagreements": disagree[:25],
        "rows": rows,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n=== is-COBOL, heuristic reclassifier vs LLM oracle ===")
    print(" ", m_heur)
    print("=== is-COBOL, division-gate baseline vs LLM oracle ===")
    print(" ", m_gate)
    print("heuristic non-COBOL fine labels:", dict(fine))
    print(f"disagreements: {len(disagree)} | oracle cost ${oracle_cost:.2f}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
