import re, hashlib, unicodedata, os
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
