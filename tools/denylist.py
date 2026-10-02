#!/usr/bin/env python3
"""Deny list: languages PL-ultimate-llm must not include (docs/DENY_LIST.md).

`data/curated/deny_list.csv` holds one row per decision (who asked, why, who
decided). Every entry point consults this module, so a denied language cannot
come back through a rebuild, a source refresh, an LLM campaign turn or a
contribution form:

  campaign       tools/validate.py (pre-commit) refuses a denied languages/ entry
  contributions  tools/process_pl_addition.py, tools/process_pl_contribute.py
  sources        tools/master_inventory.py drops denied rows from its outputs
  taxonomy       tools/build_pl_taxonomy.py drops denied records
  site           web/build_site.py skips denied pages

Matching is exact, never fuzzy — a denied "ArkScript" must not remove the
unrelated Esolang "Ark" or "ArkTS":
  names    exact names (case-insensitive, spaces collapsed)
  records  exact record ids: `repo/<languages folder>` or `pl/<taxonomy id>`
  urls     host/path fragments of the language's own sites (evidence URLs)

    python3 tools/denylist.py list
    python3 tools/denylist.py check "Name" [--url URL]     # exit 1 if denied
    python3 tools/denylist.py scan                         # languages/ + pl_list.txt
    python3 tools/denylist.py purge [--apply]              # committed artifacts (see PURGE)

`purge` removes denied rows from committed snapshots and frozen reports that no
build regenerates soon (whole records only; other lines stay byte-identical).
In *campaign* artifacts (catalog, coverage reports, legacy docs/ site) the
names of the removed `languages/` folders count too — there "Ark" is the
removed folder; in *source* artifacts (PLDB/Rosetta snapshots) they do not —
there "Ark" is another language.
"""

from __future__ import annotations

import csv
import json
import sys
import io
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DENY_CSV = ROOT / "data" / "curated" / "deny_list.csv"
LANGUAGES = ROOT / "languages"
PL_LIST = ROOT / "data" / "pl_list.txt"
REASON_KINDS = {"maintainer-opt-out", "legal", "harmful"}


def _norm(s: str) -> str:
    return " ".join(str(s or "").split()).casefold()


def _split(s: str) -> list[str]:
    return [x.strip() for x in (s or "").split(";") if x.strip()]


class DenyList:
    def __init__(self, rows: list[dict]):
        self.entries = rows
        self.by_name: dict[str, dict] = {}
        self.by_record: dict[str, dict] = {}
        self.by_slug: dict[str, dict] = {}          # pl/<id> → "<id>", for generic row filtering
        self.urls: list[tuple[str, dict]] = []
        for e in rows:
            for n in _split(e.get("names", "")):
                self.by_name[_norm(n)] = e
            for r in _split(e.get("records", "")):
                self.by_record[r] = e
                if r.startswith("pl/"):
                    self.by_slug[_norm(r)] = e
                    self.by_slug[_norm(r[3:])] = e
            for u in _split(e.get("urls", "")):
                self.urls.append((u.casefold(), e))
        # languages/ folders of denied campaign entries ("Ark" for repo/Ark)
        self.folders = {r[5:]: e for r, e in self.by_record.items() if r.startswith("repo/")}

    def __bool__(self) -> bool:
        return bool(self.entries)

    def names(self) -> list[str]:
        return sorted({n for e in self.entries for n in _split(e.get("names", ""))})

    def match_name(self, name: str) -> dict | None:
        return self.by_name.get(_norm(name)) if name else None

    def match_record(self, record: str) -> dict | None:
        return self.by_record.get(record) if record else None

    def match_url(self, url: str) -> dict | None:
        u = (url or "").casefold()
        return next((e for frag, e in self.urls if u and frag in u), None)

    def match_language(self, name: str = "", aliases=(), urls=(), record: str = "") -> dict | None:
        """A language (name + aliases + its evidence URLs, optional record id)."""
        for n in [name, *aliases]:
            e = self.match_name(n)
            if e:
                return e
        for u in urls:
            e = self.match_url(u)
            if e:
                return e
        return self.match_record(record)

    def row_denied(self, row: dict, campaign: bool = False) -> dict | None:
        """Generic filter for tabular outputs: a value equal to a denied name or
        record id, or containing one of the language's own URLs. With
        `campaign`, also the removed folders' names and paths (languages/Ark)."""
        for v in row.values():
            if not isinstance(v, str) or not v:
                continue
            k = _norm(v)
            e = self.by_name.get(k) or self.by_slug.get(k) or self.by_record.get(v)
            if e:
                return e
            if campaign:
                for f, fe in self.folders.items():
                    if v == f or re.search(rf"(^|/)languages/{re.escape(f)}(/|$)", v):
                        return fe
            if "/" in v or "." in v:
                e = self.match_url(v)
                if e:
                    return e
        return None


