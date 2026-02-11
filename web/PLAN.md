# Web Extensions Plan

## Goals
- Provide flexible preprocessing to detect duplicates, suspicious data, and clusters.
- Surface actionable quality signals directly in the site.
- Keep everything lightweight and static-first.

## Proposed Features
1. **Audit pipeline (data-quality)**
   - Run `tools/audit_repo.py` to generate `web/dist/data/audit.json`.
   - Checks: hash mismatches, missing code files, trivial code, extension mismatch, suspicious origin URLs, duplicated evidence URLs, alias/name collisions, fuzzy dupe candidates.
   - Outputs: per-language finding counts, duplicate candidates, clusters, related languages.

2. **Related languages**
   - Compute lightweight similarity from name + aliases (trigram Jaccard).
   - Display top related languages on each language page for navigation and duplicate triage.

3. **Inline quality signals**
   - Show audit counts (error/warn/info) as pills on language pages when `audit.json` is present.
   - Add an audit summary block on the stats page with total findings and top affected languages.

4. **Issue reporting**
   - Keep “Report issue” buttons per language/program that prefill GitHub issues with context.

## Notes / Future Enhancements
- Optional NLP-based embedding similarity for deeper clustering.
- Automated origin URL checks (HTTP status, content fingerprinting).
- Duplicate program detection across languages (code hash + shingling).
