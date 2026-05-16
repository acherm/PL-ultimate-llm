# How a "Label this" submission becomes a row on the site

This is the **persistence path** for the crowd-sourced extension labels —
written because the GitHub-issue indirection is not obvious from the UI alone.

## The five hops

```
  ┌───────────────────────────────┐
  │ 1. Reviewer fills the form    │   <-- /ext/<slug>/  (in-page form)
  │    on a per-extension page    │
  └───────────────────────────────┘
                │  click "Submit via GitHub"
                ▼
  ┌───────────────────────────────┐
  │ 2. A new GitHub issue is      │   <-- github.com/<owner>/<repo>/issues/new?…
  │    opened, label `ext-review` │       (pre-filled by the form's JS)
  │    body has a structured YAML │
  │    block + free-text context  │
  └───────────────────────────────┘
                │
                ▼
  ┌───────────────────────────────┐
  │ 3. `process_extension_labels` │   <-- tools/process_extension_labels.py
  │    fetches all ext-review     │       (runs in CI on every issue event,
  │    issues, parses each YAML   │        OR manually by maintainer)
  │    block, writes/updates      │
  │    extension_labels.csv       │
  └───────────────────────────────┘
                │
                ▼
  ┌───────────────────────────────┐
  │ 4. Maintainer reviews each    │   <-- /review/curator/
  │    new row (issue comments    │       (manual edit of curator_status
  │    + edits curator_status)    │        in extension_labels.csv)
  └───────────────────────────────┘
                │
                ▼
  ┌───────────────────────────────┐
  │ 5. `build_pl_taxonomy.py`     │   <-- tools/build_pl_taxonomy.py
  │    promotes `accepted`        │       (auto: runs after step 3 in CI;
  │    pl/<id> labels into        │        also any time the taxonomy is
  │    ext_claim.csv              │        rebuilt)
  └───────────────────────────────┘
                │
                ▼
  ┌───────────────────────────────┐
  │ Site rebuild renders new      │   <-- /ext/<slug>/, /l/<pl>/
  │    labels, friendly names,    │       (current: manual `build_site.py`;
  │    reference URLs             │        proposed: pages-deploy workflow)
  └───────────────────────────────┘
```

## The structured YAML block

The form JS builds this block client-side; the curator script parses it. It's
the contract between the two.

```yaml
ext: ".png"
label: "binary:image"
friendly_name: "Portable Network Graphics"
reference_url: "https://www.w3.org/TR/png/"
evidence: |
  W3C standard raster format, widely used in web and tools.
```

Anything outside this fenced block is for human consumption only and is ignored
by the parser.

## What runs where, when

| Step | Who triggers | When | Output |
|---|---|---|---|
| 1. Open form | reviewer | when visiting `/ext/<slug>/` | (no persistent state yet — just a form) |
| 2. Create issue | reviewer (browser → GitHub) | on `Submit via GitHub` click | a GitHub issue, label `ext-review` |
| 3. Parse issue → CSV | `.github/workflows/ingest_ext_labels.yml` | on issue create/label OR `workflow_dispatch` | commit to `extension_labels.csv` with `curator_status="new"` |
| 4. Triage | maintainer | when ready | edits `curator_status` to `accepted` / `rejected` / `needs-info` |
| 5. Promote | `build_pl_taxonomy.py` | every taxonomy rebuild | row added to `ext_claim.csv` (if label is `pl/<id>` and status is `accepted`) |
| 6. Render | `build_site.py` | every site rebuild | label visible on the affected `/ext/` and `/l/` pages |

## What happens if step 3's workflow isn't installed

Steps 3 → 6 don't run automatically. The site stays unchanged until a
maintainer runs locally:

```bash
python3 tools/process_extension_labels.py
# edit data/derived/extension_labels.csv to set curator_status=accepted on rows you accept
python3 tools/build_pl_taxonomy.py
python3 web/build_site.py
```

…and pushes the resulting commits. The GitHub issue is still preserved
(provenance is intact), it just doesn't surface on the site until the manual
ingestion runs.

## Why GitHub issues at all?

Each submission needs to be:

- **Auditable** — who said what, when. Issue author + timestamp + body suffice.
- **Re-readable** — comments, edits, references survive permanently.
- **Authenticatable** — the submitter is a known GitHub identity.
- **Discussable** — maintainers can ask for clarification before accepting.

A purpose-built form-backend would need to reimplement all four. GitHub issues
give them for free at the cost of one out-of-page tab when submitting.

If GH ever feels limiting, swapping the backend is small: only `app.js`'s
`_buildExtLabelIssueUrl` and the curator script's parser depend on the GH
issue format. Anything that produces JSON (or YAML) into a queue would work.

## Failure modes & recovery

| Symptom | Cause | Recovery |
|---|---|---|
| Submit button does nothing | Browser popup-blocker swallows `window.open` | Form shows a fallback link ("Or open the pre-filled issue directly →") — click it. |
| Submission opens GH but no issue gets created | Reviewer didn't click "Submit new issue" on the GitHub page | Nothing's lost; reviewer can come back and resubmit. |
| Issue parses but no row appears | `curator_status` is still `new`; promotion only happens for `accepted`. | Maintainer reviews and accepts. |
| Issue parses but the label is `pl/new:<x>` | Promotion gate only fires for `pl/<id>` (existing entity). | Maintainer adds the new PL to `pl.csv` first, then changes the label to `pl/<new-id>`. |
| Workflow committed bad data | Anyone can revert the bot's commit | `git revert` the chore(ext-labels) commit. |
