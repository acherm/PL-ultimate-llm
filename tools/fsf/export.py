"""Export the `.fsf` study to the common study-export format (tools/study_export.py).

`.fsf` is mostly *not* a programming language: it is the FSL FEAT fMRI design
file, a configuration written in Tcl `set fmri(...)` syntax. So this export
carries no language claim for the dominant meaning — it proposes a non-PL
extension label instead — and keeps the polysemy tail (GLSL fragment shaders,
git-annex pointers, XML fractal saves …) as evidence. Every number comes from
`data/derived/fsf_study/` (reports/*.json, worklist_all.csv) and
`fsf_files+origin.csv`.

    python3 -m tools.fsf.export
    python3 tools/propagate_study.py --study fsf          # plan; --apply to merge
"""

from __future__ import annotations

import csv
import glob
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import study_export as SE  # noqa: E402
from tools.cobol.common import CACHE_DIR  # noqa: E402
from tools.m.stats import wilson  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "fsf_study"
CSV_POP = ROOT / "fsf_files+origin.csv"
REVIEWS = ROOT / "reviews_fsf"
EXT = ".fsf"
REPORT = "docs/fsf_swh_study.md"
JUDGE_MODEL = "anthropic/claude-sonnet-4.6"

# label → (display, pl_id)
LABELS = {
    "not-code:fsl-feat-design": ("FSL FEAT design file (fMRI analysis config, Tcl `set fmri(...)` syntax)", ""),
    "not-code:git-annex-pointer": ("git-annex / DataLad pointer (the design is annexed, not archived)", ""),
    "not-code:git-lfs-pointer": ("Git LFS pointer", ""),
    "not-code:xml-fractal-save": ("XML fractal save file (XMLFractalSave / FractalV1)", ""),
    "glsl": ("GLSL fragment shader", "pl/glsl"),
    "c++:glsl-header": ("C++ header embedding GLSL shader strings", "pl/cpp"),
    "other-language": ("other languages (an ML-family research DSL)", ""),
    "not-code:other": ("other non-code (IDE settings, ChangeLogs, DocFX HTML, JSON/XML data …)", ""),
    "not-code:binary": ("binary", ""),
}


