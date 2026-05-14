#!/usr/bin/env python3
"""Prototype: link each programming language in this repo to a Software Heritage
example via the SWH popular-content-names parquet table.

Background
----------
Following the exchange with Valentin (SWH), the cheap and scalable way to find
real SWH examples for ~3.8k languages is NOT to ask the REST API per blob, but
to query the public derived dataset:

    s3://softwareheritage/derived_datasets/<YYYY-MM-DD>/contents/*.parquet

It has columns:
    id, length, filename, filename_occurrences,
    first_occurrence_timestamp, first_occurrence_revrel, first_occurrence_origin

Plus the nodes parquet, which maps numeric IDs to SWHIDs:
    s3://softwareheritage/derived_datasets/<YYYY-MM-DD>/nodes/node_type=cnt/*.parquet
    s3://softwareheritage/derived_datasets/<YYYY-MM-DD>/nodes/node_type=ori/*.parquet
    s3://softwareheritage/derived_datasets/<YYYY-MM-DD>/nodes/node_type=rev/*.parquet

Strategy
--------
1. Load the lang -> extensions mapping that `master_inventory.py` already built
   in `data/derived/languages_master_augmented.csv` (columns `extensions` and
   `pygments_filenames`).
2. Intersect with the in-repo `data/pl_list.txt` (canonical-name match,
   case-insensitive, alias-aware via `languages/<Name>/meta.json`).
3. Emit ONE DuckDB query that, for each extension, returns the top-K most
   popular files across the entire SWH archive (ranked by `filename_occurrences`).
4. In a second, much cheaper pass, resolve the numeric `id`,
   `first_occurrence_origin`, and `first_occurrence_revrel` to SWHIDs via the
   nodes table (filtered down to just the result set).

Modes
-----
- `--dry-run` (default): print the SQL it would run; do not touch S3.
- `--execute`: actually run the query (requires `duckdb` and S3 httpfs).
- `--shard PATH`: point at a single parquet file (local or s3 URL) instead of
  the full glob — recommended for the first execute pass while iterating.
- `--only LANG[,LANG...]`: restrict to specific canonical language names.

Output
------
- `data/derived/swh_extension_samples.csv` (one row per (lang, ext, sample))
- `data/derived/swh_extension_samples.sql`   (the exact SQL run)

Notes
-----
- Extensions with multiple language claimants (e.g. `.pl` -> Perl/Prolog,
  `.m` -> MATLAB/Objective-C/Mathematica) are tagged `shared` so we know to
  disambiguate later via content heuristics (Linguist-style classifier).
- This script intentionally avoids touching the SWH REST API; the existing
  `audit_repo.py` flow does that and is rate-limited.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DERIVED_CSV = ROOT / "data" / "derived" / "languages_master_augmented.csv"
PL_LIST = ROOT / "data" / "pl_list.txt"
LANGUAGES_DIR = ROOT / "languages"

OUT_DIR = ROOT / "data" / "derived"
OUT_CSV = OUT_DIR / "swh_extension_samples.csv"
OUT_SQL = OUT_DIR / "swh_extension_samples.sql"

DEFAULT_DATASET_DATE = "2026-03-02"  # latest mentioned by Valentin
DEFAULT_S3_PREFIX = "s3://softwareheritage/derived_datasets"
DEFAULT_TOP_K = 5

# Extensions that are too noisy or non-source to be useful evidence of a PL,
# even when an inventory claims them.
EXT_BLOCKLIST = {
    ".txt", ".md", ".html", ".htm", ".xml", ".json", ".yml", ".yaml",
    ".csv", ".tsv", ".log", ".pdf", ".png", ".jpg", ".gif", ".svg",
    ".zip", ".tar", ".gz", ".bin", ".dll", ".so", ".dylib", ".exe",
}

# Restrict to "real" extensions: start with `.`, plain ASCII, 1-8 chars.
EXT_RE = re.compile(r"^\.[A-Za-z0-9_+\-]{1,8}$")


# ---------------------------------------------------------------------------
# Lang -> extensions mapping
# ---------------------------------------------------------------------------

@dataclass
class LangEntry:
    canonical: str
    in_repo: bool
    extensions: set[str] = field(default_factory=set)
    sources: set[str] = field(default_factory=set)  # which inventory contributed each ext


def _split_ext_tokens(blob: str) -> list[str]:
    """`master_inventory.py`-compatible extension splitter."""
    if not blob:
        return []
    raw = re.split(r"[,\s;]+", blob.replace("'", "").replace('"', ""))
    out: list[str] = []
    for tok in raw:
        tok = tok.strip().lower()
        if not tok:
            continue
        if not tok.startswith("."):
            tok = "." + tok
        if EXT_RE.match(tok) and tok not in EXT_BLOCKLIST:
            out.append(tok)
    return out


def load_repo_languages() -> dict[str, str]:
    """Return {lower_name: canonical_name_in_repo} for languages present here."""
    out: dict[str, str] = {}
    if PL_LIST.exists():
        for line in PL_LIST.read_text(encoding="utf-8").splitlines():
            name = line.strip()
            if name:
                out[name.lower()] = name
    # Also pick up directory-name canonicals (which is the source of truth for
    # programs/manifest.json paths). Prefer the directory casing if present.
    if LANGUAGES_DIR.exists():
        for d in LANGUAGES_DIR.iterdir():
            if d.is_dir():
                out.setdefault(d.name.lower(), d.name)
    return out


def load_lang_aliases() -> dict[str, str]:
    """Return {lower_alias_or_name: canonical_dir_name} from per-language meta.json."""
    aliases: dict[str, str] = {}
    if not LANGUAGES_DIR.exists():
        return aliases
    for d in LANGUAGES_DIR.iterdir():
        if not d.is_dir():
            continue
        meta = d / "meta.json"
        if not meta.exists():
            continue
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        canonical_dir = d.name
        aliases[canonical_dir.lower()] = canonical_dir
        name = data.get("name") or canonical_dir
        aliases.setdefault(name.lower(), canonical_dir)
        for a in data.get("aliases") or []:
            aliases.setdefault(str(a).lower(), canonical_dir)
    return aliases


def load_extensions_inventory(repo_canon: dict[str, str], aliases: dict[str, str]) -> dict[str, LangEntry]:
    """Build {canonical_dir_name: LangEntry} keyed by in-repo canonical name."""
    if not DERIVED_CSV.exists():
        sys.exit(
            f"ERROR: {DERIVED_CSV} not found.\n"
            "Run `python3 tools/master_inventory.py` first to build the augmented inventory."
        )

    out: dict[str, LangEntry] = {}

    with DERIVED_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("canonical_name") or "").strip()
            if not name:
                continue
            # Match against in-repo canonical name (via aliases or pl_list).
            canon = aliases.get(name.lower()) or repo_canon.get(name.lower())
            if not canon:
                continue
            entry = out.setdefault(canon, LangEntry(canonical=canon, in_repo=True))
            for ext in _split_ext_tokens(row.get("extensions") or ""):
                entry.extensions.add(ext)
                entry.sources.add("master")
            for ext in _split_ext_tokens(row.get("pygments_filenames") or ""):
                # `pygments_filenames` is glob patterns like `*.py`; strip the `*`
                ext = ext if ext.startswith(".") else "." + ext
                if EXT_RE.match(ext) and ext not in EXT_BLOCKLIST:
                    entry.extensions.add(ext)
                    entry.sources.add("pygments")

    return out


# ---------------------------------------------------------------------------
# SQL generation
# ---------------------------------------------------------------------------

def build_query(
    lang_to_exts: dict[str, LangEntry],
    *,
    contents_path: str,
    top_k: int,
    min_length: int = 32,
    max_length: int = 200_000,
    sample_percent: float | None = None,
) -> tuple[str, dict[str, list[str]]]:
    """Return (SQL string, ext->list[lang] map for client-side bucketing).

    The query:
    1. Builds an inline (extension VARCHAR) values table.
    2. Cross-joins to all contents whose normalized filename ends with that
       extension (case-insensitive), within reasonable size bounds.
    3. Picks top-K by filename_occurrences per extension.
    """
    ext_to_langs: dict[str, list[str]] = defaultdict(list)
    for lang, entry in lang_to_exts.items():
        for ext in entry.extensions:
            ext_to_langs[ext].append(lang)

    if not ext_to_langs:
        sys.exit("ERROR: no (language, extension) pairs found. Check inventory CSV.")

    # Sort for stable SQL output and deduplicate (case-insensitive).
    ext_no_dot = sorted({ext.lower().lstrip(".") for ext in ext_to_langs.keys()})
    in_list = ", ".join(f"'{e}'" for e in ext_no_dot)
    sample_clause = (
        f"USING SAMPLE {sample_percent} PERCENT (BERNOULLI)"
        if sample_percent is not None
        else ""
    )

    sql = f"""\
