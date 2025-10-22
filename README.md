# PL Loop (Simplified, Local, Git-commit based)

This is a minimal scaffold for an infinite loop where, at each turn, a randomly chosen LLM proposes:
1) a programming language (that exists in the real world),
2) a real program (code + origin URL) in that language,
3) and the language must be new to the current list.

Rules enforced locally by Python:
- The proposed language name must not already be in the list (`data/pl_list.txt`).
- The proposal must include at least one evidence URL for the language (e.g., Wikipedia or official site).
- The program must include code (kept to a small size) and an origin_url (where the code came from).
- The tool commits changes to the local git repo after validation.

Quick start:

1) Initialize a new repo (once)
   git init
   git config core.hooksPath .githooks

2) (Optional) Seed the language list from your CSV
   python3 tools/seed_from_csv.py ../languages_master.csv

3) Configure OpenRouter (edit tools/config.yaml)
4) Run one turn
   python3 tools/turn.py

Structure:

pl-loop/
  data/
    pl_list.txt            # Current list of canonical PL names (source of truth for membership)
    catalog.csv            # Flat log of accepted contributions
  languages/
    <Canonical-PL-Name>/
      meta.json            # language metadata
      programs/<sha256>/{ code.<ext>, manifest.json }
  tools/
    turn.py                # orchestrates one "turn" (one commit)
    templates.py           # prompt template for the LLM
    schema.py              # JSON schema for the LLM response
    validate.py            # local validation rules
    contribute.py          # writes files and performs the git commit
    util.py                # helpers (slugify, hashing, etc.)
    config.yaml            # list of models + settings
    seed_from_csv.py       # optional seeding from your master CSV
  .githooks/
    pre-commit             # validates & regenerates catalog.csv
    commit-msg             # enforces a small trailer
