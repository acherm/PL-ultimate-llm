"""Zero-API content reclassifier for the `.rpgle` tail.

Labels: rpgle, rpgle-copybook (a /copy prototype-header member), data, docs,
binary, other. Bootstrapped from the LLM-judge labels and validated against it
(see the study report).
"""

from __future__ import annotations

import re

from tools.rpgle import indicators as ind_mod

RPGLE_LABELS = {"rpgle", "rpgle-copybook"}

_DOCS = re.compile(r"^\s*(#|<!--|={3,})")


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
        return {"label": "binary", "is_rpgle": False, "reason": "non-text bytes"}
    text = raw.decode("latin-1", "replace")
    ind = ind_mod.compute(text)

    if ind.looks_copybook:
        return {"label": "rpgle-copybook", "is_rpgle": True,
                "reason": f"dcl-pr={ind.n_dcl_pr}, no dcl-proc, include-guarded"}
    if ind.looks_rpgle:
        return {"label": "rpgle", "is_rpgle": True,
                "reason": f"format={ind.source_format_guess}, dcl={ind.n_dcl}, "
                          f"spec-lines={ind.n_fixed_spec_lines}"}

    nonblank = [l for l in text.split("\n") if l.strip()]
    if not nonblank:
        return {"label": "other", "is_rpgle": False, "reason": "empty"}
    if sum(1 for l in nonblank[:20] if _DOCS.match(l)) >= 3:
        return {"label": "docs", "is_rpgle": False, "reason": "markup/doc-like"}
    # delimited data?
    if sum(1 for l in nonblank[:20] if l.count(",") >= 3 or l.count(";") >= 3) >= 10:
        return {"label": "data", "is_rpgle": False, "reason": "delimited data"}
    return {"label": "other", "is_rpgle": False, "reason": "text, no RPG signal"}


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
