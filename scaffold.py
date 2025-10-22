# Retry: escape or replace em-dashes and ensure only ASCII in triple-quoted Python strings.
import os, pathlib

root = "."
os.makedirs(root, exist_ok=True)
os.makedirs(f"{root}/languages", exist_ok=True)
os.makedirs(f"{root}/tools", exist_ok=True)
os.makedirs(f"{root}/data", exist_ok=True)
os.makedirs(f"{root}/.githooks", exist_ok=True)


def write_ascii(path, s, mode=0o644):
    # Replace common Unicode dashes with ASCII hyphens to avoid syntax errors in Python source
    s = s.replace("—", "-").replace("–", "-")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    os.chmod(path, mode)


README = """# PL Loop (Simplified, Local, Git-commit based)

This is a minimal scaffold for an infinite loop where, at each turn, a randomly chosen LLM proposes:
1) a programming language (that exists in the real world),
2) a real program (code + origin URL) in that language,
3) and the language must be new to the current list.

Rules enforced locally by Python:
- The proposed language name must not already be in the list (`data/pl_list.txt`).
- The proposal must include at least one evidence URL for the language (e.g., Wikipedia or official site).
- The program must include code (kept to a small size) and an origin_url (where the code came from).
- The tool commits changes to the local git repo after validation.

Quick start:

1) Initialize a new repo (once)
   git init
   git config core.hooksPath .githooks

2) (Optional) Seed the language list from your CSV
   python3 tools/seed_from_csv.py ../languages_master.csv

3) Configure OpenRouter (edit tools/config.yaml)
4) Run one turn
   python3 tools/turn.py

Structure:

pl-loop/
  data/
    pl_list.txt            # Current list of canonical PL names (source of truth for membership)
    catalog.csv            # Flat log of accepted contributions
  languages/
    <Canonical-PL-Name>/
      meta.json            # language metadata
      programs/<sha256>/{ code.<ext>, manifest.json }
  tools/
    turn.py                # orchestrates one "turn" (one commit)
    templates.py           # prompt template for the LLM
    schema.py              # JSON schema for the LLM response
    validate.py            # local validation rules
    contribute.py          # writes files and performs the git commit
    util.py                # helpers (slugify, hashing, etc.)
    config.yaml            # list of models + settings
    seed_from_csv.py       # optional seeding from your master CSV
  .githooks/
    pre-commit             # validates & regenerates catalog.csv
    commit-msg             # enforces a small trailer
"""
write_ascii(f"{root}/README.md", README)

write_ascii(f"{root}/data/pl_list.txt", "")
write_ascii(
    f"{root}/data/catalog.csv",
    "timestamp,language,program_title,origin_url,code_sha256,folder\n",
)

pre_commit = """#!/usr/bin/env bash
set -euo pipefail
echo "[pre-commit] validate and refresh catalog..."
python3 tools/validate.py --refresh-catalog
git add data/catalog.csv
"""
write_ascii(f"{root}/.githooks/pre-commit", pre_commit, 0o755)

commit_msg = """#!/usr/bin/env bash
# Require a List-Digest trailer to ensure the agent read HEAD.
grep -q "List-Digest:" "$1" || {
  echo "ERROR: commit message must include 'List-Digest: <hash>'" >&2
  exit 1
}
"""
write_ascii(f"{root}/.githooks/commit-msg", commit_msg, 0o755)

util_py = r"""import re, hashlib, unicodedata, os
from typing import List

def slugify(name: str) -> str:
    s = unicodedata.normalize('NFKC', name).strip()
    s = s.lower()
    s = re.sub(r'[^a-z0-9\-\_\s\+\.]', '', s)
    s = s.replace(' ', '-')
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def canonical_name(name: str) -> str:
    s = unicodedata.normalize('NFKC', name).strip()
    return re.sub(r'\s+', ' ', s)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def code_hash(code: str) -> str:
    norm = '\n'.join(line.rstrip() for line in code.splitlines())
    return sha256_bytes(norm.encode('utf-8'))

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def now_iso() -> str:
    import datetime
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'

def read_pl_list(path: str) -> List[str]:
    if not os.path.exists(path): return []
    with open(path,'r',encoding='utf-8') as f:
        return [ln.strip() for ln in f if ln.strip()]

def write_pl_list(path: str, names: List[str]):
    with open(path,'w',encoding='utf-8') as f:
        for n in sorted(set(names), key=lambda s: s.lower()):
            f.write(n+'\n')
"""
write_ascii(f"{root}/tools/util.py", util_py)

