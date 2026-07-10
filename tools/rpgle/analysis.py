"""Cross-cutting analyses for the `.rpgle` study — the numbers quoted in the report.

  A. Frame table: by-file (uniform) vs by-repo (census), plus two post-stratified
     frames obtained by re-weighting the uniform sample (no extra judging):
       - minus language-tooling repos (jariko / antlr4-rpgle / rpgleparser)
       - deduplicated to one content per (repo, path)
  B. The tooling-repo confound: what those three repos do to the dialect answer.
  C. Version inflation: how much of the population is revisions of one file.
  D. The `**FREE` axis: deterministic rule vs LLM judge, with error direction.

    python3 -m tools.rpgle.analysis
"""

from __future__ import annotations

import csv
import glob
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
CSV_POP = ROOT / "rpgle_files+origins.csv"
STUDY = ROOT / "data" / "derived" / "rpgle_study"

TOOLING = {"https://github.com/smeup/jariko",
           "https://github.com/JCErasmus/antlr4-rpgle",
           "https://github.com/chrjorgensen/rpgleparser"}


def V(r):
    j = r.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("verdict") else None


def pcts(reps, key, keys=None):
    c = Counter(V(r).get(key) for r in reps if V(r))
    n = sum(c.values()) or 1
    items = [(k, c[k]) for k in keys] if keys else c.most_common()
    return {k: round(100 * v / n) for k, v in items}


def summarize(reps, label):
    j = [r for r in reps if V(r)]
    n = len(j) or 1
    rel = Counter()
    for r in j:
        for l in (V(r).get("related_languages") or []):
            rel[l.strip()] += 1
    return {
        "label": label, "n": len(reps), "n_judged": len(j),
        "n_repos": len({r["origin"] for r in reps}),
        "median_lines": statistics.median([r["indicators"]["total_lines"] for r in reps]) if reps else 0,
        "pct_is_pl": round(100 * sum(bool(V(r).get("is_programming_language")) for r in j) / n),
        "source_format": pcts(j, "source_format"),
        "unit_kind": pcts(j, "unit_kind"),
        "maturity": pcts(j, "maturity"),
        "domain": pcts(j, "domain"),
        "embedded_sql_pct": round(100 * sum(bool(V(r).get("embedded_sql")) for r in j) / n),
        "related_languages": {k: round(100 * v / n) for k, v in rel.most_common(8)},
    }


