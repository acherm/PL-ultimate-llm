"""Human audit of the `.m` labellers — the step the three earlier studies never closed.

`--build` draws a **stratified random** audit sample from the judged by-file
frame (U, ranks ≤ 1000):
  stratum "agree"    every labeller that answered gives the same coarse language
  stratum "disagree" at least one labeller dissents (incl. the two LLMs)
Disagreements are over-sampled (where the information is), and each item keeps
its inverse-probability weight N_h / n_h, so accuracies estimated on the audit
generalise to the whole by-file population instead of to "the hard cases".

`--score` reads `reviews_m/` (human labels, from the review app) and reports,
for every labeller, IPW accuracy against the human label with a Kish-n CI.

    python3 -m tools.m.audit --build --n-agree 40 --n-disagree 60 --seed 23
    python3 -m tools.m.audit --score
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json

from tools.m import stats as S
from tools.m.analysis import ABSTAIN, LABS, N_JUDGED, coarse
from tools.m.data import STUDY, load

QUEUE = STUDY / "audit_queue.csv"


def stratum(r) -> str:
    ans = {coarse(r.lang(l)) for l in LABS if r.lang(l) is not None and r.lang(l) not in ABSTAIN}
    return "agree" if len(ans) <= 1 else "disagree"


def build(n_agree: int, n_dis: int, seed: int):
    recs = load(with_reviews=False)
    U = [r for r in recs.values() if r.in_frame("U", N_JUDGED) and r.v("judge") and r.labels]
    strata = {"agree": [], "disagree": []}
    for r in U:
        strata[stratum(r)].append(r)
    want = {"agree": n_agree, "disagree": n_dis}
    rows = []
    for h, items in strata.items():
        items.sort(key=lambda r: hashlib.md5(f"{r.sha}|A|{seed}".encode()).hexdigest())
        pick = items[: want[h]]
        w = len(items) / max(len(pick), 1)
        for k, r in enumerate(pick, 1):
            rows.append({"sha1_git": r.sha, "stratum": h, "stratum_N": len(items), "stratum_n": len(pick),
                         "weight": round(w, 4), "order": 0, "name": r.row["name"]})
    # interleave strata in a seeded order so a partial audit is still balanced
    rows.sort(key=lambda d: hashlib.md5(f"{d['sha1_git']}|O|{seed}".encode()).hexdigest())
    for i, d in enumerate(rows, 1):
        d["order"] = i
    with QUEUE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"strata: agree N={len(strata['agree'])} disagree N={len(strata['disagree'])} → "
          f"audit {sum(1 for r in rows if r['stratum']=='agree')}+{sum(1 for r in rows if r['stratum']=='disagree')} "
          f"→ {QUEUE}")


def queue() -> list[dict]:
    if not QUEUE.exists():
        return []
    return sorted(csv.DictReader(QUEUE.open(encoding="utf-8")), key=lambda d: int(d["order"]))


def score(verbose=True) -> dict:
    recs = load()
    q = queue()
    done = [(d, recs[d["sha1_git"]]) for d in q if recs[d["sha1_git"]].reviews]
    revised = sum(1 for _, r in done if len(r.reviews) > 1 and r.reviews[0].get("blind")
                  and not r.reviews[-1].get("blind"))
    out = {"n_queue": len(q), "n_reviewed": len(done), "revised_after_unblinding": revised, "labellers": {}}
    if not done:
        if verbose:
            print(f"audit: 0/{len(q)} reviewed — nothing to score yet")
        return out
    for lab in LABS + ["judge_ind"]:
        xs, ws = [], []
        for d, r in done:
            y = r.lang(lab)
            h = r.human().get("language")
            if y is None or not h or h == "unsure":
                continue
            xs.append(int(coarse(y) == coarse(h)))
            ws.append(float(d["weight"]))
        if xs:
            p, lo, hi, neff = S.weighted_prop(xs, ws)
            out["labellers"][lab] = {"n": len(xs), "accuracy": round(p, 4), "ci": [round(lo, 4), round(hi, 4)],
                                     "n_eff": round(neff, 1)}
    if verbose:
        print(f"audit: {len(done)}/{len(q)} reviewed ({revised} revised after unblinding; the latest review counts)")
        for lab, v in out["labellers"].items():
            print(f"  {lab:10} acc={v['accuracy']:.3f}  CI [{v['ci'][0]:.3f}, {v['ci'][1]:.3f}]  n={v['n']}")
    (STUDY / "audit_score.json").write_text(json.dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--n-agree", type=int, default=40)
    ap.add_argument("--n-disagree", type=int, default=60)
    ap.add_argument("--seed", type=int, default=23)
    a = ap.parse_args()
    if a.build:
        build(a.n_agree, a.n_disagree, a.seed)
    if a.score:
        score()


if __name__ == "__main__":
    main()
