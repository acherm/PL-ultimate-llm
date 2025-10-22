#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One "turn":
- Pick a model from the pool
- Show current PL list (names only)
- Prefer Structured Outputs (json_schema) when supported; fallback chain otherwise
- Parse robustly (strip fences), coerce common key errors
- Validate: new language, ext<->language compatibility, non-trivial code
- Write contribution and make ONE commit with trailers
- Log attempts/errors if tools/logger.py exists

Deps: pydantic, requests, pyyaml
"""

import os
import re
import json
import time
import random
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import requests
import yaml

from schema import Proposal
from templates import SYSTEM, USER
from util import read_pl_list
from contribute import write_contribution, list_digest

# ---------- optional logger (no-op if missing) ----------
try:
    from logger import write_event  # type: ignore
except Exception:  # pragma: no cover
    def write_event(event: Dict[str, Any], *, suffix: str = "turn") -> None:
        pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TOOLS = ROOT / "tools"
CONFIG = TOOLS / "config.yaml"


def _err_to_str(obj) -> str:
    """Best-effort stringify OpenRouter error bodies."""
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)

# ---------- helpers: JSON extraction/coercion ----------
def extract_json_str(s: str) -> str:
    """
    Extract a JSON object string from a model reply.
    - Prefer fenced ```json ... ``` or ``` ... ```
    - Else take the outermost { ... }
    - Reject empty strings
    """
    if not isinstance(s, str):
        raise ValueError("Reply is not a string")

    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", s, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        result = fence.group(1).strip()
        if not result:
            raise ValueError("Empty JSON found in fenced block")
        return result

    first = s.find("{")
    last = s.rfind("}")
    if first != -1 and last != -1 and last > first:
        result = s[first:last + 1].strip()
        if not result:
            raise ValueError("Empty JSON object found")
        return result

    result = s.strip()
    if not result:
        raise ValueError("Empty response string")
    return result

COMMON_EXT = {
    "python": ".py",
    "rust": ".rs",
    "c": ".c",
    "c++": ".cc",
    "cpp": ".cc",
    "java": ".java",
    "javascript": ".js",
    "typescript": ".ts",
    "go": ".go",
    "ocaml": ".ml",
    "haskell": ".hs",
    "ruby": ".rb",
    "perl": ".pl",
    "php": ".php",
    "scala": ".scala",
    "r": ".r",
    "lua": ".lua",
    "kotlin": ".kt",
    "swift": ".swift",
    "csharp": ".cs",
    "c#": ".cs",
    "julia": ".jl",
    "elixir": ".exs",
    "erlang": ".erl",
    "nim": ".nim",
    "zig": ".zig",
    "fortran": ".f90",
    "matlab": ".m",
    "wolfram": ".wl",
    "j": ".ijs",
}

def infer_ext(lang_name: str, origin_url: str) -> Optional[str]:
    ln = (lang_name or "").strip().lower()
    if ln in COMMON_EXT:
        return COMMON_EXT[ln]
    for ext in {
        ".rs", ".py", ".c", ".cc", ".cpp", ".java", ".js", ".ts", ".go",
        ".ml", ".mli", ".hs", ".rb", ".pl", ".php", ".scala", ".r", ".lua",
        ".kt", ".swift", ".cs", ".jl", ".ex", ".exs", ".erl", ".nim", ".zig",
        ".f90", ".m", ".wl", ".ijs"
    }:
        if origin_url.lower().endswith(ext):
            return ext
    return None

def coerce_proposal_shape(raw_json_str: str) -> dict:
    """Coerce common model mistakes into our exact schema keys."""
    obj = json.loads(raw_json_str)

    # language
    lang = obj.get("language", {}) or {}
    if "aliases" not in lang or not isinstance(lang.get("aliases"), list):
        lang["aliases"] = []
    obj["language"] = lang

    # program
    prog = obj.get("program", {}) or {}

    # name -> title
    if "title" not in prog and "name" in prog:
        prog["title"] = prog.pop("name")

    # alt keys -> filename_ext
    if "filename_ext" not in prog:
        for k in ("ext", "extension", "file_extension", "suffix"):
            if k in prog:
                prog["filename_ext"] = prog.pop(k)
                break

    # ensure extension starts with "."
    ext = str(prog.get("filename_ext", "")).strip()
    if not ext or not ext.startswith("."):
        guessed = infer_ext(lang.get("name", ""), prog.get("origin_url", "") or "")
        if guessed:
            ext = guessed
        elif ext:
            ext = "." + ext.lstrip(".")
        else:
            ext = ".txt"  # last-resort safe default
    prog["filename_ext"] = ext

    obj["program"] = prog
    return obj

# ---------- gates: ext<->language & trivial code ----------
EXT_ALLOW = {
    ".rs": {"rust"},
    ".py": {"python"},
    ".c": {"c"},
    ".cc": {"c++", "cpp"},
    ".cpp": {"c++", "cpp"},
    ".java": {"java"},
    ".js": {"javascript"},
    ".ts": {"typescript"},
    ".go": {"go"},
    ".ml": {"ocaml"},
    ".hs": {"haskell"},
    ".rb": {"ruby"},
    ".pl": {"perl"},
    ".php": {"php"},
    ".scala": {"scala"},
    ".r": {"r"},
    ".lua": {"lua"},
    ".kt": {"kotlin"},
    ".swift": {"swift"},
    ".cs": {"c#", "csharp"},
    ".jl": {"julia"},
    ".erl": {"erlang"},
    ".ex": {"elixir"},
    ".exs": {"elixir"},
    ".nim": {"nim"},
    ".zig": {"zig"},
    ".f90": {"fortran"},
    ".m": {"matlab"},
    ".wl": {"wolfram"},
    ".ijs": {"j"},
    ".rex": {"rexx", "oorexx", "netrexx"},
}

MIN_CODE_LINES = 3

def ext_language_compatible(lang_name: str, ext: str) -> bool:
    ln = (lang_name or "").strip().lower()
    ok = EXT_ALLOW.get(ext.lower())
    return (ok is None) or (ln in ok)

def is_trivial_code(lang_name: str, code: str) -> bool:
    lines = [ln for ln in code.splitlines() if ln.strip()]
    return len(lines) < MIN_CODE_LINES

# ---------- model support detection ----------
def _model_supports_json_object(model: str) -> bool:
    m = model.lower()
    if any(m.startswith(p) for p in ("openai/", "meta-llama/", "mistralai/", "qwen/", "deepseek/")):
        return True
    if m.startswith("google/") or "gemini" in m:
        return False
    return False

def _model_supports_json_schema(model: str) -> bool:
    m = model.lower()
    if any(m.startswith(p) for p in ("openai/", "meta-llama/", "mistralai/", "qwen/", "deepseek/")):
        return True
    if m.startswith("google/") or "gemini" in m:
        return False
    return False

def pick_model(cfg: dict) -> str:
    return random.choice(cfg["models_pool"])

def build_language_list(pl_names, max_items=2000, max_chars=8000) -> str:
    joined = "\n".join(pl_names)
    if len(joined) > max_chars:
        return "\n".join(pl_names[:max_items])
    return joined

def proposal_json_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "language": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "aliases": {"type": "array", "items": {"type": "string"}},
                    "evidence_url": {"type": "string", "format": "uri"},
                },
                "required": ["name", "aliases", "evidence_url"],
            },
            "program": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "origin_url": {"type": "string", "format": "uri"},
                    "filename_ext": {"type": "string", "minLength": 1},
                    "code": {"type": "string", "minLength": 1},
                    "license_guess": {"type": ["string", "null"]},
                },
                "required": ["title", "origin_url", "filename_ext", "code"],
            },
        },
        "required": ["language", "program"],
    }

# ---------- OpenRouter call with SO + fallbacks ----------
def _choose_fallback(cfg: dict, exclude: set[str]) -> Optional[str]:
    c = [m for m in cfg["models_pool"] if m not in exclude]
    return random.choice(c) if c else None

def call_openrouter(cfg: dict, system_prompt: str, user_prompt: str, model: str):
    api_key = os.environ.get(cfg["openrouter"]["api_key_env"])
    if not api_key:
        raise SystemExit(f"Missing env {cfg['openrouter']['api_key_env']} for OpenRouter API key")

    url = cfg["openrouter"]["base_url"]

    def payload(mode: str) -> dict:
        p = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 4000,
        }
        if mode == "schema":
            p["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "proposal",
                    "strict": True,
                    "schema": proposal_json_schema(),
                },
            }
        elif mode == "json":
            p["response_format"] = {"type": "json_object"}
        return p

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "PL-ultimate-llm",
        "HTTP-Referer": "http://localhost",
        "Referer": "http://localhost",
    }

    tried: set[str] = set()
    attempt = 0
    backoff = 1.5

    if _model_supports_json_schema(model):
        modes = ["schema", "json", "none"]
    elif _model_supports_json_object(model):
        modes = ["json", "none"]
    else:
        modes = ["none"]

    mode_index = 0

    while True:
        attempt += 1
        use_mode = modes[mode_index]
        pl = payload(use_mode)

        t0 = time.time()
        r = requests.post(url, headers=headers, json=pl, timeout=120)
        dt = time.time() - t0

        req_id = r.headers.get("x-request-id") or r.headers.get("X-Request-Id")
        write_event({
            "kind": "openrouter.request",
            "attempt": attempt,
            "model": model,
            "temperature": pl["temperature"],
            "mode": use_mode,
            "status_code": r.status_code,
            "latency_s": round(dt, 3),
            "request_payload_meta": {"has_response_format": "response_format" in pl},
            "response_body_raw": r.text,
            "openrouter_request_id": req_id,
        })

        if r.ok:
            content = r.json()["choices"][0]["message"]["content"]
            write_event({
                "kind": "openrouter.content",
                "model": model,
                "temperature": pl["temperature"],
                "mode": use_mode,
                "content": content,
            })
            return content, pl["temperature"], model

        status = r.status_code
        try:
            body = r.json()
        except Exception:
            body = {"text": r.text}
        
        # msg = (body.get("error") or body.get("message") or body.get("text") or "").lower()
        raw_msg = _err_to_str(body.get("error") or body.get("message") or body.get("text") or "")
        msg = raw_msg.lower()
        
        if status == 400:
            if mode_index + 1 < len(modes):
                write_event({"kind": "openrouter.retry", "reason": "400_next_mode",
                             "from": use_mode, "to": modes[mode_index + 1],
                             "model": model, "msg": msg})
                mode_index += 1
                continue
            tried.add(model)
            fb = _choose_fallback(cfg, tried)
            if fb:
                write_event({"kind": "openrouter.failover", "from_model": model, "to_model": fb,
                             "reason": "400_all_modes_failed", "msg": msg})
                model = fb
                if _model_supports_json_schema(model):
                    modes = ["schema", "json", "none"]
                elif _model_supports_json_object(model):
                    modes = ["json", "none"]
                else:
                    modes = ["none"]
                mode_index = 0
                continue
            r.raise_for_status()

        if status in (429, 500, 502, 503, 504):
            write_event({"kind": "openrouter.backoff", "model": model,
                         "status": status, "sleep_s": round(backoff, 1), "msg": msg})
            time.sleep(backoff)
            backoff = min(60, backoff * 1.8)
            continue

        tried.add(model)
        fb = _choose_fallback(cfg, tried)
        if fb:
            write_event({"kind": "openrouter.failover", "from_model": model, "to_model": fb,
                         "reason": f"status_{status}", "msg": msg})
            model = fb
            if _model_supports_json_schema(model):
                modes = ["schema", "json", "none"]
            elif _model_supports_json_object(model):
                modes = ["json", "none"]
            else:
                modes = ["none"]
            mode_index = 0
            continue

        r.raise_for_status()

# ---------- turn-level retry with dynamic rejects ----------
def build_user_prompt(pl_names: list[str], also_avoid: list[str] | None = None) -> str:
    base = build_language_list(pl_names)
    extra = ""
    if also_avoid:
        extra = "\n\nAdditionally, DO NOT propose any of these (rejected this turn):\n" + "\n".join(sorted(set(also_avoid)))
    return USER.format(language_list=base) + extra

def main():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    model0 = pick_model(cfg)

    pl_names = read_pl_list(str(DATA / "pl_list.txt"))
    digest_before = list_digest()

    rejects: list[str] = []
    max_attempts = 5
    used_model = model0
    used_temp = 0.4

    for attempt in range(1, max_attempts + 1):
        user_prompt = build_user_prompt(pl_names, rejects)

        raw, used_temp, used_model = call_openrouter(cfg, SYSTEM, user_prompt, used_model)

        # Parse strictly -> cleaned -> coerce -> reprompt
        try:
            prop = Proposal.model_validate_json(raw)
        except Exception:
            cleaned = extract_json_str(raw)
            try:
                prop = Proposal.model_validate_json(cleaned)
            except Exception:
                try:
                    prop = Proposal.model_validate(coerce_proposal_shape(cleaned))
                except Exception as e2:
                    write_event({
                        "kind": "validation.error",
                        "attempt": attempt,
                        "model": used_model,
                        "temperature": used_temp,
                        "error": f"{type(e2).__name__}: {e2}",
                        "raw": raw,
                        "raw_cleaned": cleaned,
                        "repo_list_digest": digest_before,
                    })
                    strict_user = user_prompt + "\nWARNING: Return ONLY a bare JSON object with EXACT keys. No markdown."
                    raw2, used_temp, used_model = call_openrouter(cfg, SYSTEM, strict_user, used_model)
                    cleaned2 = extract_json_str(raw2)
                    try:
                        prop = Proposal.model_validate_json(cleaned2)
                    except Exception:
                        prop = Proposal.model_validate(coerce_proposal_shape(cleaned2))

        # NEW: language must be new
        existing = {n.lower() for n in pl_names}
        if prop.language.name.lower() in existing:
            rejects.append(prop.language.name)
            write_event({"kind": "membership.reject", "attempt": attempt,
                         "language": prop.language.name, "repo_list_digest": digest_before})
            continue

        # gates: ext compatibility + non-trivial code
        if not ext_language_compatible(prop.language.name, prop.program.filename_ext):
            write_event({"kind": "program.ext_mismatch", "attempt": attempt,
                         "language": prop.language.name, "ext": prop.program.filename_ext})
            rejects.append(prop.language.name)
            continue

        if is_trivial_code(prop.language.name, prop.program.code):
            write_event({"kind": "program.too_trivial", "attempt": attempt,
                         "language": prop.language.name, "title": prop.program.title})
            rejects.append(prop.language.name)
            continue

        # accept and write
        write_event({
            "kind": "proposal.accepted",
            "attempt": attempt,
            "model": used_model,
            "temperature": used_temp,
            "proposal_json": prop.model_dump(mode="json"),
            "repo_list_digest": digest_before,
        })

        sha = write_contribution(prop)

        commit_msg = (
            f"turn: add {prop.language.name} (+1 program)\n\n"
            f"List-Digest: {list_digest()}\n"
            f"Model: {used_model}\n"
            f"Temperature: {used_temp}\n"
        )
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        print(f"[turn] accepted: {prop.language.name} | {prop.program.title} | sha={sha}")
        return  # success

    raise SystemExit(f"No acceptable proposal after {max_attempts} attempts (rejects this turn: {', '.join(rejects)})")

if __name__ == "__main__":
    main()
