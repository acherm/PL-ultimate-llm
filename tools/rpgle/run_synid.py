"""Run SWH Synid (`synid file`) over every judged `.rpgle` content → synid.jsonl.

Same protocol as tools/m/run_synid.py: Synid's default content strategies minus
the network-bound `linguistapi`, and the same set without `comment`, on the
cached bytes, each materialised as `<sha>/<name>` (name forced to `.rpgle`).

    (cd swh-syntax-identification && cargo build --release)
    python3 -m tools.rpgle.run_synid        # → data/derived/rpgle_study/synid.jsonl
"""

from __future__ import annotations

import glob
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "rpgle_study"
CACHE = ROOT / ".cache" / "cobol"
OUT = STUDY / "synid.jsonl"
SYNID_DIR = ROOT / "swh-syntax-identification"
BIN = SYNID_DIR / "target" / "release" / "synid"
WORK = ROOT / ".cache" / "rpgle" / "synid_in"
STRATS = {
    "default": ["filename", "extension", "shebang", "comment", "hyplyheuristics",
                "hyplyclassifier", "pygmentsheuristics"],
    "nocomment": ["filename", "extension", "shebang", "hyplyheuristics",
                  "hyplyclassifier", "pygmentsheuristics"],
}
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


def judged_reports() -> list[dict]:
    out = []
    for p in glob.glob(str(STUDY / "reports" / "*.json")):
        r = json.loads(Path(p).read_text())
        j = r.get("judge")
        if isinstance(j, dict) and j.get("verdict"):
            out.append(r)
    return out


def materialise(reps) -> dict[str, str]:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    names = {}
    for r in reps:
        raw = CACHE / f"{r['sha1_git']}.bin"
        if not raw.exists():
            continue
        base = re.sub(r"[^\w.+-]", "_", (r.get("name") or "file").lstrip("/"))[:80] or "file"
        if not base.lower().endswith(".rpgle"):
            base = base + ".rpgle"
        d = WORK / r["sha1_git"]
        d.mkdir()
        (d / base).write_bytes(raw.read_bytes())
        names[r["sha1_git"]] = base
    return names


def run(config_name: str) -> dict[str, list[str]]:
    cfg = ROOT / ".cache" / "rpgle" / f"synid_{config_name}.toml"
    cfg.write_text(CONFIG.format(out=ROOT / ".cache" / "rpgle" / "synid-output",
                                 enable=json.dumps(STRATS[config_name])))
    out = subprocess.run([str(BIN), "file", "--config", str(cfg), str(WORK)],
                         capture_output=True, text=True, check=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith(str(WORK)) or line.startswith(".cache"):
            cur = Path(line.strip()).parent.name
        elif cur and line.strip().startswith("["):
            res[cur] = json.loads(line.strip())
            cur = None
    return res


def main():
    if not BIN.exists():
        sys.exit(f"synid binary missing: build it in {SYNID_DIR} (cargo build --release)")
    names = materialise(judged_reports())
    print(f"materialised {len(names)} judged contents")
    results = {k: run(k) for k in STRATS}
    commit = subprocess.check_output(["git", "-C", str(SYNID_DIR), "rev-parse", "--short", "HEAD"],
                                     text=True).strip()
    with OUT.open("w", encoding="utf-8") as f:
        for sha in sorted(names):
            f.write(json.dumps({"sha1_git": sha, "synid_commit": commit,
                                **{k: results[k].get(sha) for k in STRATS}}) + "\n")
    for k in STRATS:
        c = Counter("|".join(v) if v else "(none)" for v in results[k].values())
        print(k, c.most_common(8))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
