#!/usr/bin/env python3
"""PL identity layer: explicit, traceable `same_as` decisions between records.

Why
---
The catalog is built from source *records*: rows of
`data/derived/pl_taxonomy/pl.csv` (one per source entity, e.g. Wikipedia's
"Python (programming language)", Linguist's "Python") and the LLM-campaign
folders `languages/<Name>/`. Several records can denote the same language.
Merging them destructively would lose what each source calls the language —
which PLI tools (Linguist, Pygments, …) need — so records are NEVER edited
or deleted here. Instead:

  1. `propose` applies a named, deterministic rule to the records and lists
     candidate pairs with machine evidence
     -> data/derived/pl_concepts/link_candidates.csv  (regenerated)
  2. a reviewer records a decision per pair (accepted / rejected, with a
     note) in the only hand-edited file:
     -> data/curated/pl_links.csv
  3. `build` validates the decisions against the current records and groups
     records joined by accepted `same_as` links into *concepts*
     -> data/derived/pl_concepts/pl_concepts.csv         (one row per concept)
     -> data/derived/pl_concepts/pl_concept_members.csv  (one row per record)

`web/build_site.py` renders one page per concept: the other records' pages
redirect to it, and it lists every merged record with its sources and the
decision that joined it. Undoing a merge = flipping one decision.

Record references
-----------------
  pl/<id>            a row of pl.csv (its `pl_id`)
  repo/<folder>      a folder under languages/ (path relative to it)

Rules
-----
generic-qualifier
    Record B's name is "<N> (programming language)" (or "(language)",
    "(computer language)", "(programming)", "(software)", "(lang)") — the
    Wikipedia disambiguation style — and record A's name equals <N>, compared
    case-, accent-, space- and punctuation-insensitively, with `+ ! # *`
    significant (`Go` ≠ `Go!`, `XPL` ≠ `XPL+`). Other parentheticals are
    part of the name: Esolang's "(Keymaker)" marks a homonym, not a synonym.
    Keys shorter than 4 characters are not proposed (short names are the
    most ambiguous: `C`, `Go`, `V`, `D`); they need their own review batch.
    Pairs whose ids conflict (different Wikidata QID, Wikipedia URL, Esolang
    URL, Linguist key or Rosetta Code URL) are proposed but flagged.
    Audit (2026-09-30, docs/PL_IDENTITY.md): on the site's entries this rule
    found 42 pairs, all 42 genuine duplicates.

Usage
-----
    python3 tools/build_pl_concepts.py propose   # refresh candidates
    python3 tools/build_pl_concepts.py build     # decisions -> concepts (default)
    python3 tools/build_pl_concepts.py           # = build

Stdlib only (runs in the Pages CI).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PL_CSV = ROOT / "data" / "derived" / "pl_taxonomy" / "pl.csv"
LANGUAGES_DIR = ROOT / "languages"
DECISIONS_CSV = ROOT / "data" / "curated" / "pl_links.csv"
OUT_DIR = ROOT / "data" / "derived" / "pl_concepts"
CANDIDATES_CSV = OUT_DIR / "link_candidates.csv"
CONCEPTS_CSV = OUT_DIR / "pl_concepts.csv"
MEMBERS_CSV = OUT_DIR / "pl_concept_members.csv"

DECISION_FIELDS = ["link_id", "record_a", "name_a", "record_b", "name_b", "relation",
                   "decision", "rule", "evidence", "reviewer", "reviewed_at", "note"]
RELATIONS = {"same_as"}          # typed non-merging relations (version_of, …) come later
DECISIONS = {"accepted", "rejected"}
# Identifiers that denote ONE language each: two records with different
# values are different languages (or a contaminated record).
ID_FIELDS = ("qid", "wikipedia", "esolang", "linguist", "rosettacode")
MIN_KEY_LEN = 4

# "(programming language)"-style suffixes: Wikipedia disambiguation, not part
# of the name. Anything else in parentheses IS part of the name.
GENERIC_QUALIFIER = re.compile(
    r"\s*\((?:programming\s+language|computer\s+language|language|programming|software|lang)\)\s*$",
    re.IGNORECASE)


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

def _fold(s: str) -> str:
    """Strip accents: `Zélus` -> `Zelus`."""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def name_key(name: str) -> str:
    """Comparison key: case/accents/spaces/punctuation removed, symbols kept.

    `++` -> `pp` and `#` -> `sharp` match PLDB-style slugs (`Charm++` =
    `charmpp`, `C#` = `csharp`); single `+ ! *` are spelled out so they stay
    significant (`XPL+` ≠ `XPL`, `Go!` ≠ `Go`). Parentheses are kept, so an
    author qualifier like "(Keymaker)" keeps two homonyms apart.
    """
    s = _fold(name).lower()
    s = s.replace("++", "pp").replace("#", "sharp").replace("+", "plus")
    s = s.replace("!", "bang").replace("*", "star")
    return re.sub(r"[^a-z0-9()]", "", s)


def load_records() -> dict[str, dict]:
    """All records, keyed by reference, with the fields the rules look at."""
    recs: dict[str, dict] = {}
    with PL_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid = (r.get("pl_id") or "").strip()
            if not pid:
                continue
            recs[pid] = {
                "ref": pid,
                "name": (r.get("canonical_name") or "").strip(),
                "kind": "pl",
                "sources": sorted(k[3:] for k, v in r.items() if k.startswith("in_") and v == "yes"),
                "qid": (r.get("wikidata_qid") or "").strip(),
                "wikipedia": _wikipedia_url(r.get("wikipedia_url") or ""),
                "esolang": (r.get("esolang_url") or "").strip(),
                "linguist": (r.get("linguist_key") or "").strip(),
                "rosettacode": (r.get("rosettacode_url") or "").strip(),
                "evidence_url": "",
            }
    for meta in sorted(LANGUAGES_DIR.rglob("meta.json")):
        try:
            m = json.loads(meta.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        ref = "repo/" + meta.parent.relative_to(LANGUAGES_DIR).as_posix()
        recs[ref] = {
            "ref": ref,
            "name": (m.get("name") or meta.parent.name).strip(),
            "kind": "repo",
            "sources": ["llm-campaign"],
            # A campaign record only carries its evidence URL; when it is a
            # Wikipedia article it doubles as a Wikipedia identifier.
            "qid": "", "esolang": "", "linguist": "", "rosettacode": "",
            "wikipedia": _wikipedia_url(m.get("evidence_url") or ""),
            "evidence_url": (m.get("evidence_url") or "").strip(),
        }
    return recs


def _wikipedia_url(url: str) -> str:
    """Canonical English-Wikipedia article URL, or "" if `url` is not one.

    Percent-escapes are decoded and spaces become underscores, so the same
    article compares equal however it was written (`A%2B_(…)` = `A+_(…)`).
    """
    m = re.match(r"https?://en\.(?:m\.)?wikipedia\.org/wiki/([^#?]+)", url.strip())
    return "https://en.wikipedia.org/wiki/" + unquote(m.group(1)).replace(" ", "_") if m else ""


def _same_id(field: str, x: str, y: str) -> bool:
    # Wikipedia titles differing only by letter case are the same article in
    # practice (redirects: `Elan_(…)` -> `ELAN_(…)`); other ids are exact.
    return x.lower() == y.lower() if field == "wikipedia" else x == y


def conflicts(a: dict, b: dict) -> list[str]:
    """Identifier fields on which the two records disagree."""
    return [f for f in ID_FIELDS if a[f] and b[f] and not _same_id(f, a[f], b[f])]


def shared_ids(a: dict, b: dict) -> list[str]:
    return [f for f in ID_FIELDS if a[f] and b[f] and _same_id(f, a[f], b[f])]


def link_id(a: str, b: str, relation: str = "same_as") -> str:
    """Stable id of an unordered pair: survives re-proposals and reordering."""
    x, y = sorted((a, b))
    return "L-" + hashlib.sha1(f"{relation}|{x}|{y}".encode("utf-8")).hexdigest()[:10]


# ---------------------------------------------------------------------------
# propose
# ---------------------------------------------------------------------------

def propose_generic_qualifier(recs: dict[str, dict]) -> list[dict]:
    """Rule `generic-qualifier` (see module docstring)."""
    by_key: dict[str, list[dict]] = defaultdict(list)
    qualified: list[tuple[str, dict]] = []
    for r in recs.values():
        if GENERIC_QUALIFIER.search(r["name"]):
            qualified.append((name_key(GENERIC_QUALIFIER.sub("", r["name"])), r))
        else:
            by_key[name_key(r["name"])].append(r)
    out = []
    for key, b in qualified:
        if len(key) < MIN_KEY_LEN:
            continue
        for a in by_key.get(key, []):
            ev = [f"names: {a['name']!r} ~ {b['name']!r}"]
            ev += [f"same {f}: {a[f]}" for f in shared_ids(a, b)]
            out.append({
                "link_id": link_id(a["ref"], b["ref"]),
                "rule": "generic-qualifier",
                "record_a": a["ref"], "name_a": a["name"], "sources_a": ";".join(a["sources"]),
                "record_b": b["ref"], "name_b": b["name"], "sources_b": ";".join(b["sources"]),
                "evidence": "; ".join(ev),
                "conflicts": ";".join(f"{f}: {a[f]} vs {b[f]}" for f in conflicts(a, b)),
                "esolang_a": a["esolang"], "evidence_url_a": a["evidence_url"],
            })
    return sorted(out, key=lambda c: (c["name_a"].lower(), c["record_a"], c["record_b"]))


def cmd_propose(_args) -> int:
    recs = load_records()
    cands = propose_generic_qualifier(recs)
    decided = {d["link_id"]: d["decision"] for d in read_decisions()}
    for c in cands:
        c["decision"] = decided.get(c["link_id"], "")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["link_id", "rule", "decision", "record_a", "name_a", "sources_a",
              "record_b", "name_b", "sources_b", "evidence", "conflicts",
              "esolang_a", "evidence_url_a"]
    with CANDIDATES_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(cands)
    n_open = sum(1 for c in cands if not c["decision"])
    print(f"{len(recs):,} records; {len(cands)} candidates "
          f"({sum(1 for c in cands if c['conflicts'])} with conflicting ids; {n_open} undecided) "
          f"-> {CANDIDATES_CSV.relative_to(ROOT)}")
    return 0


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def read_decisions() -> list[dict]:
    if not DECISIONS_CSV.exists():
        return []
    with DECISIONS_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(decisions: list[dict], recs: dict[str, dict]) -> list[str]:
    """Problems that make the decisions file unusable (the build stops)."""
    errors, seen = [], set()
    for i, d in enumerate(decisions, start=2):          # line 1 = header
        where = f"{DECISIONS_CSV.relative_to(ROOT)}:{i}"
        a, b = d.get("record_a", ""), d.get("record_b", "")
        if d.get("relation") not in RELATIONS:
            errors.append(f"{where}: unknown relation {d.get('relation')!r}")
        if d.get("decision") not in DECISIONS:
            errors.append(f"{where}: decision must be one of {sorted(DECISIONS)}")
        if d.get("link_id") != link_id(a, b, d.get("relation", "same_as")):
            errors.append(f"{where}: link_id does not match its records")
        if d.get("link_id") in seen:
            errors.append(f"{where}: duplicate decision for {d.get('link_id')}")
        seen.add(d.get("link_id"))
        for r in (a, b):
            # A record that vanished (renamed pl_id, deleted folder) makes the
            # decision stale: it must be re-reviewed, not silently dropped.
            if r not in recs:
                errors.append(f"{where}: record {r!r} no longer exists")
        if not (d.get("reviewer") or "").strip():
            errors.append(f"{where}: no reviewer")
    return errors


def primary_key(r: dict) -> tuple:
    """Which record names the concept (sorts first).

    1. an LLM-campaign record (it owns programs and provenance);
    2. a name without a generic qualifier ("Python", not "Python (programming
       language)");
    3. the record backed by the most sources;
    4. the reference, as a deterministic tie-break.
    """
    return (r["kind"] != "repo", bool(GENERIC_QUALIFIER.search(r["name"])),
            -len(r["sources"]), r["ref"])


def cmd_build(_args) -> int:
    recs = load_records()
    decisions = read_decisions()
    errors = validate(decisions, recs)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"ERROR: {len(errors)} problem(s) in {DECISIONS_CSV.relative_to(ROOT)}", file=sys.stderr)
        return 1

    accepted = [d for d in decisions if d["decision"] == "accepted" and d["relation"] == "same_as"]
    # Connected components over accepted same_as links (union-find).
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    via: dict[str, list[str]] = defaultdict(list)
    for d in accepted:
        parent[find(d["record_a"])] = find(d["record_b"])
        via[d["record_a"]].append(d["link_id"])
        via[d["record_b"]].append(d["link_id"])
    groups: dict[str, list[str]] = defaultdict(list)
    for ref in parent:
        groups[find(ref)].append(ref)

    accepted_ids = {d["link_id"] for d in accepted}
    concepts, members = [], []
    for refs in groups.values():
        rs = sorted((recs[r] for r in refs), key=primary_key)
        primary = rs[0]
        # A merged concept must not join records whose ids say they are
        # different languages — even when every single link was accepted.
        # Exception: a conflict between two records that an accepted decision
        # links directly was seen by the reviewer (its note says why, e.g.
        # repo/Source cites the Source Academy article, not the language's).
        bad = [(x["ref"], y["ref"], c) for i, x in enumerate(rs) for y in rs[i + 1:]
               for c in conflicts(x, y) if link_id(x["ref"], y["ref"]) not in accepted_ids]
        if bad:
            print(f"WARNING: concept {primary['ref']} joins records with conflicting ids: {bad[:3]}",
                  file=sys.stderr)
        cid = "concept/" + primary["ref"]
        concepts.append({"concept_id": cid, "name": primary["name"], "primary_record": primary["ref"],
                         "n_records": len(rs), "records": ";".join(r["ref"] for r in rs)})
        for r in rs:
            members.append({"concept_id": cid, "record": r["ref"], "name": r["name"],
                            "role": "primary" if r is primary else "merged",
                            "sources": ";".join(r["sources"]),
                            "via_links": ";".join(sorted(set(via[r["ref"]])))})
    concepts.sort(key=lambda c: c["name"].lower())
    members.sort(key=lambda m: (m["concept_id"].lower(), m["role"] != "primary", m["record"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CONCEPTS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["concept_id", "name", "primary_record", "n_records", "records"])
        w.writeheader(); w.writerows(concepts)
    with MEMBERS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["concept_id", "record", "name", "role", "sources", "via_links"])
        w.writeheader(); w.writerows(members)

    # Undecided candidates are not an error (review is incremental), but say so.
    cand_ids = {c["link_id"] for c in propose_generic_qualifier(recs)}
    open_ids = cand_ids - {d["link_id"] for d in decisions}
    n_rej = sum(1 for d in decisions if d["decision"] == "rejected")
    print(f"{len(decisions)} decisions ({len(accepted)} accepted, {n_rej} rejected); "
          f"{len(concepts)} concepts over {len(members)} records; "
          f"{len(open_ids)} proposed candidate(s) still undecided (run `propose`).")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("propose", help="apply the rules, write link_candidates.csv")
    sub.add_parser("build", help="decisions -> concepts (default)")
    args = ap.parse_args(argv)
    return cmd_propose(args) if args.cmd == "propose" else cmd_build(args)


if __name__ == "__main__":
    raise SystemExit(main())
