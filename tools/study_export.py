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
  review_items.json   (optional) files offered for human review on the online
                      review page (/review/study/<id>/): provenance only, the
                      form's fields and options, who already reviewed each item.
                      Reviews come back as GitHub issues (tools/ingest_reviews.py)
                      and land in the review store `reviews/`.

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


CACHE = ROOT / ".cache" / "cobol"              # local SWH byte cache of the studies (not in git)
SAMPLES = ROOT / "samples" / "pl"


def content_bytes(study_id: str, sha: str) -> bytes | None:
    """The bytes of a content, verified against its sha1_git, from wherever they are:
    the local SWH cache, the files the review page serves
    (`study_exports/<study>/review_files/`), or an existing sample. The last two are
    in git, so exports and propagation also run where the cache is absent (the
    review-ingest workflow). PL_NO_CACHE=1 skips the cache (to test that path)."""
    import os
    candidates = [] if os.environ.get("PL_NO_CACHE") else [CACHE / f"{sha}.bin"]
    candidates.append(EXPORTS / study_id / "review_files" / sha)
    candidates += [f for f in SAMPLES.glob(f"*/{sha}/*") if f.name != "metadata.json"]
    for c in candidates:
        if c.is_file():
            data = c.read_bytes()
            if git_blob_sha1(data) == sha:
                return data
    return None


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


REVIEW_ITEMS_SCHEMA = "review-items/1"


def write_review_items(study_id: str, spec: dict, raw=None) -> Path:
    """Write the review items an exporter offers to the online review page.

    `spec`: {"schema", "study", "ext", "title", "queue", "queue_note",
    "fields": [{"id", "label", "required"?, "options"?: [{"value","label"}],
    "type"?: "text", "help"?}], "expertise"?: {"topics", "levels"},
    "items": [{"sha1_git", "filename", "origin", "path", …, "reviewed_by": [ids]}]}.
    Items carry no machine label: the page is blind by construction.

    `raw(sha) -> bytes | None` supplies each item's bytes; they are written to
    `review_files/<sha1_git>` (re-hashed against the sha) and served by the site
    next to the page — Software Heritage puts a bot challenge in front of its
    API for browsers, so the page cannot fetch the files from SWH itself.
    """
    if spec.get("schema") != REVIEW_ITEMS_SCHEMA:
        raise SystemExit(f"review items: schema must be {REVIEW_ITEMS_SCHEMA}")
    ids = [f["id"] for f in spec.get("fields", [])]
    if "confidence" not in ids or not any(f.get("required") for f in spec["fields"]):
        raise SystemExit("review items: fields need a required label field and `confidence`")
    for it in spec.get("items", []):
        if not (len(it.get("sha1_git", "")) == 40 and it.get("filename")):
            raise SystemExit(f"review items: bad item {it.get('sha1_git')!r}")
    out = EXPORTS / study_id
    out.mkdir(parents=True, exist_ok=True)
    if raw is not None:
        fdir = out / "review_files"
        fdir.mkdir(exist_ok=True)
        keep = set()
        for it in spec.get("items", []):
            data = raw(it["sha1_git"])
            if data is None or git_blob_sha1(data) != it["sha1_git"]:
                it["served"] = False
                continue
            (fdir / it["sha1_git"]).write_bytes(data)
            it["served"], it["size"] = True, len(data)
            keep.add(it["sha1_git"])
        for f in fdir.iterdir():
            if f.name not in keep:
                f.unlink()
    path = out / "review_items.json"
    path.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"review items {study_id}: {len(spec.get('items', []))} → {path}")
    return path


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
