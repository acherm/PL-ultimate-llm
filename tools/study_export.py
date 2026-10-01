"""Common export format for extension studies → the PL-ultimate-llm encyclopedia.

An extension study (`.cbl`/`.CBL`, `.fsf`, `.rpgle`, `.m`, …) "digs" into what an
extension actually holds in Software Heritage. What it learns belongs in the
encyclopedia, not only in a report. Every study therefore writes the same five
files to `data/derived/study_exports/<study_id>/`, and one tool
(`tools/propagate_study.py`) merges them into the encyclopedia's data:

  study.json          what was studied, how, by whom, where the report is
  ext_evidence.csv    observed share of each language/format under an extension,
                      per sampling frame, with a 95 % interval and the method
  claims.csv          proposed changes to the extension→language mapping:
                        observe    the language is there, with a measured share
                                   (evidence only — a study is never a claimant)
                        add        same, and no source claimed it before: proposed
                                   as the extension label `pl/<id>`
                        unobserved claimed by a source, never seen in the sample
                        dispute    claimed by a source, unrelated to the extension
                        label      a non-PL classification of the extension, in the
                                   extension-label vocabulary (docs/extension_labels.md),
                                   e.g. `data:domain` — collected as a proposal for the
                                   curator workflow, never written to the label store
  samples.csv         verified example files (qualified SWHID: origin + path),
                      with who verified them (judges, human reviewer)
  heuristic_eval.csv  measured behaviour of identifiers on this extension
                      (Linguist rules, Pygments, SWH Synid, the study's rules)

Conventions
-----------
* `ext` keeps its case (`.CBL` and `.cbl` are different rows).
* `pl_id` must exist in `data/derived/pl_taxonomy/pl.csv`; non-languages
  (XML layers, data, binaries) have an empty `pl_id` and a `label` like
  `not-code:pml-xml`.
* Shares are percentages of the *frame* (`file`, `repo`, `path`, …), never of
  the archive in general — the frame is part of the fact.
* An `add`/`observe` claim is only proposed when the extension is a
  *conventional* extension of that language (Magma's `.m`), not when a file is
  merely misnamed (C code saved as `main.m`) — that stays evidence only.

This module holds the schema, writers and validation shared by the per-study
exporters (`tools/<study>/export.py`). An exporter provides `main()` (writes the
export) and may provide `study_reviews(sample_row) -> list[review]` — the
study's labels for one sample as `tools/reviewstore.py` records (LLM judges as
`kind=llm`, human reviews as `kind=human`); `tools/propagate_study.py` calls it.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "data" / "derived" / "study_exports"
PL_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "pl.csv"
EXT_CLAIM_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "ext_claim.csv"
SCHEMA_VERSION = "study-export/1"

COLUMNS = {
    "ext_evidence.csv": ["study", "ext", "label", "display", "pl_id", "frame", "share_pct", "ci_lo_pct",
                         "ci_hi_pct", "n_class", "n_frame", "method", "note"],
    "claims.csv": ["study", "ext", "pl_id", "action", "strength", "source_disputed", "label", "share_file_pct",
                   "share_repo_pct", "evidence", "rationale", "status"],
    "samples.csv": ["study", "ext", "pl_id", "label", "sha1_git", "filename", "origin", "path", "branch",
                    "visit_ts", "qualified_swhid", "verified_by", "language_detail", "provenance_kind", "note"],
    "heuristic_eval.csv": ["study", "ext", "heuristic_id", "tool", "metric", "value", "n", "reference", "note"],
}
ACTIONS = {"observe", "add", "unobserved", "dispute", "label"}
FRAMES = {"file", "repo", "path", "repo-reweighted", "file-ppi", "repo-ppi", "file-census", "repo-census",
          "census", "file-filtered"}


def pl_ids() -> set[str]:
    with PL_CSV.open(encoding="utf-8") as f:
        return {r["pl_id"] for r in csv.DictReader(f)}


def ext_claims() -> list[dict]:
    with EXT_CLAIM_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def git_blob_sha1(data: bytes) -> str:
    """sha1_git of a blob — lets an exporter prove the bytes are the SWH content."""
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def qualified_swhid(sha: str, origin: str | None, path: str | None) -> str:
    s = f"swh:1:cnt:{sha}"
    if origin:
        s += f";origin={origin}"
    if path:
        s += f";path={path if path.startswith('/') else '/' + path}"
    return s


def write_export(study_id: str, meta: dict, tables: dict[str, list[dict]]) -> Path:
    """Validate and write one study's export. Returns the export directory."""
    out = EXPORTS / study_id
    out.mkdir(parents=True, exist_ok=True)
    known = pl_ids()
    problems = []
    for name, rows in tables.items():
        cols = COLUMNS[name]
        for i, r in enumerate(rows):
            r.setdefault("study", study_id)
            extra = set(r) - set(cols)
            if extra:
                problems.append(f"{name}[{i}]: unknown columns {sorted(extra)}")
            pid = r.get("pl_id") or ""
            if pid and pid not in known:
                problems.append(f"{name}[{i}]: pl_id {pid!r} not in pl.csv")
            if name == "claims.csv" and r.get("action") not in ACTIONS:
                problems.append(f"{name}[{i}]: bad action {r.get('action')!r}")
            if name == "ext_evidence.csv" and r.get("frame") not in FRAMES:
                problems.append(f"{name}[{i}]: bad frame {r.get('frame')!r}")
    if problems:
        raise SystemExit("export validation failed:\n  " + "\n  ".join(problems[:30]))
    for name, rows in tables.items():
        with (out / name).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS[name])
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLUMNS[name]})
    meta = {"schema": SCHEMA_VERSION, "study_id": study_id, **meta,
            "counts": {k: len(v) for k, v in tables.items()}}
    (out / "study.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"export {study_id}: " + ", ".join(f"{k} {len(v)}" for k, v in tables.items()) + f" → {out}")
    return out
