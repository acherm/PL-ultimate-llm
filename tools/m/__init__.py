"""`.m` extension study — fourth application of the extension-study playbook
(after `.cbl`/`.CBL`, `.fsf`, `.rpgle`), and the first on a *massively
polysemous* extension: MATLAB, GNU Octave, Objective-C, Mathematica/Wolfram,
Mercury, MUMPS (M), Limbo, MUF and Mason all claim `.m`.

Reuses tools.cobol for SWH fetch/cache + OpenRouter plumbing. The population
file is 14 GB, so ingest goes through DuckDB into a Parquet table
(`tools/m/ingest.py`, run with `.venv/bin/python`); everything downstream of
the Parquet is stdlib.
"""
