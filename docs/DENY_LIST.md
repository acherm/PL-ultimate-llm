# Deny list

PL-ultimate-llm collects every programming language it can find evidence for.
A few must stay out — first case: **ArkScript**, whose maintainer asked for its
removal ("The language is not meant to be used by AIs or LLMs",
[PR #36](https://github.com/acherm/PL-ultimate-llm/pull/36)). Removing the
files once is not enough: the LLM campaign, a source refresh (PLDB, Rosetta
Code, …), a contribution form or a rebuild would bring the language back. The
deny list makes the decision durable.

## Policy

**Grounds** (`reason_kind`):

| kind | when | example |
|---|---|---|
| `maintainer-opt-out` | the language's creator or maintainer asks, from an account or channel that verifiably controls the language (its repository, organisation or website) | ArkScript — request from the top contributor of `ArkScript-lang/Ark` |
| `legal` | a takedown with a legal basis (copyright, …) | — |
| `harmful` | an entry that is abusive or harmful in itself | — |

Quality judgements ("not a real language", duplicates, wrong merges) are *not*
deny-list matters: they belong to the identity layer (`data/curated/pl_links.csv`,
`docs/PL_IDENTITY.md`).

**Process.** A request comes as an issue or pull request. A maintainer of this
repository checks the requester (e.g. commit history of the language's
repository), adds a row to `data/curated/deny_list.csv` with the evidence, and
runs `python3 tools/denylist.py purge --apply`. The requester can lift the
entry the same way.

**Scope.** A denied language gets no page, no campaign entry, no taxonomy
record, no sample and no mention in the generated site. The list itself is
public — it is the record of the decision (who asked, why, who decided, when).
**Git history is not rewritten**: past commits keep the removed files; a history
rewrite is reserved for legal takedowns.

**Precision.** Matching is exact, never fuzzy: a denied "ArkScript" must not
remove the Esolang "Ark", the 1990s "ARK" (University of Glasgow), "Ark"
(ark-lang, 2014) or ArkTS. An entry lists:

- `names` — exact names (case-insensitive);
- `records` — exact record ids: `repo/<languages folder>`, `pl/<taxonomy id>`;
- `urls` — fragments of the language's own sites, so that a campaign entry
  under another name ("Ark" with evidence `arkscript.org`) is still caught.

## Enforcement (tools/denylist.py)

| entry point | check |
|---|---|
| LLM campaign | every prompt lists the denied names (`tools/claude/prompt.py`); `CLAUDE.md` asks agents to run `python3 tools/denylist.py check "<Name>" --url <evidence>`; the pre-commit check (`tools/validate.py`) **refuses a commit** that adds a denied language to `languages/` or `pl_list.txt` |
| contribution forms | `tools/process_pl_addition.py`, `tools/process_pl_contribute.py` refuse with the reason |
| source refresh | `tools/master_inventory.py` drops denied rows from every CSV it writes |
| taxonomy | `tools/build_pl_taxonomy.py` drops denied records and every alias, claim, fact or heuristic pointing at them |
| site | `web/build_site.py` skips denied languages (defensive) |
| committed snapshots, frozen reports, the legacy `docs/` site | `python3 tools/denylist.py purge [--apply]` removes whole records, leaving every other byte (line endings included) as it was |

```
python3 tools/denylist.py list
python3 tools/denylist.py check "ArkScript"            # exit 1: denied
python3 tools/denylist.py check "Ark" --url https://esolangs.org/wiki/Ark   # exit 0
python3 tools/denylist.py scan                          # languages/ + pl_list.txt
python3 tools/denylist.py purge                         # dry run; --apply to write
```
