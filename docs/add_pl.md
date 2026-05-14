# Adding a new programming language via the web

The catalog grows two ways:

1. **Agentic** — the `/loop` campaign described in [CLAUDE.md](../CLAUDE.md).
   An LLM agent picks a missing language, finds evidence + a program, and
   commits the files. Bulk path; one PL per turn.
2. **Crowdsourced** — the **Add a PL** form at
   `/contribute/add-pl/` on the live site. Anyone with a GitHub account
   can propose a language; an Actions workflow turns the submission into a
   pull request that a maintainer reviews. This document covers (2).

## Submitter flow

1. Visit `/contribute/add-pl/`.
2. Fill the form:
   - **Canonical name** (required) — e.g. `Portable Game Notation`.
   - **Aliases** (optional, comma-separated) — e.g. `PGN, ChessPGN`.
   - **Evidence URL** (required) — Wikipedia page or official site.
   - **Program example** (optional, skeleton proposals accepted):
     - title (e.g. `Famous game: Adams vs Torre`)
     - file extension (e.g. `.pgn`)
     - origin URL (where the code appears publicly)
     - license guess (e.g. `Public Domain`)
     - the code itself (paste; <200 lines)
   - **Notes** (optional, e.g. inclusion-bar rationale for borderline cases).
3. Click **Submit via GitHub**. A pre-filled issue opens; confirm in
   GitHub. The issue carries the `pl-add` label.

## Issue body schema

```yaml
name: "Portable Game Notation"
aliases: ["PGN"]
evidence_url: "https://en.wikipedia.org/wiki/Portable_Game_Notation"
program:
  title: "Famous game: Adams vs Torre"
  ext: ".pgn"
  origin_url: "https://www.chessgames.com/perl/chessgame?gid=1019082"
  license_guess: "Public Domain"
  code: |
    [Event "New Orleans"]
    [Date "1920.??.??"]
    ...
notes: |
  PL inclusion-bar rationale (corpus already includes YAML, TOML, DOT, …).
```

Skeleton proposals use `program: null` (the form does this automatically
when the program fields are empty).

## What the workflow does

`.github/workflows/pl_add_pr.yml` reacts to:
- `issues.labeled` / `issues.opened` when the `pl-add` label appears, or
- `workflow_dispatch` with an `issue_number` input.

For each fire it:

1. Checks out `swh-evidence-v1` (the branch where the processor script lives).
2. Runs `python3 tools/process_pl_addition.py --issue <N>`:
   - Validates the YAML block.
   - Refuses if the name is already in `data/pl_list.txt` (case-insensitive).
   - Writes `languages/<safe-name>/meta.json`.
   - If a program was provided: writes
     `languages/<safe-name>/programs/<sha256>/{code.<ext>,manifest.json}`.
   - Appends the canonical name to `data/pl_list.txt` (kept sorted).
3. Commits everything on a new branch `pl-add/<dir>-issue-<N>` with a
   `Resolves #<N>` trailer + the `List-Digest:` trailer required by the
   pre-commit hook.
4. Opens a **draft** PR (`gh pr create --draft`) against `swh-evidence-v1`.
   The PR body carries a review checklist (evidence URL resolves, name is
   canonical, aliases are real, program is verbatim, license matches).

The PR is **never** auto-merged; a maintainer reviews and merges.

## Validations the processor enforces

| Check | Failure mode |
|---|---|
| YAML block present in the issue | exit code 3 (no PR opened) |
| `name` + `evidence_url` non-empty | exit code 3 |
| `name` not already in `pl_list.txt` (case-insensitive) | exit code 2 |
| Program code SHA-256 normalized (strip trailing whitespace per line) | (computed; mismatched manifests would fail the pre-commit `validate` hook) |

When the processor exits with a non-zero status, the workflow step fails
and GitHub leaves the issue open; a maintainer can read the failure log
and either fix the issue body or close it.

## Operator CLI (mirroring the workflow locally)

For testing or to materialize a submission on a developer machine:

```bash
# Dry-run — parse + validate, don't write files.
python3 tools/process_pl_addition.py --issue 17 --dry-run

# Real run — write languages/<Name>/, update pl_list.txt.
python3 tools/process_pl_addition.py --issue 17
```

The script writes a small JSON summary at
`.tmp/pl_add_summary_<N>.json` (consumed by the workflow to build the
PR title/body).

## Why a PR, not a direct commit?

Adding a PL touches both `languages/` and `pl_list.txt`. Mistakes (wrong
canonical name, evidence URL that 404s, a code paste that includes
non-source markup) are easier to spot in a PR diff than to revert after
the fact. The draft-PR model gates every web-form submission with one
maintainer pair of eyes.
