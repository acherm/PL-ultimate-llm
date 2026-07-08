"""Orchestrator for the .fsf study: sample (uniform + origin-diverse),
fetch (cached), indicators, LLM-judge, reclassify, aggregate.

    python3 -m tools.fsf.study --sample --n 1000 --seed 5
    OPENROUTER_API_KEY=… python3 -m tools.fsf.study --run --judge
    python3 -m tools.fsf.study --report
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.common import fetch_content  # noqa: E402
from tools.fsf import indicators as ind_mod    # noqa: E402
from tools.fsf import judge as judge_mod        # noqa: E402
from tools.fsf import reclassify as rc          # noqa: E402
from tools.fsf import taxonomy as tax           # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "fsf_files+origin.csv"
STUDY = ROOT / "data" / "derived" / "fsf_study"
REPORTS = STUDY / "reports"
WORKLIST = STUDY / "worklist_all.csv"


def parse_csv():
    """Yield {sha, name, origin, forge} from fsf_files+origin.csv."""
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 3:
                continue
            sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
            q = parse_qs(urlparse(row[2]).query)
            origin = (q.get("origin_url") or [None])[0]
            if sha and origin:
                yield {"sha": sha, "name": row[1], "origin": origin,
                       "forge": urlparse(origin).netloc}


def do_sample(n, seed):
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = list(parse_csv())
    by_sha = {r["sha"]: r for r in rows}          # dedup by content
    by_origin = defaultdict(list)
    for r in by_sha.values():
        by_origin[r["origin"]].append(r)
    rng = random.Random(seed)

    uniform = set(rng.sample(sorted(by_sha), min(n, len(by_sha))))
    origins = sorted(by_origin)
    rng.shuffle(origins)
    diverse = {rng.choice(by_origin[o])["sha"] for o in origins}  # 1 per origin

    allshas = uniform | diverse
    with WORKLIST.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["swhid", "sha1_git", "name", "origin", "forge",
                    "in_uniform", "in_diverse"])
        for sha in sorted(allshas):
            r = by_sha[sha]
            w.writerow([f"swh:1:cnt:{sha}", sha, r["name"], r["origin"],
                        r["forge"], int(sha in uniform), int(sha in diverse)])
    print(f"pool: {len(by_sha)} contents / {len(by_origin)} origins")
    print(f"uniform={len(uniform)}  diverse(by-repo)={len(diverse)}  union={len(allshas)}")
    print(f"wrote {WORKLIST}")


def report_path(sha):
    return REPORTS / f"{sha}.json"


def do_run(judge_on, model, sleep):
    rows = list(csv.DictReader(WORKLIST.open(encoding="utf-8")))
    print(f"worklist {len(rows)} | judge={'on' if judge_on else 'off'}")
    for i, row in enumerate(rows, 1):
        sha = row["sha1_git"]
        rp = report_path(sha)
        if rp.exists():
            ex = json.loads(rp.read_text())
            has_j = isinstance(ex.get("judge"), dict) and ex["judge"].get("verdict")
            if (not judge_on) or has_j:
                continue
        try:
            c = fetch_content(row["swhid"], filename=row["name"], polite_delay=sleep)
            ind = ind_mod.compute(c.text, bytes_len=c.length, is_text=c.is_text)
            recl = rc.classify(row["name"], c.raw)
            rep = {"sha1_git": sha, "name": row["name"], "origin": row["origin"],
                   "forge": row["forge"], "length": c.length,
                   "indicators": ind.to_dict(), "reclass": recl, "judge": None}
            if judge_on and c.is_text:
                rep["judge"] = judge_mod.judge(row["name"], ind.to_dict(), c.text, model=model)
        except Exception as e:
            print(f"[{i}/{len(rows)}] {sha[:10]} ERROR: {e}", file=sys.stderr)
            continue
        rp.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        if i % 25 == 0:
            v = (rep.get("judge") or {}).get("verdict", {}) if isinstance(rep.get("judge"), dict) else {}
            print(f"[{i}/{len(rows)}] {sha[:10]} {row['name'][:26]:28} "
                  f"feat={rep['indicators']['has_feat']} kind={v.get('artifact_kind','-')}")
    print("run complete")


def _load_reports():
    return {p.stem: json.loads(p.read_text()) for p in REPORTS.glob("*.json")}


def _dist(reports, getter):
    c = Counter(getter(r) for r in reports)
    n = sum(c.values()) or 1
    return {k: (v, round(100 * v / n)) for k, v in c.most_common()}


def do_report():
    reps = _load_reports()
    wl = {r["sha1_git"]: r for r in csv.DictReader(WORKLIST.open())}
    frames = {"uniform": [], "diverse": []}
    for sha, rep in reps.items():
        row = wl.get(sha)
        if not row:
            continue
        if row.get("in_uniform") == "1":
            frames["uniform"].append(rep)
        if row.get("in_diverse") == "1":
            frames["diverse"].append(rep)

    def V(r):
        j = r.get("judge")
        return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None

    out = {}
    for fname, reps_f in frames.items():
        judged = [r for r in reps_f if V(r)]
        n = len(reps_f)
        has_feat = sum(r["indicators"]["has_feat"] for r in reps_f)
        is_pl = Counter(str(V(r).get("is_programming_language")) for r in judged)
        kind = _dist(judged, lambda r: V(r).get("artifact_kind", ""))
        level = _dist(judged, lambda r: V(r).get("feat_level", ""))
        atype = _dist(judged, lambda r: V(r).get("analysis_type", ""))
        gen = _dist(judged, lambda r: V(r).get("generated", ""))
        recl = _dist(reps_f, lambda r: r["reclass"]["label"])
        origins = len({r["origin"] for r in reps_f})
        loc = [r["indicators"]["total_lines"] for r in reps_f]
        out[fname] = {
            "n": n, "n_judged": len(judged), "distinct_origins": origins,
            "has_feat_pct": round(100 * has_feat / n) if n else 0,
            "median_lines": statistics.median(loc) if loc else 0,
            "is_programming_language": dict(is_pl),
            "artifact_kind": kind, "feat_level": level,
            "analysis_type": atype, "generated": gen, "reclass_label": recl,
        }
    (STUDY / "summary_fsf.json").write_text(json.dumps(out, indent=2))

    # reclassifier vs judge on "is this FEAT"
    judged_all = [r for r in reps.values() if V(r)]
    agree = sum((r["reclass"]["label"] in tax.FEAT_LABELS) ==
                (V(r).get("artifact_kind", "").startswith("fsl-"))
                for r in judged_all)

    print(f"=== .fsf study — {len(reps)} contents ===")
    for fname in ("uniform", "diverse"):
        d = out[fname]
        print(f"\n## {fname.upper()} frame  (n={d['n']}, judged {d['n_judged']}, "
              f"{d['distinct_origins']} origins, has_feat {d['has_feat_pct']}%, "
              f"median {d['median_lines']} lines)")
        print("  is_programming_language:", d["is_programming_language"])
        for lbl in ("artifact_kind", "feat_level", "analysis_type", "generated"):
            top = list(d[lbl].items())[:5]
            print(f"  {lbl}:", {k: f"{v[1]}%" for k, v in top})
    print(f"\nreclassifier vs judge agree on is-FEAT: {agree}/{len(judged_all)}"
          f" ({round(100*agree/max(len(judged_all),1))}%)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--model", default=os.environ.get("COBOL_JUDGE_MODEL", judge_mod.DEFAULT_MODEL))
    ap.add_argument("--sleep", type=float, default=0.2)
    a = ap.parse_args()
    if a.sample:
        do_sample(a.n, a.seed)
    if a.run:
        do_run(a.judge, a.model, a.sleep)
    if a.report:
        do_report()


if __name__ == "__main__":
    main()
