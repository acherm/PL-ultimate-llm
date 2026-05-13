# Extension label vocabulary

Controlled vocabulary for labelling file extensions during manual review.
Used by the `/review/extensions/` review queue on the site.

A label is one of:

| Label | Meaning | Examples |
|---|---|---|
| `pl/<id>` | This extension belongs to an existing PL in our taxonomy. Use the PL's `pl_id` (e.g., `pl/r`, `pl/zig`). | `.zig` → `pl/zig` |
| `pl/new:<name>` | This extension belongs to a real PL that's **not in our taxonomy yet**. The reviewer proposes adding it. | `.fsf` → `pl/new:fsl` (neuroimaging Feat Setup Language) |
| `pl/dialect:<parent>` | Extension belongs to a dialect / variant of a known PL. | `.pp` → `pl/dialect:pascal` |
| `pl/family:<family>` | Extension is shared by several languages in a family (BASIC, Pascal, …). Not a single-language label. | `.bas` → `pl/family:basic` |
| `binary:image` | Image file. | `.png`, `.jpg`, `.svg` |
| `binary:audio` | Audio file. | `.mp3`, `.wav` |
| `binary:video` | Video file. | `.mp4` |
| `binary:font` | Font file. | `.ttf`, `.woff` |
| `binary:archive` | Compressed / archive. | `.zip`, `.tar.gz` |
| `binary:executable` | Compiled binary, bytecode, or installable. | `.exe`, `.dll`, `.pyc`, `.class` |
| `binary:db` | Database file. | `.db`, `.sqlite` |
| `binary:other` | Other binary format. | `.pdf`, `.docx`, `.psd` |
| `data:json-like` | JSON or JSON-derived structured data. | `.json`, `.geojson`, `.jsonl` |
| `data:xml-like` | XML or XML-derived structured data. | `.xml`, `.xsd`, `.plist` |
| `data:yaml` | YAML serialisation. | `.yaml`, `.yml` |
| `data:csv-tsv` | Tabular plain text. | `.csv`, `.tsv` |
| `data:config` | Config / INI / TOML files. | `.toml`, `.ini`, `.conf`, `.env` |
| `data:domain` | Domain-specific data format (one or more applications). | `.npy`, `.h5`, `.mat`, `.uasset` |
| `docs` | Documentation, prose, markup. | `.md`, `.rst`, `.tex` |
| `lock/cache` | Lock files, caches, backups. | `.lock`, `.cache`, `.tmp` |
| `build-artifact` | Build outputs, intermediate artefacts. | `.o`, `.obj`, `.map`, `.log`, `.tlog` |
| `model/data` | ML model files / serialized model data. | `.onnx`, `.pkl`, `.tflite` |
| `license/manifest` | Project-meta files (often without a real "extension"). | `LICENSE`, `README` (rare). |
| `numeric-suffix` | Numeric-only suffix (manpage section, version number, etc.). | `.1`, `.2`, `.3`. |
| `sha-filename` | 32+ hex-char "extension" — content-addressable filename. | `.abcdef0123…` |
| `unknown` | Reviewer looked and could not classify; needs more info. | (use sparingly — leave it `pending` if you didn't review) |
| `noise` | One-off / typo / single-project filename / not worth a separate label. | `.tmpconfig123`, `.mybackup` |

## How to label

There are two entry points:

**Option A — In context, from a per-extension page.**
Visit `/ext/<slug>/` for the extension you know about (e.g. `/ext/png/`).
If it's not already well-attributed, the page shows an inline form:

1. Pick a **label** from the dropdown (vocabulary above).
2. If the label has `<...>`, fill the **custom** field (e.g. for `pl/<id>` type
   the actual id like `rust` or `julia`).
3. Optionally add a **friendly name** (e.g. "Portable Network Graphics") and a
   **reference URL** (spec, Wikipedia, vendor page, …).
4. Write **evidence/notes**: 1–3 sentences explaining the label fit.
5. Click **Submit via GitHub**. A new tab opens with a pre-filled GitHub issue
   carrying the structured YAML block. You only need to confirm + submit.

**Option B — From the review queue.**
Visit `/review/extensions/` (ranked queue — most-popular unattributed
extensions first). Click "Label this" on a row to jump to that extension's
form.

Either way, your GitHub login is captured automatically on submit, and the
issue carries the `ext-review` label so the curator script picks it up.

## What gets recorded per submission

| Field | Required | Source |
|---|---|---|
| `ext` | yes | the extension being labelled |
| `label` | yes | from the vocabulary above (or `pl/<id>` with real id substituted) |
| `friendly_name` | no | human-readable name (e.g. "Portable Network Graphics", "Markdown") |
| `reference_url` | no but recommended | spec, Wikipedia, vendor, format docs |
| `evidence` | yes | 1–3 sentences justifying the label |
| `annotator` | auto | GitHub login (from issue author) |
| `submitted_at` | auto | issue `created_at` |
| `issue_url` | auto | permalink to the issue |

## How labels feed back

A scheduled curator script (`tools/process_extension_labels.py`) reads
GitHub issues with label `ext-review`, parses their structured body, and
writes/updates `data/derived/extension_labels.csv` with:

| Column | Source |
|---|---|
| `ext` | the extension being labelled |
| `label` | from the vocabulary above |
| `annotator` | GitHub login of the issue author |
| `submitted_at` | ISO timestamp of the issue |
| `evidence` | free-text + URLs from the issue body |
| `issue_url` | link to the issue (for re-reading the discussion) |
| `confirmed_by` | maintainer who reviewed/accepted (added by curator) |

From that CSV, two things happen:

- Labels starting with `pl/` (existing PL id) are inserted into
  `ext_claim.csv` with `source="manual_review:<annotator>"`,
  `strength="proposed"`, `evidence="<issue_url>"`. Maintainers can later
  promote to `strength="primary"` after a content-classifier confirmation.
- Labels starting with `pl/new:` propose a *new* PL entity. These are batched
  into a maintainer review queue (issue) before being added to `pl.csv`.
- Non-`pl/` labels (binary/data/etc.) update the extension's row directly so
  that the site renders the label and (optionally) hides the extension from
  PL-resolution pipelines.

## Rules

- **One label per (ext, annotator).** Multiple labels per extension are
  allowed (different annotators), and the curator resolves disagreements by
  opening a comment thread on the issue.
- **Evidence required.** Empty `evidence` field → curator rejects the
  submission.
- **Use existing pl_ids when possible.** `pl/new:` is for cases where no
  reasonable existing entity exists.
- **No private data in `evidence`.** Issues are public; treat them as such.

## Vocabulary updates

To propose a new label, open an issue titled `Label proposal: <new-label>`
with the justification and a few example extensions. New labels added here
become valid for review.
