#!/usr/bin/env python3
"""Check candidate language names against pl_list.txt.

Usage:
    python3 tools/claude/check_candidates.py candidates.txt
    python3 tools/claude/check_candidates.py -  # read from stdin
    echo -e "Python\nFooLang\nRust" | python3 tools/claude/check_candidates.py -

Output: prints only the candidates NOT already in pl_list.txt (one per line).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PL_LIST = ROOT / "data" / "pl_list.txt"


def load_existing() -> set[str]:
    """Load existing language names (lowercased) from pl_list.txt."""
    if not PL_LIST.exists():
        return set()
    return {line.strip().lower() for line in PL_LIST.read_text().splitlines() if line.strip()}


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # Read candidates from file or stdin
    source = sys.argv[1]
    if source == "-":
        lines = sys.stdin.read().splitlines()
    else:
        lines = Path(source).read_text().splitlines()

    candidates = [line.strip() for line in lines if line.strip()]
    existing = load_existing()

    # Print candidates not in the list
    new = []
    seen = set()
    for name in candidates:
        lower = name.lower()
        if lower not in existing and lower not in seen:
            seen.add(lower)
            new.append(name)
            print(name)

    # Summary to stderr
    print(f"\n--- {len(new)}/{len(candidates)} candidates are NEW (not in pl_list.txt) ---", file=sys.stderr)


if __name__ == "__main__":
    main()
