"""Run SWH Synid (`synid file`) over every fetched `.fsf` content → data/derived/fsf_study/synid.jsonl.

Same two configurations as tools/m/run_synid.py (default content strategies;
the same without `comment`). Synid's syntaxes table has no `.fsf` entry, so
this measures what its content strategies make of FEAT designs, git-annex
pointers and the GLSL shaders that share the extension.

    python3 -m tools.fsf.run_synid
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.common import CACHE_DIR  # noqa: E402
from tools.m.run_synid import BIN, CONFIG, STRATS, synid_commit  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "fsf_study"
WORK = ROOT / ".cache" / "fsf" / "synid_in"
OUT = STUDY / "synid.jsonl"


def materialise() -> list[str]:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    shas = []
    for r in csv.DictReader((STUDY / "worklist_all.csv").open(encoding="utf-8")):
        p = CACHE_DIR / f"{r['sha1_git']}.bin"
        if not p.exists():
            continue
        base = re.sub(r"[^\w.+-]", "_", r["name"].lstrip("/"))[:80] or "file.fsf"
        if not base.endswith(".fsf"):
            base += ".fsf"
        d = WORK / r["sha1_git"]
        d.mkdir()
        (d / base).write_bytes(p.read_bytes())
        shas.append(r["sha1_git"])
    return shas


def run(cfg_name: str) -> dict[str, list[str]]:
    cfg = ROOT / ".cache" / "fsf" / f"synid_{cfg_name}.toml"
    cfg.write_text(CONFIG.format(out=ROOT / ".cache" / "fsf" / "synid-output",
                                 enable=json.dumps(STRATS[cfg_name])))
    out = subprocess.run([str(BIN), "file", "--config", str(cfg), str(WORK)],
                         capture_output=True, text=True, check=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith(str(WORK)):
            cur = Path(line.strip()).parent.name
        elif cur and line.strip().startswith("["):
            res[cur] = json.loads(line.strip())
            cur = None
    return res


def main():
    if not BIN.exists():
        sys.exit(f"synid binary missing: {BIN}")
    shas = materialise()
    results = {k: run(k) for k in STRATS}
    commit = synid_commit()
    with OUT.open("w", encoding="utf-8") as f:
        for sha in sorted(shas):
            f.write(json.dumps({"sha1_git": sha, "synid_commit": commit,
                                **{k: results[k].get(sha) for k in STRATS}}) + "\n")
    for k in STRATS:
        c = Counter("|".join(v) if v else "(none)" for v in results[k].values())
        print(k, c.most_common(8))
    print(f"wrote {OUT} ({len(shas)} contents)")


if __name__ == "__main__":
    main()
