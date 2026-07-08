"""Zero-API content reclassifier for the .fsf tail.

The `set fmri(` marker is a near-certain FEAT signal, so this is a much
cleaner target than COBOL. Labels: fsl-feat, tcl-other, config-other,
data, binary, other.
"""

from __future__ import annotations

import re

_SET_FMRI = re.compile(r"^\s*set\s+fmri\(", re.M)
_SET = re.compile(r"^\s*set\s+\S", re.M)

FEAT_LABELS = {"fsl-feat"}


def _is_binary(raw: bytes) -> bool:
    if b"\x00" in raw[:8192]:
        return True
    if not raw:
        return False
    s = raw[:4096]
    printable = sum(1 for b in s if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return printable / len(s) < 0.75


def classify(filename: str, raw: bytes) -> dict:
    if _is_binary(raw):
        return {"label": "binary", "is_feat": False, "reason": "non-text bytes"}
    text = raw.decode("latin-1", "replace")
    if _SET_FMRI.search(text):
        return {"label": "fsl-feat", "is_feat": True, "reason": "has set fmri(...)"}
    n_set = len(_SET.findall(text))
    nonblank = sum(1 for l in text.split("\n") if l.strip() and not l.lstrip().startswith("#"))
    if n_set >= 3 and n_set >= 0.4 * max(nonblank, 1):
        return {"label": "tcl-other", "is_feat": False, "reason": "Tcl set-config, no fmri()"}
    # a few key=value config lines?
    if re.search(r"^\s*\w[\w.-]*\s*[=:]\s*\S", text, re.M):
        return {"label": "config-other", "is_feat": False, "reason": "key=value config"}
    if nonblank == 0:
        return {"label": "docs" if text.strip() else "other", "is_feat": False, "reason": "comments/blank only"}
    return {"label": "other", "is_feat": False, "reason": "no FEAT/Tcl signal"}


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
    print(json.dumps({"filename": c.filename, **classify(c.filename, c.raw)}, indent=2))
