#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One "turn":
- Pick a model from the pool
- Show it the current PL list
- Ask for ONE new language + ONE real program (JSON)
- Validate + coerce common variants
- Write contribution to repo
- Make ONE git commit with trailers (List-Digest, Model, Temperature)
- Log the entire session to logs/turn-YYYYMMDD.jsonl

Dependencies: pydantic, requests, pyyaml
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
from contribute import write_contribution, list_digest  # reuse existing functions

# -------- Optional logger (graceful fallback if logger.py not present) --------
try:
    from logger import write_event  # type: ignore
except Exception:  # pragma: no cover

    def write_event(event: Dict[str, Any], *, suffix: str = "turn") -> None:
        # no-op logger
        pass


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TOOLS = ROOT / "tools"
CONFIG = TOOLS / "config.yaml"

# -------- Coercion helpers to tolerate minor model key-mismatches --------
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
}


def infer_ext(lang_name: str, origin_url: str) -> Optional[str]:
    ln = (lang_name or "").strip().lower()
    if ln in COMMON_EXT:
        return COMMON_EXT[ln]
    for ext in {
        ".rs",
        ".py",
        ".c",
        ".cc",
        ".cpp",
        ".java",
        ".js",
        ".ts",
        ".go",
        ".ml",
        ".mli",
        ".hs",
        ".rb",
        ".pl",
        ".php",
        ".scala",
        ".r",
        ".lua",
        ".kt",
        ".swift",
        ".cs",
    }:
        if origin_url.lower().endswith(ext):
            return ext
    return None


# tools/turn.py (inside coerce_proposal_shape)
def coerce_proposal_shape(raw_json_str: str) -> dict:
    obj = json.loads(raw_json_str)
    lang = obj.get("language", {}) or {}
    if "aliases" not in lang or not isinstance(lang.get("aliases"), list):
        lang["aliases"] = []
    obj["language"] = lang

    prog = obj.get("program", {}) or {}

    if "title" not in prog and "name" in prog:
        prog["title"] = prog.pop("name")

    # Map common alt keys to filename_ext
    if "filename_ext" not in prog:
        for k in ("ext", "extension", "file_extension", "suffix"):
            if k in prog:
                prog["filename_ext"] = prog.pop(k)
                break

    # If missing or malformed, infer or normalize to start with "."
    ext = str(prog.get("filename_ext", "")).strip()
    if not ext or not ext.startswith("."):
        guessed = infer_ext(lang.get("name", ""), prog.get("origin_url", "") or "")
        if guessed:
            ext = guessed
        elif ext:  # we had something like "jl" -> ".jl"
            ext = "." + ext.lstrip(".")
        else:
            ext = ".txt"  # last-resort safe default (should be rare)
    prog["filename_ext"] = ext

    obj["program"] = prog
    return obj


# -------- Model selection & prompt building --------
def pick_model(cfg: dict) -> str:
    return random.choice(cfg["models_pool"])


def build_language_list(pl_names, max_items=2000, max_chars=12000) -> str:
    joined = "\n".join(pl_names)
    if len(joined) > max_chars:
        return "\n".join(pl_names[:max_items])
    return joined


# -------- OpenRouter call with logging --------
def call_openrouter(cfg: dict, system_prompt: str, user_prompt: str, model: str):
    api_key = os.environ.get(cfg["openrouter"]["api_key_env"])
    if not api_key:
        raise SystemExit(
            f"Missing env {cfg['openrouter']['api_key_env']} for OpenRouter API key"
        )

    url = cfg["openrouter"]["base_url"]
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.4,  # tweak here; it will be logged & committed
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    t0 = time.time()
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    dt = time.time() - t0

    req_id = r.headers.get("x-request-id") or r.headers.get("X-Request-Id")

    write_event(
        {
            "kind": "openrouter.request",
            "model": model,
            "temperature": payload["temperature"],
            "url": url,
            "status_code": r.status_code,
            "latency_s": round(dt, 3),
            "request_headers": {"Content-Type": "application/json"},
            "request_payload": payload,  # contains prompts
            "response_headers": dict(r.headers),
            "response_body_raw": r.text,
            "openrouter_request_id": req_id,
        }
    )

    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]

    write_event(
        {
            "kind": "openrouter.content",
            "model": model,
            "temperature": payload["temperature"],
            "content": content,
        }
    )

    return content, payload["temperature"], model


# -------- Main turn logic --------
def main():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    model = pick_model(cfg)

    # Read current state for context + digest we will record
    pl_names = read_pl_list(str(DATA / "pl_list.txt"))
    digest_before = list_digest()

    user_prompt = USER.format(language_list=build_language_list(pl_names))

    # 1st attempt
    raw, used_temp, used_model = call_openrouter(cfg, SYSTEM, user_prompt, model)

    # Validate strictly, then with a coercion pass if needed
    coerced_obj = None
    try:
        prop = Proposal.model_validate_json(raw)
    except Exception as e1:
        # Coerce common mistakes once
        try:
            coerced_obj = coerce_proposal_shape(raw)
            prop = Proposal.model_validate(coerced_obj)
        except Exception as e2:
            write_event(
                {
                    "kind": "validation.error",
                    "model": used_model,
                    "temperature": used_temp,
                    "error": f"{type(e2).__name__}: {e2}",
                    "raw": raw,
                    "repo_list_digest": digest_before,
                }
            )
            # Strict reprompt
            strict_user = (
                user_prompt
                + "\nWARNING: Your previous output was invalid JSON. Return ONLY valid JSON, with EXACT keys!"
            )
            raw2, used_temp, used_model = call_openrouter(
                cfg, SYSTEM, strict_user, model
            )
            # Final attempt with coercion
            try:
                coerced_obj2 = coerce_proposal_shape(raw2)
                prop = Proposal.model_validate(coerced_obj2)
            except Exception as e3:
                write_event(
                    {
                        "kind": "validation.fail",
                        "model": used_model,
                        "temperature": used_temp,
                        "error": f"{type(e3).__name__}: {e3}",
                        "raw": raw2,
                        "repo_list_digest": digest_before,
                    }
                )
                raise

    # Membership check: must be new
    existing = {n.lower() for n in pl_names}
    if prop.language.name.lower() in existing:
        write_event(
            {
                "kind": "membership.reject",
                "model": used_model,
                "temperature": used_temp,
                "language": prop.language.name,
                "reason": "already exists",
                "repo_list_digest": digest_before,
            }
        )
        raise SystemExit(f"LLM proposed existing language: {prop.language.name}")

    # Accept: write files
    write_event(
        {
            "kind": "proposal.accepted",
            "model": used_model,
            "temperature": used_temp,
            "proposal_json": prop.model_dump(mode="json"),
            "repo_list_digest": digest_before,
        }
    )

    sha = write_contribution(prop)

    # Create ONE commit (include trailers for audit)
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
