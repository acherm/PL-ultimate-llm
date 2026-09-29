### 3. Labellers and experiments

#### 3.1 Seven labellers, one question: *which language is this `.m` file?*

| Labeller | Kind | Sees | Cost |
|---|---|---|---|
| **LLM judge** — `anthropic/claude-sonnet-4.6`, T=0, schema `m-judge/1` | semantic | bytes (≤ 16 k chars), file name, path, repository — **no indicators** | ⟪J1_COST⟫ |
| **LLM judge 2** — `google/gemini-3.8-flash`, same prompt and schema | semantic | same | ⟪J2_COST⟫ |
| **our reclassifier** — `m-reclass/1` (frozen before judging) and `/2` (tuned on U ranks 1–300) | rules | bytes | $0 |
| **Linguist** — the `.m` block of `heuristics.yml`, first match wins, else abstain | rules | bytes | $0 |
| **Pygments** 2.19 — `guess_lexer_for_filename`, choosing among its four `*.m` lexers | scores | bytes + name | $0 |
| **SWH Synid** `9bc1c32` — `synid file`, default content strategies | tool | bytes + name | $0 |
| **SWH Synid**, without its `comment` strategy | tool | bytes + name | $0 |

Linguist, Pygments and Synid are the identifiers the ecosystem actually runs;
Synid is Software Heritage's own. None of them was written for this study, so
their agreement with the judges is evidence rather than an echo. The judge schema
asks for the language *and* the semantic context the rules cannot give:
`content_type`, `provenance_kind` (hand-written / IDE-or-framework template /
tool-generated / vendored third-party / decompiled), `unit_kind`,
`matlab_dialect`, `related_languages[]`, `domain`, `maturity`, and free-text
details.

#### 3.2 Experiments

| # | Question | Design |
|---|---|---|
| **E1** | What is `.m`, by file? | judge + all labellers on U ranks 1–1,000 |
| **E2** | …and by repository? | the same on R ranks 1–1,000; U″ and U′ re-weightings for free |
| **E3** | Lexical vs semantic: who decides "Octave"? | judge's `octave` vs Octave-only tokens computed in code (H5) |
| **E4** | Do two LLMs from different vendors agree? | κ per schema field, 2,000 files (H7) |
| **E5** | Does showing the indicators anchor the judge? | U ranks 1–300 re-judged *with* indicators; agreement with our rules, blind vs shown (H6) |
| **E6** | How good are the ecosystem's identifiers? | Linguist, Pygments, Synid vs the two-judge consensus; failure modes traced to code |
| **E7** | Can cheap labels carry the estimate? | our frozen v1 on U/R ranks 1,001–2,000 + judge on ranks 1–1,000 → PPI |
| **E8** | Is the mapping right? | `ext_claim.csv` claims vs observed languages; the Pygments join |
| **E9** | Who is right when they disagree? | blind, stratified, weighted human audit — **tool and queue ready; reviews pending** |

**Spend.** ⟪SPEND⟫
