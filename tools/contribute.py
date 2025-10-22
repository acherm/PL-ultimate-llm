import os, json, subprocess, sys
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
