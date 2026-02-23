# tools/claude/prompt.py
"""
Agent prompt templates for Claude Code agents.
"""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _get_list_digest() -> str:
    """Compute the List-Digest from pl_list.txt."""
    pl_path = ROOT / "data" / "pl_list.txt"
    content = pl_path.read_text() if pl_path.exists() else ""
    return hashlib.sha256(content.encode()).hexdigest()[:8]


def _get_lang_count() -> int:
    """Count languages in pl_list.txt."""
    pl_path = ROOT / "data" / "pl_list.txt"
    if not pl_path.exists():
        return 0
    return sum(1 for line in pl_path.read_text().splitlines() if line.strip())


# Base prompt — optimized to avoid reading the full list into context
BASE_PROMPT = """Your task: Add ONE new programming language to this collection ({lang_count} languages currently).

CRITICAL EFFICIENCY RULES:
- Do NOT read data/pl_list.txt — use: grep -ix "LangName" data/pl_list.txt
- Do NOT use TodoWrite — just work directly
- Do NOT read project memory files — read only CLAUDE.md in the current directory
- The List-Digest is: {list_digest} (use this in your commit, do NOT recompute it)
- Most common languages (Python, Rust, Go, Haskell, etc.) are ALREADY listed. Pick something unlikely to be listed.
- You can check multiple languages at once: grep -ix -e "Lang1" -e "Lang2" -e "Lang3" data/pl_list.txt

STRATEGY: Before searching, decide on a search strategy — a short label describing your approach to finding
a language not yet in the collection. Be creative: you might explore by paradigm, era, geography, domain,
language family, a random letter, inspiration from a known resource, or anything else you can think of.
Record your strategy as a short phrase (2-5 words) — you will include it in the commit as a Strategy: trailer.

Steps:
1. Read CLAUDE.md for file format requirements
2. Decide your strategy (a short phrase like "concatenative-languages", "1960s-mainframe", "letter-Q-exploration", etc.)
3. Pick 3-5 candidates based on your strategy and batch-check: grep -ix -e "Lang1" -e "Lang2" -e "Lang3" data/pl_list.txt
4. For the FIRST one NOT in the list, create all files immediately:
   - languages/<Name>/meta.json
   - languages/<Name>/programs/<sha256>/code.<ext>
   - languages/<Name>/programs/<sha256>/manifest.json
5. Update data/pl_list.txt: python3 -c "lines=sorted(set(open('data/pl_list.txt').read().splitlines()+['YourLang']),key=str.lower);open('data/pl_list.txt','w').write('\\n'.join(l for l in lines if l)+'\\n')"
6. Commit: git add -A && git commit -m "turn: add <Name> (+1 program)\\n\\nList-Digest: {list_digest}\\nModel: {{model}}\\nAgent: claude-code\\nWebSearch: {{ws}}\\nStrategy: <your-strategy>"
"""

# Additional instructions for web search mode
WEB_SEARCH_INSTRUCTIONS = """
Use WebSearch to find lesser-known languages, verify evidence URLs, and find real program examples."""

# Additional instructions for no web search mode
NO_WEB_SEARCH_INSTRUCTIONS = """
Rely on your training knowledge. Choose a language you're confident exists. Use evidence URLs you know are valid. Write a correct program example."""

# Rejection list template (appended when retrying)
REJECTION_TEMPLATE = """
DO NOT propose any of these languages (already rejected this session):
{rejected_languages}
"""


def build_prompt(
    web_search: bool,
    model: str,
    rejected_languages: list[str] | None = None
) -> str:
    """
    Build the agent prompt.

    Args:
        web_search: Whether web search is enabled
        model: Model name for the commit trailer
        rejected_languages: Languages to exclude (from previous failed attempts)

    Returns:
        Complete prompt string
    """
    ws_value = "enabled" if web_search else "disabled"

    base = BASE_PROMPT.format(
        lang_count=_get_lang_count(),
        list_digest=_get_list_digest(),
    ).replace("{model}", model).replace("{ws}", ws_value).strip()

    parts = [base]

    if web_search:
        parts.append(WEB_SEARCH_INSTRUCTIONS.strip())
    else:
        parts.append(NO_WEB_SEARCH_INSTRUCTIONS.strip())

    # Add rejection list if any
    if rejected_languages:
        parts.append(
            REJECTION_TEMPLATE.format(
                rejected_languages=", ".join(rejected_languages)
            ).strip()
        )

    return "\n\n".join(parts)


def build_system_prompt() -> str:
    """
    Build the system prompt for the agent.

    This provides context about the project structure.
    """
    return """You are an autonomous agent contributing to a programming language collection.

Your goal is to add ONE new programming language with a real program example.
The repository contains:
- data/pl_list.txt: List of existing languages (one per line)
- languages/: Directory with language metadata and programs
- CLAUDE.md: Detailed instructions for file formats and commit structure

Follow the instructions in CLAUDE.md precisely. Create all required files and make exactly one git commit.
"""


if __name__ == "__main__":
    # Test prompt generation
    print("=== With Web Search ===")
    print(build_prompt(web_search=True, model="claude-sonnet-4"))
    print()
    print("=== Without Web Search ===")
    print(build_prompt(web_search=False, model="claude-opus-4"))
    print()
    print("=== With Rejections ===")
    print(build_prompt(
        web_search=True,
        model="claude-sonnet-4",
        rejected_languages=["Python", "Rust", "Go"]
    ))
