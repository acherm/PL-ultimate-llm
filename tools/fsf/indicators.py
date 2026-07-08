"""Deterministic structural indicators for a .fsf file.

FSL FEAT design files are Tcl `set fmri(...) value` configs, heavily
commented (`#`). The `set fmri(` marker is a near-certain FEAT signal.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

_SET = re.compile(r"^\s*set\s+\S", re.M)
_SET_FMRI = re.compile(r"^\s*set\s+fmri\(", re.M)
_FEAT_FILES = re.compile(r"^\s*set\s+feat_files\(", re.M)
_LEVEL = re.compile(r"set\s+fmri\(level\)\s+(\d+)")
_INMELODIC = re.compile(r"set\s+fmri\(inmelodic\)\s+(\d+)")
_ANALYSIS = re.compile(r"set\s+fmri\(analysis\)\s+(\d+)")
_EVS = re.compile(r"set\s+fmri\(evs_orig\)\s+(\d+)")
_NPTS = re.compile(r"set\s+fmri\(npts\)\s+(\d+)")
_VERSION = re.compile(r"set\s+fmri\(version\)\s+(\S+)")


@dataclass
class Indicators:
    bytes_len: int = 0
    is_text: bool = True
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    comment_ratio: float = 0.0
    n_set: int = 0
    n_set_fmri: int = 0
    n_feat_files: int = 0
    has_feat: bool = False
    is_tcl_set: bool = False          # `set ...` dominates the non-comment lines
    feat_level: int | None = None     # 1 first-level, 2 higher-level
    inmelodic: int | None = None      # 1 = MELODIC
    analysis: int | None = None
    n_evs: int | None = None
    n_timepoints: int | None = None
    feat_version: str | None = None
    max_line_length: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def _int(m):
    return int(m.group(1)) if m else None


def compute(text: str, *, bytes_len: int = 0, is_text: bool = True) -> Indicators:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    ind = Indicators(bytes_len=bytes_len, is_text=is_text, total_lines=len(lines))
    code = 0
    for ln in lines:
        s = ln.strip()
        if not s:
            ind.blank_lines += 1
        elif s.startswith("#"):
            ind.comment_lines += 1
        else:
            code += 1
        ind.max_line_length = max(ind.max_line_length, len(ln.rstrip("\r")))
    denom = code + ind.comment_lines
    ind.comment_ratio = round(ind.comment_lines / denom, 3) if denom else 0.0

    ind.n_set = len(_SET.findall(text))
    ind.n_set_fmri = len(_SET_FMRI.findall(text))
    ind.n_feat_files = len(_FEAT_FILES.findall(text))
    ind.has_feat = ind.n_set_fmri > 0
    ind.is_tcl_set = code > 0 and ind.n_set >= 0.5 * code
    ind.feat_level = _int(_LEVEL.search(text))
    ind.inmelodic = _int(_INMELODIC.search(text))
    ind.analysis = _int(_ANALYSIS.search(text))
    ind.n_evs = _int(_EVS.search(text))
    ind.n_timepoints = _int(_NPTS.search(text))
    m = _VERSION.search(text)
    ind.feat_version = m.group(1) if m else None
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
