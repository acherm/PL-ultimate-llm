# Sample-mining requests

Per-extension pages let any visitor request that the maintainer run a
**targeted SWH mining pass** for a specific extension. Useful when an
extension has zero archived examples on the site (e.g. `.mjava`) and
the visitor needs verbatim bytes to decide what the extension is or
which PL claims it.

The flow is symmetric to the `ext-review` labelling pipeline:

1. **Reviewer** clicks "Request SWH samples" on `/ext/<x>/`.
2. A pre-filled GitHub issue opens with the `sample-request` label and a
   structured YAML block (ext + optional notes).
3. **Maintainer** runs `python3 tools/process_sample_requests.py` on demand.
   The script:
   - lists open issues with the `sample-request` label,
   - parses each YAML block for `ext`,
   - writes a temporary target file,
   - invokes `swh_extension_mining.py` against the SWH parquet datasets,
   - runs `fetch_samples.py` to materialize verbatim bytes under
     `samples/unclassified/<sha>/`,
   - counts samples per extension, comments on each issue, and closes
     issues whose extension landed at least one sample.
4. **Site rebuild** (next push or chained workflow) surfaces the new
   bytes on `/ext/<x>/index.html#samples`.

## Issue body schema

```yaml
ext: ".mjava"
notes: |
  Looking for examples to disambiguate from .java — is this a Modular
  Java dialect or just modified Java?
```

`notes` is optional (the form sends `(no notes)` if empty). The structured
block is recognised by `tools/process_sample_requests.py`; free-text
discussion in the rest of the issue body is preserved on close.

## Operator commands

```
# Dry-run — just show what would happen.
python3 tools/process_sample_requests.py --dry-run

# Real run — mine, materialize, comment, close issues that got samples.
python3 tools/process_sample_requests.py

# Run but don't close issues (e.g. exploratory pass).
python3 tools/process_sample_requests.py --no-close

# Wider candidate window (default 5) — slower but better hit rate.
python3 tools/process_sample_requests.py --qualify-max-candidates 10
```

The mining step talks to the SWH parquet datasets in `s3://softwareheritage/derived_datasets/<DATE>/contents/*.parquet` via DuckDB + httpfs. Expect 10-30 min per
run because the duckdb scan touches every shard; the per-extension count
doesn't change the scan cost meaningfully.

## Rules

- **One label**: only `sample-request`. Issues without this label are
  ignored.
- **Comment on every processed issue**, even those that yielded zero
  samples (kept open for retry).
- **Don't bulk-close manually closed issues**: the script only touches
  issues that were `open` at fetch time.

## Why issues, not a CSV file?

Same rationale as `ext-review`: anyone with a GitHub account can request
samples without needing local clone access, the request carries a
preserved audit trail (who, when, why), and the resolution shows up
next to the discussion. The pipeline is fully reproducible from the
issue's structured block.
