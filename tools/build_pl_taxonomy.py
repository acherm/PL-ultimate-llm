#!/usr/bin/env python3
"""Phase 1: build a first-class PL taxonomy with provenance per ext claim.

Produces four tables under `data/derived/pl_taxonomy/`:

- `pl.csv`        — one row per programming language entity
- `pl_alias.csv`  — many-to-one aliases (with source)
- `ext_claim.csv` — many-to-many (pl, ext, source) with `strength`
- `ext_summary.csv` — per-extension polysemy report aggregated from `ext_claim`

Why this exists
---------------
`tools/master_inventory.py` already harvests data from PLDB, GitHub Linguist,
Pygments, Wikipedia, Esolang, Hyperpolyglot, Rosetta Code — but it *unions*
the extensions per language into a single set, dropping two crucial signals:

1. **Source of each claim** (was this Linguist's call, Pygments', or PLDB's?)
2. **Strength of each claim** (Linguist's primary vs secondary distinction)

Without these, `Python -> .rpy` and `Ren'Py -> .rpy` look equally confident,
even though Linguist explicitly lists `.rpy` as Python's *secondary* extension
and Ren'Py's only/primary one.

Strength inference rules
------------------------
- **Linguist**: by Linguist's own convention, `extensions[0]` is *primary*,
  the rest are *secondary*. Source: `lib/linguist/languages.yml`.
- **Pygments**: each lexer's `filenames` glob list is in stated-priority
  order; the first non-trivial entry is treated as *primary*.
- **PLDB / Wikipedia / Esolang / Rosetta Code / Hyperpolyglot**: no upstream
  primary/secondary distinction — recorded with `strength='unknown'`.

The taxonomy preserves multiple claims for the same `(pl, ext)` pair if they
come from different sources (e.g., Linguist says secondary, Pygments says
primary). Downstream consumers (e.g., `swh_extension_mining.py`) decide how
to weight them.

Inputs
------
- `data/derived/languages_master_augmented.csv`   (built by master_inventory.py)
- `data/raw/linguist_languages.yml`               (raw Linguist YAML)
- `pygments.lexers._mapping.LEXERS`               (in-process)
- `languages/<L>/meta.json`                       (in-repo aliases)

Run
---
    python3 tools/build_pl_taxonomy.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def _gh_owner_repo() -> str | None:
    """Best-effort: resolve owner/name via `gh repo view`. Used to build
    issue URLs as evidence on manual_add ext claims."""
    try:
        r = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name"],
            check=True, text=True, capture_output=True, timeout=5,
        )
        data = json.loads(r.stdout)
        return f"{data['owner']['login']}/{data['name']}"
    except Exception:
        return None

ROOT = Path(__file__).resolve().parents[1]
# Pick the most-augmented master CSV available (the master_inventory pipeline
# layers Pygments and Rosetta Code on top of the base). The earlier
# `languages_master_augmented.csv` only has Hyperpolyglot — pygments_name and
# pygments_filenames are empty in that file.
_MASTER_DERIVED = ROOT / "data" / "derived"
_MASTER_CANDIDATES = [
    _MASTER_DERIVED / "languages_master_augmented_rosettacode.csv",
    _MASTER_DERIVED / "languages_master_augmented_pygments.csv",
    _MASTER_DERIVED / "languages_master_augmented.csv",
    _MASTER_DERIVED / "languages_master.csv",
]
MASTER_CSV = next((p for p in _MASTER_CANDIDATES if p.exists()), _MASTER_CANDIDATES[-1])
LINGUIST_YAML = ROOT / "data" / "raw" / "linguist_languages.yml"
LINGUIST_HEURISTICS_YAML = ROOT / "data" / "raw" / "linguist_heuristics.yml"
LANGUAGES_DIR = ROOT / "languages"
OUT_DIR = ROOT / "data" / "derived" / "pl_taxonomy"

# Same defensive cleanup as swh_extension_mining.
EXT_RE = re.compile(r"^\.[A-Za-z0-9_+\-]{1,12}$")


# ---------------------------------------------------------------------------
# Slug / id generation
# ---------------------------------------------------------------------------

# Common PL-name special characters mapped to readable ASCII so slugs stay
# distinguishable: `C++` vs `C#` vs `C` should not collide.
_SLUG_REPLACEMENTS = [
    ("++", "pp"),
    ("#", "sharp"),
    ("*", "star"),
    ("&", "and"),
    ("@", "at"),
    ("?", "q"),
    ("!", "bang"),
    ("/", "-"),
    (":", "-"),
    (".", "-"),
    (" ", "-"),
    ("'", ""),
    ('"', ""),
]


def slugify(name: str) -> str:
    s = name.strip()
    for old, new in _SLUG_REPLACEMENTS:
        s = s.replace(old, new)
    s = re.sub(r"[^A-Za-z0-9\-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-").lower()
    return s or "unknown"


def make_pl_id(name: str, used: set[str]) -> str:
    base = slugify(name)
    cand = f"pl/{base}"
    if cand not in used:
        used.add(cand)
        return cand
    # Disambiguate collisions deterministically.
    for i in range(2, 1000):
        cand = f"pl/{base}-{i}"
        if cand not in used:
            used.add(cand)
            return cand
    raise RuntimeError(f"too many collisions for slug base {base!r}")


# ---------------------------------------------------------------------------
# Source loaders
# ---------------------------------------------------------------------------

def _norm_ext(tok: str) -> str | None:
    tok = tok.strip().lower()
    if not tok:
        return None
    # Pygments globs use `*.py`; strip the glob marker if present.
    if tok.startswith("*"):
        tok = tok[1:]
    if not tok.startswith("."):
        tok = "." + tok
    return tok if EXT_RE.match(tok) else None


def load_linguist() -> dict[str, dict]:
    """Return {linguist_name: {'extensions': [list_in_order], 'type': str, ...}}."""
    if not LINGUIST_YAML.exists():
        sys.exit(f"ERROR: {LINGUIST_YAML} not found. Run master_inventory.py first.")
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.exit("ERROR: PyYAML required (`pip install pyyaml`).")
    with LINGUIST_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        sys.exit("ERROR: linguist YAML did not parse to a dict.")
    return data


def load_pygments() -> dict[str, dict]:
    """Return {pygments_class: {'filenames': [...], 'aliases': [...], 'mimetypes': [...]}}."""
    try:
        from pygments.lexers._mapping import LEXERS  # type: ignore
    except ImportError:
        sys.exit("ERROR: Pygments required (`pip install pygments`).")
    out = {}
    for cls, (module, name, aliases, filenames, mimetypes) in LEXERS.items():
        out[cls] = {
            "name": name,
            "aliases": list(aliases),
            "filenames": list(filenames),
            "mimetypes": list(mimetypes),
        }
    return out


def load_master_inventory() -> list[dict]:
    if not MASTER_CSV.exists():
        sys.exit(f"ERROR: {MASTER_CSV} not found. Run master_inventory.py first.")
    rows = []
    with MASTER_CSV.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def load_linguist_heuristics() -> dict | None:
    """Return parsed heuristics.yml or None if absent."""
    if not LINGUIST_HEURISTICS_YAML.exists():
        return None
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.exit("ERROR: PyYAML required for heuristics parsing.")
    with LINGUIST_HEURISTICS_YAML.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_predicates(rule: dict, named_patterns: dict) -> list[dict]:
    """Compile a Linguist rule (or sub-rule) into a flat list of predicates.

    Each predicate is `{kind: 'any'|'not_any', regexes: [str, ...]}`.
    A rule matches iff *every* predicate holds for the content.
    Returns [] for a "default" rule with no pattern (always matches).
    """
    if "and" in rule:
        out: list[dict] = []
        for sub in rule.get("and", []) or []:
            out.extend(_resolve_predicates(sub, named_patterns))
        return out

    out = []
    pat = rule.get("pattern")
    neg = rule.get("negative_pattern")
    named = rule.get("named_pattern")

    def _as_list(x) -> list[str]:
        if x is None:
            return []
        if isinstance(x, str):
            return [x]
        if isinstance(x, list):
            return [str(p) for p in x]
        return [str(x)]

    if pat is not None:
        out.append({"kind": "any", "regexes": _as_list(pat)})
    if neg is not None:
        out.append({"kind": "not_any", "regexes": _as_list(neg)})
    if named is not None:
        np = named_patterns.get(named)
        if np is None:
            # Unknown named pattern — record as always-fails so we don't silently match.
            out.append({"kind": "any", "regexes": [r"(?!)"]})
        else:
            out.append({"kind": "any", "regexes": _as_list(np)})
    return out


def build_heuristic_rows(heur: dict, linguist_to_pl_id: dict[str, str]) -> list[dict]:
    """Flatten heuristics.yml into one row per (ext, rule). Resolve named patterns inline.

    Schema:
      heuristic_id, applies_to_ext, priority, predicts_language, predicts_pl_id,
      pattern_kind, predicates_json, source
    """
    if not heur:
        return []
    named_patterns = (heur.get("named_patterns") or {})
    out: list[dict] = []
    for block_idx, block in enumerate(heur.get("disambiguations") or []):
        exts = [e for e in (block.get("extensions") or []) if isinstance(e, str)]
        rules = block.get("rules") or []
        for ext in exts:
            for rule_idx, rule in enumerate(rules):
                preds = _resolve_predicates(rule, named_patterns)
                lang = rule.get("language") or ""
                if isinstance(lang, list):
                    # Some rules predict multiple languages (rare). Emit one
                    # row per claimant.
                    langs = [str(L) for L in lang]
                else:
                    langs = [str(lang)] if lang else []
                if not langs:
                    continue
                kind = "default" if not preds else "predicates"
                for lg in langs:
                    out.append({
                        "heuristic_id": f"h/linguist/{ext}/{rule_idx}",
                        "applies_to_ext": ext,
                        "priority": rule_idx,
                        "predicts_language": lg,
                        "predicts_pl_id": linguist_to_pl_id.get(lg, ""),
                        "pattern_kind": kind,
                        "predicates_json": json.dumps(preds, ensure_ascii=False),
                        "source": "linguist/heuristics.yml",
                    })
    return out


def load_accepted_manual_labels() -> list[dict]:
    """Load promotable manual extension labels from `data/derived/extension_labels.csv`.

    Returns rows where `label` starts with `pl/<id>` (existing PL only — not
    `pl/new:`, `pl/dialect:`, or `pl/family:`) and `curator_status` is one of:

    - `accepted` → promoted with `strength="proposed"` (maintainer-confirmed).
    - `new`      → also promoted with `strength="proposed"`. A submitted-but-
      -not-yet-reviewed label is still an attribution signal — it flips the
      ext from `unattributed` to `weakly-attributed` on the per-ext page.
      The strength stays `proposed` (vs accepted's `primary`-on-promote) so
      maintainers can tell them apart. Once accepted, the row is replaced
      (same key) with the upgraded strength.

    Rows with `curator_status` in {`rejected`, `needs-info`} are NOT
    promoted — they only show up on the curator triage view at
    `/review/curator/`.
    """
    path = ROOT / "data" / "derived" / "extension_labels.csv"
    if not path.exists():
        return []
    out: list[dict] = []
    PROMOTABLE = {"accepted", "new"}
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            label = (r.get("label") or "").strip()
            status = (r.get("curator_status") or "").strip()
            if status not in PROMOTABLE:
                continue
            if not (label.startswith("pl/") and not label.startswith("pl/new:")
                    and not label.startswith("pl/dialect:")
                    and not label.startswith("pl/family:")):
                # Only existing-PL labels get auto-promoted. Other label types
                # (binary/data/etc) and new-PL proposals need separate handling.
                continue
            out.append(r)
    return out


def load_repo_meta_aliases() -> dict[str, list[tuple[str, str]]]:
    """Map directory canonical -> [(alias, 'repo')...] from per-lang meta.json."""
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    if not LANGUAGES_DIR.exists():
        return out
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
        canonical = (data.get("name") or d.name).strip()
        for a in data.get("aliases") or []:
            a = str(a).strip()
            if a and a.lower() != canonical.lower():
                out[canonical].append((a, "repo"))
    return out


def load_repo_meta_extensions() -> dict[str, list[str]]:
    """Map directory canonical -> [extensions] from per-lang meta.json.

    Optional `extensions` field in meta.json (added by the /contribute/add-pl/
    web form). First entry is treated as primary, the rest as secondary —
    matching Linguist's `extensions[0] == primary` convention.
    """
    out: dict[str, list[str]] = defaultdict(list)
    if not LANGUAGES_DIR.exists():
        return out
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
        canonical = (data.get("name") or d.name).strip()
        for e in data.get("extensions") or []:
            e = str(e).strip()
            if e:
                out[canonical].append(e)
    return out


def load_repo_meta_full() -> dict[str, dict]:
    """Return the full meta.json contents keyed by canonical name.

    Used to mint pl_rows for in-repo-only PLs (those added via
    /contribute/add-pl/ that aren't yet in any upstream source). Carries
    aliases, evidence_url, extensions, and created_via_issue.
    """
    out: dict[str, dict] = {}
    if not LANGUAGES_DIR.exists():
        return out
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
        canonical = (data.get("name") or d.name).strip()
        out[canonical] = data
    return out


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def _repo_meta_source_and_evidence(canonical: str,
                                   meta: dict | None,
                                   owner_repo: str | None) -> tuple[str, str]:
    """Return (source, evidence) for a repo_meta ext_claim row.

    When `meta.json` carries `created_via_issue: <N>` AND we know the
    owner/repo, source becomes `manual_add:#<N>` and evidence is the GitHub
    issue URL — both threaded through to the per-PL Extensions table so a
    reviewer can click straight to the originating submission.

    Falls back to plain `repo_meta` (with the meta.json path) for PLs
    added by the agentic /loop or any other path that doesn't record an
    issue number.
    """
    issue = (meta or {}).get("created_via_issue")
    if issue and owner_repo:
        return (
            f"manual_add:#{issue}",
            f"https://github.com/{owner_repo}/issues/{issue}",
        )
    return ("repo_meta", f"languages/{canonical}/meta.json")


def build(*, master: list[dict], linguist: dict, pygments_lex: dict,
          repo_aliases: dict[str, list[tuple[str, str]]],
          repo_meta_extensions: dict[str, list[str]] | None = None,
          repo_meta_full: dict[str, dict] | None = None,
          owner_repo: str | None = None):
    pl_rows = []
    alias_rows = []
    ext_claim_rows = []
    used_ids: set[str] = set()

    # Index pygments by lexer "name" for joining via master_inventory's
    # `pygments_name` column.
    pyg_by_name = {info["name"]: info for info in pygments_lex.values()}

    for row in master:
        canonical = (row.get("canonical_name") or "").strip()
        if not canonical:
            continue
        pl_id = make_pl_id(canonical, used_ids)

        flags = {k: row.get(k) == "True" for k in [
            "in_pldb", "in_linguist", "in_pygments", "in_wikipedia",
            "in_esolang", "in_hyperpolyglot", "in_rosettacode",
        ]}

        pl_rows.append({
            "pl_id": pl_id,
            "canonical_name": canonical,
            "lang_id_master": row.get("lang_id", ""),
            "linguist_key": row.get("linguist_key", "") or "",
            "pygments_name": row.get("pygments_name", "") or "",
            "hyperpolyglot_name": row.get("hyperpolyglot_name", "") or "",
            "rosettacode_name": row.get("rosettacode_name", "") or "",
            "source_flags": row.get("source_flags", ""),
            "source_count": row.get("source_count", ""),
            "first_appeared": row.get("first_appeared", ""),
            "homepage": row.get("homepage", ""),
            "evidence_urls": row.get("evidence_urls", ""),
            "paradigms": row.get("paradigms", ""),
            "typing": row.get("typing", ""),
            "designed_by": row.get("designed_by", ""),
            "types": row.get("types", ""),
            **{k: ("yes" if v else "no") for k, v in flags.items()},
            "in_manual_add": "no",
            "created_via_issue": "",
        })

        # Aliases (from Pygments + Hyperpolyglot + Rosetta Code + repo meta)
        alias_seen: set[tuple[str, str]] = set()
        def add_alias(a: str, src: str) -> None:
            a = (a or "").strip()
            if not a or a.lower() == canonical.lower():
                return
            key = (a.lower(), src)
            if key in alias_seen:
                return
            alias_seen.add(key)
            alias_rows.append({"pl_id": pl_id, "alias": a, "source": src})

        # Pygments aliases
        pyg_aliases_str = row.get("pygments_aliases") or ""
        for tok in re.split(r"[\s,;]+", pyg_aliases_str):
            add_alias(tok, "pygments")
        # Other named keys
        if row.get("hyperpolyglot_name"):
            add_alias(row["hyperpolyglot_name"], "hyperpolyglot")
        if row.get("rosettacode_name"):
            add_alias(row["rosettacode_name"], "rosettacode")
        if row.get("linguist_key"):
            add_alias(row["linguist_key"], "linguist")
        # Repo aliases
        for a, src in repo_aliases.get(canonical, []):
            add_alias(a, src)

        # ----- Ext claims -----
        # 1. Linguist (primary/secondary by extensions[0])
        lkey = row.get("linguist_key") or ""
        if lkey and lkey in linguist:
            l_exts = linguist[lkey].get("extensions") or []
            for i, raw in enumerate(l_exts):
                ext = _norm_ext(str(raw))
                if not ext:
                    continue
                ext_claim_rows.append({
                    "pl_id": pl_id,
                    "ext": ext,
                    "source": "linguist",
                    "strength": "primary" if i == 0 else "secondary",
                    "source_key": lkey,
                    "evidence": (
                        "https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml"
                    ),
                })

        # 2. Pygments — parse directly from the master CSV's `pygments_filenames`.
        # Master_inventory stores Pygments info per language as a string of
        # globs ("*.abap;*.ABAP"). Lexer ordering in the source preserves
        # priority: first glob == primary, the rest == secondary. (Note:
        # `pygments_name` in master CSV is the lexer *class name* like
        # `ABAPLexer`, NOT the display name, so we don't bother looking it up.)
        pyg_filenames_raw = row.get("pygments_filenames") or ""
        pyg_class = row.get("pygments_name") or ""
        seen_pyg_ext: set[str] = set()
        for raw in re.split(r"[;,\s]+", pyg_filenames_raw):
            ext = _norm_ext(raw)
            if not ext or ext in seen_pyg_ext:
                continue
            strength = "primary" if not seen_pyg_ext else "secondary"
            seen_pyg_ext.add(ext)
            ext_claim_rows.append({
                "pl_id": pl_id,
                "ext": ext,
                "source": "pygments",
                "strength": strength,
                "source_key": pyg_class,
                "evidence": "pygments.lexers._mapping.LEXERS (via master CSV)",
            })

        # 3. Catch-all: anything in master_inventory's unioned `extensions` not
        # yet covered. We don't know which upstream contributed (Linguist and
        # Pygments are already accounted for above; what's left is from PLDB
        # or Wikipedia or other sources that don't carry primary/secondary).
        already = {(c["ext"], c["pl_id"]) for c in ext_claim_rows
                   if c["pl_id"] == pl_id}
        for raw in re.split(r"[\s,;]+", row.get("extensions") or ""):
            ext = _norm_ext(raw)
            if not ext:
                continue
            if (ext, pl_id) in already:
                continue
            ext_claim_rows.append({
                "pl_id": pl_id,
                "ext": ext,
                "source": "master_unioned",
                "strength": "unknown",
                "source_key": row.get("lang_id", ""),
                "evidence": "data/derived/languages_master_augmented.csv",
            })

        # 4. In-repo meta.json (e.g. from /contribute/add-pl/ submissions).
        # `extensions[0]` → primary (Linguist convention), rest → secondary.
        if repo_meta_extensions:
            repo_exts = repo_meta_extensions.get(canonical, [])
            seen_in_repo: set[str] = set()
            meta = (repo_meta_full or {}).get(canonical)
            src_str, evidence_str = _repo_meta_source_and_evidence(
                canonical, meta, owner_repo,
            )
            for raw in repo_exts:
                ext = _norm_ext(str(raw))
                if not ext or ext in seen_in_repo:
                    continue
                seen_in_repo.add(ext)
                strength = "primary" if len(seen_in_repo) == 1 else "secondary"
                ext_claim_rows.append({
                    "pl_id": pl_id,
                    "ext": ext,
                    "source": src_str,
                    "strength": strength,
                    "source_key": canonical,
                    "evidence": evidence_str,
                })

    # 5. In-repo-only PLs: any meta.json whose canonical name didn't match
    # an upstream-derived row. These are typically Add-PL form submissions
    # for PLs not yet in PLDB/Linguist/Pygments/etc. We mint a pl_row with
    # `in_manual_add: yes` and emit repo_meta ext_claim rows from the
    # extensions list. This is what makes the new PL visible in
    # `/source/manual_add/`, gives the extensions a real claim target, and
    # lets the manual-review promotion step resolve `pl/<id>` against an
    # existing pl_id.
    existing_canonicals = {p["canonical_name"].lower() for p in pl_rows}
    repo_meta_full = repo_meta_full or {}
    repo_meta_extensions = repo_meta_extensions or {}
    in_repo_only_canonicals = sorted(
        c for c in repo_meta_full.keys()
        if c.lower() not in existing_canonicals
    )
    for canonical in in_repo_only_canonicals:
        meta = repo_meta_full[canonical]
        pl_id = make_pl_id(canonical, used_ids)
        evidence_url = (meta.get("evidence_url") or "").strip()
        created_via = meta.get("created_via_issue")
        created_via_str = str(created_via) if created_via not in (None, "") else ""
        pl_rows.append({
            "pl_id": pl_id,
            "canonical_name": canonical,
            "lang_id_master": "",
            "linguist_key": "",
            "pygments_name": "",
            "hyperpolyglot_name": "",
            "rosettacode_name": "",
            "source_flags": "manual_add",
            "source_count": "1",
            "first_appeared": "",
            "homepage": "",
            "evidence_urls": evidence_url,
            "paradigms": "",
            "typing": "",
            "designed_by": "",
            "types": "",
            "in_pldb": "no",
            "in_linguist": "no",
            "in_pygments": "no",
            "in_wikipedia": "no",
            "in_esolang": "no",
            "in_hyperpolyglot": "no",
            "in_rosettacode": "no",
            "in_manual_add": "yes",
            "created_via_issue": created_via_str,
        })
        # Aliases from meta.json + any extra `repo_aliases` entry under the
        # same canonical (the alias loader covers the latter).
        for raw_alias in (meta.get("aliases") or []):
            a = str(raw_alias).strip()
            if a and a.lower() != canonical.lower():
                alias_rows.append({
                    "pl_id": pl_id, "alias": a, "source": "repo",
                })
        for a, src in (repo_aliases.get(canonical) or []):
            alias_rows.append({"pl_id": pl_id, "alias": a, "source": src})

        # Extensions → repo_meta ext_claim rows. `extensions[0]` → primary.
        seen_in_repo: set[str] = set()
        src_str, evidence_str = _repo_meta_source_and_evidence(
            canonical, meta, owner_repo,
        )
        for raw in (repo_meta_extensions.get(canonical) or []):
            ext = _norm_ext(str(raw))
            if not ext or ext in seen_in_repo:
                continue
            seen_in_repo.add(ext)
            strength = "primary" if len(seen_in_repo) == 1 else "secondary"
            ext_claim_rows.append({
                "pl_id": pl_id,
                "ext": ext,
                "source": src_str,
                "strength": strength,
                "source_key": canonical,
                "evidence": evidence_str,
            })

    return pl_rows, alias_rows, ext_claim_rows


def build_ext_summary(ext_claim_rows: list[dict], pl_rows: list[dict]) -> list[dict]:
    pl_name = {p["pl_id"]: p["canonical_name"] for p in pl_rows}
    by_ext: dict[str, list[dict]] = defaultdict(list)
    for c in ext_claim_rows:
        by_ext[c["ext"]].append(c)

    out = []
    for ext in sorted(by_ext):
        claims = by_ext[ext]
        # Collapse to unique (pl_id, strongest_strength) per extension.
        # Order: primary > secondary > unknown > proposed > disputed.
        # Unknown strength strings default to 0 (treated as least authoritative).
        STRENGTH_ORDER = {"primary": 5, "secondary": 4, "unknown": 3,
                          "proposed": 2, "disputed": 1}
        strongest: dict[str, str] = {}
        for c in claims:
            cur = strongest.get(c["pl_id"])
            s_new = STRENGTH_ORDER.get(c.get("strength", ""), 0)
            s_cur = STRENGTH_ORDER.get(cur, 0) if cur is not None else -1
            if s_new > s_cur:
                strongest[c["pl_id"]] = c["strength"]
        # Sort claimants by strength rank then name for stable output.
        ranked = sorted(
            strongest.items(),
            key=lambda kv: (-STRENGTH_ORDER[kv[1]], pl_name.get(kv[0], "").lower()),
        )
        primary = [pl_name[p] for p, s in ranked if s == "primary"]
        secondary = [pl_name[p] for p, s in ranked if s == "secondary"]
        unknown = [pl_name[p] for p, s in ranked if s == "unknown"]
        out.append({
            "ext": ext,
            "n_claimants": len(strongest),
            "n_primary": len(primary),
            "n_secondary": len(secondary),
            "n_unknown": len(unknown),
            "primary_claimants": "; ".join(primary),
            "secondary_claimants": "; ".join(secondary),
            "unknown_claimants": "; ".join(unknown),
        })
    return out


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    args = parser.parse_args()

    out_dir = Path(args.out_dir)

    print("Loading sources...")
    master = load_master_inventory()
    linguist = load_linguist()
    pygments_lex = load_pygments()
    repo_aliases = load_repo_meta_aliases()
    repo_meta_extensions = load_repo_meta_extensions()
    repo_meta_full = load_repo_meta_full()
    heuristics = load_linguist_heuristics()
    manual_labels = load_accepted_manual_labels()
    print(f"  manual review (accepted): {len(manual_labels)} ext-label submissions to promote")

    print(f"  master_inventory: {len(master)} rows")
    print(f"  linguist:         {len(linguist)} entries")
    print(f"  pygments:         {len(pygments_lex)} lexers")
    print(f"  heuristics:       "
          f"{len((heuristics or {}).get('disambiguations') or [])} disambig blocks, "
          f"{len((heuristics or {}).get('named_patterns') or {})} named patterns")
    print(f"  repo aliases:     {sum(len(v) for v in repo_aliases.values())} alias entries")

    print("\nBuilding tables...")
    pl_rows, alias_rows, ext_claim_rows = build(
        master=master,
        linguist=linguist,
        pygments_lex=pygments_lex,
        repo_aliases=repo_aliases,
        repo_meta_extensions=repo_meta_extensions,
        repo_meta_full=repo_meta_full,
        owner_repo=_gh_owner_repo(),
    )

    # Promote accepted/new manual labels into ext_claim. Each row gets
    # source="manual_review:<annotator>" and strength="proposed".
    # A maintainer can later edit the row's strength to "primary" / "secondary"
    # once a content classifier confirms.
    #
    # Dedup: if the (pl_id, ext) edge ALREADY exists from `repo_meta` (i.e.
    # the PL's own meta.json lists the extension), the manual_review row
    # would be a duplicate signal from the same in-repo origin — skip it.
    # We still promote when the edge is genuinely new (different ext on the
    # same PL, or different PL claiming the same ext).
    if manual_labels:
        valid_pl_ids = {p["pl_id"] for p in pl_rows}
        # In-repo origin can be either `repo_meta` (legacy / agentic /loop) or
        # `manual_add:#<N>` (issue-provenance-enriched via the Add-PL form).
        # Both signal "the PL's own meta.json already claims this extension."
        repo_meta_edges = {
            (c["pl_id"], c["ext"]) for c in ext_claim_rows
            if c.get("source") == "repo_meta"
            or c.get("source", "").startswith("manual_add:")
        }
        promoted = skipped = dedup_skipped = 0
        for ml in manual_labels:
            ext = (ml.get("ext") or "").strip()
            label = (ml.get("label") or "").strip()  # "pl/<id>"
            if not (ext.startswith(".") and label.startswith("pl/")):
                skipped += 1
                continue
            pl_id = label  # already in "pl/<id>" form
            if pl_id not in valid_pl_ids:
                skipped += 1
                continue
            if (pl_id, ext.lower()) in repo_meta_edges:
                # The PL's own meta.json already claims this extension.
                # The manual_review submission is a duplicate signal —
                # skip the promotion (the repo_meta row already covers it).
                dedup_skipped += 1
                continue
            annotator = ml.get("annotator") or "unknown"
            ext_claim_rows.append({
                "pl_id": pl_id,
                "ext": ext.lower(),
                "source": f"manual_review:{annotator}",
                "strength": "proposed",
                "source_key": ml.get("issue_number", ""),
                "evidence": ml.get("issue_url") or "data/derived/extension_labels.csv",
            })
            promoted += 1
        print(f"  promoted {promoted} manual labels into ext_claim "
              f"(skipped {skipped} unknown-pl_id, "
              f"deduped {dedup_skipped} already-in-meta.json).")

    ext_summary = build_ext_summary(ext_claim_rows, pl_rows)

    # Map Linguist language name -> pl_id (via linguist_key on pl rows).
    linguist_to_pl_id = {p["linguist_key"]: p["pl_id"]
                         for p in pl_rows if p.get("linguist_key")}
    heuristic_rows = build_heuristic_rows(heuristics or {}, linguist_to_pl_id)

    print(f"  pl:         {len(pl_rows):>6}")
    print(f"  pl_alias:   {len(alias_rows):>6}")
    print(f"  ext_claim:  {len(ext_claim_rows):>6}")
    print(f"  ext_summary:{len(ext_summary):>6}")
    print(f"  heuristic:  {len(heuristic_rows):>6}")

    write_csv(out_dir / "pl.csv", pl_rows, [
        "pl_id", "canonical_name", "lang_id_master",
        "linguist_key", "pygments_name", "hyperpolyglot_name", "rosettacode_name",
        "source_flags", "source_count",
        "first_appeared", "homepage", "evidence_urls",
        "paradigms", "typing", "designed_by", "types",
        "in_pldb", "in_linguist", "in_pygments", "in_wikipedia",
        "in_esolang", "in_hyperpolyglot", "in_rosettacode",
        "in_manual_add", "created_via_issue",
    ])
    write_csv(out_dir / "pl_alias.csv", alias_rows, ["pl_id", "alias", "source"])
    write_csv(out_dir / "ext_claim.csv", ext_claim_rows, [
        "pl_id", "ext", "source", "strength", "source_key", "evidence",
    ])
    write_csv(out_dir / "ext_summary.csv", ext_summary, [
        "ext", "n_claimants", "n_primary", "n_secondary", "n_unknown",
        "primary_claimants", "secondary_claimants", "unknown_claimants",
    ])
    write_csv(out_dir / "heuristic.csv", heuristic_rows, [
        "heuristic_id", "applies_to_ext", "priority",
        "predicts_language", "predicts_pl_id",
        "pattern_kind", "predicates_json", "source",
    ])

    print(f"\nWrote {out_dir}/{{pl,pl_alias,ext_claim,ext_summary,heuristic}}.csv")

    # Quick sanity check on famous polysemy cases.
    print("\n--- Sanity check (selected extensions) ---")
    by_ext = {r["ext"]: r for r in ext_summary}
    for ext in [".py", ".rpy", ".spec", ".pyi", ".m", ".h", ".pl", ".t", ".r", ".rs"]:
        r = by_ext.get(ext)
        if r:
            print(f"  {ext:6s} primary={r['primary_claimants'] or '-':40s} "
                  f"secondary={r['secondary_claimants'] or '-':40s}")
        else:
            print(f"  {ext:6s} <no claimants>")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
