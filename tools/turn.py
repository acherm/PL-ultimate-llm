#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One "turn":
- Pick a model from the pool
- Show it the current PL list
- Ask for ONE new language + ONE real program (JSON)
- Prefer OpenRouter Structured Outputs (json_schema) when the model supports it
- Fallbacks: json_schema -> json_object -> no JSON mode -> model failover
- Validate + coerce common variants
- Write contribution
- Make ONE git commit with trailers (List-Digest, Model, Temperature)
- Log the session to logs/turn-YYYYMMDD.jsonl if tools/logger.py exists

Deps: pydantic, requests, pyyaml
"""

import os
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any

import requests
import yaml
from schema import Proposal
from templates import SYSTEM, USER
from util import read_pl_list
from contribute import write_contribution, list_digest  # writing + digest

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

# ---------- coercion helpers ----------
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

    # map alt keys to filename_ext
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


# ---------- model support detection ----------
def _model_supports_json_object(model: str) -> bool:
    m = model.lower()
    # generally good: OpenAI, Llama, Mistral, Qwen, DeepSeek via OpenRouter
    if any(m.startswith(p) for p in (
        "openai/", "meta-llama/", "mistralai/", "qwen/", "deepseek/"
    )):
        return True
    # generally not via OpenRouter: Gemini
    if m.startswith("google/") or "gemini" in m:
        return False
    return False


def _model_supports_json_schema(model: str) -> bool:
    m = model.lower()
    # OpenAI + several OSS routes accept json_schema structured outputs on OpenRouter
    if any(m.startswith(p) for p in (
        "openai/", "meta-llama/", "mistralai/", "qwen/", "deepseek/"
    )):
        return True
    # conservative: not Gemini via OpenRouter
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


# ---------- JSON schema for Structured Outputs ----------
def proposal_json_schema() -> dict:
    """JSON Schema matching our Proposal model."""
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


# ---------- OpenRouter call with Structured Outputs & fallbacks ----------
def _choose_fallback(cfg: dict, exclude: set[str]) -> Optional[str]:
    c = [m for m in cfg["models_pool"] if m not in exclude]
    return random.choice(c) if c else None


def call_openrouter(cfg: dict, system_prompt: str, user_prompt: str, model: str):
    api_key = os.environ.get(cfg["openrouter"]["api_key_env"])
    if not api_key:
        raise SystemExit(f"Missing env {cfg['openrouter']['api_key_env']} for OpenRouter API key")

    url = cfg["openrouter"]["base_url"]

    def payload(mode: str) -> dict:
        """
        mode: 'schema' | 'json' | 'none'
        """
        p = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 1200,
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
        "HTTP-Referer": "http://localhost",  # change to your site if you have one
        "Referer": "http://localhost",
    }

    tried: set[str] = set()
    attempt = 0
    backoff = 1.5

    # choose best initial mode for this model
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
        error_msg = body.get("error") or body.get("message") or body.get("text") or ""
        msg = str(error_msg).lower()

        # 400: try next mode (schema -> json -> none). If exhausted, failover model.
        if status == 400:
            if mode_index + 1 < len(modes):
                write_event({"kind": "openrouter.retry", "reason": "400_next_mode", "from": use_mode,
                             "to": modes[mode_index+1], "model": model, "msg": msg})
                mode_index += 1
                continue
            # failover
            tried.add(model)
            fb = _choose_fallback(cfg, tried)
            if fb:
                write_event({"kind": "openrouter.failover", "from_model": model, "to_model": fb,
                             "reason": "400_all_modes_failed", "msg": msg})
                model = fb
                # recompute modes for the fallback
                if _model_supports_json_schema(model):
                    modes = ["schema", "json", "none"]
                elif _model_supports_json_object(model):
                    modes = ["json", "none"]
                else:
                    modes = ["none"]
                mode_index = 0
                continue
            r.raise_for_status()

        # rate limits / transient
        if status in (429, 500, 502, 503, 504):
            write_event({"kind": "openrouter.backoff", "model": model,
                         "status": status, "sleep_s": round(backoff, 1), "msg": msg})
            time.sleep(backoff)
            backoff = min(60, backoff * 1.8)
            continue

        # other errors: try one failover
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


# ---------- main turn ----------
def main():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    model = pick_model(cfg)

    # current PL list + digest
    pl_names = read_pl_list(str(DATA / "pl_list.txt"))
    digest_before = list_digest()

    user_prompt = USER.format(language_list=build_language_list(pl_names))

    # attempt with structured outputs preference
    raw, used_temp, used_model = call_openrouter(cfg, SYSTEM, user_prompt, model)

    # strict validate -> coerce -> strict retry
    coerced_obj = None
    try:
        prop = Proposal.model_validate_json(raw)
    except Exception:
        try:
            coerced_obj = coerce_proposal_shape(raw)
            prop = Proposal.model_validate(coerced_obj)
        except Exception as e2:
            write_event({
                "kind": "validation.error",
                "model": used_model,
                "temperature": used_temp,
                "error": f"{type(e2).__name__}: {e2}",
                "raw": raw,
                "repo_list_digest": digest_before,
            })
            strict_user = user_prompt + "\nWARNING: Your previous output was invalid JSON. Return ONLY valid JSON, with EXACT keys!"
            raw2, used_temp, used_model = call_openrouter(cfg, SYSTEM, strict_user, model)
            try:
                coerced_obj2 = coerce_proposal_shape(raw2)
                prop = Proposal.model_validate(coerced_obj2)
            except Exception as e3:
                write_event({
                    "kind": "validation.fail",
                    "model": used_model,
                    "temperature": used_temp,
                    "error": f"{type(e3).__name__}: {e3}",
                    "raw": raw2,
                    "repo_list_digest": digest_before,
                })
                raise

    # must be a NEW language
    existing = {n.lower() for n in pl_names}
    if prop.language.name.lower() in existing:
        write_event({
            "kind": "membership.reject",
            "model": used_model,
            "temperature": used_temp,
            "language": prop.language.name,
            "reason": "already exists",
            "repo_list_digest": digest_before,
        })
        raise SystemExit(f"LLM proposed existing language: {prop.language.name}")

    # accept + write files
    write_event({
        "kind": "proposal.accepted",
        "model": used_model,
        "temperature": used_temp,
        "proposal_json": prop.model_dump(mode="json"),
        "repo_list_digest": digest_before,
    })

    sha = write_contribution(prop)

    # one commit with trailers
    commit_msg = (
        f"turn: add {prop.language.name} (+1 program)\n\n"
        f"List-Digest: {list_digest()}\n"
        f"Model: {used_model}\n"
        f"Temperature: {used_temp}\n"
    )
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print(f"[turn] accepted: {prop.language.name} | {prop.program.title} | sha={sha}")


if __name__ == "__main__":
    main()
