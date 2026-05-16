#!/usr/bin/env python3
"""Predict the programming language of a file using the taxonomy + Linguist heuristics.

Reads `data/derived/pl_taxonomy/{heuristic,ext_summary,pl}.csv` (built by
`tools/build_pl_taxonomy.py`) and applies them in this order:

1. Look up the file's extension. If only one PL is a *primary* claimant and
   that ext has no heuristic rules, predict that PL with high confidence.
2. If the ext has heuristic rules (Linguist's `heuristics.yml`), apply them
   in priority order. The first rule whose predicates all match wins.
3. If no rule matches and there's a "default" rule (no patterns), use it.
4. Otherwise, fall back to the strongest claimant from `ext_summary` and
   flag the prediction as `fallback`.

Usage
-----
As a CLI:
    python tools/pl_classify.py path/to/file [path/to/file ...]

As a library (from swh_extension_mining or anywhere else):
    from pl_classify import Classifier
    cls = Classifier()
    res = cls.classify_bytes('.m', open('foo.m', 'rb').read())
    print(res.pl_id, res.confidence, res.via)

Pattern compatibility
---------------------
Linguist's heuristics.yml uses Ruby-flavoured regexes. The vast majority
work unchanged in Python with re.MULTILINE. We compile each predicate
pattern lazily and skip ones Python can't parse (rare, logged as warnings
on first compile).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_DIR = ROOT / "data" / "derived" / "pl_taxonomy"
DEFAULT_HEURISTIC_CSV = TAXONOMY_DIR / "heuristic.csv"
DEFAULT_EXT_SUMMARY_CSV = TAXONOMY_DIR / "ext_summary.csv"
DEFAULT_PL_CSV = TAXONOMY_DIR / "pl.csv"

# Linguist tells classifiers to look only at the first ~50 KB. Beyond that
# the marginal value drops fast and the runtime grows linearly.
MAX_BYTES_TO_SCAN = 50_000


@dataclass
class HeuristicRule:
    heuristic_id: str
    ext: str
    priority: int
    predicts_language: str
    predicts_pl_id: str
    is_default: bool
    predicates: list[dict]  # [{'kind': 'any'|'not_any', 'regexes': [...]}]
    compiled: list[list[re.Pattern]] | None = None  # parallel to predicates


@dataclass
class ClassifyResult:
    pl_id: str | None
    predicts_language: str | None
    via: str  # 'unique-primary' | 'heuristic' | 'default-rule' | 'fallback' | 'unknown-ext' | 'no-ext'
    confidence: str  # 'high' | 'medium' | 'low' | 'none'
    matched_heuristic_id: str | None = None
    fallback_choices: list[str] = field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Pattern compilation — handle Ruby/Python regex differences gracefully.
# ---------------------------------------------------------------------------

# Rubyisms that Python's `re` rejects. We translate the common ones; everything
# else gets dropped (and the rule is treated as never-match for that predicate).
def _try_compile(pattern: str) -> re.Pattern | None:
    # Most Linguist patterns work as-is. Try directly first.
    for variant in (pattern, _ruby_to_python_regex(pattern)):
        try:
            return re.compile(variant, re.MULTILINE)
        except re.error:
            continue
    return None


_RUBYISMS = [
    (re.compile(r"\(\?\#"), "(?:#"),  # Ruby comment groups (rare)
]


def _ruby_to_python_regex(p: str) -> str:
    out = p
    for rx, repl in _RUBYISMS:
        out = rx.sub(repl, out)
    return out


def _compile_predicates(preds: list[dict]) -> list[list[re.Pattern]]:
    out: list[list[re.Pattern]] = []
    for pred in preds:
        compiled = []
        for rx in pred.get("regexes", []):
            c = _try_compile(rx)
            if c is not None:
                compiled.append(c)
        out.append(compiled)
    return out


def _eval_predicates(preds: list[dict], compiled: list[list[re.Pattern]], text: str) -> bool:
    for pred, regs in zip(preds, compiled):
        any_hit = any(r.search(text) for r in regs) if regs else False
        if pred["kind"] == "any":
            if not any_hit:
                return False
        elif pred["kind"] == "not_any":
            if any_hit:
                return False
        else:
            return False  # unknown kind -> conservative
    return True


# Common suffixes that signal a near-duplicate pl_id in master_inventory.
# master_inventory's union has both `pl/zig` and `pl/zig-programming-language`
# as distinct entities representing the same language. We collapse these so
# the classifier's "unique-primary" fast path actually fires.
_PL_ID_SUFFIXES = [
    "-programming-language",
    "-the-programming-language",
    "-programminglanguage",
    "-lang",
    "-language",
]


def _consolidate_pl_ids(pl_ids: list[str]) -> list[str]:
    """Collapse pl_ids that differ only by a known canonical-name suffix.

    Preserves order; keeps the shortest representative per group. Examples:
      ['pl/zig', 'pl/zig-programming-language'] -> ['pl/zig']
      ['pl/c-programming-language', 'pl/c']     -> ['pl/c']
      ['pl/matlab', 'pl/mercury']               -> ['pl/matlab', 'pl/mercury'] (no change)
    """
    if len(pl_ids) <= 1:
        return list(pl_ids)
    groups: dict[str, list[str]] = {}
    insertion_order: list[str] = []
    for pid in pl_ids:
        base = pid
        for s in _PL_ID_SUFFIXES:
            if base.endswith(s):
                base = base[: -len(s)]
                break
        if base not in groups:
            insertion_order.append(base)
        groups.setdefault(base, []).append(pid)
    return [min(groups[b], key=len) for b in insertion_order]


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

@dataclass
class _ExtSummary:
    ext: str
    n_primary: int
    n_secondary: int
    primary_pl_ids: list[str]
    secondary_pl_ids: list[str]


class Classifier:
    def __init__(
        self,
        *,
        heuristic_csv: Path = DEFAULT_HEURISTIC_CSV,
        ext_summary_csv: Path = DEFAULT_EXT_SUMMARY_CSV,
        pl_csv: Path = DEFAULT_PL_CSV,
    ) -> None:
        if not heuristic_csv.exists() or not ext_summary_csv.exists():
            sys.exit(
                f"Run `tools/build_pl_taxonomy.py` first; missing "
                f"{heuristic_csv} or {ext_summary_csv}."
            )
        self.rules_by_ext: dict[str, list[HeuristicRule]] = {}
        for r in csv.DictReader(open(heuristic_csv, encoding="utf-8")):
            ext = r["applies_to_ext"]
            preds = json.loads(r["predicates_json"]) if r["predicates_json"] else []
            rule = HeuristicRule(
                heuristic_id=r["heuristic_id"],
                ext=ext,
                priority=int(r["priority"]),
                predicts_language=r["predicts_language"],
                predicts_pl_id=r["predicts_pl_id"] or "",
                is_default=(r["pattern_kind"] == "default"),
                predicates=preds,
            )
            self.rules_by_ext.setdefault(ext, []).append(rule)
        for ext, rs in self.rules_by_ext.items():
            rs.sort(key=lambda x: x.priority)

        # ext_summary feeds the unique-primary fast path and the fallback.
        # We need pl_id, but ext_summary stores canonical_name; cross-reference
        # via pl.csv.
        name_to_pl_id: dict[str, str] = {}
        for p in csv.DictReader(open(pl_csv, encoding="utf-8")):
            if p.get("canonical_name"):
                name_to_pl_id[p["canonical_name"]] = p["pl_id"]
        self.ext_summary: dict[str, _ExtSummary] = {}
        for r in csv.DictReader(open(ext_summary_csv, encoding="utf-8")):
            primary_names = [s.strip() for s in (r["primary_claimants"] or "").split(";") if s.strip()]
            secondary_names = [s.strip() for s in (r["secondary_claimants"] or "").split(";") if s.strip()]
            primary_pl_ids = _consolidate_pl_ids([name_to_pl_id.get(n, f"?:{n}") for n in primary_names])
            secondary_pl_ids = _consolidate_pl_ids([name_to_pl_id.get(n, f"?:{n}") for n in secondary_names])
            # Refresh counts after consolidation (master_inventory still has the
            # un-merged Python/Python-programming-language style duplicates).
            self.ext_summary[r["ext"]] = _ExtSummary(
                ext=r["ext"],
                n_primary=len(primary_pl_ids),
                n_secondary=len(secondary_pl_ids),
                primary_pl_ids=primary_pl_ids,
                secondary_pl_ids=secondary_pl_ids,
            )

    @staticmethod
    def _ext_of(filename: str) -> str | None:
        # Only the last suffix; lowercase. ".tar.gz" -> ".gz" (linguist convention).
        name = os.path.basename(filename).lower()
        i = name.rfind(".")
        if i <= 0:
            return None
        return name[i:]

    def classify_bytes(self, ext: str, content: bytes) -> ClassifyResult:
        ext = ext.lower()
        text = content[:MAX_BYTES_TO_SCAN].decode("utf-8", errors="replace")

        ex_sum = self.ext_summary.get(ext)
        rules = self.rules_by_ext.get(ext, [])

        # Fast path: only one primary claimant *and* no heuristic rules
        # exist for this ext. This is the common case (~80% of all exts).
        if ex_sum and ex_sum.n_primary == 1 and not rules:
            pid = ex_sum.primary_pl_ids[0]
            return ClassifyResult(
                pl_id=pid, predicts_language=None,
                via="unique-primary", confidence="high",
                notes=f"only primary claimant of {ext}; no heuristic rules",
            )

        # Heuristic path
        for rule in rules:
            if rule.is_default:
                # Default rules always match — record but keep looking is wrong;
                # Linguist evaluates rules in order and stops at first match.
                # A default rule with no patterns is the catch-all at the end.
                return ClassifyResult(
                    pl_id=rule.predicts_pl_id or None,
                    predicts_language=rule.predicts_language,
                    via="default-rule",
                    confidence="medium",
                    matched_heuristic_id=rule.heuristic_id,
                    notes="Linguist default fallback rule for this ext",
                )
            if rule.compiled is None:
                rule.compiled = _compile_predicates(rule.predicates)
            if _eval_predicates(rule.predicates, rule.compiled, text):
                return ClassifyResult(
                    pl_id=rule.predicts_pl_id or None,
                    predicts_language=rule.predicts_language,
                    via="heuristic",
                    confidence="high",
                    matched_heuristic_id=rule.heuristic_id,
                )

        # No heuristic matched and no default rule — fall back to ext_summary.
        if ex_sum:
            choices = ex_sum.primary_pl_ids or ex_sum.secondary_pl_ids
            if len(choices) == 1:
                return ClassifyResult(
                    pl_id=choices[0], predicts_language=None,
                    via="fallback", confidence="medium",
                    fallback_choices=choices,
                    notes="no heuristic matched; single primary claimant",
                )
            if choices:
                return ClassifyResult(
                    pl_id=None, predicts_language=None,
                    via="fallback", confidence="low",
                    fallback_choices=choices,
                    notes=f"no heuristic matched; {len(choices)} candidates",
                )

        return ClassifyResult(
            pl_id=None, predicts_language=None,
            via="unknown-ext", confidence="none",
            notes=f"extension {ext!r} not in taxonomy",
        )

    def classify_file(self, path: str | Path) -> ClassifyResult:
        path = Path(path)
        ext = self._ext_of(path.name)
        if ext is None:
            return ClassifyResult(
                pl_id=None, predicts_language=None,
                via="no-ext", confidence="none",
                notes=f"no extension on {path.name!r}",
            )
        try:
            data = path.read_bytes()
        except Exception as e:
            return ClassifyResult(
                pl_id=None, predicts_language=None,
                via="unknown-ext", confidence="none",
                notes=f"read error: {e}",
            )
        return self.classify_bytes(ext, data)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paths", nargs="+", help="files to classify")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="print full provenance per file")
    args = p.parse_args(argv)

    cls = Classifier()
    for path in args.paths:
        r = cls.classify_file(path)
        if args.verbose:
            print(f"{path}")
            print(f"  pl_id:      {r.pl_id}")
            print(f"  language:   {r.predicts_language}")
            print(f"  via:        {r.via} ({r.confidence})")
            if r.matched_heuristic_id:
                print(f"  heuristic:  {r.matched_heuristic_id}")
            if r.fallback_choices:
                print(f"  candidates: {r.fallback_choices}")
            if r.notes:
                print(f"  notes:      {r.notes}")
        else:
            label = r.pl_id or (f"<{','.join(r.fallback_choices)}>" if r.fallback_choices else "?")
            print(f"{path}\t{label}\t{r.via}\t{r.confidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