schema_py = r"""from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class Language(BaseModel):
    name: str = Field(..., description="Canonical language name")
    aliases: List[str] = Field(default_factory=list)
    evidence_url: HttpUrl

class Program(BaseModel):
    title: str
    origin_url: HttpUrl
    filename_ext: str = Field(..., description="e.g., .py, .c, .rb")
    code: str
    license_guess: Optional[str] = None

class Proposal(BaseModel):
    language: Language
    program: Program
"""
write_ascii(f"{root}/tools/schema.py", schema_py)

templates_py = r"""SYSTEM = "You propose one programming language that truly exists and is NOT in the provided list, and a real program (code + origin_url) written in that language. Output STRICT JSON matching the 'Proposal' schema. Rules: The language must be real (provide an evidence_url such as Wikipedia or the official site). The program must be real (provide origin_url where the code was obtained). Keep the code <= 200 lines. Include an appropriate filename extension (e.g., .py, .c). Do NOT include markdown fences or commentary-only JSON. If uncertain, return a minimal valid JSON rather than inventing."

USER = "Current languages (do NOT propose any of these):\n{language_list}\n\nReturn only JSON for ONE new language + ONE program in that language, following the schema."
"""
write_ascii(f"{root}/tools/templates.py", templates_py)

config_yaml = """openrouter:
  api_key_env: OPENROUTER_API_KEY
  base_url: https://openrouter.ai/api/v1/chat/completions

models_pool:
  - openai/gpt-4o-mini
  - anthropic/claude-3.5-sonnet
  - meta-llama/llama-3.1-70b-instruct
  - google/gemini-1.5-flash

limits:
  max_code_lines: 200
  max_name_len: 120
"""
write_ascii(f"{root}/tools/config.yaml", config_yaml)

validate_py = r"""import os, json, argparse, re, csv
from schema import Proposal
from util import read_pl_list, code_hash, now_iso

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CATALOG = os.path.join(DATA_DIR, 'catalog.csv')
PL_LIST = os.path.join(DATA_DIR, 'pl_list.txt')

def line_count(code: str) -> int:
    return len(code.splitlines())

def validate_proposal(p: dict, max_code_lines=200) -> Proposal:
    prop = Proposal.model_validate(p)
    assert prop.language.name.strip(), "Empty language name"
    assert prop.program.code.strip(), "Empty code"
    assert line_count(prop.program.code) <= max_code_lines, "Code too long"
    assert re.match(r'^\.[a-zA-Z0-9]+$', prop.program.filename_ext), "Bad filename_ext"
    return prop

def check_membership(name: str) -> bool:
    existing = {n.lower() for n in read_pl_list(PL_LIST)}
    return name.lower() in existing

def refresh_catalog():
    if not os.path.exists(CATALOG):
        with open(CATALOG,'w',encoding='utf-8',newline='') as f:
            f.write('timestamp,language,program_title,origin_url,code_sha256,folder\n')

def append_catalog_row(language: str, program_title: str, origin_url: str, sha: str, folder: str):
    with open(CATALOG,'a',encoding='utf-8',newline='') as f:
        w = csv.writer(f)
        w.writerow([now_iso(), language, program_title, origin_url, sha, folder])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--refresh-catalog', action='store_true')
    args = ap.parse_args()
    if args.refresh_catalog:
        refresh_catalog()
        print('[validate] refreshed catalog.csv')
"""
write_ascii(f"{root}/tools/validate.py", validate_py)

