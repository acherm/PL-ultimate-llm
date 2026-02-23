# PL-ultimate-llm Agent Instructions

You are an autonomous agent contributing to the Programming Languages collection.

## Your Task

Add **ONE** new programming language that:
1. Actually exists (not invented by you)
2. Is **NOT** already in `data/pl_list.txt`
3. Has credible evidence (Wikipedia page or official site)
4. Includes a real, non-trivial program example

## Required Steps

### Step 1: Read Current State

Read `data/pl_list.txt` to see existing languages (580+ currently).

Compute the List-Digest (you'll need this for the commit):
```python
import hashlib
content = open("data/pl_list.txt").read()
digest = hashlib.sha256(content.encode()).hexdigest()[:8]
```

### Step 2: Choose a Language

- Must **NOT** be in the existing list (case-insensitive check)
- Must be a real programming language (not an IDE, framework, library, or tool)
- Prefer lesser-known languages to increase collection diversity

### Step 3: Find Evidence URL

Find a credible URL proving the language exists:
- Wikipedia page (preferred): `https://en.wikipedia.org/wiki/<Language>_(programming_language)`
- Official language site
- Academic paper or specification

### Step 4: Find a Program Example

Find a real program written in this language:
- Must be from a public URL (GitHub, Rosetta Code, official docs, tutorials)
- Must be non-trivial (at least 3 meaningful lines of code)
- Keep under 200 lines
- Note the exact origin URL

### Step 5: Create Files

Create exactly these files:

#### `languages/<Name>/meta.json`
```json
{
  "name": "<Canonical Name>",
  "aliases": ["alias1", "alias2"],
  "evidence_url": "https://...",
  "added_at": "<ISO timestamp>Z"
}
```

- `name`: Canonical language name (use title case, e.g., "Python", "Rust", "Open Shading Language")
- `aliases`: Array of alternative names (can be empty `[]`)
- `evidence_url`: URL to Wikipedia or official site
- `added_at`: Current UTC timestamp in ISO format (e.g., "2025-02-05T12:30:45Z")

#### `languages/<Name>/programs/<sha256>/code.<ext>`

The actual program code.

- `<sha256>`: SHA256 hash of the normalized code (see below)
- `<ext>`: File extension matching the language (e.g., `.py`, `.rs`, `.jl`, `.ml`)

#### `languages/<Name>/programs/<sha256>/manifest.json`
```json
{
  "title": "<Program Title>",
  "origin_url": "https://...",
  "license_guess": "<license or null>",
  "code_sha256": "<sha256>",
  "added_at": "<ISO timestamp>Z"
}
```

- `title`: Short human-readable title (e.g., "Hello World", "Quicksort", "Fibonacci")
- `origin_url`: URL where this exact code appears
- `license_guess`: License if known (e.g., "MIT", "Apache-2.0", "Public Domain"), or `null`
- `code_sha256`: SHA256 of normalized code (same as directory name)
- `added_at`: Current UTC timestamp

### Step 6: Update pl_list.txt

Add the language name to `data/pl_list.txt`:
- Keep the file sorted alphabetically (case-insensitive)
- One language per line

### Step 7: Git Commit

Stage and commit all changes:

```bash
git add -A
git commit -m "turn: add <LanguageName> (+1 program)

List-Digest: <digest>
Model: <your-model-name>
Agent: claude-code
WebSearch: <enabled|disabled>
Strategy: <strategy>"
```

**Important**: Replace placeholders:
- `<LanguageName>`: The canonical language name
- `<digest>`: 8-character SHA256 prefix of pl_list.txt content (computed BEFORE your changes)
- `<your-model-name>`: Your model identifier (e.g., "claude-sonnet-4", "claude-opus-4")
- `<enabled|disabled>`: Whether you used web search to find the language/example
- `<strategy>`: Short phrase (2-5 words) describing how you chose this language (e.g., "concatenative-languages", "1960s-mainframe", "letter-Q-exploration", "stack-based-vms")

## Computing SHA256 for Code

Normalize the code by stripping trailing whitespace from each line:

```python
import hashlib

def code_hash(code: str) -> str:
    # Strip trailing whitespace from each line
    normalized = '\n'.join(line.rstrip() for line in code.splitlines())
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
```

## File Extension Reference

Common extensions (use the appropriate one for your language):

| Language | Extension |
|----------|-----------|
| Python | .py |
| Rust | .rs |
| Go | .go |
| Julia | .jl |
| OCaml | .ml |
| Haskell | .hs |
| Ruby | .rb |
| JavaScript | .js |
| TypeScript | .ts |
| C | .c |
| C++ | .cpp |
| Java | .java |
| Kotlin | .kt |
| Swift | .swift |
| Scala | .scala |
| Clojure | .clj |
| Erlang | .erl |
| Elixir | .ex |
| Lua | .lua |
| Perl | .pl |
| PHP | .php |
| R | .r |
| MATLAB | .m |
| Fortran | .f90 |
| Ada | .adb |
| COBOL | .cob |
| Prolog | .pl |
| Lisp | .lisp |
| Scheme | .scm |
| Racket | .rkt |

For other languages, use the standard file extension for that language.

## Critical Rules

1. **NEVER** propose a language already in `pl_list.txt`
2. **NEVER** invent a fake programming language
3. **NEVER** fabricate evidence URLs or program origin URLs
4. The `code_sha256` must match the actual SHA256 of the normalized code
5. File extension must match the language
6. Do **NOT** push to remote - only commit locally
7. Create exactly one commit with the format specified above

## Example Directory Structure

After adding "Sidef" language:

```
languages/Sidef/
├── meta.json
└── programs/
    └── a1b2c3d4e5f6.../
        ├── code.sf
        └── manifest.json
```

## Troubleshooting

- If git hooks fail, check that `List-Digest:` trailer is present
- If the language appears to exist, double-check `pl_list.txt` (case-insensitive)
- If code hash doesn't match, ensure you're stripping trailing whitespace per line
