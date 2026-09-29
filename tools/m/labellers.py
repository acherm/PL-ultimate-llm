"""Existing, *independent* language identifiers applied to `.m` contents.

The earlier studies compared the LLM judge only with our own heuristics, so
the judge was implicitly the oracle. Here every content is labelled by tools
that exist independently of this study:

  linguist   GitHub Linguist's `.m` disambiguation rules (heuristics.yml),
             exactly as vendored by hyperpolyglot / SWH Synid — first
             matching rule wins; no match = abstain (Linguist would then fall
             back to its Bayesian classifier).
  pygments   `guess_lexer_for_filename` — the lexer Pygments picks among
             the four that claim `*.m` (Matlab, Octave, Objective-C, Mason).
  synid      SWH's own Syntax Identification tool (`synid file`), run
             separately by `tools/m/run_synid.py` (Rust binary).

All return a label in `taxonomy.LANGUAGES` plus the tool's raw answer.
"""

from __future__ import annotations

import re

from tools.m import taxonomy as tax

# heuristics.yml, `.m` block — order matters (first match wins). Patterns are
# PCRE with multi_line(true) in Synid; Python `re.M` is equivalent here.
LINGUIST_M_RULES = [
    ("Objective-C", [re.compile(r"^\s*(@(interface|class|protocol|property|end|synchronised|selector|"
                                r"implementation)\b|#import\s+.+\.h[\">])", re.M)]),
    ("Mercury", [re.compile(r":- module")]),
    ("MUF", [re.compile(r"^: ", re.M)]),
    ("M", [re.compile(r"^\s*;", re.M)]),
    ("Mathematica", [re.compile(r"\(\*"), re.compile(r"\*\)$", re.M)]),
    ("MATLAB", [re.compile(r"^\s*%", re.M)]),
    ("Limbo", [re.compile(r"^\w+\s*:\s*module\s*\{", re.M)]),
]


def linguist(text: str) -> dict:
    for name, pats in LINGUIST_M_RULES:
        if all(p.search(text) for p in pats):
            return {"raw": name, "lang": tax.LINGUIST_TO_LANG[name]}
    return {"raw": None, "lang": "unknown"}   # abstain


def pygments(filename: str, text: str) -> dict:
    try:
        from pygments.lexers import guess_lexer_for_filename
        from pygments.util import ClassNotFound
    except ImportError:                       # pragma: no cover
        return {"raw": None, "lang": "unknown", "error": "pygments missing"}
    name = filename if filename.lower().endswith(".m") else "x.m"
    try:
        lx = guess_lexer_for_filename(name, text[:200000])
    except ClassNotFound:
        return {"raw": None, "lang": "unknown"}
    return {"raw": lx.name, "lang": tax.PYGMENTS_TO_LANG.get(lx.name, "other-programming-language")}
