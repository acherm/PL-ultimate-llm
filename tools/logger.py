import json, time, os
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)


def now_ms() -> int:
    return int(time.time() * 1000)


def write_event(event: Dict[str, Any], *, suffix: str = "turn") -> Path:
    """Append one JSON object per line to logs/<suffix>-YYYYMMDD.jsonl"""
    ts = time.strftime("%Y%m%d", time.gmtime())
    p = LOGS / f"{suffix}-{ts}.jsonl"
    event = {"ts_ms": now_ms(), **event}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return p
