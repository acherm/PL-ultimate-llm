# Standalone contributor CLI — roadmap

Vision and deferred work for a terminal-first way to "fill the site's
forms". Nothing here is committed work except where a seed tool already
exists — it's a queue of "worth-building-eventually", in the spirit of
[`taxonomy_future_work.md`](taxonomy_future_work.md).

## Trigger

Submitting the mystery `.m` file from Xorg
(`swh:1:cnt:f851a314d7b2dfc8949028f3671dba8f268ac4ee`,
`XSetModifierMapping.m` — an xts5/VSW5 TET test-case source, not
MATLAB/Objective-C/Mercury) revealed a gap: every submission flow on the
site is a *web form that opens a GitHub issue*, and the only
sample-related form requests mining **per extension**
([`sample_requests.md`](sample_requests.md)). There was no form, CLI, or
documented process to submit **one specific program file** with a given
extension. The addition had to be done by hand: verify the `sha1_git`,
reconstruct provenance via a bare clone + `git log --find-object`, check
`/api/1/known/`, and hand-write `metadata.json`.

## Vision

One standalone CLI mirroring every web form, so a contributor with a
clone (or just `gh`) can do everything from the terminal. Two modes per
form:

- **local-first** — write the files the form's processor would have
  produced (no issue, no round-trip); for maintainers and PR authors.
- **issue mode** — emit the *same structured YAML block* the web form
  posts, via `gh issue create`; for contributors without a clone. The
  existing processors (`process_sample_requests.py`,
  `process_pl_contribute.py`, `process_extension_labels.py`) stay the
  single source of truth for what each block means.

Use-cases to cover (one subcommand each):

| Use-case | Web form today | CLI status |
|---|---|---|
| Submit a specific program file w/ extension (SWHID and/or local bytes) | **none** (the gap) | ✅ seed: `tools/submit_sample.py` |
| Request per-extension SWH mining | `/ext/<x>/` → `sample-request` issue | TODO (`gh issue create` wrapper) |
| Label / review an extension | `/ext/<x>/` → ext-review flow | TODO |
| Claim an ext / attach a program to a PL | `/l/<slug>/` → `pl-contribute` issue | TODO |
| Propose a new PL | agent flow (`CLAUDE.md`) / `tools/contribute.py` | partial (`contribute.py`, no form UX) |

Sketch: a single entry point (e.g. `tools/plcli.py` or a `pl` console
script) with subcommands `sample submit`, `sample request`, `ext review`,
`pl contribute`, `pl new`; `--form` everywhere for field-by-field
prompting; shared helpers for SWH verification (`/api/1/known/`, origin
lookup, raw fetch) extracted from `submit_sample.py` /
`verify_swh_samples.py`.

## Seed: `tools/submit_sample.py`

Covers the first use-case end to end:

```bash
# Local bytes, ext inferred, lands in samples/unclassified/
python3 tools/submit_sample.py --file ~/Downloads/XSetModifierMapping.m

# No local bytes — fetch from SWH by content SWHID
python3 tools/submit_sample.py --swhid swh:1:cnt:f851a314… --filename XSetModifierMapping.m

# Full provenance → qualified SWHID (strong citation)
python3 tools/submit_sample.py --file X.m \
    --origin https://gitlab.freedesktop.org/xorg/test/xts \
    --anchor 497a0865… --path /xts5/tset/Xlib13/XSetModifierMapping/XSetModifierMapping.m

# Interactive form
python3 tools/submit_sample.py --form
```

Guarantees: `sha1_git` always computed from the real bytes (a provided
SWHID must match); content existence checked against SWH `/api/1/known/`
(refused if unknown, unless `--allow-unarchived`); origin/anchor checked
too, degrading to a warning per the aspirational-provenance policy
([`samples_aspirational_provenance.md`](samples_aspirational_provenance.md));
output is the exact `samples/<slot>/<sha1_git>/{file,metadata.json}`
layout that `web/build_site.py` and `tools/verify_swh_samples.py` walk.

## Open questions

- **Provenance discovery.** For the `.m` case the anchor commit had to be
  found by cloning the origin and running `git log --find-object=<blob>`.
  That's mechanical — `submit_sample.py` could grow a
  `--discover-provenance <git-url>` flag doing exactly that (bare clone to
  a temp dir, find first commit containing the blob + its path, clean up).
- **Issue mode parity.** Should `sample submit` also have an issue mode
  (a `sample-submit` label + YAML with `swhid`/`filename`/provenance) so
  clone-less visitors can point at a specific file? The processor would
  be ~30 lines on top of `submit_sample.py`.
- **Where the CLI lives.** Separate `tools/plcli.py` vs growing
  subcommands on `contribute.py`. Leaning separate: `contribute.py` is
  wired to the `languages/` collection and its schema, not `samples/`.
