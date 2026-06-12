#!/usr/bin/env python3
"""Shared storage layer for per-program PL reviews (ground-truth collection).

A *review* is one immutable fact: "<reviewer> looked at <content> and says
<label>". Storage is one JSON file per review:

    reviews/<sha1_git>/<UTC-stamp>--<reviewer-id>--<hash8>.json

Design invariants (see docs/reviews.md for the rationale):
- Keyed by content (sha1_git), NOT by sample path — reviews survive
  reclassification and apply to any future sample with the same bytes.
- Append-only: reviews are never edited. Changing your mind = a new review
  whose `verdict.supersedes` names the old file. Consensus (a derived
  artifact, Phase 2) takes each reviewer's latest.
- One file per review = concurrent reviewers can never produce a git merge
  conflict. Git is the sync layer; there is no central database.
- Humans, PLI tools and LLMs write the same record; they differ only in the
  `reviewer` block (`kind`, `id`, `version`, `runner`, `params`).
- `shown` records the suggestions displayed at review time (anchoring-bias
  trace; for tools, `params.mode` says whether the filename was visible).

`verdict.label` reuses the extension-label vocabulary
(docs/extension_labels.md) at program granularity: `pl/<id>`,
`pl/new:<slug>`, `pl/dialect:<parent>`, `pl/family:<name>`, plus the fixed
non-PL labels (`binary:*`, `data:*`, `docs`, `unknown`, …).
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS_DIR = ROOT / "reviews"
SAMPLES_DIR = ROOT / "samples"
TAXONOMY_DIR = ROOT / "data" / "derived" / "pl_taxonomy"

SCHEMA_VERSION = 1

REVIEWER_KINDS = ("human", "tool", "llm")
CONFIDENCES = ("high", "medium", "low")

# Fixed (non-parameterized) labels from docs/extension_labels.md.
FIXED_LABELS = (
    "binary:image", "binary:audio", "binary:video", "binary:font",
    "binary:archive", "binary:executable", "binary:db", "binary:other",
    "data:json-like", "data:xml-like", "data:yaml", "data:csv-tsv",
    "data:config", "data:domain",
    "docs", "lock/cache", "build-artifact", "model/data",
    "license/manifest", "numeric-suffix", "sha-filename",
    "unknown", "noise",
)

_SLUG = re.compile(r"^[a-z0-9][a-z0-9+._-]*$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_LABEL_PARAM = re.compile(r"^pl/(new|dialect|family):([a-z0-9][a-z0-9+._-]*)$")


# ---------------------------------------------------------------------------
# Taxonomy + samples context (read-only inputs for suggestions/validation)
# ---------------------------------------------------------------------------

def load_pl_index() -> dict[str, str]:
    """pl_id -> canonical_name from the taxonomy."""
    out: dict[str, str] = {}
    try:
        with (TAXONOMY_DIR / "pl.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("pl_id"):
                    out[row["pl_id"]] = row.get("canonical_name") or row["pl_id"]
    except FileNotFoundError:
        pass
    return out


def load_ext_claimants() -> dict[str, list[dict]]:
    """ext -> [{pl_id, strength, source}] (deduped, primaries first)."""
    best: dict[tuple[str, str], dict] = {}
    rank = {"primary": 0, "secondary": 1}
    try:
        with (TAXONOMY_DIR / "ext_claim.csv").open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ext, pl_id = row.get("ext"), row.get("pl_id")
                if not ext or not pl_id:
                    continue
                claim = {
                    "pl_id": pl_id,
                    "strength": row.get("strength") or "",
                    "source": row.get("source") or "",
                }
                prev = best.get((ext, pl_id))
                if prev is None or (rank.get(claim["strength"], 9)
                                    < rank.get(prev["strength"], 9)):
                    best[(ext, pl_id)] = claim
    except FileNotFoundError:
        pass
    out: dict[str, list[dict]] = {}
    for (ext, _), claim in best.items():
        out.setdefault(ext, []).append(claim)
    for claims in out.values():
        claims.sort(key=lambda c: (rank.get(c["strength"], 9), c["pl_id"]))
    return out


def load_samples_index(samples_dir: Path = SAMPLES_DIR) -> dict[str, dict]:
    """sha1_git -> subject info, deduped across sample slots.

    {sha: {sha1_git, swhid, filename, ext, length, predicted_pl_id,
           slots: ["unclassified", "pl/matlab", ...], dir: Path}}
    """
    out: dict[str, dict] = {}
    sha_dirs = list(samples_dir.glob("pl/*/*")) + list(samples_dir.glob("unclassified/*"))
    for sha_dir in sorted(sha_dirs):
        meta_path = sha_dir / "metadata.json"
        if not sha_dir.is_dir() or not meta_path.exists():
            continue
        try:
            m = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        sha = (m.get("sha1_git") or sha_dir.name).lower()
        slot = str(sha_dir.parent.relative_to(samples_dir))
        entry = out.get(sha)
        if entry is None:
            entry = {
                "sha1_git": sha,
                "swhid": f"swh:1:cnt:{sha}",
                "qualified_swhid": m.get("qualified_swhid") or "",
                "filename": m.get("filename") or "",
                "ext": (m.get("ext") or "").lower(),
                "length": int(m.get("length_bytes") or 0),
                "predicted_pl_id": m.get("predicted_pl_id") or "",
                "predicted_via": m.get("predicted_via") or "",
                "slots": [],
                "dir": sha_dir,
            }
            out[sha] = entry
        entry["slots"].append(slot)
    return out


# ---------------------------------------------------------------------------
# Review records
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "anonymous"


def default_reviewer_id() -> str:
    try:
        r = subprocess.run(["git", "config", "user.name"],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0 and r.stdout.strip():
            return slugify(r.stdout.strip())
    except Exception:
        pass
    import getpass
    return slugify(getpass.getuser())


def git_head_short() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def validate_label(label: str, known_pl_ids: set[str]) -> str | None:
    """Return an error string, or None if the label is valid."""
    if label in FIXED_LABELS:
        return None
    m = _LABEL_PARAM.match(label)
    if m:
        if m.group(1) == "dialect" and f"pl/{m.group(2)}" not in known_pl_ids:
            return (f"pl/dialect parent '{m.group(2)}' is not a known pl_id — "
                    f"use pl/new:{m.group(2)} if the parent itself is missing")
        return None
    if label.startswith("pl/"):
        if label in known_pl_ids:
            return None
        if not _SLUG.match(label[3:]):
            return f"malformed pl id in {label!r}"
        return (f"{label!r} is not in the taxonomy — pick an existing pl_id "
                f"or propose it as pl/new:{label[3:]}")
    return (f"unknown label {label!r} — expected pl/<id>, pl/new:<slug>, "
            f"pl/dialect:<parent>, pl/family:<name>, or one of the fixed "
            f"labels from docs/extension_labels.md")


def validate_review(review: dict, known_pl_ids: set[str]) -> list[str]:
    """Return a list of problems (empty = valid)."""
    errs: list[str] = []
    if review.get("schema") != SCHEMA_VERSION:
        errs.append(f"schema must be {SCHEMA_VERSION}")
    subj = review.get("subject") or {}
    if not _HEX40.match((subj.get("sha1_git") or "").lower()):
        errs.append("subject.sha1_git must be a 40-hex sha1_git")
    rev = review.get("reviewer") or {}
    if rev.get("kind") not in REVIEWER_KINDS:
        errs.append(f"reviewer.kind must be one of {REVIEWER_KINDS}")
    if not _SLUG.match(rev.get("id") or ""):
        errs.append("reviewer.id must be a non-empty slug ([a-z0-9+._-])")
    verdict = review.get("verdict") or {}
    label = verdict.get("label")
    comment = (review.get("comment") or "").strip()
    if not label and not comment:
        errs.append("need at least a verdict.label or a comment")
    if label:
        err = validate_label(label, known_pl_ids)
        if err:
            errs.append(err)
        if verdict.get("confidence") not in CONFIDENCES:
            errs.append(f"verdict.confidence must be one of {CONFIDENCES}")
    if not review.get("created_at"):
        errs.append("created_at missing")
    return errs


def new_review(*, subject: dict, reviewer: dict, label: str | None,
               confidence: str | None, comment: str | None,
               shown: dict, supersedes: str | None = None) -> dict:
    return {
        "schema": SCHEMA_VERSION,
        "subject": {
            "sha1_git": subject["sha1_git"],
            "swhid": subject.get("swhid") or f"swh:1:cnt:{subject['sha1_git']}",
            "filename": subject.get("filename") or "",
            "ext": subject.get("ext") or "",
        },
        "reviewer": {
            "kind": reviewer.get("kind") or "human",
            "id": reviewer["id"],
            "version": reviewer.get("version"),
            "runner": reviewer.get("runner"),
            "params": reviewer.get("params"),
        },
        "verdict": {
            "label": label,
            "confidence": confidence if label else None,
            "supersedes": supersedes,
        },
        "comment": (comment or "").strip() or None,
        "shown": shown,
        "created_at": utc_now_iso(),
    }


def review_filename(review: dict) -> str:
    stamp = review["created_at"].replace(":", "").replace("-", "")  # 20260612T093102Z
    payload = json.dumps(review, sort_keys=True, ensure_ascii=False)
    h8 = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
    rid = review["reviewer"]["id"][:24]
    return f"{stamp}--{rid}--{h8}.json"


def write_review(review: dict, *, reviews_dir: Path = REVIEWS_DIR,
                 known_pl_ids: set[str] | None = None) -> Path:
    """Validate and persist one review. O_EXCL: never overwrites."""
    if known_pl_ids is None:
        known_pl_ids = set(load_pl_index())
    errs = validate_review(review, known_pl_ids)
    if errs:
        raise ValueError("; ".join(errs))
    sha = review["subject"]["sha1_git"].lower()
    target_dir = reviews_dir / sha
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / review_filename(review)
    with path.open("x", encoding="utf-8") as f:
        json.dump(review, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def iter_reviews(sha: str | None = None, *,
                 reviews_dir: Path = REVIEWS_DIR):
    """Yield (path, review_dict), oldest first (filenames sort by stamp)."""
    if not reviews_dir.exists():
        return
    dirs = [reviews_dir / sha] if sha else sorted(reviews_dir.iterdir())
    for d in dirs:
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            try:
                yield p, json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue


def reviews_by_sha(*, reviews_dir: Path = REVIEWS_DIR) -> dict[str, list[dict]]:
    """sha -> [review, ...] (each review gains '_file': filename)."""
    out: dict[str, list[dict]] = {}
    for p, r in iter_reviews(reviews_dir=reviews_dir):
        r["_file"] = p.name
        out.setdefault(p.parent.name, []).append(r)
    return out


def latest_per_reviewer(reviews: list[dict]) -> list[dict]:
    """Collapse a sha's reviews to each reviewer's most recent one.

    Reviewer identity is (kind, id, version) so a tool upgrade counts as a
    new, separately-tracked reviewer.
    """
    latest: dict[tuple, dict] = {}
    for r in reviews:  # iter order is oldest->newest
        rev = r.get("reviewer") or {}
        latest[(rev.get("kind"), rev.get("id"), rev.get("version"))] = r
    return list(latest.values())


# ---------------------------------------------------------------------------
# CLI: list reviews for a program (or a summary of everything reviewed)
# ---------------------------------------------------------------------------

def _print_reviews(sha: str, subject: dict, revs: list[dict]) -> None:
    name = subject.get("filename") or "?"
    ext = subject.get("ext") or "?"
    print(f"{name} ({ext}) · {sha}")
    if not revs:
        print("  (no reviews yet)")
        return
    superseded = {(r.get("verdict") or {}).get("supersedes") for r in revs}
    for r in revs:
        v = r.get("verdict") or {}
        rv = r.get("reviewer") or {}
        flags = " [superseded]" if r.get("_file") in superseded else ""
        label = v.get("label") or "(comment only)"
        conf = f" ({v['confidence']})" if v.get("confidence") else ""
        ver = f" {rv['version']}" if rv.get("version") else ""
        print(f"  {r.get('created_at', '?')}  {rv.get('id', '?')} "
              f"<{rv.get('kind', '?')}{ver}>  {label}{conf}{flags}")
        if r.get("comment"):
            print(f"      {r['comment']}")


def _cli(argv: list[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(
        description="List reviews. With no argument: summary of every "
                    "reviewed program. With a sha1_git (full or prefix) or "
                    "a filename substring: that program's full review log.")
    p.add_argument("query", nargs="?")
    args = p.parse_args(argv)

    samples = load_samples_index()
    by_sha = reviews_by_sha()

    if not args.query:
        if not by_sha:
            print("no reviews yet (reviews/ is empty)")
            return 0
        print(f"{len(by_sha)} program(s) reviewed:")
        for sha in sorted(by_sha):
            s = samples.get(sha, {})
            revs = by_sha[sha]
            latest = latest_per_reviewer(revs)
            print(f"  {sha[:12]}  {(s.get('filename') or '?'):<36} "
                  f"{len(revs)} review(s) / {len(latest)} reviewer(s)")
        return 0

    qq = args.query.lower()
    matches = [sha for sha in samples if sha.startswith(qq)]
    if not matches:
        matches = [sha for sha, s in samples.items()
                   if qq in (s.get("filename") or "").lower()]
    if not matches:  # reviews can exist for content no longer in samples/
        matches = [sha for sha in by_sha if sha.startswith(qq)]
    if not matches:
        print(f"no program matches {args.query!r}")
        return 1
    for i, sha in enumerate(sorted(matches)[:20]):
        if i:
            print()
        _print_reviews(sha, samples.get(sha, {}), by_sha.get(sha, []))
    if len(matches) > 20:
        print(f"\n…and {len(matches) - 20} more matches; narrow the query.")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(_cli(sys.argv[1:]))
