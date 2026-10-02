#!/usr/bin/env python3
"""Propagate extension-study exports into the PL-ultimate-llm encyclopedia.

Reads `data/derived/study_exports/<study>/` (format: tools/study_export.py) and
shows — or applies — what each study changes in the encyclopedia:

  mapping    disputes mark the named source's `ext_claim.csv` row `disputed`
             (tools/build_pl_taxonomy.py reads the exports directly, so the CI
             taxonomy rebuild keeps them); a study is never a claimant itself —
             observations are evidence, and edges no source has (`add`) are
             proposals, like non-PL labels;
  evidence   `pl_taxonomy/ext_evidence.csv` (observed shares per frame) and
             `pl_taxonomy/heuristic_eval.csv` (measured identifier behaviour);
  samples    verified files materialised as `samples/pl/<slug>/<sha1_git>/`
             (bytes from the study cache, re-hashed against the SWHID);
  reviews    the study's judgements on those samples, written to the
             encyclopedia's review store `reviews/<sha>/` — LLM judges as
             `kind=llm`, human reviews as `kind=human` — so sample cards show
             them as ground truth.

    python3 tools/propagate_study.py                 # plan for every study
    python3 tools/propagate_study.py --study m       # one study
    python3 tools/propagate_study.py --study m --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
import reviewstore as RS  # noqa: E402
from tools import study_export as SE  # noqa: E402

SAMPLES = ROOT / "samples" / "pl"
SWH = "https://archive.softwareheritage.org"


def read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def studies(selected: list[str] | None) -> list[Path]:
    dirs = sorted(p for p in SE.EXPORTS.iterdir() if p.is_dir()) if SE.EXPORTS.exists() else []
    return [d for d in dirs if not selected or d.name in selected]


# ---------------------------------------------------------------- plan
def plan(d: Path) -> dict:
    meta = json.loads((d / "study.json").read_text())
    claims = read(d / "claims.csv")
    samples = read(d / "samples.csv")
    existing = SE.ext_claims()
    have = {(c["pl_id"], c["ext"], c["source"]) for c in existing}
    adds = [c for c in claims if c["action"] == "add" and c.get("status", "accepted") == "accepted"]
    disputes = [c for c in claims if c["action"] == "dispute" and c.get("status", "accepted") == "accepted"]
    disputed_now = {(c["pl_id"], c["ext"], c["source"]) for c in existing if c.get("strength") == "disputed"}
    pending_disputes = [c for c in disputes if (c["pl_id"], c["ext"], c["source_disputed"]) not in disputed_now]
    new_samples = [s for s in samples if not (SAMPLES / slug(s["pl_id"]) / s["sha1_git"]).exists()]
    print(f"\n=== study {d.name}: {meta.get('title', '')}")
    print(f"    extensions {meta.get('extensions')} · report {meta.get('report')}")
    print(f"    claims: {Counter(c['action'] for c in claims)}")
    for c in claims:
        if c["action"] == "observe":
            print(f"      = observed   {c['ext']:6} {c['pl_id']:28} file {c['share_file_pct']}% "
                  f"repo {c['share_repo_pct']}% (evidence only)")
    for c in adds:
        print(f"      ? add        {c['ext']:6} {c['pl_id']:28} (proposal: no source claims it; "
              f"file {c['share_file_pct']}%)")
    for c in pending_disputes:
        print(f"      ! dispute    {c['ext']:6} {c['pl_id']:28} source={c['source_disputed']}")
    for c in claims:
        if c["action"] == "unobserved":
            print(f"      · unobserved {c['ext']:6} {c['pl_id']:28} ({c['rationale'][:60]})")
        elif c["action"] == "label":
            print(f"      ? label      {c['ext']:6} {c.get('label', ''):28} (proposal for the curator workflow)")
    print(f"    evidence rows: {len(read(d / 'ext_evidence.csv'))} · heuristic evaluations: "
          f"{len(read(d / 'heuristic_eval.csv'))}")
    print(f"    samples: {len(samples)} verified, {len(new_samples)} new → samples/pl/<slug>/<sha>/")
    return {"meta": meta, "adds": adds, "disputes": pending_disputes, "samples": samples,
            "new_samples": new_samples}


def slug(pl_id: str) -> str:
    return pl_id.split("/", 1)[1]


# ---------------------------------------------------------------- apply: samples
def materialise_sample(s: dict, pl_name: dict) -> Path | None:
    raw = SE.content_bytes(s["study"], s["sha1_git"])      # cache, review files or existing sample
    if raw is None:
        print(f"      skip {s['sha1_git'][:10]}: bytes not available (or sha1_git mismatch)")
        return None
    d = SAMPLES / slug(s["pl_id"]) / s["sha1_git"]
    d.mkdir(parents=True, exist_ok=True)
    fname = re.sub(r"[/\x00]", "_", s["filename"]) or "sample" + s["ext"]
    (d / fname).write_bytes(raw)
    qswhid = s["qualified_swhid"]
    meta = {
        "language_claim": pl_name.get(s["pl_id"], s["pl_id"]),
        "predicted_pl_id": s["pl_id"],
        "predicted_via": f"swh_study:{s['study']} ({s['verified_by']})",
        "predicted_confidence": "high",
        "predicted_heuristic_id": None,
        "predicted_matches_claim": "yes",
        "filename": fname,
        "length_bytes": len(raw),
        "expected_length_bytes": len(raw),
        "sha1_git": s["sha1_git"],
        "sha1_git_matches": True,
        "qualified_swhid": qswhid,
        "swh_browser_url": f"{SWH}/{qswhid}/",
        "swh_raw_url": f"{SWH}/api/1/content/sha1_git:{s['sha1_git']}/raw/",
        "github_raw_url": None,
        "fetched_from": "swh",
        "ext": s["ext"],
        "occurrences_in_swh": None,
        "study": {"id": s["study"], "label": s["label"], "language_detail": s["language_detail"],
                  "provenance_kind": s["provenance_kind"], "verified_by": s["verified_by"],
                  "origin": s["origin"], "path": s["path"], "branch": s["branch"], "visit_ts": s["visit_ts"],
                  "note": s["note"]},
    }
    (d / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return d


# ---------------------------------------------------------------- apply: reviews
def study_reviews(study_id: str, s: dict) -> list[dict]:
    """The study's own labels for one sample (hook `tools.<study>.export.study_reviews`)."""
    import importlib
    try:
        mod = importlib.import_module(f"tools.{study_id}.export")
    except ModuleNotFoundError:
        return []
    fn = getattr(mod, "study_reviews", None)
    return fn(s) if fn else []