def committed_at(path: Path) -> str:
    """UTC time of the commit that last touched `path` — a stable timestamp for exported records."""
    out = subprocess.run(["git", "log", "-1", "--date=format-local:%Y-%m-%dT%H:%M:%SZ", "--format=%cd", "--",
                          str(path.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True,
                         env={"TZ": "UTC", "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}).stdout.strip()
    return out or "1970-01-01T00:00:00Z"


def V(rep):
    j = rep.get("judge")
    return j.get("verdict") if isinstance(j, dict) and j.get("parse_ok") and j.get("verdict") else None


def classify(rep) -> str:
    """One label per content, from the judge's verdict (the study's own fields)."""
    v = V(rep)
    if not v:
        return "not-code:binary" if not rep["indicators"].get("is_text", True) else "not-code:other"
    fmt = (v.get("format") or "").lower()
    hay = " ".join(str(v.get(k, "")) for k in ("format", "expressed_in", "ecosystem_tool", "purpose")).lower()
    rel = [x.lower() for x in (v.get("related_languages") or [])]
    if (v.get("artifact_kind") or "").startswith("fsl-") or re.search(r"\bfeat\b", fmt):
        return "not-code:fsl-feat-design"
    if "annex" in hay or "datalad" in hay:
        return "not-code:git-annex-pointer"
    if "lfs" in fmt:
        return "not-code:git-lfs-pointer"
    if "fractal" in fmt and ("xml" in fmt or "fractalv1" in fmt or "xmlfractalsave" in fmt):
        return "not-code:xml-fractal-save"
    if "glsl" in rel or "glsl" in fmt:
        return "c++:glsl-header" if "c++" in fmt else "glsl"
    if v.get("is_programming_language"):
        return "other-language"
    if v.get("content_type") == "binary":
        return "not-code:binary"
    return "not-code:other"


def load():
    wl = {r["sha1_git"]: r for r in csv.DictReader((STUDY / "worklist_all.csv").open(encoding="utf-8"))}
    reps = {}
    for p in glob.glob(str(STUDY / "reports" / "*.json")):
        d = json.loads(Path(p).read_text())
        reps[d["sha1_git"]] = d
    return wl, reps


def population():
    shas, origins, paths = set(), set(), {}
    with CSV_POP.open(encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) < 3:
                continue
            sha = row[0].replace("swh:1:cnt:", "").split(";")[0].strip()
            q = parse_qs(urlparse(row[2]).query)
            o = (q.get("origin_url") or [None])[0]
            shas.add(sha)
            if o:
                origins.add(o)
                paths.setdefault(sha, {"origin": o, "path": (q.get("path") or [""])[0],
                                       "branch": (q.get("branch") or [""])[0],
                                       "visit_ts": (q.get("timestamp") or [""])[0]})
    return len(shas), len(origins), paths


def frames(wl, reps):
    return {"file": [reps[s] for s, w in wl.items() if w["in_uniform"] == "1" and s in reps],
            "repo": [reps[s] for s, w in wl.items() if w["in_diverse"] == "1" and s in reps]}


def evidence_rows(fr):
    rows = []
    method = {"file": "judge (Sonnet 4.6, shown indicators), uniform by-file sample",
              "repo": "judge (Sonnet 4.6, shown indicators), one file per repository — a census of all 757 repositories"}
    for frame, rs in fr.items():
        n = len(rs)
        c = Counter(classify(r) for r in rs)
        for lab, (display, pid) in LABELS.items():
            k = c.get(lab, 0)
            if not k:
                continue
            p, lo, hi = wilson(k, n)
            note = ""
            if lab == "other-language":
                origins = sorted({r["origin"] for r in rs if classify(r) == lab})
                note = "origins: " + ", ".join(o.replace("https://", "") for o in origins)
            if lab == "glsl":
                origins = sorted({r["origin"].replace("https://", "") for r in rs if classify(r) == lab})
                note = ("not claimed: .fsf is not a documented GLSL extension (Linguist GLSL lists .glsl/.frag/.fs/"
                        ".fsh/… but not .fsf); project-local naming in " + ", ".join(origins))
            if lab == "not-code:binary":
                nj = sum(1 for r in rs if classify(r) == lab and not V(r))
                note = f"{nj} of {k} are non-text bytes not sent to the judge (indicator is_text=False)"
            if lab == "not-code:other":
                fm = Counter((V(r) or {}).get("format", "?")[:40] for r in rs if classify(r) == lab)
                note = "top formats: " + "; ".join(f"{f} ({n_})" for f, n_ in fm.most_common(4))
            rows.append({"ext": EXT, "label": lab, "display": display, "pl_id": pid, "frame": frame,
                         "share_pct": round(100 * p, 2), "ci_lo_pct": round(100 * lo, 1),
                         "ci_hi_pct": round(100 * hi, 1), "n_class": k, "n_frame": n,
                         "method": method[frame], "note": note})
        # host notation: share of judged files the judge relates to Tcl (the FEAT `set` syntax)
        judged = [r for r in rs if V(r)]
        k = sum(1 for r in judged if "tcl" in [x.lower() for x in (V(r).get("related_languages") or [])])
        p, lo, hi = wilson(k, len(judged))
        rows.append({"ext": EXT, "label": "expressed-in:tcl", "display": "expressed in Tcl (host notation, not the file's language)",
                     "pl_id": "pl/tcl", "frame": frame, "share_pct": round(100 * p, 2),
                     "ci_lo_pct": round(100 * lo, 1), "ci_hi_pct": round(100 * hi, 1), "n_class": k,
                     "n_frame": len(judged), "method": method[frame] + "; denominator = judged files",
                     "note": "FEAT designs are Tcl `set fmri(...)` statements sourced by FSL's Tcl GUI — a config/DSL over Tcl, not a Tcl program"})
    return rows


def share(fr, frame, lab):
    rs = fr[frame]
    return round(100 * sum(1 for r in rs if classify(r) == lab) / max(len(rs), 1), 1)


def claim_rows(fr, reps):
    judged = [r for r in reps.values() if V(r)]
    not_pl = sum(1 for r in judged if V(r).get("is_programming_language") is False)
    feat_f, feat_r = share(fr, "file", "not-code:fsl-feat-design"), share(fr, "repo", "not-code:fsl-feat-design")
    annex_f, annex_r = share(fr, "file", "not-code:git-annex-pointer"), share(fr, "repo", "not-code:git-annex-pointer")
    glsl_f, glsl_r = share(fr, "file", "glsl"), share(fr, "repo", "glsl")
    rows = [{
        "ext": EXT, "pl_id": "", "action": "label", "label": "data:domain",
        "share_file_pct": feat_f, "share_repo_pct": feat_r,
        "evidence": f"{REPORT} §4.1–4.4; data/derived/fsf_study/reports/",
        "rationale": (f"FSL FEAT design file (fMRI analysis configuration in Tcl `set fmri(...)` syntax, read by FSL's "
                      f"FEAT GUI): {feat_f} % of files and {feat_r} % of repositories; a further {annex_f} % / {annex_r} % "
                      f"are git-annex pointers to annexed designs. {not_pl}/{len(judged)} judged files are not a "
                      f"programming language. `data:domain` (domain-specific format of one application) fits better than "
                      f"`data:config` (generic INI/TOML-style syntaxes). This contradicts the example `.fsf → pl/new:fsl` "
                      f"in docs/extension_labels.md: FEAT designs parametrise a pipeline and do not compute. Polysemy tail: "
                      f"XML fractal saves, GLSL shaders, IDE settings."),
        "status": "accepted"}]
    # GLSL: evidence only — `.fsf` is not a documented GLSL extension (see the note on the GLSL evidence row)
    _ = (glsl_f, glsl_r)
    return rows


def pick_samples(reps, paths):
    """GLSL fragment shaders only (the only programming language under .fsf); FEAT designs are evidence."""
    out, seen = [], set()
    cands = sorted((r for r in reps.values() if classify(r) == "glsl" and V(r).get("is_programming_language")),
                   key=lambda r: (abs(r["indicators"].get("total_lines", 0) - 60), r["sha1_git"]))
    for r in cands:
        sha = r["sha1_git"]
        ctx = paths.get(sha, {"origin": r.get("origin", ""), "path": "", "branch": "", "visit_ts": ""})
        if ctx["origin"] in seen:
            continue
        raw_p = CACHE_DIR / f"{sha}.bin"
        if not raw_p.exists() or SE.git_blob_sha1(raw_p.read_bytes()) != sha:
            continue
        seen.add(ctx["origin"])
        v = V(r)
        out.append({"ext": EXT, "pl_id": "pl/glsl", "label": "glsl", "sha1_git": sha,
                    "filename": r["name"].lstrip("/"), "origin": ctx["origin"], "path": ctx["path"],
                    "branch": ctx["branch"], "visit_ts": ctx["visit_ts"],
                    "qualified_swhid": SE.qualified_swhid(sha, ctx["origin"], ctx["path"]),
                    "verified_by": "judge:claude-sonnet-4.6",
                    "language_detail": v.get("format", ""), "provenance_kind": "",
                    "note": (v.get("purpose") or "")[:160]})
        if len(out) >= 3:
            break
    return out


def heuristic_rows(reps):
    rows = []
    judged = [r for r in reps.values() if V(r)]
    ref = f"LLM judge (Sonnet 4.6), {len(judged)} judged files (both frames)"
    agree = sum((r["reclass"]["label"] == "fsl-feat") == (V(r).get("artifact_kind", "") or "").startswith("fsl-")
                for r in judged)
    rows.append({"ext": EXT, "heuristic_id": "", "tool": "study rules fsf reclassifier (`set fmri(` marker)",
                 "metric": "agreement:is-feat", "value": round(agree / len(judged), 4), "n": len(judged),
                 "reference": ref, "note": "judge FEAT = artifact_kind fsl-*; the judge was shown the indicators"})
    syn = STUDY / "synid.jsonl"
    if syn.exists():
        S = {json.loads(l)["sha1_git"]: json.loads(l) for l in syn.open(encoding="utf-8")}
        for cfg in ("default", "nocomment"):
            tool = f"swh-synid 9bc1c32 (file mode, {'default strategies' if cfg == 'default' else 'without comment strategy'})"
            by_lab = defaultdict(Counter)
            for r in judged:
                s = S.get(r["sha1_git"])
                if not s:
                    continue
                ans = s.get(cfg) or []
                by_lab[classify(r)]["|".join(ans) if ans else "(none)"] += 1
            for lab in ("not-code:fsl-feat-design", "glsl", "not-code:git-annex-pointer"):
                c = by_lab.get(lab)
                if not c:
                    continue
                n = sum(c.values())
                for ans, k in c.most_common(3):
                    rows.append({"ext": EXT, "heuristic_id": "", "tool": tool, "metric": f"answer[{lab}]:{ans}",
                                 "value": round(k / n, 4), "n": n, "reference": ref,
                                 "note": "share of files of that judged class getting this Synid answer"})
            glsl = by_lab.get("glsl", Counter())
            n = sum(glsl.values())
            if n:
                ok = sum(k for a, k in glsl.items() if "GLSL" in a.split("|") and len(a.split("|")) == 1)
                rows.append({"ext": EXT, "heuristic_id": "", "tool": tool, "metric": "recall:glsl",
                             "value": round(ok / n, 4), "n": n, "reference": ref, "note": ""})
    return rows


def study_reviews(s: dict) -> list[dict]:
    """Hook for tools/propagate_study.py: the judge's verdict on an exported GLSL sample (kind=llm).
    reviews_fsf/ reviews (fsf-review/1) record content_type / is_feat, not a language label, so they
    are not mapped to reviewstore labels."""
    import reviewstore as RS
    _, reps = load()
    r = reps.get(s["sha1_git"])
    v = V(r) if r else None
    if not v or s["pl_id"] not in ("pl/glsl",):
        return []
    rev = RS.new_review(
        subject={"sha1_git": s["sha1_git"], "filename": s["filename"], "ext": s["ext"]},
        reviewer={"kind": "llm", "id": JUDGE_MODEL.replace("/", "-"), "version": r["judge"].get("schema"),
                  "runner": "tools/fsf/judge.py",
                  "params": {"study": "fsf", "mode": "bytes + filename + mechanical indicators", "temperature": 0}},
        label=s["pl_id"], confidence=v.get("confidence") if v.get("confidence") in RS.CONFIDENCES else "medium",
        comment=v.get("format"), shown={"study": "fsf"})
    rev["created_at"] = committed_at(STUDY / "reports" / f"{s['sha1_git']}.json")   # deterministic → idempotent
    return [rev]


def main():
    wl, reps = load()
    n_contents, n_origins, paths = population()
    fr = frames(wl, reps)
    samples = pick_samples(reps, paths)
    tables = {"ext_evidence.csv": evidence_rows(fr), "samples.csv": samples,
              "claims.csv": claim_rows(fr, reps), "heuristic_eval.csv": heuristic_rows(reps)}
    spend = sum(((r.get("judge") or {}).get("usage") or {}).get("cost", 0) or 0 for r in reps.values())
    meta = {"title": "What is actually in the .fsf extension on Software Heritage?", "extensions": [EXT],
            "case_sensitive": True, "report": REPORT, "toolkit": "tools/fsf/",
            "population": {"contents": n_contents, "repositories": n_origins,
                           "source": "fsf_files+origin.csv (graph-derived, maintainer export)"},
            "frames": {"file": f"uniform over contents, n={len(fr['file'])} fetched",
                       "repo": f"one file per repository, all {len(fr['repo'])} repositories (census)"},
            "judges": [f"{JUDGE_MODEL} (shown mechanical indicators; schema fsf-judge/1)"],
            "human_reviews": sum(1 for d in REVIEWS.glob("*") if d.is_dir()) if REVIEWS.exists() else 0,
            "spend_usd": round(spend, 2), "date": committed_at(STUDY / "summary_fsf.json")[:10]}
    SE.write_export("fsf", meta, tables)


if __name__ == "__main__":
    main()
