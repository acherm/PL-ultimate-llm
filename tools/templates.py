# tools/templates.py

# System prompt: explains the task and **shows** an exact JSON shape.
SYSTEM = """You must propose exactly ONE programming language that truly exists and is NOT in the provided list,
and ONE *real* program (code + origin_url) written in that language.

Return STRICT JSON with EXACT keys and types that match the schema below. No markdown, no comments, no extra keys.

SCHEMA (JSON object):
{
  "language": {
    "name": "string",                      // canonical language name
    "aliases": ["string", "..."],          // may be empty
    "evidence_url": "https://..."          // Wikipedia or official site
  },
  "program": {
    "title": "string",                     // a short human title
    "origin_url": "https://...",           // where this code was obtained
    "filename_ext": ".ext",                // file extension, e.g. .rs, .py, .c
    "code": "string",                      // <= 200 lines; no fences
    "license_guess": "string or null"      // if unknown, null
  }
}

RULES:
- The language MUST already exist (not invented); include a credible evidence_url.
- The program MUST be real; include the origin_url.
- The proposed language MUST NOT be in the provided list.
- The code MUST be valid for that language and <= 200 lines.
- Use the correct filename_ext for the language (e.g., .rs for Rust, .jl for Julia, .ml for OCaml).
- Output ONLY the JSON object (no prose).
"""

# User prompt: provides the current language list and asks for JSON only.
USER = """Current languages (do NOT propose any of these):
{language_list}

Return only the JSON object, nothing else."""