@lru_cache(maxsize=1)
def get() -> DenyList:
    if not DENY_CSV.exists():
        return DenyList([])
    with DENY_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("deny_id") or "").strip()]
    for r in rows:
        if r.get("reason_kind") not in REASON_KINDS:
            raise SystemExit(f"{DENY_CSV}: {r['deny_id']}: reason_kind must be one of {sorted(REASON_KINDS)}")
    return DenyList(rows)


def describe(e: dict) -> str:
    return (f"{e.get('names') or e.get('records')} is on the deny list ({e.get('deny_id')}, "
            f"{e.get('reason_kind')}: {e.get('reason')} — {e.get('request_url')}). "
            f"See data/curated/deny_list.csv and docs/DENY_LIST.md.")


def scan() -> list[str]:
    """Denied languages present in the campaign data (languages/ + pl_list.txt)."""
    dl, problems = get(), []
    if not dl:
        return problems
    if LANGUAGES.is_dir():
        for d in sorted(LANGUAGES.iterdir()):
            meta = d / "meta.json"
            if not meta.is_file():
                continue
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
            except Exception:
                continue
            urls = [m.get("evidence_url", "")]
            for man in d.glob("programs/*/manifest.json"):
                try:
                    urls.append(json.loads(man.read_text(encoding="utf-8")).get("origin_url", ""))
                except Exception:
                    pass
            e = dl.match_language(m.get("name", ""), m.get("aliases") or [], urls, f"repo/{d.name}")
            if e:
                problems.append(f"languages/{d.name}: " + describe(e))
    if PL_LIST.exists():
        for line in PL_LIST.read_text(encoding="utf-8").splitlines():
            e = dl.match_name(line.strip())
            if e:
                problems.append(f"data/pl_list.txt '{line.strip()}': " + describe(e))
    return problems


# Committed artifacts that list languages but are not rebuilt on every deploy:
# path → kind (campaign: built from languages/; source: built from upstream sources).
PURGE = {
    "data/catalog.csv": "campaign",
    "data/derived/aliases.csv": "source",
    "data/derived/languages_master.csv": "source",
    "data/derived/languages_master_augmented.csv": "source",
    "data/derived/languages_master_augmented_pygments.csv": "source",
    "data/derived/languages_master_augmented_rosettacode.csv": "source",
    "data/derived/rosettacode_languages.csv": "source",
    "reports/master_inventory/pl_list_matches_master.csv": "campaign",
    "reports/swh_languages.csv": "campaign",
    "reports/swh_programs.csv": "campaign",
    "reports/swh_coverage_report.json": "campaign",
    "reports/swh_coverage_report.md": "campaign",
    "docs/data/index.json": "campaign",        # legacy static site (main branch era)
}


def _purge_csv(text: str, dl: DenyList, campaign: bool) -> tuple[str, int]:
    """Drop whole records; every kept byte (line endings included — these files
    mix CRLF records and LF headers) stays as it was. `text` must be read with
    newline="" so nothing is translated."""
    lines = io.StringIO(text, newline="").readlines()       # the physical lines csv consumes
    rd = csv.reader(io.StringIO(text, newline=""))
    header = next(rd)
    keep, prev, dropped = [lines[: rd.line_num]], rd.line_num, 0
    for rec in rd:
        span = lines[prev: rd.line_num]
        prev = rd.line_num
        if dl.row_denied(dict(zip(header, rec)), campaign=campaign):
            dropped += 1
        else:
            keep.append(span)
    return "".join(x for part in keep for x in part), dropped


