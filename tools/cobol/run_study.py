"""Run the COBOL-in-SWH study over a worklist.

Pipeline per sample: fetch bytes (cached) -> structural indicators ->
optional LLM-judge -> per-file report JSON. Then aggregate into an
indicators CSV + a Markdown/JSON summary.

The fetch + indicators steps need NO API key. The judge step needs
``OPENROUTER_API_KEY`` and runs only with ``--judge``.

Examples
--------
# No key needed: fetch + indicators for the whole worklist.
python3 -m tools.cobol.run_study --no-judge

# Full study with the LLM-judge (needs OPENROUTER_API_KEY):
python3 -m tools.cobol.run_study --judge --model anthropic/claude-sonnet-4.6
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from . import indicators as ind_mod
from . import judge as judge_mod
from . import taxonomy as tax
from .common import (STUDY_DIR, SWH_BASE, ensure_dirs, fetch_content, now_iso)

REPORT_SCHEMA = "cobol-report/1"


def canonical_view(verdict) -> dict | None:
    """Normalize a judge verdict (v1 free-text OR v2 enum) to canonical fields.

    Lets aggregation treat both schema versions uniformly — and cleans up the
    v1 free-text dialect/domain into the stable vocabulary with no re-judge.
    """
    if not isinstance(verdict, dict) or not verdict or verdict.get("_parse_error"):
        return None
    dia = verdict.get("dialect") or {}
    pur = verdict.get("purpose") or {}
    dom_raw = pur.get("domain") or ""
    return {
        "cobol_confirmed": str(verdict.get("cobol_confirmed")).lower(),
        "family": tax.normalize_dialect_family(dia.get("family") or dia.get("guess") or ""),
        "standard": tax.coerce_enum(dia.get("standard", ""), tax.STANDARDS),
        "source_format": tax.coerce_enum(verdict.get("source_format", ""), tax.SOURCE_FORMATS),
        "domain": tax.normalize_domain(dom_raw),
        "program_type": tax.coerce_enum(pur.get("program_type", ""), tax.PROGRAM_TYPES),
        "maturity": tax.coerce_enum(verdict.get("maturity", ""), tax.MATURITIES),
        "confidence": verdict.get("overall_confidence", ""),
        "dialect_detail": dia.get("detail") or dia.get("guess") or "",
        "domain_detail": pur.get("domain_detail") or (dom_raw if dom_raw not in tax.DOMAINS else ""),
    }


def load_worklist(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def report_path(sha1_git: str) -> Path:
    return STUDY_DIR / "reports" / f"{sha1_git}.json"


def looks_like_cobol(ind: dict, min_divisions: int) -> bool:
    """Cheap gate so we don't spend LLM calls on obvious non-COBOL noise.

    Files like ``WBC_*_FOO.CBL`` ("This is cobol file number N") have 0
    divisions and no PROGRAM-ID; they fail this gate.
    """
    if min_divisions <= 0:
        return True
    if ind["n_divisions"] >= min_divisions:
        return True
    # Salvage real snippets that have a PROGRAM-ID and COBOL-ish verbs.
    if ind["program_ids"] and (ind["perform_count"] or ind["pic_count"]):
        return True
    return False


def build_report(row: dict, *, do_judge: bool, model: str,
                 sleep: float, judge_min_divisions: int = 0) -> dict:
    swhid = row["swhid"]
    sha = row["sha1_git"]
    filename = row.get("name", "")
    c = fetch_content(swhid, filename=filename, polite_delay=sleep)

    is_text = c.is_text
    text = c.text if is_text else ""
    decoded = "utf-8"
    if is_text:
        try:
            c.raw.decode("utf-8")
        except UnicodeDecodeError:
            decoded = "latin-1"
    ind = ind_mod.compute(text, bytes_len=c.length, is_text=is_text,
                          decoded_with=decoded)

    report = {
        "schema": REPORT_SCHEMA,
        "sample": {
            "swhid": swhid,
            "sha1_git": sha,
            "filename": filename,
            "source_csv": row.get("source_csv", ""),
            "n_filenames": int(row.get("n_filenames", 1) or 1),
        },
        "content": {
            "length": c.length,
            "status": c.status,
            "is_text": is_text,
            "decoded_with": decoded,
            "swh_url": f"{SWH_BASE}/{swhid}/",
            "raw_url": f"{SWH_BASE}/api/1/content/sha1_git:{sha}/raw/",
        },
        "indicators": ind.to_dict(),
        "judge": None,
        "generated_at": now_iso(),
    }

    if do_judge and not is_text:
        report["judge"] = {"skipped": "non-text content"}
    elif do_judge and not looks_like_cobol(ind.to_dict(), judge_min_divisions):
        report["judge"] = {"skipped": "below judge-min-divisions gate"}
    elif do_judge:
        report["judge"] = judge_mod.judge(
            filename or swhid, ind.to_dict(), text, model=model)
    return report


def write_indicators_csv(reports: list[dict], path: Path) -> None:
    cols = [
        "sha1_git", "filename", "source_csv", "length", "is_text",
        "total_lines", "blank_lines", "comment_lines", "code_lines",
        "comment_ratio", "source_format_guess", "n_divisions",
        "has_exec_sql", "has_exec_cics", "copy_count", "call_count",
        "perform_count", "goto_count", "comp3_count", "pic_count",
        "program_ids",
        # judge-derived, canonicalized (blank if --no-judge / gated)
        "judge_cobol_confirmed", "judge_dialect_family", "judge_standard",
        "judge_source_format", "judge_domain", "judge_program_type",
        "judge_maturity", "judge_confidence", "judge_dialect_detail",
        "judge_domain_detail",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in reports:
            ind = r["indicators"]
            j = (r.get("judge") or {})
            cv = canonical_view(j.get("verdict")) if isinstance(j, dict) else None
            cv = cv or {}
            w.writerow([
                r["sample"]["sha1_git"], r["sample"]["filename"],
                r["sample"]["source_csv"], r["content"]["length"],
                r["content"]["is_text"],
                ind["total_lines"], ind["blank_lines"], ind["comment_lines"],
                ind["code_lines"], ind["comment_ratio"],
                ind["source_format_guess"], ind["n_divisions"],
                ind["has_exec_sql"], ind["has_exec_cics"], ind["copy_count"],
                ind["call_count"], ind["perform_count"], ind["goto_count"],
                ind["comp3_count"], ind["pic_count"],
                "|".join(ind["program_ids"]),
                cv.get("cobol_confirmed", ""), cv.get("family", ""),
                cv.get("standard", ""), cv.get("source_format", ""),
                cv.get("domain", ""), cv.get("program_type", ""),
                cv.get("maturity", ""), cv.get("confidence", ""),
                cv.get("dialect_detail", ""), cv.get("domain_detail", ""),
            ])


def _dist(counter: Counter, total: int) -> list[str]:
    lines = []
    for k, n in counter.most_common():
        pct = round(100 * n / total, 1) if total else 0.0
        lines.append(f"  - {k or '(blank)'}: {n} ({pct}%)")
    return lines


def summarize(reports: list[dict]) -> dict:
    n = len(reports)
    text_reports = [r for r in reports if r["content"]["is_text"]]
    code_lines = [r["indicators"]["code_lines"] for r in text_reports]
    judged = [r for r in reports if isinstance(r.get("judge"), dict)
              and r["judge"].get("verdict")]
    views = [cv for r in judged
             for cv in [canonical_view(r["judge"]["verdict"])] if cv]

    fmt_ind = Counter(r["indicators"]["source_format_guess"] for r in text_reports)
    cobol_conf = Counter(cv["cobol_confirmed"] for cv in views)
    standards = Counter(cv["standard"] for cv in views)
    families = Counter(cv["family"] for cv in views)
    domains = Counter(cv["domain"] for cv in views)
    ptypes = Counter(cv["program_type"] for cv in views)
    maturity = Counter(cv["maturity"] for cv in views)
    src_fmt_judge = Counter(cv["source_format"] for cv in views)

    feats = {
        "EXEC SQL": sum(r["indicators"]["has_exec_sql"] for r in text_reports),
        "EXEC CICS": sum(r["indicators"]["has_exec_cics"] for r in text_reports),
        "COMP-3": sum(r["indicators"]["comp3_count"] > 0 for r in text_reports),
        "COPY": sum(r["indicators"]["copy_count"] > 0 for r in text_reports),
        "CALL": sum(r["indicators"]["call_count"] > 0 for r in text_reports),
    }

    tok_prompt = sum((r["judge"].get("usage") or {}).get("prompt_tokens", 0)
                     for r in judged)
    tok_completion = sum((r["judge"].get("usage") or {}).get("completion_tokens", 0)
                         for r in judged)

    loc_stats = {}
    if code_lines:
        loc_stats = {
            "min": min(code_lines), "max": max(code_lines),
            "mean": round(statistics.mean(code_lines), 1),
            "median": statistics.median(code_lines),
            "total": sum(code_lines),
        }

    return {
        "n_samples": n,
        "n_text": len(text_reports),
        "n_binary": n - len(text_reports),
        "n_judged": len(judged),
        "loc_code_lines": loc_stats,
        "source_format_indicator": dict(fmt_ind),
        "judge_cobol_confirmed": dict(cobol_conf),
        "judge_dialect_family": dict(families),
        "judge_standard": dict(standards),
        "judge_source_format": dict(src_fmt_judge),
        "judge_domain": dict(domains),
        "judge_program_type": dict(ptypes),
        "judge_maturity": dict(maturity),
        "feature_prevalence": feats,
        "tokens": {"prompt": tok_prompt, "completion": tok_completion},
        "generated_at": now_iso(),
    }


def write_summary_md(summary: dict, reports: list[dict], path: Path) -> None:
    n = summary["n_samples"]
    nt = summary["n_text"]
    L = []
    L.append("# COBOL-in-SWH exploratory study — summary\n")
    L.append(f"_Generated {summary['generated_at']} · {n} samples "
             f"({nt} text, {summary['n_binary']} non-text), "
             f"{summary['n_judged']} LLM-judged._\n")

    loc = summary["loc_code_lines"]
    if loc:
        L.append("## Lines of code (code lines, excl. blank/comment)\n")
        L.append(f"- min **{loc['min']}** · median **{loc['median']}** · "
                 f"mean **{loc['mean']}** · max **{loc['max']}** · "
                 f"total **{loc['total']}**\n")

    L.append("## Source format (mechanical heuristic)\n")
    for k, v in sorted(summary["source_format_indicator"].items(),
                       key=lambda kv: -kv[1]):
        L.append(f"- {k}: {v}")
    L.append("")

    L.append("## Feature prevalence (mechanical, over text files)\n")
    for k, v in summary["feature_prevalence"].items():
        pct = round(100 * v / nt, 1) if nt else 0.0
        L.append(f"- {k}: {v} ({pct}%)")
    L.append("")

    if summary["n_judged"]:
        for title, key in [
            ("Is COBOL? (judge)", "judge_cobol_confirmed"),
            ("Dialect family (judge)", "judge_dialect_family"),
            ("COBOL standard (judge)", "judge_standard"),
            ("Source format (judge)", "judge_source_format"),
            ("Domain (judge)", "judge_domain"),
            ("Program type (judge)", "judge_program_type"),
            ("Maturity (judge)", "judge_maturity"),
        ]:
            c = Counter(summary.get(key, {}))
            total = sum(c.values())
            L.append(f"## {title}\n")
            L.extend(_dist(c, total))
            L.append("")
        tok = summary["tokens"]
        L.append(f"_Judge tokens: {tok['prompt']} prompt + "
                 f"{tok['completion']} completion._\n")

    # A compact per-sample table for quick scanning.
    L.append("## Samples\n")
    L.append("| sha1_git | file | LOC | fmt | divs | SQL | CICS | "
             "family | domain | type | std |")
    L.append("|---|---|---:|---|---:|:-:|:-:|---|---|---|---|")
    for r in reports:
        ind = r["indicators"]
        cv = canonical_view((r.get("judge") or {}).get("verdict")) \
            if isinstance(r.get("judge"), dict) else None
        cv = cv or {}
        L.append("| {sha} | {f} | {loc} | {fmt} | {dv} | {sql} | {cics} | "
                 "{fam} | {dom} | {pt} | {std} |".format(
                     sha=r["sample"]["sha1_git"][:10],
                     f=(r["sample"]["filename"] or "")[:28],
                     loc=ind["code_lines"], fmt=ind["source_format_guess"],
                     dv=ind["n_divisions"],
                     sql="✓" if ind["has_exec_sql"] else "",
                     cics="✓" if ind["has_exec_cics"] else "",
                     fam=cv.get("family", ""), dom=cv.get("domain", ""),
                     pt=cv.get("program_type", ""), std=cv.get("standard", "")))
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the COBOL-in-SWH study.")
    ap.add_argument("--worklist", default=str(STUDY_DIR / "worklist.csv"))
    ap.add_argument("--limit", type=int, default=None,
                    help="process only the first N worklist rows")
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--judge", dest="judge", action="store_true",
                     help="run the LLM-judge (needs OPENROUTER_API_KEY)")
    grp.add_argument("--no-judge", dest="judge", action="store_false",
                     help="fetch + indicators only (no key)")
    ap.set_defaults(judge=False)
    ap.add_argument("--model",
                    default=os.environ.get("COBOL_JUDGE_MODEL", judge_mod.DEFAULT_MODEL))
    ap.add_argument("--judge-min-divisions", type=int, default=0,
                    help="skip the LLM-judge (no API spend) for files with fewer "
                         "than N COBOL divisions, e.g. 2 to skip synthetic noise")
    ap.add_argument("--sleep", type=float, default=0.2,
                    help="polite delay (s) between SWH requests on cache miss")
    ap.add_argument("--force", action="store_true",
                    help="re-judge even if a report with a judge verdict exists")
    ap.add_argument("--tag", default="",
                    help="suffix for aggregate outputs (indicators_<tag>.csv, "
                         "summary_<tag>.[md|json]); reports/ stay shared by sha")
    ap.add_argument("--refresh-indicators", action="store_true",
                    help="recompute indicators/content from cached bytes (no "
                         "fetch, no API) for existing reports, preserving their "
                         "judge verdict; use after an indicators bug fix")
    args = ap.parse_args()
    suffix = f"_{args.tag}" if args.tag else ""

    ensure_dirs()
    rows = load_worklist(Path(args.worklist))
    if args.limit is not None:
        rows = rows[: args.limit]
    print(f"worklist: {len(rows)} samples | judge={'on' if args.judge else 'off'} "
          f"| model={args.model if args.judge else '-'}")

    reports: list[dict] = []
    for i, row in enumerate(rows, 1):
        sha = row["sha1_git"]
        rp = report_path(sha)
        # Refresh: recompute indicators from cached bytes, keep the verdict.
        if args.refresh_indicators and rp.exists():
            existing = json.loads(rp.read_text(encoding="utf-8"))
            try:
                fresh = build_report(row, do_judge=False, model=args.model,
                                     sleep=args.sleep)
            except Exception as e:
                print(f"[{i}/{len(rows)}] {sha[:10]} REFRESH-ERROR: {e}",
                      file=sys.stderr)
                reports.append(existing)
                continue
            fresh["judge"] = existing.get("judge")
            rp.write_text(json.dumps(fresh, indent=2, ensure_ascii=False),
                          encoding="utf-8")
            reports.append(fresh)
            print(f"[{i}/{len(rows)}] {sha[:10]} refreshed "
                  f"copy={fresh['indicators']['copy_count']}")
            continue
        # Resume: reuse an existing report unless we now need a judge it lacks.
        if rp.exists() and not args.force:
            existing = json.loads(rp.read_text(encoding="utf-8"))
            ej = existing.get("judge")
            has_judge = isinstance(ej, dict) and (ej.get("verdict") or ej.get("skipped"))
            if (not args.judge) or has_judge:
                reports.append(existing)
                print(f"[{i}/{len(rows)}] {sha[:10]} cached")
                continue
        try:
            rep = build_report(row, do_judge=args.judge, model=args.model,
                               sleep=args.sleep,
                               judge_min_divisions=args.judge_min_divisions)
        except Exception as e:
            print(f"[{i}/{len(rows)}] {sha[:10]} ERROR: {e}", file=sys.stderr)
            continue
        rp.write_text(json.dumps(rep, indent=2, ensure_ascii=False),
                      encoding="utf-8")
        reports.append(rep)
        jflag = ""
        if args.judge and isinstance(rep.get("judge"), dict):
            v = rep["judge"].get("verdict", {})
            jflag = f" | judge: {v.get('cobol_confirmed')}, " \
                    f"{(v.get('purpose') or {}).get('domain','?')}"
        print(f"[{i}/{len(rows)}] {sha[:10]} {row.get('name','')[:30]} "
              f"loc={rep['indicators']['code_lines']}{jflag}")

    # Aggregate outputs (suffixed by --tag so parallel studies don't clobber).
    write_indicators_csv(reports, STUDY_DIR / f"indicators{suffix}.csv")
    summary = summarize(reports)
    (STUDY_DIR / f"summary{suffix}.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    write_summary_md(summary, reports, STUDY_DIR / f"summary{suffix}.md")
    print(f"\nwrote {len(reports)} reports + indicators{suffix}.csv + "
          f"summary{suffix}.[json|md] -> {STUDY_DIR}")


if __name__ == "__main__":
    main()
