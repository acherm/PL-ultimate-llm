"""LLM-as-judge for `.m` files (OpenRouter; reuses the COBOL judge plumbing).

Playbook lessons applied:
  * lead with *what the content is* and *which languages it relates to*
    (`.m` is claimed by ≥ 8 languages; never ask "is it MATLAB?");
  * enum-constrained structured output (`json_schema`, strict);
  * split by decidability (rpgle): the judge is asked for **semantic** fields
    (language identity in context, provenance kind, purpose, domain, maturity,
    portability). Lexical facts (Octave-only tokens, `@` directives, …) are
    computed in `indicators.py` and passed in as *context*, and are scored
    against the judge afterwards — the judge is not the oracle for them.

The judge is also told the file's repository path, because `.m` identity is
often settled by context (an Xcode project vs a `toolbox/` folder).

**Blind by default.** The cobol/fsf/rpgle judges were shown the mechanical
indicators and then *compared against a classifier built on those same
indicators* — agreement was inflated by construction. The primary `.m` judge
sees only bytes + filename + path + repository (`with_indicators=False`); the
indicator-anchored variant exists only for the anchoring ablation (E5).
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.judge import _post, _parse_json, DEFAULT_MODEL, MAX_CODE_CHARS  # noqa: E402
from tools.m import taxonomy as tax  # noqa: E402

SCHEMA_VERSION = "m-judge/1"

SYSTEM_PROMPT = (
    "You are a meticulous expert in programming-language identification. You are "
    "given one file that Software Heritage archived under the `.m` extension, with "
    "its filename and repository path. `.m` is claimed by many languages: "
    "MATLAB, GNU Octave, Objective-C, Wolfram/Mathematica, Mercury, MUMPS (M), "
    "Magma, Maple, Scilab, Limbo, MUF, Perl Mason templates — and some `.m` files "
    "are not code at all (XML annotation layers, generated numeric expressions, "
    "text). Decide WHAT THIS CONTENT IS and WHICH LANGUAGES/NOTATIONS IT RELATES "
    "TO from the evidence, without assuming the most popular reading. "
    "`language` = the language the content is written in; use 'matlab' for "
    "MATLAB-family code that MATLAB accepts, 'octave' ONLY when the file uses "
    "Octave-only syntax that MATLAB rejects (e.g. `#` comments, endfunction/endif, "
    "printf, ++, !=). `provenance_kind` = how the file came to exist: hand-written, "
    "an IDE/framework template (Xcode, CocoaPods dummy, Flutter registrant, React "
    "Native AppDelegate), tool-generated (codegen, symbolic export, GUIDE), a "
    "vendored copy of a known third-party library, or decompiled/dumped. For enum "
    "fields pick exactly one allowed value; put the substance in the free-text "
    "fields. Respond with a SINGLE JSON object."
)


def json_schema() -> dict:
    return {
        "type": "object", "additionalProperties": False,
        "required": ["language", "language_detail", "content_type", "is_programming_language",
                     "provenance_kind", "provenance_detail", "unit_kind", "matlab_dialect",
                     "related_languages", "domain", "maturity", "purpose", "confidence"],
        "properties": {
            "language": {"type": "string", "enum": tax.LANGUAGES},
            "language_detail": {"type": "string",
                                "description": "specific language/dialect/format, e.g. 'Objective-C (UIKit)', 'MATLAB R2016b+', 'Magma', 'PML m-layer XML'"},
            "content_type": {"type": "string", "enum": tax.CONTENT_TYPES},
            "is_programming_language": {"type": "boolean"},
            "provenance_kind": {"type": "string", "enum": tax.PROVENANCE_KINDS},
            "provenance_detail": {"type": "string",
                                  "description": "e.g. 'CocoaPods dummy', 'AFNetworking 2.x', 'Coursera ML ex2', 'Maple CodeGeneration output'"},
            "unit_kind": {"type": "string", "enum": tax.UNIT_KINDS},
            "matlab_dialect": {"type": "string", "enum": tax.MATLAB_DIALECTS},
            "related_languages": {"type": "array", "items": {"type": "string"},
                                  "description": "languages/notations this content is written in, embeds, calls or targets, e.g. ['Objective-C','C'] or ['MATLAB','Octave']"},
            "domain": {"type": "string", "enum": tax.DOMAINS},
            "maturity": {"type": "string", "enum": tax.MATURITIES},
            "purpose": {"type": "string"},
            "confidence": {"type": "string", "enum": tax.CONFIDENCES},
        },
    }


def _user_prompt(filename, path, origin, indicators, code, truncated):
    note = f"\n[truncated to first {MAX_CODE_CHARS} chars]" if truncated else ""
    ind_block = ""
    if indicators:
        ind = {k: v for k, v in indicators.items() if v not in (0, False, 0.0, None)}
        ind_block = f"Mechanical indicators (non-zero only):\n```json\n{json.dumps(ind)}\n```\n\n"
    return (f"Filename: {filename or '(unknown)'}\nPath in repository: {path or '(unknown)'}\n"
            f"Repository: {origin or '(unknown)'}\n\n{ind_block}"
            f"Pick exactly one allowed value per enum field (see schema).\n\n"
            f"Content:{note}\n```\n{code}\n```\n")


def judge(filename, indicators, code, *, path="", origin="", model=DEFAULT_MODEL, api_key=None,
          with_indicators=False):
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    truncated = len(code) > MAX_CODE_CHARS
    base = {
        "model": model, "temperature": 0.0, "max_tokens": 1400,
        "usage": {"include": True},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_prompt(
                filename, path, origin, indicators if with_indicators else None,
                code[:MAX_CODE_CHARS] if truncated else code, truncated)},
        ],
    }
    rf = {"type": "json_schema", "json_schema": {
        "name": "m_verdict", "strict": True, "schema": json_schema()}}
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
    return {"schema": SCHEMA_VERSION, "model": model, "with_indicators": with_indicators,
            "response_format": used,
            "parse_ok": parse_ok, "verdict": verdict, "truncated": truncated,
            "usage": resp.get("usage", {}), "latency_s": round(time.time() - t0, 2),
            "raw": content if not parse_ok else None}
