"""LLM-as-judge for `.rpgle` files (via OpenRouter). Reuses the COBOL judge's
HTTP + JSON plumbing; supplies an RPGLE-specific enum schema.

Per the playbook lesson: lead with *what the content is* and *which languages it
relates to*, not "is it language X".
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.judge import _post, _parse_json, DEFAULT_MODEL, MAX_CODE_CHARS  # noqa: E402
from tools.rpgle import taxonomy as tax  # noqa: E402

SCHEMA_VERSION = "rpgle-judge/1"

SYSTEM_PROMPT = (
    "You are a meticulous expert in IBM midrange (IBM i / AS-400) languages and "
    "file formats. You are given a file indexed under the .rpgle extension in "
    "Software Heritage, plus mechanical indicators. .rpgle is normally RPG IV / "
    "ILE RPG source. Characterise WHAT THIS CONTENT IS and WHICH LANGUAGES OR "
    "NOTATIONS IT RELATES TO (RPG itself, embedded SQL, CL commands, C "
    "prototypes via EXTPROC, DDS/display files, …) — do not merely confirm a "
    "preconceived language, and remember an extension can be polysemous. Note "
    "whether it is a program, a module, a service-program procedure, or a "
    "/copy prototype-header member. Judge only from the evidence. For enum "
    "fields pick exactly one allowed value; use the free-text fields for the "
    "substance. Respond with a SINGLE JSON object."
)


def json_schema() -> dict:
    conf = {"type": "string", "enum": tax.CONFIDENCES}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["content_type", "is_programming_language", "language",
                     "source_format", "unit_kind", "related_languages",
                     "embedded_sql", "platform", "domain", "maturity",
                     "not_rpgle_label", "purpose", "confidence"],
        "properties": {
            "content_type": {"type": "string", "enum": tax.CONTENT_TYPES},
            "is_programming_language": {"type": "boolean"},
            "language": {"type": "string",
                         "description": "specific language/dialect, e.g. 'RPG IV / ILE RPG (free-form)'"},
            "source_format": {"type": "string", "enum": tax.SOURCE_FORMATS},
            "unit_kind": {"type": "string", "enum": tax.UNIT_KINDS},
            "related_languages": {"type": "array", "items": {"type": "string"},
                                  "description": "languages/notations this content is written in, embeds, or relates to, e.g. ['RPG','SQL','CL']"},
            "embedded_sql": {"type": "boolean"},
            "platform": {"type": "string", "enum": tax.PLATFORMS},
            "domain": {"type": "string", "enum": tax.DOMAINS},
            "maturity": {"type": "string", "enum": tax.MATURITIES},
            "not_rpgle_label": {"type": "string", "enum": tax.NOT_RPGLE_LABELS},
            "purpose": {"type": "string"},
            "confidence": conf,
        },
    }


def _user_prompt(filename, indicators, code, truncated):
    note = f"\n[truncated to first {MAX_CODE_CHARS} chars]" if truncated else ""
    return (f"Filename: {filename or '(unknown)'}\n\n"
            f"Mechanical indicators:\n```json\n{json.dumps(indicators, indent=2)}\n```\n\n"
            f"Pick exactly one allowed value per enum field (see schema).\n\n"
            f"Content:{note}\n```\n{code}\n```\n")


def judge(filename, indicators, code, *, model=DEFAULT_MODEL, api_key=None):
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    truncated = len(code) > MAX_CODE_CHARS
    base = {
        "model": model, "temperature": 0.0, "max_tokens": 1400,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_prompt(
                filename, indicators, code[:MAX_CODE_CHARS] if truncated else code, truncated)},
        ],
    }
    rf = {"type": "json_schema", "json_schema": {
        "name": "rpgle_verdict", "strict": True, "schema": json_schema()}}
    used = "json_schema"
    t0 = time.time()
    try:
        resp = _post({**base, "response_format": rf}, api_key)
    except Exception:
        used = "json_object"
        resp = _post({**base, "response_format": {"type": "json_object"}}, api_key)
    content = ((resp.get("choices") or [{}])[0].get("message") or {}).get("content", "")
    try:
        verdict, parse_ok = _parse_json(content), True
    except Exception as e:
        verdict, parse_ok = {"_parse_error": str(e)}, False
    return {"schema": SCHEMA_VERSION, "model": model, "response_format": used,
            "parse_ok": parse_ok, "verdict": verdict, "truncated": truncated,
            "usage": resp.get("usage", {}), "latency_s": round(time.time() - t0, 2),
            "raw": content if not parse_ok else None}


if __name__ == "__main__":
    import argparse
    from tools.cobol.common import fetch_content
    from tools.rpgle import indicators as I
    ap = argparse.ArgumentParser()
    ap.add_argument("swhid")
    a = ap.parse_args()
    c = fetch_content(a.swhid)
    ind = I.compute(c.text, bytes_len=c.length, is_text=c.is_text)
    print(json.dumps(judge(c.filename or a.swhid, ind.to_dict(), c.text), indent=2))