-- SWH popular-content-names mining for {len(ext_no_dot)} extensions
-- spanning {len(lang_to_exts)} in-repo languages.
-- Contents source: {contents_path}
--
-- Strategy: extract the extension ONCE per row via a single regex (capture
-- group is restricted to ASCII so `lower()` is safe), then filter against an
-- IN-set. This is O(rows) vs the previous O(rows * extensions) cross-join.
-- The full filename is only decoded for the final K * N output rows.

WITH cnts AS (
    SELECT
        c.id                                      AS content_id,
        c.length                                  AS length,
        c.filename                                AS filename_blob,
        c.filename_occurrences                    AS occurrences,
        c.first_occurrence_timestamp              AS first_ts,
        c.first_occurrence_revrel                 AS first_revrel_id,
        c.first_occurrence_origin                 AS first_origin_id,
        lower(regexp_extract(
            decode(c.filename, 'ignore'),
            '\\.([A-Za-z0-9_+\\-]{{1,8}})$',
            1
        )) AS ext_no_dot
    FROM read_parquet('{contents_path}') AS c
    WHERE c.length BETWEEN {min_length} AND {max_length}
      AND octet_length(c.filename) BETWEEN 4 AND 256
    {sample_clause}
),
matched AS (
    SELECT
        content_id, length, filename_blob, occurrences,
        first_ts, first_revrel_id, first_origin_id,
        '.' || ext_no_dot AS extension
    FROM cnts
    WHERE ext_no_dot <> ''
      AND ext_no_dot IN ({in_list})
),
ranked AS (
    SELECT *,
        row_number() OVER (
            PARTITION BY extension
            ORDER BY occurrences DESC, length ASC, content_id ASC
        ) AS rk
    FROM matched
)
SELECT
    extension,
    rk,
    content_id,
    decode(filename_blob, 'ignore') AS filename_str,
    length,
    occurrences,
    first_ts,
    first_revrel_id,
    first_origin_id
