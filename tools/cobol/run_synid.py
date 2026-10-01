"""Run SWH Synid (`synid file`) over the COBOL study's uniform and by-repo samples.

Mirrors tools/m/run_synid.py (default content strategies minus the network-bound
`linguistapi`). Each content is materialised under its archived file name, so
`.cbl` and `.CBL` are presented exactly as in SWH (does Synid treat them alike?).

    python3 -m tools.cobol.run_synid      # → data/derived/cobol_study/synid.jsonl
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.cobol.common import CACHE_DIR  # noqa: E402

STUDY = ROOT / "data" / "derived" / "cobol_study"
OUT = STUDY / "synid.jsonl"
SYNID_DIR = ROOT / "swh-syntax-identification"
BIN = SYNID_DIR / "target" / "release" / "synid"
WORK = ROOT / ".cache" / "cobol_synid_in"
WORKLISTS = ("worklist_1k.csv", "worklist_div.csv")
STRATEGIES = ["filename", "extension", "shebang", "comment", "hyplyheuristics",
              "hyplyclassifier", "pygmentsheuristics"]
CONFIG = """[graph]
path = "/nonexistent/graph"
[graph.content]
content_host = "WebAPI"
[graph.output]
directory = "{out}"
[strategies]
enable = {enable}
disable = []
"""


def materialise() -> dict[str, str]:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    names = {}
    for wl in WORKLISTS:
        for r in csv.DictReader((STUDY / wl).open(encoding="utf-8")):
            sha = r["sha1_git"]
            raw = CACHE_DIR / f"{sha}.bin"
            if sha in names or not raw.exists():
                continue
            base = re.sub(r"[^\w.+-]", "_", Path(r["name"]).name) or "file.cbl"
            d = WORK / sha
            d.mkdir()
            (d / base).write_bytes(raw.read_bytes())
            names[sha] = base
    return names


def main():
    if not BIN.exists():
        sys.exit(f"synid binary missing: build it in {SYNID_DIR} (cargo build --release)")
    names = materialise()
    cfg = ROOT / ".cache" / "cobol_synid.toml"
    cfg.write_text(CONFIG.format(out=ROOT / ".cache" / "cobol_synid_out", enable=json.dumps(STRATEGIES)))
    out = subprocess.run([str(BIN), "file", "--config", str(cfg), str(WORK)],
                         capture_output=True, text=True, check=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith(str(WORK)) or line.startswith(".cache"):
            cur = Path(line.strip()).parent.name
        elif cur and line.strip().startswith("["):
            res[cur] = json.loads(line.strip())
            cur = None
    commit = subprocess.check_output(["git", "-C", str(SYNID_DIR), "rev-parse", "--short", "HEAD"],
                                     text=True).strip()
    with OUT.open("w", encoding="utf-8") as f:
        for sha in sorted(names):
            f.write(json.dumps({"sha1_git": sha, "name": names[sha], "synid_commit": commit,
                                "default": res.get(sha)}) + "\n")
    print(Counter("|".join(v) if v else "(none)" for v in res.values()).most_common(10))
    print(f"wrote {OUT} ({len(names)} contents)")


if __name__ == "__main__":
    main()