def main():
    reps = [json.loads(Path(p).read_text()) for p in glob.glob(str(STUDY / "reports" / "*.json"))]
    wl = {r["sha1_git"]: r for r in csv.DictReader((STUDY / "worklist_all.csv").open())}
    for r in reps:
        r["_wl"] = wl.get(r["sha1_git"], {})

    uniform = [r for r in reps if r["_wl"].get("in_uniform") == "1"]
    diverse = [r for r in reps if r["_wl"].get("in_diverse") == "1"]

    # post-stratified frames from the SAME judged uniform sample
    no_tool = [r for r in uniform if r["origin"] not in TOOLING]
    seen, dedup = set(), []
    for r in sorted(uniform, key=lambda r: r["sha1_git"]):
        k = (r["origin"], r["name"])
        if k not in seen:
            seen.add(k)
            dedup.append(r)

    out = {"frames": [summarize(uniform, "E1 by-file (uniform n=1000)"),
                      summarize(diverse, "E2 by-repo (census, 534 repos)"),
                      summarize(no_tool, "E1' by-file minus 3 tooling repos"),
                      summarize(dedup, "E1'' by-file, one content per (repo,path)")]}

    # ---- B. tooling confound
    tool = [r for r in reps if r["origin"] in TOOLING]
    rest = [r for r in reps if r["origin"] not in TOOLING]
    out["tooling_confound"] = {
        "tooling": summarize(tool, "language-tooling repos"),
        "rest": summarize(rest, "all other repos"),
    }

    # ---- C. version inflation (population level)
    pairs = defaultdict(set)
    by_origin = defaultdict(set)
    for row in csv.reader(CSV_POP.open(encoding="utf-8")):
        if len(row) < 3 or row[0].startswith("swhid"):
            continue
        sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
        o = (parse_qs(urlparse(row[2]).query).get("origin_url") or [None])[0]
        if sha and o:
            pairs[(o, row[1])].add(sha)
            by_origin[o].add(sha)
    ncont = sum(len(v) for v in pairs.values())
    out["version_inflation"] = {
        "contents": ncont, "distinct_repo_path_files": len(pairs),
        "extra_contents_from_revisions": ncont - len(pairs),
        "pct_of_corpus_that_is_revisions": round(100 * (ncont - len(pairs)) / ncont, 1),
        "paths_with_multiple_versions": sum(1 for v in pairs.values() if len(v) > 1),
        "max_versions_of_one_path": max(len(v) for v in pairs.values()),
        "tooling_repo_share_pct": round(100 * sum(len(by_origin[o]) for o in TOOLING if o in by_origin) / ncont, 1),
    }

    # ---- D. the **FREE axis: code vs judge
    j3 = [r for r in reps if V(r) and V(r).get("source_format") in
          ("fully-free", "hybrid-free", "fixed-format")]
    code_says = lambda r: r["indicators"]["is_fully_free"]          # noqa: E731
    judge_says = lambda r: V(r)["source_format"] == "fully-free"    # noqa: E731
    fp = [r for r in j3 if judge_says(r) and not code_says(r)]      # judge invents fully-free
    fn = [r for r in j3 if code_says(r) and not judge_says(r)]      # judge denies **FREE
    out["free_axis"] = {
        "n": len(j3),
        "agree": sum(1 for r in j3 if code_says(r) == judge_says(r)),
        "agree_pct": round(100 * sum(1 for r in j3 if code_says(r) == judge_says(r)) / len(j3), 1),
        "judge_says_fullyfree_without_directive": len(fp),
        "judge_denies_fullyfree_with_directive": len(fn),
        "of_those_de_facto_col1": sum(1 for r in fp if r["indicators"]["free_code_at_col1"]),
        "examples_denied": [r["name"] for r in fn][:5],
    }

    (STUDY / "analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # ---- print
    print("=" * 92)
    print("A. FRAME TABLE")
    hdr = f"{'frame':44}{'n':>6}{'repos':>7}{'medLOC':>8}{'fully':>7}{'hybrid':>8}{'fixed':>7}{'prod':>7}{'toy':>6}"
    print(hdr)
    for f in out["frames"]:
        sf, mt = f["source_format"], f["maturity"]
        print(f"{f['label']:44}{f['n_judged']:>6}{f['n_repos']:>7}{f['median_lines']:>8.0f}"
              f"{sf.get('fully-free',0):>6}%{sf.get('hybrid-free',0):>7}%{sf.get('fixed-format',0):>6}%"
              f"{mt.get('production-like',0):>6}%{mt.get('toy-or-hello-world',0):>5}%")

    print("\nB. TOOLING CONFOUND (3 RPG parser/interpreter repos)")
    for k in ("tooling", "rest"):
        d = out["tooling_confound"][k]
        print(f"  {d['label']:26} n={d['n_judged']:<5} medLOC={d['median_lines']:<6.0f} "
              f"fixed={d['source_format'].get('fixed-format',0)}%  "
              f"snippet={d['maturity'].get('snippet',0)}%  "
              f"production={d['maturity'].get('production-like',0)}%")

    v = out["version_inflation"]
    print(f"\nC. VERSION INFLATION\n  {v['contents']:,} contents = {v['distinct_repo_path_files']:,} distinct "
          f"(repo,path) files + {v['extra_contents_from_revisions']:,} revisions "
          f"({v['pct_of_corpus_that_is_revisions']}% of corpus)")
    print(f"  max versions of one path: {v['max_versions_of_one_path']}; "
          f"tooling repos = {v['tooling_repo_share_pct']}% of contents")

    f = out["free_axis"]
    print(f"\nD. `**FREE` AXIS — deterministic rule vs LLM judge (n={f['n']})")
    print(f"  agreement {f['agree']}/{f['n']} = {f['agree_pct']}%")
    print(f"  judge calls fully-free WITHOUT the directive : {f['judge_says_fullyfree_without_directive']} "
          f"(of which {f['of_those_de_facto_col1']} do have code in cols 1-5)")
    print(f"  judge denies fully-free WITH the directive   : {f['judge_denies_fullyfree_with_directive']} "
          f"{f['examples_denied']}")

    print(f"\nrelated_languages (by-repo census): {out['frames'][1]['related_languages']}")
    print(f"wrote {STUDY / 'analysis.json'}")


if __name__ == "__main__":
    main()
