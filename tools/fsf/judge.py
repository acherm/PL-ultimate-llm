"""LLM-as-judge for .fsf files (via OpenRouter). Reuses the COBOL judge's
HTTP + JSON plumbing; supplies an fsf-specific schema/prompt.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.judge import _post, _parse_json, DEFAULT_MODEL, MAX_CODE_CHARS  # noqa: E402
from tools.fsf import taxonomy as tax  # noqa: E402

SCHEMA_VERSION = "fsf-judge/1"

SYSTEM_PROMPT = (
    "You are a meticulous expert in scientific file formats. You are given a "
    "file indexed under the .fsf extension in Software Heritage, plus "
    "mechanical indicators. .fsf is typically an FSL FEAT design file (fMRI "
    "neuroimaging analysis config, Tcl `set fmri(...)` syntax) — a "
    "configuration format, NOT a general-purpose programming language. Decide "
    "what THIS file actually is, judging only from the evidence. For enum "
    "fields pick exactly one allowed value; put nuance in the *detail* fields. "
    "Respond with a SINGLE JSON object, no prose."
)


def json_schema() -> dict:
    conf = {"type": "string", "enum": tax.CONFIDENCES}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["is_programming_language", "artifact_kind", "not_fsf_label",
                     "feat_level", "analysis_type", "generated", "domain",
                     "feat_version", "n_evs", "summary", "confidence"],
        "properties": {
            "is_programming_language": {"type": "boolean"},
            "artifact_kind": {"type": "string", "enum": tax.ARTIFACT_KINDS},
            "not_fsf_label": {"type": "string", "enum": tax.NOT_FSF_LABELS},
            "feat_level": {"type": "string", "enum": tax.FEAT_LEVELS},
            "analysis_type": {"type": "string", "enum": tax.ANALYSIS_TYPES},
            "generated": {"type": "string", "enum": tax.GENERATED},
            "domain": {"type": "string", "enum": tax.DOMAINS},
            "feat_version": {"type": "string"},
            "n_evs": {"type": "integer"},
            "summary": {"type": "string"},
            "confidence": conf,
        },
    }


def _user_prompt(filename, indicators, code, truncated):
    note = (f"\n[truncated to first {MAX_CODE_CHARS} chars]" if truncated else "")
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
        "model": model, "temperature": 0.0, "max_tokens": 1200,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_prompt(
                filename, indicators, code[:MAX_CODE_CHARS] if truncated else code, truncated)},
        ],
    }
    rf = {"type": "json_schema", "json_schema": {
        "name": "fsf_verdict", "strict": True, "schema": json_schema()}}
    used = "json_schema"
    t0 = time.time()
    try:
        resp = _post({**base, "response_format": rf}, api_key)
    except Exception:
        used = "json_object"
        resp = _post({**base, "response_format": {"type": "json_object"}}, api_key)
    content = ((resp.get("choices") or [{}])[0].get("message") or {}).get("content", "")
    try:
        verdict = _parse_json(content)
        parse_ok = True
    except Exception as e:
        verdict, parse_ok = {"_parse_error": str(e)}, False
    return {
        "schema": SCHEMA_VERSION, "model": model, "response_format": used,
        "parse_ok": parse_ok, "verdict": verdict, "truncated": truncated,
        "usage": resp.get("usage", {}), "latency_s": round(time.time() - t0, 2),
        "raw": content if not parse_ok else None,
    }


if __name__ == "__main__":
    import argparse
    from tools.cobol.common import fetch_content
    from tools.fsf import indicators as I
    ap = argparse.ArgumentParser()
    ap.add_argument("swhid")
    a = ap.parse_args()
    c = fetch_content(a.swhid)
    ind = I.compute(c.text, bytes_len=c.length, is_text=c.is_text)
    print(json.dumps(judge(c.filename or a.swhid, ind.to_dict(), c.text), indent=2))
