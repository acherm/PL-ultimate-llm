import os, json, random, subprocess, sys
from pathlib import Path
import requests, yaml
from util import read_pl_list
from schema import Proposal
from templates import SYSTEM, USER

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TOOLS = ROOT / "tools"
CONFIG = TOOLS / "config.yaml"

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
}


def infer_ext(lang_name: str, origin_url: str) -> str | None:
    ln = (lang_name or "").strip().lower()
    # try from language table
    if ln in COMMON_EXT:
        return COMMON_EXT[ln]
    # try from URL suffix
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
        ".hs",
        ".rb",
        ".pl",
        ".php",
        ".scala",
        ".r",
        ".lua",
    }:
        if origin_url.lower().endswith(ext):
            return ext
    return None


def coerce_proposal_shape(raw_json_str: str) -> dict:
    """Accept common key variants from models and coerce to our exact schema keys."""
    obj = json.loads(raw_json_str)
    if "language" in obj and isinstance(obj["language"], dict):
        lang = obj["language"]
        # ensure aliases array exists
        if "aliases" not in lang or not isinstance(lang.get("aliases"), list):
            lang["aliases"] = []
        obj["language"] = lang
    # program
    prog = obj.get("program", {})
    if not isinstance(prog, dict):
        prog = {}
    # map common variants
    if "title" not in prog and "name" in prog:
        prog["title"] = prog.pop("name")
    if "filename_ext" not in prog:
        # try common alt keys
        for k in ("ext", "extension", "file_extension", "suffix"):
            if k in prog:
                prog["filename_ext"] = prog.pop(k)
                break
    # infer extension if still missing
    if "filename_ext" not in prog or not str(prog.get("filename_ext", "")).startswith(
        "."
    ):
        ext_guess = infer_ext(
            obj.get("language", {}).get("name", ""), prog.get("origin_url", "") or ""
        )
        if ext_guess:
            prog["filename_ext"] = ext_guess
    obj["program"] = prog
    return obj


def pick_model(cfg):
    import random

    return random.choice(cfg["models_pool"])


def build_language_list(pl_names, max_items=2000, max_chars=12000):
    joined = "\n".join(pl_names)
    if len(joined) > max_chars:
        return "\n".join(pl_names[:max_items])
    return joined


def call_openrouter(cfg, system_prompt, user_prompt, model):
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
        "temperature": 0.4,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def main():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    model = pick_model(cfg)
    pl_names = read_pl_list(str(DATA / "pl_list.txt"))
    user_prompt = USER.format(language_list=build_language_list(pl_names))
    raw = call_openrouter(cfg, SYSTEM, user_prompt, model)
    try:
        prop = Proposal.model_validate_json(raw)
    except Exception as e:
        # try to coerce common variants once
        coerced = coerce_proposal_shape(raw)
        try:
            prop = Proposal.model_validate(coerced)
        except Exception:
            # One more strict reprompt
            strict_user = (
                user_prompt
                + "\nWARNING: Your previous output was invalid JSON. Return ONLY valid JSON, with EXACT keys!"
            )
            raw2 = call_openrouter(cfg, SYSTEM, strict_user, model)
            coerced2 = coerce_proposal_shape(raw2)
            prop = Proposal.model_validate(coerced2)

    # Pipe to contribute
    p = subprocess.Popen(
        [sys.executable, str(TOOLS / "contribute.py")], stdin=subprocess.PIPE, text=True
    )
    p.communicate(prop.model_dump_json())
    if p.returncode != 0:
        sys.exit(p.returncode)
    print(f"[turn] accepted: {prop.language.name} | {prop.program.title}")


if __name__ == "__main__":
    main()
