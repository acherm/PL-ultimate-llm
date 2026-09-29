"""Run SWH Synid (`synid file`) over every fetched `.m` content → synid.jsonl.

Synid is SWH's own syntax identifier (Linguist + hyperpolyglot + Pygments
strategies, chained). We run it locally in `file` mode — no graph needed — in
two configurations over the same bytes:

  default   all content strategies of Synid's default config except the
            network-bound `linguistapi` (no repo context in file mode):
            filename, extension, shebang, comment, hyplyheuristics,
            hyplyclassifier, pygmentsheuristics
  nocomment the same without the `comment` strategy — isolates a failure
            mode found while calibrating: the comment strategy runs before the
            Linguist heuristics and drops Objective-C when a file's only `#`
            lines are `#import`/`#define`, so the pipeline answers "Text".

Each content is materialised as `<sha>/<name>.m` (the `.m` claim is what we
test, so a provenance name like `test.lua` is presented as `test.m`).

    cargo build --release   (in swh-syntax-identification/)
    python3 -m tools.m.run_synid
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.m.study import SYNID, raw_bytes, worklist  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SYNID_DIR = ROOT / "swh-syntax-identification"
BIN = SYNID_DIR / "target" / "release" / "synid"
WORK = ROOT / ".cache" / "m" / "synid_in"
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


def synid_commit() -> str:
    try:
        return subprocess.check_output(["git", "-C", str(SYNID_DIR), "rev-parse", "--short", "HEAD"],
                                       text=True).strip()
    except Exception:
        return "unknown"


def materialise() -> dict[str, str]:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    names = {}
    for r in worklist():
        raw = raw_bytes(r["sha1_git"])
        if raw is None:
            continue
        base = re.sub(r"[^\w.+-]", "_", r["name"] or "file")[:80] or "file"
        if not base.endswith(".m"):
            base = re.sub(r"\.[^.]*$", "", base) + ".m" if "." in base else base + ".m"
        d = WORK / r["sha1_git"]
        d.mkdir()
        (d / base).write_bytes(raw)
        names[r["sha1_git"]] = base
    return names


def run(config_name: str) -> dict[str, list[str]]:
    cfg = ROOT / ".cache" / "m" / f"synid_{config_name}.toml"
    cfg.write_text(CONFIG.format(out=ROOT / ".cache" / "m" / "synid-output",
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
    names = materialise()
    print(f"materialised {len(names)} contents")
    results = {k: run(k) for k in STRATS}
    commit = synid_commit()
    with SYNID.open("w", encoding="utf-8") as f:
        for sha in sorted(names):
            f.write(json.dumps({"sha1_git": sha, "synid_commit": commit,
                                **{k: results[k].get(sha) for k in STRATS}}) + "\n")
    for k in STRATS:
        from collections import Counter
        c = Counter("|".join(v) if v else "(none)" for v in results[k].values())
        print(k, c.most_common(12))
    print(f"wrote {SYNID}")


if __name__ == "__main__":
    main()
