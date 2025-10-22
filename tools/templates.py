# tools/templates.py

# System prompt: explains the task and shows an exact JSON shape.
SYSTEM = """You must propose exactly ONE programming language that truly exists and is NOT in the provided list,
and ONE real program (code + origin_url) written in that language.

Return STRICT JSON with EXACT keys and types that match the schema below. No markdown, no comments, no extra keys.

SCHEMA (JSON object):
{
  "language": {
    "name": "string",                      // canonical language name
    "aliases": ["string", "..."],          // may be empty
    "evidence_url": "https://..."          // Wikipedia page for the language or the language's official site
  },
  "program": {
    "title": "string",                     // short human title
    "origin_url": "https://...",           // public URL where this exact code appears
    "filename_ext": ".ext",                // file extension, e.g., .rs, .py, .c, .jl
    "code": "string",                      // <= 200 lines; plain text; no fences
    "license_guess": "string or null"      // if unknown, null
  }
}

RULES:
- The language MUST already exist (not invented). Provide a credible evidence_url about the language itself.
- The program MUST be real. The origin_url MUST point to a public page containing this exact code.
- The filename_ext MUST match the language (e.g., .rs for Rust, .jl for Julia, .ml for OCaml; .rex implies the REXX family).
- The proposed language MUST NOT be in the provided list.
- The code MUST be valid for that language and reasonably non-trivial (more than a couple of lines).
- Output ONLY the JSON object (no prose, no code fences, no extra text).

If a language’s usual filename extensions contradict the provided filename_ext, correct the filename_ext or choose a different language.
Do NOT propose toolkits/IDEs/frameworks/control systems that are not textual programming languages.
"""

# User prompt: provides the current language list and asks for JSON only.
# (The orchestrator may append an additional blacklist for this turn.)
USER = """Current languages (do NOT propose any of these):
{language_list}

Important:
- You MUST propose a language that is NOT in the list above.
- If you propose an already-listed language or an invalid program, your output will be discarded and you will be asked again.

Return only the JSON object, nothing else."""
