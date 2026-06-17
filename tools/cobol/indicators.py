"""Structural indicators for a COBOL source file.

These are cheap, deterministic metrics computed from the bytes alone — no
LLM, no network. They feed both the per-file report and the LLM-judge
prompt (so the judge sees the same facts a human reviewer would).

COBOL column model (fixed/standard format), 1-indexed:
    cols 1-6   sequence-number area (often blank or line numbers)
    col  7     indicator area: '*' or '/' = comment, '-' = continuation,
               'D'/'d' = debugging line
    cols 8-11  Area A   (division/section/paragraph headers, FD, 01/77)
    cols 12-72 Area B   (statements)
    cols 73-80 identification area (ignored by the compiler)

Free format (COBOL-2002+, GnuCOBOL ``>>SOURCE FORMAT FREE``) drops the
column rules; comments are introduced by ``*>`` (inline) or a line whose
first non-blank char is ``*``.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

_DIVISIONS = ["identification", "environment", "data", "procedure"]

# Whole-line, case-insensitive, anchored loosely so a leading sequence
# number (fixed format) before the keyword still matches.
_DIV_RE = {
    d: re.compile(rf"(?im)^.{{0,7}}\b{d if d != 'identification' else r'(identification|id)'}\s+division\b")
    for d in _DIVISIONS
}
_PROGRAM_ID_RE = re.compile(r"(?im)\bPROGRAM-ID\b\s*\.?\s*['\"]?([A-Za-z0-9][A-Za-z0-9_-]*)")
_EXEC_SQL_RE = re.compile(r"(?i)\bEXEC\s+SQL\b")
_EXEC_CICS_RE = re.compile(r"(?i)\bEXEC\s+CICS\b")
# COPY is a statement in Area B (fixed format: ~col 12) or anywhere (free), so
# allow leading sequence/indent (spaces or seq digits) before the verb. The
# leading class excludes '*'/'/' so fixed-format comment lines don't match.
_COPY_RE = re.compile(r"(?im)^[\s0-9]{0,15}COPY\s+[\"'A-Za-z0-9(]")
_CALL_RE = re.compile(r"(?i)\bCALL\s+['\"A-Za-z0-9]")
_PERFORM_RE = re.compile(r"(?i)\bPERFORM\b")
_GOTO_RE = re.compile(r"(?i)\bGO\s+TO\b")
_PIC_RE = re.compile(r"(?i)\bPIC(?:TURE)?\b")
_COMP3_RE = re.compile(r"(?i)\bCOMP-3\b")
_INLINE_FREE_COMMENT = re.compile(r"\*>")
_DIRECTIVE_RE = re.compile(r"(?im)^\s*>>\s*\S")  # >>SOURCE FORMAT, >>SET, etc.


@dataclass
class Indicators:
    bytes_len: int = 0
    is_text: bool = True
    decoded_with: str = "utf-8"
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    comment_ratio: float = 0.0
    max_line_length: int = 0
    avg_line_length: float = 0.0
    long_lines_over_72: int = 0
    source_format_guess: str = "unknown"  # fixed | free | unknown
    divisions_present: dict = field(default_factory=dict)
    n_divisions: int = 0
    program_ids: list = field(default_factory=list)
    has_exec_sql: bool = False
    has_exec_cics: bool = False
    copy_count: int = 0
    call_count: int = 0
    perform_count: int = 0
    goto_count: int = 0
    pic_count: int = 0
    comp3_count: int = 0
    has_compiler_directives: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _classify_line(line: str) -> str:
    """Return 'blank' | 'comment' | 'code' for one physical line."""
    if not line.strip():
        return "blank"
    # Fixed-format comment: indicator column (7th char, index 6) is '*' or '/'.
    if len(line) >= 7 and line[6] in "*/":
        # Guard: only treat as fixed-format comment if cols 1-6 are plausibly
        # the sequence area (blank or alnum), not arbitrary code text.
        if re.fullmatch(r"[0-9A-Za-z ]{6}", line[:6]):
            return "comment"
    stripped = line.lstrip()
    # Free-format full-line comment: first non-blank char is '*' (and not the
    # fixed-format col-7 case handled above), or the line is only an inline note.
    if stripped.startswith("*>"):
        return "comment"
    if stripped.startswith("*") and not (len(line) >= 7 and line[6] in "*/"):
        # A line beginning with '*' in area A of free format.
        return "comment"
    return "code"


def _guess_source_format(lines: list[str]) -> str:
    fixed_comments = 0
    seq_area_lines = 0
    free_comments = 0
    directive = False
    for line in lines:
        if not line.strip():
            continue
        if len(line) >= 7 and line[6] in "*/" and re.fullmatch(r"[0-9A-Za-z ]{6}", line[:6]):
            fixed_comments += 1
        if len(line) >= 6 and re.fullmatch(r"[0-9 ]{6}", line[:6]) and line[6:].strip():
            seq_area_lines += 1
        if _INLINE_FREE_COMMENT.search(line):
            free_comments += 1
        if _DIRECTIVE_RE.match(line):
            directive = True
    # Explicit free-format directive wins.
    nonblank = sum(1 for l in lines if l.strip())
    if directive and free_comments and not fixed_comments:
        return "free"
    if fixed_comments or (seq_area_lines and seq_area_lines > 0.30 * max(nonblank, 1)):
        return "fixed"
    if free_comments and not fixed_comments:
        return "free"
    # Many programs start statements at column 1 with no col-7 markers => free.
    col1_starts = sum(1 for l in lines if l[:1] not in (" ", "") and not l[:6].strip().isdigit())
    if not fixed_comments and not seq_area_lines and col1_starts > 0.5 * max(nonblank, 1):
        return "free"
    return "unknown"


def compute(text: str, *, bytes_len: int = 0, is_text: bool = True,
            decoded_with: str = "utf-8") -> Indicators:
    lines = text.split("\n")
    # Drop a trailing empty element from a final newline so counts are intuitive.
    if lines and lines[-1] == "":
        lines = lines[:-1]

    ind = Indicators(bytes_len=bytes_len, is_text=is_text, decoded_with=decoded_with)
    ind.total_lines = len(lines)

    lengths = []
    for line in lines:
        line = line.rstrip("\r")
        lengths.append(len(line))
        kind = _classify_line(line)
        if kind == "blank":
            ind.blank_lines += 1
        elif kind == "comment":
            ind.comment_lines += 1
        else:
            ind.code_lines += 1
        if len(line) > 72:
            ind.long_lines_over_72 += 1

    if lengths:
        ind.max_line_length = max(lengths)
        ind.avg_line_length = round(sum(lengths) / len(lengths), 1)
    denom = ind.comment_lines + ind.code_lines
    ind.comment_ratio = round(ind.comment_lines / denom, 3) if denom else 0.0

    ind.source_format_guess = _guess_source_format(lines)
    ind.divisions_present = {d: bool(_DIV_RE[d].search(text)) for d in _DIVISIONS}
    ind.n_divisions = sum(ind.divisions_present.values())
    ind.program_ids = sorted(set(_PROGRAM_ID_RE.findall(text)))[:8]
    ind.has_exec_sql = bool(_EXEC_SQL_RE.search(text))
    ind.has_exec_cics = bool(_EXEC_CICS_RE.search(text))
    ind.copy_count = len(_COPY_RE.findall(text))
    ind.call_count = len(_CALL_RE.findall(text))
    ind.perform_count = len(_PERFORM_RE.findall(text))
    ind.goto_count = len(_GOTO_RE.findall(text))
    ind.pic_count = len(_PIC_RE.findall(text))
    ind.comp3_count = len(_COMP3_RE.findall(text))
    ind.has_compiler_directives = bool(_DIRECTIVE_RE.search(text))
    return ind


# --- tiny self-test / CLI -------------------------------------------------
if __name__ == "__main__":
    import argparse
    import json
    from .common import fetch_content

    ap = argparse.ArgumentParser(description="Compute indicators for one SWHID.")
    ap.add_argument("swhid", help="swh:1:cnt:<sha> or bare sha1_git")
    args = ap.parse_args()
    c = fetch_content(args.swhid)
    ind = compute(c.text, bytes_len=c.length, is_text=c.is_text)
    print(json.dumps(ind.to_dict(), indent=2))