def _purge_json(obj, dl: DenyList, campaign: bool) -> tuple[object, int]:
    dropped = 0
    if isinstance(obj, list):
        out = []
        for x in obj:
            if isinstance(x, dict) and dl.row_denied({k: v for k, v in x.items() if isinstance(v, str)}, campaign):
                dropped += 1
                continue
            y, n = _purge_json(x, dl, campaign)
            dropped += n
            out.append(y)
        return out, dropped
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            y, n = _purge_json(v, dl, campaign)
            dropped += n
            out[k] = y
        return out, dropped
    return obj, 0


def purge(apply: bool) -> list[str]:
    """Remove denied rows from PURGE artifacts and the legacy docs/ pages of
    removed folders. Returns a report."""
    dl, report = get(), []
    for rel, kind in PURGE.items():
        p = ROOT / rel
        if not p.exists():
            continue
        with p.open(encoding="utf-8", newline="") as fh:        # no newline translation
            text = fh.read()
        campaign = kind == "campaign"
        if p.suffix == ".csv":
            new, n = _purge_csv(text, dl, campaign)
        elif p.suffix == ".json":
            obj, n = _purge_json(json.loads(text), dl, campaign)
            new = (json.dumps(obj, indent=2, ensure_ascii=False) + ("\n" if text.endswith("\n") else "")
                   if n else text)
        else:                                   # markdown table rows: | Name | …
            all_lines = io.StringIO(text, newline="").readlines()
            kept = [ln for ln in all_lines
                    if not (ln.startswith("|") and dl.row_denied(
                        {"c": c.strip() for c in ln.strip().strip("|").split("|")[:1]}, campaign))]
            new, n = "".join(kept), len(all_lines) - len(kept)
        if n:
            report.append(f"{rel}: {n} row(s)")
            if apply:
                with p.open("w", encoding="utf-8", newline="") as fh:
                    fh.write(new)
    # legacy static site under docs/: pages and program copies of removed folders
    docs = ROOT / "docs"
    for page in sorted((docs / "l").glob("*/index.html")) if (docs / "l").is_dir() else []:
        head = page.read_text(encoding="utf-8", errors="replace")[:4000]
        m = re.search(r"<title>([^<·|]+)", head)
        name = (m.group(1).strip() if m else "")
        if name and (dl.match_name(name) or name in dl.folders):
            report.append(f"docs/l/{page.parent.name}/ (legacy page '{name}')")
            if apply:
                import shutil
                shutil.rmtree(page.parent)
    for man in sorted((docs / "code").glob("*/manifest.json")) if (docs / "code").is_dir() else []:
        try:
            m = json.loads(man.read_text(encoding="utf-8"))
        except Exception:
            continue
        if dl.row_denied({k: v for k, v in m.items() if isinstance(v, str)}, campaign=True):
            report.append(f"docs/code/{man.parent.name[:12]}…/ (legacy program copy)")
            if apply:
                import shutil
                shutil.rmtree(man.parent)
    return report


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("check")
    c.add_argument("name")
    c.add_argument("--url", action="append", default=[])
    sub.add_parser("scan")
    pg = sub.add_parser("purge")
    pg.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    dl = get()
    if a.cmd == "list":
        for e in dl.entries:
            print(f"{e['deny_id']}: names={e['names']} records={e['records']} ({e['reason_kind']}, {e['decided_at']})")
        return 0
    if a.cmd == "check":
        e = dl.match_language(a.name, urls=a.url)
        print(describe(e) if e else f"'{a.name}' is not on the deny list.")
        return 1 if e else 0
    if a.cmd == "purge":
        rep = purge(a.apply)
        print("\n".join(rep) if rep else "nothing to purge")
        if rep and not a.apply:
            print("(dry run — add --apply)")
        return 0
    problems = scan()
    print("\n".join(problems) if problems else "deny list: no denied language in languages/ or pl_list.txt")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
