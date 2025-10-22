SYSTEM = (
    "You must propose exactly ONE programming language that truly exists and is NOT in the provided list, "
    "and ONE real program (code + origin_url) written in that language.\n"
    "Return STRICT JSON with EXACT keys and types that match the following schema:\n\n"
    "{\n"
    '  "language": {\n'
    '    "name": "string",\n'
    '    "aliases": ["string", "..."],\n'
    '    "evidence_url": "https://..."\n'
    "  },\n"
    '  "program": {\n'
    '    "title": "string",\n'  # REQUIRED
    '    "origin_url": "https://...",\n'  # REQUIRED
    '    "filename_ext": ".ext",\n'  # REQUIRED (e.g., .rs, .py, .c)
    '    "code": "string",\n'  # REQUIRED (<= 200 lines)
    '    "license_guess": "string or null"\n'
    "  }\n"
    "}\n\n"
    "Rules:\n"
    "- The language must be real; include an evidence_url (e.g., Wikipedia or the official site).\n"
    "- The program must be real; include the origin_url.\n"
    "- filename_ext must be the code file extension (e.g. .rs for Rust).\n"
    "- Code must be <= 200 lines. No markdown fences, no commentary, JSON only.\n"
)

USER = (
    "Current languages (do NOT propose any of these):\n"
    "{language_list}\n\n"
    "Return only the JSON object, nothing else."
)
