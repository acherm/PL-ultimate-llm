"""Orchestrator for the `.rpgle` study: sample (uniform + origin-diverse),
fetch (cached), indicators, LLM-judge, reclassify, aggregate.

    python3 -m tools.rpgle.study --sample --n 1000 --seed 5
    SWH_TOKEN=… OPENROUTER_API_KEY=… python3 -m tools.rpgle.study --run --judge
    python3 -m tools.rpgle.study --report
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
from tools.cobol.common import fetch_content   # noqa: E402
from tools.rpgle import indicators as ind_mod  # noqa: E402
from tools.rpgle import judge as judge_mod     # noqa: E402
from tools.rpgle import reclassify as rc       # noqa: E402
from tools.rpgle import taxonomy as tax        # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "rpgle_files+origins.csv"
STUDY = ROOT / "data" / "derived" / "rpgle_study"
REPORTS = STUDY / "reports"
WORKLIST = STUDY / "worklist_all.csv"


def parse_csv():
    with CSV.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
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
    by_sha = {r["sha"]: r for r in parse_csv()}
    by_origin = defaultdict(list)
    for r in by_sha.values():
        by_origin[r["origin"]].append(r)
    rng = random.Random(seed)

    uniform = set(rng.sample(sorted(by_sha), min(n, len(by_sha))))
    origins = sorted(by_origin)
    rng.shuffle(origins)
    diverse = {rng.choice(by_origin[o])["sha"] for o in origins}  # 1 per repo = census

    allshas = uniform | diverse
    with WORKLIST.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["swhid", "sha1_git", "name", "origin", "forge",
                    "in_uniform", "in_diverse"])
        for sha in sorted(allshas):
            r = by_sha[sha]
            w.writerow([f"swh:1:cnt:{sha}", sha, r["name"], r["origin"], r["forge"],
                        int(sha in uniform), int(sha in diverse)])
    print(f"pool: {len(by_sha)} contents / {len(by_origin)} origins")
    print(f"uniform={len(uniform)}  diverse(by-repo census)={len(diverse)}  union={len(allshas)}")
    print(f"wrote {WORKLIST}")


def do_run(judge_on, model, sleep):
    rows = list(csv.DictReader(WORKLIST.open(encoding="utf-8")))
    print(f"worklist {len(rows)} | judge={'on' if judge_on else 'off'}", flush=True)
    for i, row in enumerate(rows, 1):
        sha = row["sha1_git"]
        rp = REPORTS / f"{sha}.json"
        if rp.exists():
            ex = json.loads(rp.read_text())
            if (not judge_on) or (isinstance(ex.get("judge"), dict) and ex["judge"].get("verdict")):
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
            print(f"[{i}/{len(rows)}] {sha[:10]} ERROR: {e}", file=sys.stderr, flush=True)
            continue
        rp.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        if i % 25 == 0:
            v = (rep.get("judge") or {}).get("verdict", {}) if isinstance(rep.get("judge"), dict) else {}
            print(f"[{i}/{len(rows)}] {sha[:10]} {row['name'][:24]:26} "
                  f"fmt={rep['indicators']['source_format_guess']} kind={v.get('unit_kind','-')}", flush=True)
    print("run complete", flush=True)


def do_refresh_indicators():
    """Recompute indicators + reclass label from cached bytes; keep judge verdicts.

    Used when the mechanical layer changes (e.g. indicators v1 -> v2) so the
    oracle does not have to be paid for twice.
    """
    n = 0
    for p in sorted(REPORTS.glob("*.json")):
        rep = json.loads(p.read_text())
        try:
            c = fetch_content(f"swh:1:cnt:{rep['sha1_git']}", filename=rep["name"])
        except Exception as e:
            print(f"{rep['sha1_git'][:10]}: {e}", file=sys.stderr)
            continue
        rep["indicators"] = ind_mod.compute(c.text, bytes_len=c.length, is_text=c.is_text).to_dict()
        rep["reclass"] = rc.classify(rep["name"], c.raw)
        p.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        n += 1
    print(f"refreshed indicators on {n} reports")


def _reports():
    return {p.stem: json.loads(p.read_text()) for p in REPORTS.glob("*.json")}


def V(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def _pct(c):
    n = sum(c.values()) or 1
    return {k: (v, round(100 * v / n)) for k, v in c.most_common()}


def do_report():
    reps = _reports()
    wl = {r["sha1_git"]: r for r in csv.DictReader(WORKLIST.open())}
    frames = defaultdict(list)
    for sha, rep in reps.items():
        row = wl.get(sha)
        if not row:
            continue
        if row.get("in_uniform") == "1":
            frames["uniform"].append(rep)
        if row.get("in_diverse") == "1":
            frames["diverse"].append(rep)

    out = {}
    for fname, fr in frames.items():
        judged = [r for r in fr if V(r)]
        nj = len(judged) or 1
        rel = Counter()
        for r in judged:
            for l in (V(r).get("related_languages") or []):
                rel[l.strip()] += 1
        loc = [r["indicators"]["total_lines"] for r in fr]
        out[fname] = {
            "n": len(fr), "n_judged": len(judged),
            "distinct_origins": len({r["origin"] for r in fr}),
            "median_lines": statistics.median(loc) if loc else 0,
            "is_programming_language": dict(Counter(str(V(r).get("is_programming_language")) for r in judged)),
            "content_type": _pct(Counter(V(r).get("content_type", "") for r in judged)),
            "source_format": _pct(Counter(V(r).get("source_format", "") for r in judged)),
            "unit_kind": _pct(Counter(V(r).get("unit_kind", "") for r in judged)),
            "domain": _pct(Counter(V(r).get("domain", "") for r in judged)),
            "maturity": _pct(Counter(V(r).get("maturity", "") for r in judged)),
            "platform": _pct(Counter(V(r).get("platform", "") for r in judged)),
            "embedded_sql_pct": round(100 * sum(bool(V(r).get("embedded_sql")) for r in judged) / nj),
            "related_languages": {k: (v, round(100 * v / nj)) for k, v in rel.most_common(12)},
            "reclass_label": _pct(Counter(r["reclass"]["label"] for r in fr)),
            "indicator_format": _pct(Counter(r["indicators"]["source_format_guess"] for r in fr)),
        }
    (STUDY / "summary_rpgle.json").write_text(json.dumps(out, indent=2))

    judged_all = [r for r in reps.values() if V(r)]
    agree = sum((r["reclass"]["label"] in tax.RPGLE_LABELS) ==
                bool(V(r).get("content_type", "") in ("source-code", "copybook-or-header"))
                for r in judged_all)
    print(f"=== .rpgle study — {len(reps)} contents ===")
    for fn in ("uniform", "diverse"):
        if fn not in out:
            continue
        d = out[fn]
        print(f"\n## {fn.upper()} (n={d['n']}, judged {d['n_judged']}, "
              f"{d['distinct_origins']} origins, median {d['median_lines']} lines, "
              f"embedded SQL {d['embedded_sql_pct']}%)")
        print("  is_PL:", d["is_programming_language"])
        for k in ("content_type", "source_format", "unit_kind", "domain", "maturity"):
            print(f"  {k}:", {a: f"{b[1]}%" for a, b in list(d[k].items())[:5]})
        print("  related_languages:", {a: f"{b[1]}%" for a, b in list(d["related_languages"].items())[:7]})
    print(f"\nreclassifier vs judge (is-RPGLE): {agree}/{len(judged_all)} "
          f"({round(100*agree/max(len(judged_all),1))}%)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--refresh-indicators", action="store_true")
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--model", default=os.environ.get("COBOL_JUDGE_MODEL", judge_mod.DEFAULT_MODEL))
    ap.add_argument("--sleep", type=float, default=0.0)
    a = ap.parse_args()
    if a.sample:
        do_sample(a.n, a.seed)
    if a.run:
        do_run(a.judge, a.model, a.sleep)
    if a.refresh_indicators:
        do_refresh_indicators()
    if a.report:
        do_report()


if __name__ == "__main__":
    main()