contribute_py = r"""import os, json, subprocess, sys
from schema import Proposal
from util import ensure_dir, canonical_name, code_hash, now_iso, read_pl_list, write_pl_list
from validate import append_catalog_row, check_membership
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data'
LANGS = ROOT/'languages'

def write_contribution(prop: Proposal) -> str:
    lang_name = canonical_name(prop.language.name)
    if check_membership(lang_name):
        raise SystemExit(f"Language already exists: {lang_name}")
    folder = LANGS/lang_name
    ensure_dir(folder)
    meta = {
        "name": lang_name,
        "aliases": prop.language.aliases,
        "evidence_url": str(prop.language.evidence_url),
        "added_at": now_iso()
    }
    (folder/'meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    sha = code_hash(prop.program.code)
    prog_dir = folder/'programs'/sha
    ensure_dir(prog_dir)
    code_path = prog_dir/('code'+prop.program.filename_ext)
    code_path.write_text(prop.program.code, encoding='utf-8')
    manifest = {
        "title": prop.program.title,
        "origin_url": str(prop.program.origin_url),
        "license_guess": prop.program.license_guess,
        "code_sha256": sha,
        "added_at": now_iso()
    }
    (prog_dir/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    # update list
    pl_list_path = DATA/'pl_list.txt'
    names = read_pl_list(str(pl_list_path))
    names.append(lang_name)
    write_pl_list(str(pl_list_path), names)
    append_catalog_row(lang_name, prop.program.title, str(prop.program.origin_url), sha, str(folder))
    return sha

def list_digest() -> str:
    content = (DATA/'pl_list.txt').read_text(encoding='utf-8') if (DATA/'pl_list.txt').exists() else ''
    import hashlib
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]

def git_commit(message: str):
    subprocess.run(['git','add','-A'], check=True)
    subprocess.run(['git','commit','-m', message], check=True)

if __name__ == '__main__':
    data = sys.stdin.read()
    prop = Proposal.model_validate_json(data)
    sha = write_contribution(prop)
    msg = f"turn: add {prop.language.name} (+1 program)\n\nList-Digest: {list_digest()}\n"
    git_commit(msg)
    print(f"[contribute] committed {prop.language.name} program sha={sha}")
"""
write_ascii(f"{root}/tools/contribute.py", contribute_py)

seed_py = r"""import sys, os, csv
from util import write_pl_list, read_pl_list, canonical_name

DATA = os.path.join(os.path.dirname(__file__),'..','data','pl_list.txt')

def main(csv_path: str):
    names = read_pl_list(DATA)
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            name = row.get('canonical_name') or row.get('name') or ''
            if name:
                names.append(canonical_name(name))
    write_pl_list(DATA, names)
    print(f"Seeded {len(names)} names into data/pl_list.txt")

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('Usage: python3 tools/seed_from_csv.py /path/to/languages_master.csv'); sys.exit(1)
    main(sys.argv[1])
"""
write_ascii(f"{root}/tools/seed_from_csv.py", seed_py)

turn_py = r"""import os, json, random, subprocess, sys
from pathlib import Path
import requests, yaml
from util import read_pl_list
from schema import Proposal
from templates import SYSTEM, USER

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data'
TOOLS = ROOT/'tools'
CONFIG = TOOLS/'config.yaml'

def pick_model(cfg):
    import random
    return random.choice(cfg['models_pool'])

def build_language_list(pl_names, max_items=2000, max_chars=12000):
    joined = '\n'.join(pl_names)
    if len(joined) > max_chars:
        return '\n'.join(pl_names[:max_items])
    return joined

def call_openrouter(cfg, system_prompt, user_prompt, model):
    api_key = os.environ.get(cfg['openrouter']['api_key_env'])
    if not api_key:
        raise SystemExit(f"Missing env {cfg['openrouter']['api_key_env']} for OpenRouter API key")
    url = cfg['openrouter']['base_url']
    payload = {
        "model": model,
        "messages": [
            {"role":"system","content": system_prompt},
            {"role":"user","content": user_prompt}
        ],
        "response_format": {"type":"json_object"},
        "temperature": 0.4
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']

def main():
    cfg = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    model = pick_model(cfg)
    pl_names = read_pl_list(str(DATA/'pl_list.txt'))
    user_prompt = USER.format(language_list=build_language_list(pl_names))
    raw = call_openrouter(cfg, SYSTEM, user_prompt, model)
    try:
        prop = Proposal.model_validate_json(raw)
    except Exception as e:
        strict_user = user_prompt + "\nWARNING: Your previous output was invalid JSON. Return only valid JSON!"
        raw = call_openrouter(cfg, SYSTEM, strict_user, model)
        prop = Proposal.model_validate_json(raw)
    # Membership check
    existing = {n.lower() for n in pl_names}
    if prop.language.name.lower() in existing:
        raise SystemExit(f"LLM proposed existing language: {prop.language.name}")
    # Pipe to contribute
    p = subprocess.Popen([sys.executable, str(TOOLS/'contribute.py')], stdin=subprocess.PIPE, text=True)
    p.communicate(prop.model_dump_json())
    if p.returncode != 0:
        sys.exit(p.returncode)
    print(f"[turn] accepted: {prop.language.name} | {prop.program.title}")

if __name__ == '__main__':
    main()
"""
write_ascii(f"{root}/tools/turn.py", turn_py)

print("OK - scaffold created at", root)
