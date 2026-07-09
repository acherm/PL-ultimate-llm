"""Deterministic structural indicators for a `.rpgle` (ILE RPG) file.

Source-format model (the central axis):
  - **fully-free** : `**FREE` (or `**free`) on the first line; free-form
    `ctl-opt` / `dcl-s` / `dcl-proc` throughout; `//` comments.
  - **hybrid-free**: fixed-format skeleton containing `/free … /end-free`.
  - **fixed-format**: column-oriented. Column 6 (index 5) carries the
    *specification letter* — H control, F file, D definition, C calculation,
    P procedure, O output; column 7 (`*`) marks a comment.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

_FULLY_FREE = re.compile(r"^\s*\*\*\s*free\b", re.I)
_FREE_BLOCK = re.compile(r"^\s*/free\b", re.I | re.M)
_END_FREE = re.compile(r"^\s*/end-free\b", re.I | re.M)
_CTL_OPT = re.compile(r"(?im)^\s*ctl-opt\b")
_DCL = re.compile(r"(?im)^\s*(dcl-(?:s|ds|f|c|pr|pi|proc|subf|parm|enum))\b")
_DCL_PROC = re.compile(r"(?im)^\s*dcl-proc\b")
_DCL_PR = re.compile(r"(?im)^\s*dcl-pr\b")
_DCL_F = re.compile(r"(?im)^\s*dcl-f\b")
_EXEC_SQL = re.compile(r"(?i)\bexec\s+sql\b")
_COPY_INC = re.compile(r"(?im)^\s*/(copy|include)\b")
_COND_DIR = re.compile(r"(?im)^\s*/(if|else|endif|define|undefine|eof)\b")
_WORKSTN = re.compile(r"(?i)\bworkstn\b")
_PRINTER = re.compile(r"(?i)\bprinter\b")
_CALLP = re.compile(r"(?i)\b(callp|monitor|on-error)\b")
_EXTPROC = re.compile(r"(?i)\bextproc\b")
# fixed-format specification line: col6 in HFDCPOI (and col7 not '*')
_SPEC_LETTERS = set("HFDCPOIhfdcpoi")


@dataclass
class Indicators:
    bytes_len: int = 0
    is_text: bool = True
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    comment_ratio: float = 0.0
    max_line_length: int = 0

    is_fully_free: bool = False
    n_free_blocks: int = 0
    n_fixed_spec_lines: int = 0
    source_format_guess: str = "unknown"

    has_ctl_opt: bool = False
    n_dcl: int = 0
    n_dcl_proc: int = 0
    n_dcl_pr: int = 0
    n_dcl_f: int = 0
    has_exec_sql: bool = False
    n_copy_include: int = 0
    n_cond_directives: int = 0
    has_workstn: bool = False
    has_printer: bool = False
    has_extproc: bool = False
    looks_rpgle: bool = False
    looks_copybook: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _classify_line(line: str, fully_free: bool) -> str:
    s = line.strip()
    if not s:
        return "blank"
    if fully_free:
        return "comment" if s.startswith("//") else "code"
    # fixed format: col 7 (index 6) == '*' is a comment; also allow // in /free
    if len(line) >= 7 and line[6] == "*":
        return "comment"
    if s.startswith("//") or s.startswith("*"):
        return "comment"
    return "code"


def compute(text: str, *, bytes_len: int = 0, is_text: bool = True) -> Indicators:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    ind = Indicators(bytes_len=bytes_len, is_text=is_text, total_lines=len(lines))
    ind.is_fully_free = bool(lines and _FULLY_FREE.match(lines[0]))

    for ln in lines:
        ln = ln.rstrip("\r")
        ind.max_line_length = max(ind.max_line_length, len(ln))
        k = _classify_line(ln, ind.is_fully_free)
        if k == "blank":
            ind.blank_lines += 1
        elif k == "comment":
            ind.comment_lines += 1
        # fixed-format spec line: col6 a spec letter, col7 not a comment marker
        if (not ind.is_fully_free and len(ln) >= 7 and ln[5] in _SPEC_LETTERS
                and ln[6] != "*" and ln[:5].strip() == ""):
            ind.n_fixed_spec_lines += 1

    code = ind.total_lines - ind.blank_lines - ind.comment_lines
    denom = code + ind.comment_lines
    ind.comment_ratio = round(ind.comment_lines / denom, 3) if denom else 0.0

    ind.n_free_blocks = len(_FREE_BLOCK.findall(text))
    ind.has_ctl_opt = bool(_CTL_OPT.search(text))
    ind.n_dcl = len(_DCL.findall(text))
    ind.n_dcl_proc = len(_DCL_PROC.findall(text))
    ind.n_dcl_pr = len(_DCL_PR.findall(text))
    ind.n_dcl_f = len(_DCL_F.findall(text))
    ind.has_exec_sql = bool(_EXEC_SQL.search(text))
    ind.n_copy_include = len(_COPY_INC.findall(text))
    ind.n_cond_directives = len(_COND_DIR.findall(text))
    ind.has_workstn = bool(_WORKSTN.search(text))
    ind.has_printer = bool(_PRINTER.search(text))
    ind.has_extproc = bool(_EXTPROC.search(text))

    # source format
    if ind.is_fully_free:
        ind.source_format_guess = "fully-free"
    elif ind.n_free_blocks:
        ind.source_format_guess = "hybrid-free"
    elif ind.n_fixed_spec_lines >= 3:
        ind.source_format_guess = "fixed-format"
    elif ind.has_ctl_opt or ind.n_dcl >= 2:
        ind.source_format_guess = "fully-free"   # free syntax without the **FREE line
    else:
        ind.source_format_guess = "unknown"

    ind.looks_rpgle = (ind.is_fully_free or ind.has_ctl_opt or ind.n_dcl >= 2
                       or ind.n_free_blocks > 0 or ind.n_fixed_spec_lines >= 3)
    # a copy/header member: prototypes + include guards, no procedure bodies
    ind.looks_copybook = (ind.n_dcl_pr > 0 and ind.n_dcl_proc == 0
                          and (ind.n_cond_directives > 0 or ind.n_dcl_pr >= 2))
    return ind


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tools.cobol.common import fetch_content
    ap = argparse.ArgumentParser()
    ap.add_argument("swhid")
    a = ap.parse_args()
    c = fetch_content(a.swhid)
    print(json.dumps(compute(c.text, bytes_len=c.length, is_text=c.is_text).to_dict(), indent=2))
