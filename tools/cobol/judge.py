"""LLM-as-judge over a COBOL source, via the OpenRouter API.

OpenRouter is OpenAI-compatible: POST /api/v1/chat/completions with a
``Bearer`` key. We ask the model for a single JSON object categorising the
program (is-it-COBOL, dialect, source format, purpose, domain, features).

Key:    set ``OPENROUTER_API_KEY`` in the environment.
Model:  ``--model`` or ``COBOL_JUDGE_MODEL`` env; default below.

The structural indicators (tools/cobol/indicators.py) are shown to the
judge as ground-truth facts so its reasoning is anchored to the same
evidence a human reviewer would see.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from . import taxonomy as tax

# Reuse the repo's tolerant JSON extractor when available.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from turn import extract_json_str  # type: ignore
except Exception:  # pragma: no cover - fallback if import shape changes
    extract_json_str = None  # type: ignore

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.6"
MAX_CODE_CHARS = 16000  # keep prompt bounded; note truncation in the report

JUDGE_SCHEMA_VERSION = "cobol-judge/2"

SYSTEM_PROMPT = (
    "You are a meticulous COBOL expert acting as a classifier for a software "
    "archaeology study. You are given the contents of one file that was "
    "indexed as COBOL in the Software Heritage archive, plus structural "
    "indicators computed mechanically. Judge ONLY from the evidence shown. "
    "For the categorical fields you MUST pick exactly one value from the "
    "allowed enum; put any nuance in the matching free-text *detail* field "
    "(e.g. family=gnucobol, detail='JMA ORCA medical receipt system'). Be "
    "explicit about uncertainty. Respond with a SINGLE JSON object, no prose."
)


def judge_json_schema() -> dict:
    """Enum-constrained JSON Schema for OpenRouter structured outputs."""
    conf = {"type": "string", "enum": tax.CONFIDENCES}
    strlist = {"type": "array", "items": {"type": "string"}}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["cobol_confirmed", "not_cobol_label", "dialect",
                     "source_format", "purpose", "notable_features",
                     "maturity", "overall_confidence", "notes"],
        "properties": {
            "cobol_confirmed": {"type": "boolean"},
            "not_cobol_label": {"type": "string", "enum": tax.NOT_COBOL_LABELS},
            "dialect": {
                "type": "object", "additionalProperties": False,
                "required": ["family", "standard", "detail", "evidence", "confidence"],
                "properties": {
                    "family": {"type": "string", "enum": tax.DIALECT_FAMILIES},
                    "standard": {"type": "string", "enum": tax.STANDARDS},
                    "detail": {"type": "string"},
                    "evidence": strlist,
                    "confidence": conf,
                },
            },
            "source_format": {"type": "string", "enum": tax.SOURCE_FORMATS},
            "purpose": {
                "type": "object", "additionalProperties": False,
                "required": ["domain", "domain_detail", "summary", "program_type"],
                "properties": {
                    "domain": {"type": "string", "enum": tax.DOMAINS},
                    "domain_detail": {"type": "string"},
                    "summary": {"type": "string"},
                    "program_type": {"type": "string", "enum": tax.PROGRAM_TYPES},
                },
            },
            "notable_features": strlist,
            "maturity": {"type": "string", "enum": tax.MATURITIES},
            "overall_confidence": conf,
            "notes": {"type": "string"},
        },
    }


# Human-readable shape for the prompt + the json_object fallback.
OUTPUT_SHAPE = {
    "cobol_confirmed": "boolean (is this genuinely COBOL source?)",
    "not_cobol_label": f"one of {tax.NOT_COBOL_LABELS} ('none' if it IS COBOL)",
    "dialect": {
        "family": f"one of {tax.DIALECT_FAMILIES}",
        "standard": f"one of {tax.STANDARDS}",
        "detail": "free-text: specific product/system/version nuance",
        "evidence": ["short strings citing tokens you saw"],
        "confidence": "high|medium|low",
    },
    "source_format": f"one of {tax.SOURCE_FORMATS}",
    "purpose": {
        "domain": f"one of {tax.DOMAINS}",
        "domain_detail": "free-text: the specific business context",
        "summary": "1-3 sentences: what the program does",
        "program_type": f"one of {tax.PROGRAM_TYPES}",
    },
    "notable_features": ["e.g. EXEC SQL (DB2), EXEC CICS, COMP-3, screen section"],
    "maturity": f"one of {tax.MATURITIES}",
    "overall_confidence": "high|medium|low",
    "notes": "free-text caveats (encoding, truncation, ambiguity)",
}


def build_user_prompt(filename: str, indicators: dict, code: str,
                      truncated: bool) -> str:
    ind_json = json.dumps(indicators, indent=2)
    shape_json = json.dumps(OUTPUT_SHAPE, indent=2)
    trunc_note = (
        f"\n[NOTE: source truncated to first {MAX_CODE_CHARS} chars for length]"
        if truncated else "")
    return (
        f"Filename (as archived): {filename or '(unknown)'}\n\n"
        f"Mechanical indicators:\n```json\n{ind_json}\n```\n\n"
        f"Fill this JSON shape. For enum fields pick EXACTLY one allowed value; "
        f"put nuance in the *detail* fields:\n```json\n{shape_json}\n```\n\n"
        f"Source code:{trunc_note}\n```cobol\n{code}\n```\n"
    )


def normalize_verdict(v: dict) -> dict:
    """Safety net: coerce categorical fields to the canonical vocab in place.

    Strict structured outputs already guarantee valid enums, but this also
    canonicalizes free-text (cobol-judge/1) verdicts and any stray values.
    """
    if not isinstance(v, dict):
        return v
    dia = v.get("dialect")
    if isinstance(dia, dict):
        fam = dia.get("family") or dia.get("guess") or ""
        dia["family"] = tax.normalize_dialect_family(fam)
        dia["standard"] = tax.coerce_enum(dia.get("standard", ""), tax.STANDARDS)
    pur = v.get("purpose")
    if isinstance(pur, dict):
        pur["domain"] = tax.normalize_domain(pur.get("domain", ""))
        pur["program_type"] = tax.coerce_enum(
            pur.get("program_type", ""), tax.PROGRAM_TYPES)
    v["source_format"] = tax.coerce_enum(v.get("source_format", ""), tax.SOURCE_FORMATS)
    v["maturity"] = tax.coerce_enum(v.get("maturity", ""), tax.MATURITIES)
    return v


def _post(payload: dict, api_key: str, *, timeout: float = 120.0,
          max_retries: int = 3) -> dict:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/PL-ultimate-llm",
        "X-Title": "PL-ultimate-llm COBOL study",
    }
    last_err: Exception | None = None
    for attempt in range(max_retries):
        req = urllib.request.Request(OPENROUTER_URL, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            last_err = RuntimeError(f"HTTP {e.code}: {detail}")
            if e.code in (429, 500, 502, 503, 529):
                time.sleep(2.0 * (attempt + 1))
                continue
            raise last_err
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(2.0 * (attempt + 1))
            continue
    raise RuntimeError(f"OpenRouter POST failed after {max_retries} tries: {last_err}")


def _parse_json(content: str) -> dict:
    content = (content or "").strip()
    if extract_json_str is not None:
        try:
            return json.loads(extract_json_str(content))
        except Exception:
            pass
    # Fallbacks: strip code fences, take first {...} block.
    if content.startswith("```"):
        content = content.split("```", 2)[1]
        if content.lstrip().lower().startswith("json"):
            content = content.lstrip()[4:]
    try:
        return json.loads(content)
    except Exception:
        i, j = content.find("{"), content.rfind("}")
        if i != -1 and j != -1 and j > i:
            return json.loads(content[i:j + 1])
        raise


def judge(filename: str, indicators: dict, code: str, *,
          model: str = DEFAULT_MODEL, api_key: str | None = None,
          temperature: float = 0.0) -> dict:
    """Return a verdict dict: {schema, model, verdict, usage, raw, latency_s}."""
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set in environment.")

    truncated = len(code) > MAX_CODE_CHARS
    code_to_send = code[:MAX_CODE_CHARS] if truncated else code
    base = {
        "model": model,
        "temperature": temperature,
        # Headroom so a verbose verdict (long detail/evidence) doesn't get
        "max_tokens": 2048,  # truncated mid-JSON and fail to parse.
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(
                filename, indicators, code_to_send, truncated)},
        ],
    }
    # Prefer strict enum-constrained structured outputs; fall back to a plain
    # JSON object if the provider/model rejects the json_schema format.
    schema_rf = {"type": "json_schema", "json_schema": {
        "name": "cobol_verdict", "strict": True, "schema": judge_json_schema()}}
    used = "json_schema"
    t0 = time.time()
    try:
        resp = _post({**base, "response_format": schema_rf}, api_key)
    except Exception:
        used = "json_object"
        resp = _post({**base, "response_format": {"type": "json_object"}}, api_key)
    latency = round(time.time() - t0, 2)

    choice = (resp.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content", "")
    try:
        verdict = normalize_verdict(_parse_json(content))
        parse_ok = True
    except Exception as e:
        verdict = {"_parse_error": str(e)}
        parse_ok = False

    return {
        "schema": JUDGE_SCHEMA_VERSION,
        "model": model,
        "response_format": used,
        "parse_ok": parse_ok,
        "verdict": verdict,
        "truncated": truncated,
        "usage": resp.get("usage", {}),
        "provider": resp.get("provider"),
        "latency_s": latency,
        "raw": content if not parse_ok else None,
    }


if __name__ == "__main__":
    import argparse
    from .common import fetch_content
    from . import indicators as ind_mod

    ap = argparse.ArgumentParser(description="Judge one SWHID with the LLM.")
    ap.add_argument("swhid")
    ap.add_argument("--model", default=os.environ.get("COBOL_JUDGE_MODEL", DEFAULT_MODEL))
    args = ap.parse_args()

    c = fetch_content(args.swhid)
    ind = ind_mod.compute(c.text, bytes_len=c.length, is_text=c.is_text)
    out = judge(c.filename or args.swhid, ind.to_dict(), c.text, model=args.model)
    print(json.dumps(out, indent=2))
