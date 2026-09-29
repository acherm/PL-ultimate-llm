"""Orchestrator for the `.m` study — labels are stored as independent *layers*.

Methodological change vs the cobol/fsf/rpgle toolkits: there each content had
one report mixing indicators, reclassifier and judge, so refreshing the cheap
layer meant rewriting the expensive one. Here every labeller writes its own
layer, keyed by sha1_git, and nothing expensive is ever overwritten:

  labels/<sha>.json            indicators + ours + linguist + pygments   (free, regenerable)
  synid.jsonl                  SWH Synid verdicts                         (free, tools/m/run_synid.py)
  judge/<model-slug>/<sha>.json one file per (model, content)             (paid, append-only)

    python3 -m tools.m.study --label                     # all cached worklist contents
    python3 -m tools.m.study --judge --n 1000            # U rank<=1000 + R rank<=1000
    python3 -m tools.m.study --judge --n 1000 --model google/gemini-3.8-flash
    python3 -m tools.m.study --status
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.cobol.common import CACHE_DIR  # noqa: E402
from tools.m import indicators as ind_mod  # noqa: E402
from tools.m import labellers  # noqa: E402
from tools.m import reclassify as rc  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "m_study"
WORKLIST = STUDY / "worklist_all.csv"
LABELS = STUDY / "labels"
JUDGE = STUDY / "judge"
SYNID = STUDY / "synid.jsonl"
PRIMARY_MODEL = "anthropic/claude-sonnet-4.6"
SECOND_MODEL = "google/gemini-3.8-flash"


def slug(model: str, with_indicators: bool = False) -> str:
    return model.replace("/", "__").replace(":", "_") + ("+ind" if with_indicators else "")


def worklist() -> list[dict]:
    return list(csv.DictReader(WORKLIST.open(encoding="utf-8")))


def raw_bytes(sha: str) -> bytes | None:
    p = CACHE_DIR / f"{sha}.bin"
    return p.read_bytes() if p.exists() else None


def is_text(raw: bytes) -> bool:
    if b"\x00" in raw:
        return False
    if not raw:
        return True
    s = raw[:4096]
    printable = sum(1 for b in s if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return printable / len(s) > 0.85


def decode(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def label_one(row: dict) -> dict | None:
    raw = raw_bytes(row["sha1_git"])
    if raw is None:
        return None
    txt, ok = decode(raw), is_text(raw)
    ind = ind_mod.compute(txt, bytes_len=len(raw), is_text=ok)
    return {
        "sha1_git": row["sha1_git"], "name": row["name"], "path": row["path"],
        "origin": row["origin"], "forge": row["forge"], "length": len(raw),
        "indicators": ind.to_dict(),
        "ours": rc.classify(row["name"], raw),
        "linguist": labellers.linguist(txt) if ok else {"raw": None, "lang": "not-code"},
        "pygments": labellers.pygments(row["name"], txt) if ok else {"raw": None, "lang": "not-code"},
    }


def do_label():
    LABELS.mkdir(parents=True, exist_ok=True)
    n = 0
    for row in worklist():
        rep = label_one(row)
        if rep is None:
            continue
        (LABELS / f"{row['sha1_git']}.json").write_text(json.dumps(rep, ensure_ascii=False), encoding="utf-8")
        n += 1
    print(f"labelled {n} contents → {LABELS}")


def judge_targets(n: int, frames: str = "UR") -> list[dict]:
    out = []
    for r in worklist():
        u = int(r["u_rank"]) if r["u_rank"] and "U" in frames else 10**9
        d = int(r["d_rank"]) if r["d_rank"] and "R" in frames else 10**9
        if min(u, d) <= n:
            out.append(r)
    out.sort(key=lambda r: min(int(r["u_rank"] or 10**9), int(r["d_rank"] or 10**9)))
    return out


def do_judge(n: int, model: str, workers: int, max_cost: float, frames: str = "UR",
             with_indicators: bool = False):
    from tools.m import judge as judge_mod
    outdir = JUDGE / slug(model, with_indicators)
    outdir.mkdir(parents=True, exist_ok=True)
    spent = sum((json.loads(p.read_text()).get("usage") or {}).get("cost", 0) or 0
                for p in outdir.glob("*.json"))
    todo = []
    for r in judge_targets(n, frames):
        if (outdir / f"{r['sha1_git']}.json").exists():
            continue
        raw = raw_bytes(r["sha1_git"])
        if raw is None or not is_text(raw):
            continue
        todo.append(r)
    print(f"[{model}] targets≤{n}: to judge {len(todo)} | spent so far ${spent:.2f} | cap ${max_cost}", flush=True)
    lock = threading.Lock()
    state = {"spent": spent, "done": 0, "fail": 0, "stop": False}

    def work(r):
        if state["stop"]:
            return
        raw = raw_bytes(r["sha1_git"])
        txt = decode(raw)
        ind = ind_mod.compute(txt, bytes_len=len(raw)).to_dict()
        out = judge_mod.judge(r["name"], ind, txt, path=r["path"], origin=r["origin"], model=model,
                              with_indicators=with_indicators)
        out["sha1_git"] = r["sha1_git"]
        out["judged_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (outdir / f"{r['sha1_git']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        with lock:
            state["spent"] += (out.get("usage") or {}).get("cost", 0) or 0
            state["done"] += 1
            state["fail"] += 0 if out["parse_ok"] else 1
            if state["spent"] >= max_cost:
                state["stop"] = True
            if state["done"] % 50 == 0:
                print(f"  {state['done']}/{len(todo)} ${state['spent']:.2f} parse-fail={state['fail']}", flush=True)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(work, r) for r in todo]
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                print(f"  ERROR {str(e)[:200]}", file=sys.stderr, flush=True)
    print(f"[{model}] done {state['done']} | total spent ${state['spent']:.2f} | "
          f"parse failures {state['fail']}{' | STOPPED AT COST CAP' if state['stop'] else ''}", flush=True)


def do_status():
    wl = worklist()
    cached = sum(1 for r in wl if (CACHE_DIR / f"{r['sha1_git']}.bin").exists())
    print(f"worklist {len(wl)} | fetched {cached} | labelled {len(list(LABELS.glob('*.json')))}")
    for d in sorted(JUDGE.glob("*")) if JUDGE.exists() else []:
        files = list(d.glob("*.json"))
        cost = sum((json.loads(p.read_text()).get("usage") or {}).get("cost", 0) or 0 for p in files)
        print(f"judge {d.name}: {len(files)} verdicts, ${cost:.2f}")
    if SYNID.exists():
        print(f"synid: {sum(1 for _ in SYNID.open())} verdicts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", action="store_true")
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--n", type=int, default=1000, help="judge frame ranks <= n (both frames)")
    ap.add_argument("--model", default=PRIMARY_MODEL)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-cost", type=float, default=40.0)
    ap.add_argument("--frames", default="UR", help="U, R or UR")
    ap.add_argument("--with-indicators", action="store_true", help="anchoring ablation (E5)")
    a = ap.parse_args()
    if a.label:
        do_label()
    if a.judge:
        do_judge(a.n, a.model, a.workers, a.max_cost, a.frames, a.with_indicators)
    if a.status:
        do_status()


if __name__ == "__main__":
    main()