def write_reviews(study_id: str, samples: list[dict], known: set[str]) -> int:
    n = 0
    for s in samples:
        for rev in study_reviews(study_id, s):
            try:
                RS.write_review(rev, known_pl_ids=known)
                n += 1
            except FileExistsError:
                pass                                     # deterministic filename: already propagated
            except ValueError as e:
                print(f"      review skipped ({s['sha1_git'][:10]}): {e}")
    return n


# ---------------------------------------------------------------- apply: prune
def prune_orphans(study_id: str, samples: list[dict]) -> int:
    """Remove samples this study propagated earlier but no longer exports (and the
    study's own review records on them), so re-exporting with a different pick
    does not leave stale files behind. Samples from other sources are untouched."""
    import shutil
    keep = {s["sha1_git"] for s in samples}
    n = 0
    for meta_path in SAMPLES.glob("*/*/metadata.json"):
        try:
            via = json.loads(meta_path.read_text()).get("predicted_via") or ""
        except (OSError, json.JSONDecodeError):
            continue
        sha = meta_path.parent.name
        if not via.startswith(f"swh_study:{study_id} ") or sha in keep:
            continue
        shutil.rmtree(meta_path.parent)
        for r in (ROOT / "reviews" / sha).glob("*.json"):
            if (json.loads(r.read_text()).get("shown") or {}).get("study") == study_id:
                r.unlink()
        if (ROOT / "reviews" / sha).is_dir() and not any((ROOT / "reviews" / sha).iterdir()):
            (ROOT / "reviews" / sha).rmdir()
        print(f"      pruned {meta_path.parent.relative_to(ROOT)} (no longer in the export)")
        n += 1
    return n


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--study", action="append", help="study id (repeatable); default: all exports")
    ap.add_argument("--apply", action="store_true", help="materialise samples + reviews, rebuild the taxonomy")
    a = ap.parse_args()
    ds = studies(a.study)
    if not ds:
        print("no study exports found under", SE.EXPORTS)
        return 1
    plans = {d.name: plan(d) for d in ds}
    if not a.apply:
        print("\n(plan only — re-run with --apply)")
        return 0
    pl_name = {r["pl_id"]: r["canonical_name"] for r in read(SE.PL_CSV)}
    known = set(pl_name)
    for sid, p in plans.items():
        prune_orphans(sid, p["samples"])
        made = [materialise_sample(s, pl_name) for s in p["samples"]]
        n_rev = write_reviews(sid, [s for s, m in zip(p["samples"], made) if m], known)
        print(f"\n[{sid}] samples written/refreshed: {sum(1 for m in made if m)} · reviews added: {n_rev}")
    # Proposals for the curator workflow: non-PL labels, and PL edges no source has
    # (an `add` is proposed as the extension label `pl/<id>`).
    proposals = []
    for d in ds:
        for c in read(d / "claims.csv"):
            if c.get("status", "accepted") != "accepted":
                continue
            if c.get("action") == "label":
                proposals.append(c)
            elif c.get("action") == "add":
                proposals.append({**c, "label": c["pl_id"]})
    out = ROOT / "data" / "derived" / "study_label_proposals.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["study", "ext", "label", "evidence", "rationale", "status"])
        w.writeheader()
        for c in proposals:
            w.writerow({k: c.get(k, "") for k in w.fieldnames})
    print(f"\nlabel proposals: {len(proposals)} → {out.relative_to(ROOT)} "
          "(file them through the extension-labelling issue form)")
    print("\nrebuilding the taxonomy (tools/build_pl_taxonomy.py) …")
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_pl_taxonomy.py")], check=True,
                   stdout=subprocess.DEVNULL)
    exts = sorted({e for p in plans.values() for e in p["meta"].get("extensions", [])})
    claims = [c for c in SE.ext_claims() if c["ext"] in exts]
    print("ext_claim now, for the studied extensions:")
    for e in exts:
        rows = [c for c in claims if c["ext"] == e]
        print(f"  {e}: {len(rows)} rows · {Counter(c['strength'] for c in rows)} · "
              f"disputed by a study {sum(1 for c in rows if 'disputed by swh_study:' in c.get('evidence', ''))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