FROM ranked
WHERE rk <= {top_k}
ORDER BY extension, rk;
"""
    return sql, dict(ext_to_langs)


def build_resolver_query(
    *, nodes_path_template: str, content_ids: list[int], origin_ids: list[int], rev_ids: list[int]
) -> str:
    """Cheap second-pass query: numeric ID -> SWHID via nodes parquet."""
    cnt_path = nodes_path_template.format(node_type="cnt")
    ori_path = nodes_path_template.format(node_type="ori")
    rev_path = nodes_path_template.format(node_type="rev")

    def _list(ids: Iterable[int]) -> str:
        ids = sorted(set(ids))
        return ",".join(str(i) for i in ids) if ids else "NULL"

    return f"""\
-- Resolve numeric IDs to SWHIDs.
WITH cnts AS (
    SELECT id, swhid FROM read_parquet('{cnt_path}')
    WHERE id IN ({_list(content_ids)})
),
oris AS (
    SELECT id, swhid, url FROM read_parquet('{ori_path}')
    WHERE id IN ({_list(origin_ids)})
),
revs AS (
    SELECT id, swhid FROM read_parquet('{rev_path}')
    WHERE id IN ({_list(rev_ids)})
)
SELECT 'content' AS kind, id, swhid, NULL AS url FROM cnts
UNION ALL
SELECT 'origin'  AS kind, id, swhid, url        FROM oris
UNION ALL
SELECT 'revrel'  AS kind, id, swhid, NULL       FROM revs;
"""


# ---------------------------------------------------------------------------
# Qualified SWHID via GitHub side-channel
# ---------------------------------------------------------------------------
#
# A qualified SWHID looks like:
#   swh:1:cnt:<sha1git>;origin=<URL>;anchor=swh:1:rev:<commit>;path=/<path>
#
# We don't need the SWH cnt-nodes parquet (~840 GB total) for any of these
# four ingredients. Once we have the bytes, the content SWHID is local. The
# trick is going from the parquet's (filename, length) to a credible origin
# + commit. We do that by:
#   1. Searching GitHub by `filename:NAME`.
#   2. For each candidate, fetching the raw bytes; keep the first whose
#      length matches the parquet row.
#   3. Asking GitHub for the latest commit touching that path.
#   4. Re-fetching the file at that commit and re-hashing — if the bytes
#      changed since, drop the anchor (the latest-commit pointer would
#      misrepresent the content).
#   5. Optionally verifying the resulting content SWHID exists in SWH.
#
# Rate-limit notes:
#   - `gh search code` is 30 req/min authenticated.
#   - Repo API calls are 5000/h authenticated.
#   - raw.githubusercontent.com is CDN-served; no rate limit.
#   - SWH API is 120 req/h anonymous.

GH_USER_AGENT = "PL-ultimate-llm/swh_extension_mining"

# GitHub code search has a *separate* rate limit of 10 requests/minute even
# when authenticated. We self-throttle so we don't slam the wall and silently
# get HTTP 403s.
import time as _time
_GH_CODE_SEARCH_INTERVAL = 6.5  # seconds between code-search calls
_gh_last_code_search_at = 0.0


def _gh_token() -> str | None:
    """Pull token from `gh auth token` so urllib can use it."""
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _http_json(url: str, *, token: str | None = None, timeout: float = 20.0) -> object:
    req = urllib.request.Request(url, headers={
        "User-Agent": GH_USER_AGENT,
        "Accept": "application/vnd.github+json",
    })
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _http_bytes(url: str, *, timeout: float = 20.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": GH_USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def sha1_git(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode() + b"\0")
    h.update(data)
    return h.hexdigest()


def gh_search_filename(filename: str, *, token: str | None, max_candidates: int = 5) -> tuple[list[dict], str]:
    """Return (candidates, status). Status is 'ok', 'empty', 'rate_limited', 'http_<code>', 'unprocessable'."""
    global _gh_last_code_search_at
    elapsed = _time.time() - _gh_last_code_search_at
    if elapsed < _GH_CODE_SEARCH_INTERVAL:
        _time.sleep(_GH_CODE_SEARCH_INTERVAL - elapsed)
    _gh_last_code_search_at = _time.time()

    safe = filename.replace('"', '')
    q = f'filename:"{safe}"'
    url = f"https://api.github.com/search/code?q={urllib.parse.quote(q)}&per_page={max_candidates}"
    req = urllib.request.Request(url, headers={
        "User-Agent": GH_USER_AGENT,
        "Accept": "application/vnd.github+json",
    })
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        # On 403 with rate-limit reset header, sleep and retry once.
        if e.code == 403:
            reset = e.headers.get("X-RateLimit-Reset")
            if reset:
                wait = max(0.0, int(reset) - _time.time()) + 1
                if wait < 90:  # don't block forever on a quota that takes >1 min
                    _time.sleep(wait)
                    _gh_last_code_search_at = _time.time()
                    try:
                        with urllib.request.urlopen(req, timeout=20) as r:
                            data = json.loads(r.read())
                    except urllib.error.HTTPError as e2:
                        return [], f"http_{e2.code}"
                else:
                    return [], "rate_limited"
            else:
                return [], "rate_limited"
        elif e.code == 422:
            return [], "unprocessable"
        else:
            return [], f"http_{e.code}"

    items = data.get("items", []) if isinstance(data, dict) else []
    out = []
    for it in items[:max_candidates]:
        repo = (it.get("repository") or {}).get("full_name")
        path = it.get("path")
        if repo and path:
            out.append({"repo": repo, "path": path})
    return out, ("ok" if out else "empty")


def gh_latest_commit_for_path(repo: str, path: str, *, token: str | None) -> str | None:
    safe_path = urllib.parse.quote(path)
    url = f"https://api.github.com/repos/{repo}/commits?path={safe_path}&per_page=1"
    try:
        data = _http_json(url, token=token)
    except urllib.error.HTTPError:
        return None
    if isinstance(data, list) and data:
        return data[0].get("sha")
    return None


def gh_default_branch(repo: str, *, token: str | None) -> str:
    try:
        data = _http_json(f"https://api.github.com/repos/{repo}", token=token)
        if isinstance(data, dict) and data.get("default_branch"):
            return str(data["default_branch"])
    except urllib.error.HTTPError:
        pass
    return "HEAD"


def fetch_raw(repo: str, ref: str, path: str) -> bytes:
    safe_path = urllib.parse.quote(path)
    return _http_bytes(f"https://raw.githubusercontent.com/{repo}/{ref}/{safe_path}")


def verify_swhid_in_swh(sha1git_hex: str, *, timeout: float = 15.0) -> bool:
    """Return True if SWH archive has this content SWHID."""
    url = f"https://archive.softwareheritage.org/api/1/content/sha1_git:{sha1git_hex}/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": GH_USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except urllib.error.HTTPError:
        return False
    except Exception:
        return False


def build_qualified_swhid(content_swhid: str, *, origin: str, anchor: str | None, path: str) -> str:
    parts = [content_swhid, f"origin={origin}"]
    if anchor:
        parts.append(f"anchor={anchor}")
    parts.append(f"path={path}")
    return ";".join(parts)


@dataclass
class QualifyResult:
    status: str  # 'ok' | 'no_candidate' | 'length_mismatch' | 'fetch_error' | 'commit_drift'
    content_swhid: str | None = None
    origin: str | None = None
    anchor: str | None = None  # swh:1:rev:<commit-sha>
    path: str | None = None
    qualified: str | None = None
    verified_in_swh: bool | None = None
    notes: str = ""
    # Phase-3 classification (set when bytes were fetched and classifier ran).
    predicted_pl_id: str | None = None
    predicted_language: str | None = None
    predicted_via: str | None = None
    predicted_confidence: str | None = None
    predicted_heuristic_id: str | None = None


def qualify_via_github(
    filename: str,
    expected_length: int,
    *,
    token: str | None,
    max_candidates: int = 5,
    verify_in_swh: bool = True,
    classifier=None,  # optional pl_classify.Classifier
    file_ext: str | None = None,  # e.g. '.m'; classifier needs this
) -> QualifyResult:
    candidates, search_status = gh_search_filename(filename, token=token, max_candidates=max_candidates)
    if not candidates:
        # Map the search-side status to a QualifyResult status so the failure
        # mode is visible in the CSV instead of being lost as a generic miss.
        status_map = {
            "empty": "no_candidate",
            "rate_limited": "rate_limited",
            "unprocessable": "unprocessable_query",
        }
        st = status_map.get(search_status, search_status if search_status.startswith("http_") else "search_error")
        return QualifyResult(status=st, notes=f"github search: {search_status}")

    last_notes = ""
    for cand in candidates:
        repo, path = cand["repo"], cand["path"]
        try:
            ref = gh_default_branch(repo, token=token)
            data = fetch_raw(repo, ref, path)
        except Exception as e:
            last_notes = f"fetch error on {repo}: {type(e).__name__}"
            continue
        if len(data) != expected_length:
            last_notes = f"length {len(data)} vs expected {expected_length} on {repo}"
            continue

        content_hash = sha1_git(data)
        content_swhid = f"swh:1:cnt:{content_hash}"

        # Anchor: latest commit on this path, *if* the file at that commit still
        # has the same bytes (otherwise the anchor would misrepresent content).
        anchor = None
        commit_sha = gh_latest_commit_for_path(repo, path, token=token)
        if commit_sha:
            try:
                pinned = fetch_raw(repo, commit_sha, path)
                if sha1_git(pinned) == content_hash:
                    anchor = f"swh:1:rev:{commit_sha}"
                else:
                    last_notes = "latest commit drifted; bytes differ from HEAD"
            except Exception:
                pass

        origin = f"https://github.com/{repo}"
        norm_path = path if path.startswith("/") else "/" + path
        qualified = build_qualified_swhid(content_swhid, origin=origin, anchor=anchor, path=norm_path)
        verified = verify_swhid_in_swh(content_hash) if verify_in_swh else None

        # Phase-3: classify the bytes against the taxonomy + Linguist heuristics.
        pred_pl_id = pred_lang = pred_via = pred_conf = pred_h = None
        if classifier is not None and file_ext:
            try:
                cres = classifier.classify_bytes(file_ext, data)
                pred_pl_id = cres.pl_id
                pred_lang = cres.predicts_language
                pred_via = cres.via
                pred_conf = cres.confidence
                pred_h = cres.matched_heuristic_id
            except Exception as e:
                pred_via = f"classify_error:{type(e).__name__}"

        return QualifyResult(
            status="ok" if anchor else "commit_drift",
            content_swhid=content_swhid,
            origin=origin,
            anchor=anchor,
            path=norm_path,
            qualified=qualified,
            verified_in_swh=verified,
            notes=last_notes,
            predicted_pl_id=pred_pl_id,
            predicted_language=pred_lang,
            predicted_via=pred_via,
            predicted_confidence=pred_conf,
            predicted_heuristic_id=pred_h,
        )

    return QualifyResult(status="length_mismatch", notes=last_notes)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset-date", default=DEFAULT_DATASET_DATE,
                   help=f"SWH derived dataset date (default: {DEFAULT_DATASET_DATE}).")
    p.add_argument("--s3-prefix", default=DEFAULT_S3_PREFIX,
                   help="Prefix for SWH derived datasets (default: %(default)s).")
    p.add_argument("--shard", default=None,
                   help="Override the contents path with a single parquet (local or s3 URL). "
                        "Useful for low-cost smoke tests.")
    p.add_argument("--top-k", type=int, default=DEFAULT_TOP_K,
                   help="Examples per extension (default: %(default)d).")
    p.add_argument("--sample-percent", type=float, default=None,
                   help="If set, scan only this percent of rows via "
                        "USING SAMPLE Bernoulli. Use for fast smoke tests "
                        "(e.g. --sample-percent 1).")
    p.add_argument("--memory-limit", default="6GB",
                   help="DuckDB memory limit (default: %(default)s).")
    p.add_argument("--threads", type=int, default=8,
                   help="DuckDB thread count (default: %(default)d).")
    p.add_argument("--skip-resolve", action="store_true",
                   help="Skip the SWHID resolver pass (numeric IDs only). "
                        "The resolver hits the multi-GB nodes/ parquets on S3 "
                        "and is slow over flaky links.")
    p.add_argument("--no-qualify", action="store_true",
                   help="Skip the GitHub-side-channel pass that builds qualified "
                        "SWHIDs (origin + anchor commit + path) per row. By "
                        "default, qualified SWHIDs are computed when --execute.")
    p.add_argument("--qualify-max-candidates", type=int, default=5,
                   help="Per row, max GitHub search candidates to try before "
                        "giving up (default: %(default)d).")
    p.add_argument("--qualify-skip-swh-verify", action="store_true",
                   help="Skip the optional one-shot SWH archive HTTP check "
                        "for each computed content SWHID. SWH's anonymous "
                        "rate limit is 120 req/h.")
    p.add_argument("--no-classify", action="store_true",
                   help="Skip the content-based PL classifier "
                        "(`pl_classify.Classifier`). By default, when bytes "
                        "are fetched during the qualify pass, they're classified "
                        "against the taxonomy + Linguist heuristics so the CSV "
                        "carries `predicted_pl_id` per row.")
    p.add_argument("--nodes-base", default=None,
                   help="Override base path for nodes parquets (e.g. a local "
                        "directory). Default: <s3-prefix>/<dataset-date>/nodes.")
    p.add_argument("--only", default="",
                   help="Comma-separated language canonical names to restrict to.")
    p.add_argument("--mine-extensions", default=None,
                   help="Bypass the PL-driven inventory and mine an explicit list of "
                        "extensions. Argument is a path to a text file with one ext per "
                        "line (with or without leading dot). Use to mine samples for "
                        "unattributed/weakly-attributed extensions (e.g. the review "
                        "queue's top-N). Mined samples land under samples/unclassified/ "
                        "or under their classifier-predicted pl_id; per-ext pages render "
                        "them on /ext/<x>/ regardless of pl_id attribution.")
    p.add_argument("--execute", action="store_true",
                   help="Actually run the query via duckdb. Default is dry-run (print SQL).")
    p.add_argument("--out-csv", default=str(OUT_CSV),
                   help="Output CSV path (default: %(default)s).")
    p.add_argument("--out-sql", default=str(OUT_SQL),
                   help="Where to save the generated SQL (default: %(default)s).")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    repo_canon = load_repo_languages()
    aliases = load_lang_aliases()

    if args.mine_extensions:
        # Bypass the PL-driven inventory entirely. Build a single synthetic
        # entry whose "extensions" set is exactly the list from the file. The
        # ext_to_langs map will tag every extension with the synthetic
        # claimant "_review_queue" — that's fine because the actual per-row
        # `predicted_pl_id` is set by the classifier at fetch time, and the
        # site renders these samples on /ext/<x>/ pages by extension, not
        # by claimed language.
        src = Path(args.mine_extensions)
        if not src.exists():
            sys.exit(f"ERROR: --mine-extensions file not found: {src}")
        exts: set[str] = set()
        for line in src.read_text(encoding="utf-8").splitlines():
            tok = line.strip()
            if not tok or tok.startswith("#"):
                continue
            ext = tok if tok.startswith(".") else "." + tok
            ext = ext.lower()
            if EXT_RE.match(ext) and ext not in EXT_BLOCKLIST:
                exts.add(ext)
        if not exts:
            sys.exit(f"ERROR: --mine-extensions {src} contained no valid extensions.")
        print(f"--mine-extensions: {len(exts)} explicit extensions from {src}")
        inventory = {"_review_queue": LangEntry(
            canonical="_review_queue", in_repo=False, extensions=exts,
        )}
    else:
        inventory = load_extensions_inventory(repo_canon, aliases)

    if args.only:
        wanted = {n.strip() for n in args.only.split(",") if n.strip()}
        inventory = {k: v for k, v in inventory.items() if k in wanted}
        if not inventory:
            sys.exit(f"ERROR: --only filter matched nothing. Available canonicals like: "
                     f"{sorted(list(repo_canon.values()))[:5]}")

    # Stats
    total_langs = len(inventory)
    total_pairs = sum(len(e.extensions) for e in inventory.values())
    langs_no_ext = [lang for lang, e in inventory.items() if not e.extensions]
    print(f"Languages with extensions: {total_langs - len(langs_no_ext)} / {total_langs} matched in repo")
    print(f"(language, extension) pairs: {total_pairs}")
    if langs_no_ext[:5]:
        print(f"Examples without extensions (skipped): {langs_no_ext[:5]}")

    contents_path = args.shard or (
        f"{args.s3_prefix}/{args.dataset_date}/contents/*.parquet"
    )
    nodes_base = args.nodes_base or f"{args.s3_prefix}/{args.dataset_date}/nodes"
    nodes_path_template = f"{nodes_base}/node_type={{node_type}}/*.parquet"

    sql, ext_to_langs = build_query(
        inventory,
        contents_path=contents_path,
        top_k=args.top_k,
        sample_percent=args.sample_percent,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    Path(args.out_sql).write_text(sql, encoding="utf-8")
    print(f"Wrote SQL to {args.out_sql} ({len(sql)} bytes)")

    # Always emit the ext->langs map so downstream can disambiguate shared extensions.
    map_path = Path(args.out_sql).with_suffix(".extmap.json")
    map_path.write_text(json.dumps(ext_to_langs, indent=2, sort_keys=True), encoding="utf-8")
    shared = sum(1 for v in ext_to_langs.values() if len(v) > 1)
    print(f"Wrote extension->languages map to {map_path} (shared extensions: {shared})")

    if not args.execute:
        print("\n--- DRY RUN ---")
        print("Re-run with --execute to actually query SWH.")
        print("First, smoke-test with a single shard, e.g.:")
        print(f"  --shard '{args.s3_prefix}/{args.dataset_date}/contents/0.parquet' --execute")
        return 0

    # --execute path: lazy-import duckdb and run.
    try:
        import duckdb  # type: ignore
    except ImportError:
        sys.exit("ERROR: duckdb not installed. `pip install duckdb` then re-run with --execute.")

    print(f"\nExecuting against: {contents_path}")
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    # Public anonymous S3 read. HTTP defaults are too tight for multi-GB shards.
    con.execute("SET s3_region='us-east-1';")
    con.execute("SET http_timeout=600000;")  # 10 min per request
    con.execute("SET http_retries=5;")
    con.execute(f"SET memory_limit='{args.memory_limit}';")
    con.execute(f"SET threads={args.threads};")
    rows = con.execute(sql).fetchall()
    columns = [d[0] for d in con.description]
    print(f"Got {len(rows)} sample rows from {contents_path}.")

    # Resolve IDs -> SWHIDs.
    content_ids = [r[columns.index("content_id")] for r in rows]
    origin_ids = [r[columns.index("first_origin_id")] for r in rows if r[columns.index("first_origin_id")] is not None]
    rev_ids = [r[columns.index("first_revrel_id")] for r in rows if r[columns.index("first_revrel_id")] is not None]

    swhid_map: dict[tuple[str, int], dict] = {}
    if not args.skip_resolve and (content_ids or origin_ids or rev_ids):
        resolver_sql = build_resolver_query(
            nodes_path_template=nodes_path_template,
            content_ids=content_ids,
            origin_ids=origin_ids,
            rev_ids=rev_ids,
        )
        print(f"Resolving SWHIDs against {nodes_base} (this can be slow over S3)...")
        try:
            for kind, nid, swhid, url in con.execute(resolver_sql).fetchall():
                swhid_map[(kind, nid)] = {"swhid": swhid, "url": url}
        except Exception as exc:
            print(f"WARNING: SWHID resolution failed ({exc!r}); writing CSV with NULL SWHIDs.")
    elif args.skip_resolve:
        print("Skipping SWHID resolution (--skip-resolve). CSV will have numeric IDs only.")

    # Optionally build qualified SWHIDs via GitHub side-channel.
    # Cache by (filename, length) so duplicates across shared extensions and
    # multiple language claimants only cost one GitHub round-trip.
    qualify_cache: dict[tuple[str, int], QualifyResult] = {}
    name_to_pl_id: dict[str, str] = {}  # populated below if classifier loads
    classifier = None
    if args.execute and not args.no_qualify:
        token = _gh_token()
        if not token:
            print("WARNING: gh CLI not authenticated; using anonymous GitHub API "
                  "(60 req/h). Run `gh auth login` for higher limits.")

        # Phase-3: lazy-load classifier + canonical_name -> pl_id index from the
        # taxonomy. Best-effort: if the taxonomy hasn't been built, we still
        # qualify (just without language predictions).
        if not args.no_classify:
            try:
                sys.path.insert(0, str(ROOT / "tools"))
                from pl_classify import Classifier  # type: ignore
                classifier = Classifier()
                pl_csv = ROOT / "data" / "derived" / "pl_taxonomy" / "pl.csv"
                if pl_csv.exists():
                    for p in csv.DictReader(open(pl_csv, encoding="utf-8")):
                        # Index canonical_name AND linguist_key, lowercased,
                        # so the row's `lang` column resolves regardless of
                        # which spelling/casing master_inventory chose.
                        if p.get("canonical_name"):
                            name_to_pl_id.setdefault(p["canonical_name"].lower(), p["pl_id"])
                        if p.get("linguist_key"):
                            name_to_pl_id.setdefault(p["linguist_key"].lower(), p["pl_id"])
                # Also fold in aliases for one more shot at resolving.
                pl_alias_csv = ROOT / "data" / "derived" / "pl_taxonomy" / "pl_alias.csv"
                if pl_alias_csv.exists():
                    for a in csv.DictReader(open(pl_alias_csv, encoding="utf-8")):
                        if a.get("alias") and a.get("pl_id"):
                            name_to_pl_id.setdefault(a["alias"].lower(), a["pl_id"])
                print(f"Classifier loaded: {len(classifier.rules_by_ext)} exts with rules; "
                      f"{len(name_to_pl_id)} canonical names indexed.")
            except SystemExit as e:
                print(f"WARNING: classifier unavailable ({e}); continuing without predictions.")
                classifier = None
            except Exception as e:
                print(f"WARNING: classifier import failed ({type(e).__name__}: {e}); "
                      "continuing without predictions.")
                classifier = None

        unique_files = {(r[columns.index("filename_str")],
                         r[columns.index("length")],
                         r[columns.index("extension")]) for r in rows}
        print(f"Building qualified SWHIDs for {len(unique_files)} unique (filename, length) pairs...")
        ok = drift = miss = 0
        for i, (fname, flen, ext) in enumerate(sorted(unique_files), start=1):
            res = qualify_via_github(
                fname, flen,
                token=token,
                max_candidates=args.qualify_max_candidates,
                verify_in_swh=not args.qualify_skip_swh_verify,
                classifier=classifier,
                file_ext=ext,
            )
            qualify_cache[(fname, flen)] = res
            if res.status == "ok": ok += 1
            elif res.status == "commit_drift": drift += 1
            else: miss += 1
            if i % 10 == 0 or i == len(unique_files):
                print(f"  [{i}/{len(unique_files)}] ok={ok} drift={drift} miss={miss}")
        print(f"Qualify done: ok={ok}, commit_drift={drift}, no_anchor/no_match={miss}")

    # Write CSV: explode each (extension) row into one row per claiming language.
    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "language", "extension", "shared", "rk",
            "filename", "length", "occurrences", "first_ts",
            "content_id", "content_swhid",
            "first_revrel_id", "revrel_swhid",
            "first_origin_id", "origin_swhid", "origin_url",
            # Qualified-SWHID columns (GitHub side-channel).
            "qualify_status", "qualified_swhid",
            "qualify_origin", "qualify_anchor", "qualify_path",
            "qualify_verified_in_swh", "qualify_notes",
            # Phase-3 classification columns.
            "predicted_pl_id", "predicted_language",
            "predicted_via", "predicted_confidence", "predicted_heuristic_id",
            "predicted_matches_claim",
        ])
        for r in rows:
            row = dict(zip(columns, r))
            ext = row["extension"]
            langs = ext_to_langs.get(ext, [])
            shared = "yes" if len(langs) > 1 else "no"
            content_swhid_resolved = swhid_map.get(("content", row["content_id"]), {}).get("swhid")
            origin_meta = swhid_map.get(("origin", row.get("first_origin_id")), {})
            rev_swhid = swhid_map.get(("revrel", row.get("first_revrel_id")), {}).get("swhid")
            qres = qualify_cache.get((row["filename_str"], row["length"]))
            content_swhid = (qres.content_swhid if qres and qres.content_swhid
                             else content_swhid_resolved)
            for lang in langs:
                # Compare classifier's prediction against the language credited
                # to this row. Resolve `lang` to a pl_id via the taxonomy index
                # we built earlier; if not in index, leave the comparison blank.
                lang_pl_id = name_to_pl_id.get(lang.lower(), "")
                if qres and qres.predicted_pl_id and lang_pl_id:
                    matches = "yes" if qres.predicted_pl_id == lang_pl_id else "no"
                elif qres and qres.predicted_pl_id and not lang_pl_id:
                    matches = "unknown_lang"
                else:
                    matches = ""
                w.writerow([
                    lang, ext, shared, row["rk"],
                    row["filename_str"], row["length"], row["occurrences"], row["first_ts"],
                    row["content_id"], content_swhid,
                    row.get("first_revrel_id"), rev_swhid,
                    row.get("first_origin_id"), origin_meta.get("swhid"), origin_meta.get("url"),
                    (qres.status if qres else ""),
                    (qres.qualified if qres else ""),
                    (qres.origin if qres else ""),
                    (qres.anchor if qres else ""),
                    (qres.path if qres else ""),
                    ("" if not qres or qres.verified_in_swh is None
                     else ("yes" if qres.verified_in_swh else "no")),
                    (qres.notes if qres else ""),
                    (qres.predicted_pl_id if qres else "") or "",
                    (qres.predicted_language if qres else "") or "",
                    (qres.predicted_via if qres else "") or "",
                    (qres.predicted_confidence if qres else "") or "",
                    (qres.predicted_heuristic_id if qres else "") or "",
                    matches,
                ])
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
