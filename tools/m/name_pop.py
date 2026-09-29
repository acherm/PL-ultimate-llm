"""Population-level duplication signal for every sampled `.m` content.

For each sampled filename, count in the *whole* 51 M population how many
distinct contents and distinct repositories carry a file of that name.
`AFURLSessionManager.m` in 20,000 repos is a vendored library; `ex2.m` in
30,000 repos is a course exercise; `lnd92254_094.m` in 1 repo is data. The
judge's `provenance_kind` can then be checked against a signal it never saw.

    .venv/bin/python -m tools.m.name_pop     # → data/derived/m_study/name_popularity.json
                                              #   + population_signals.json

`population_signals.json` sizes, over the whole population, the duplication
families the judge surfaces in the sample: Xcode template names, CocoaPods
dummy stubs, Flutter plugin registrants, and the Coursera *Machine Learning*
exercise set; plus the provenance-path quirks (non-`.m` context names).
"""

from __future__ import annotations

import json

from tools.m.ingest import PARQUET, STUDY


COURSERA_ML = ["warmUpExercise.m", "plotData.m", "computeCost.m", "gradientDescent.m", "featureNormalize.m",
               "computeCostMulti.m", "gradientDescentMulti.m", "normalEqn.m", "sigmoid.m", "costFunction.m",
               "predict.m", "costFunctionReg.m", "mapFeature.m", "plotDecisionBoundary.m", "lrCostFunction.m",
               "oneVsAll.m", "predictOneVsAll.m", "displayData.m", "nnCostFunction.m", "sigmoidGradient.m",
               "randInitializeWeights.m", "checkNNGradients.m", "linearRegCostFunction.m", "learningCurve.m",
               "polyFeatures.m", "validationCurve.m", "gaussianKernel.m", "dataset3Params.m", "processEmail.m",
               "emailFeatures.m", "findClosestCentroids.m", "computeCentroids.m", "kMeansInitCentroids.m",
               "projectData.m", "recoverData.m", "estimateGaussian.m", "selectThreshold.m", "cofiCostFunc.m",
               "fmincg.m", "debugInitializeWeights.m", "computeNumericalGradient.m"]


def signals(con):
    con.execute(f"""CREATE TEMP TABLE m AS SELECT origin, regexp_extract(coalesce(path,''), '([^/]*)$', 1) fname
                    FROM read_parquet('{PARQUET}') WHERE status IN ('ok','multiline')""")
    one = lambda q: con.execute(q).fetchone()  # noqa: E731
    tot, repos = one("SELECT count(*), count(DISTINCT origin) FROM m")
    con.execute("CREATE TEMP TABLE cn(n VARCHAR)")
    con.executemany("INSERT INTO cn VALUES (?)", [(n,) for n in COURSERA_ML])
    fam = {}
    for key, where in (("xcode_template_names", "fname IN ('AppDelegate.m','main.m','ViewController.m','SceneDelegate.m')"),
                       ("cocoapods_dummy", "regexp_matches(fname, '-dummy\\.m$')"),
                       ("flutter_registrant", "fname = 'GeneratedPluginRegistrant.m'")):
        c, r = one(f"SELECT count(*), count(DISTINCT origin) FROM m WHERE {where}")
        fam[key] = {"contents": c, "repos": r, "pct_contents": round(100 * c / tot, 2),
                    "pct_repos": round(100 * r / repos, 2)}
    r, k = one("""SELECT count(*), sum(k) FROM (SELECT origin, count(DISTINCT fname) d, count(*) k
                  FROM m JOIN cn ON fname = cn.n GROUP BY origin) WHERE d >= 5""")
    fam["coursera_ml_repos_ge5_exercises"] = {"contents": int(k), "repos": r, "pct_contents": round(100 * k / tot, 2),
                                              "pct_repos": round(100 * r / repos, 2)}
    ext = con.execute("""SELECT regexp_extract(fname, '(\\.[^.]*)$', 1) e, count(*) FROM m
                         WHERE NOT fname LIKE '%.m' GROUP BY 1 ORDER BY 2 DESC LIMIT 15""").fetchall()
    nonm = one("SELECT count(*) FROM m WHERE NOT fname LIKE '%.m'")[0]
    sizes = [r[0] for r in con.execute("SELECT count(*) n FROM m GROUP BY origin ORDER BY n DESC").fetchall()]
    lorenz, cum, step = [], 0, max(1, len(sizes) // 2000)
    for i, sz in enumerate(sizes, 1):
        cum += sz
        if i <= 100 or i % step == 0 or i == len(sizes):
            lorenz.append([round(100 * i / len(sizes), 5), round(100 * cum / tot, 4)])
    out = {"contents_with_origin": tot, "repos": repos, "families": fam, "lorenz": lorenz,
           "largest_repo_pct": round(100 * sizes[0] / tot, 3),
           "non_dot_m_context_names": {"n": nonm, "pct": round(100 * nonm / tot, 3), "top": dict(ext)}}
    (STUDY / "population_signals.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


def main():
    import duckdb
    from tools.m.study import worklist
    names = sorted({r["name"] for r in worklist() if r["name"]})
    con = duckdb.connect()
    con.execute("SET threads=14")
    con.execute("CREATE TEMP TABLE want(name VARCHAR)")
    con.executemany("INSERT INTO want VALUES (?)", [(n,) for n in names])
    rows = con.execute(f"""
        SELECT w.name, count(*) contents, count(DISTINCT m.origin) repos
        FROM read_parquet('{PARQUET}') m
        JOIN want w ON regexp_extract(coalesce(m.path,''), '([^/]*)$', 1) = w.name
        GROUP BY 1""").fetchall()
    out = {n: {"contents": c, "repos": r} for n, c, r in rows}
    (STUDY / "name_popularity.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"{len(out)} names; top by repos:")
    for n, d in sorted(out.items(), key=lambda kv: -kv[1]["repos"])[:15]:
        print(f"  {d['repos']:>8} repos {d['contents']:>8} contents  {n}")
    signals(con)


if __name__ == "__main__":
    main()
