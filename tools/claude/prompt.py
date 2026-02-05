# tools/claude/prompt.py
"""
Agent prompt templates for Claude Code agents.
"""

# Base prompt shared by both modes
BASE_PROMPT = """Your task: Add ONE new programming language to this collection.

Steps:
1. Read data/pl_list.txt to see existing languages (580+ currently)
2. Choose a language NOT in that list
3. Find evidence URL (Wikipedia or official site)
4. Find a real program example with origin URL
5. Create files in languages/<Name>/ following CLAUDE.md format
6. Update data/pl_list.txt (keep sorted alphabetically)
7. Git commit with trailers: List-Digest, Model, Agent, WebSearch

Read CLAUDE.md for detailed file format requirements and validation rules.
"""

# Additional instructions for web search mode
WEB_SEARCH_INSTRUCTIONS = """
You have access to WebSearch. USE IT to:
- Search for lesser-known or obscure programming languages
- Verify that evidence URLs actually exist and are valid
- Find real program examples with verifiable source URLs
- Confirm the language is not already in the collection

WebSearch helps you find authentic, verifiable information. Use it actively.
"""

# Additional instructions for no web search mode
NO_WEB_SEARCH_INSTRUCTIONS = """
You must rely on your training knowledge (no web search available).

Guidelines:
- Choose a language you are confident exists
- Use evidence URLs you know are valid (Wikipedia, official sites)
- Write a program example you know is correct for this language
- Be conservative - prefer well-documented languages you're certain about
"""

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
    parts = [BASE_PROMPT.strip()]

    if web_search:
        parts.append(WEB_SEARCH_INSTRUCTIONS.strip())
    else:
        parts.append(NO_WEB_SEARCH_INSTRUCTIONS.strip())

    # Add model-specific instruction for commit trailer
    parts.append(f"\nFor the commit, use Model: {model}")

    # Add WebSearch trailer instruction
    ws_value = "enabled" if web_search else "disabled"
    parts.append(f"For the commit, use WebSearch: {ws_value}")

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
