# Static website (browse PLs + programs)

This folder contains a tiny **static site generator** that turns the repository data:

- `languages/**/meta.json`
- `languages/**/programs/*/{manifest.json,<code file>}`

into a browsable website (search, browse by letter, per-language pages, stats).

## Build

From the repo root:

```bash
python3 web/build_site.py
```

Output goes to `web/dist/`.

### With audit report

To also generate `web/dist/data/audit.json` (duplicates/integrity checks/clustering hints):

```bash
python3 web/build_site.py --with-audit
```

The audit view is available at `web/dist/audit/index.html` and loads `data/audit.json` on demand.

## Preview locally

```bash
python3 -m http.server --directory web/dist 8000
```

Then open `http://localhost:8000`.

## Notes

- The generator is **dependency-free** (standard library only).
- It avoids rendering all languages at once: the Browse view requires picking a letter or searching.
- Slugs include a short hash to avoid collisions (`C`, `C#`, `C--`, …).
- “Indexed languages” means “folders with a readable `meta.json` somewhere under `languages/`”. Some languages are nested (e.g., `languages/PL/0/meta.json`), and some top-level folders may be group folders or missing metadata.
- Agent/LLM statistics come from git commit trailers on `turn: add …` commits (e.g., `Model:`, `Agent:`, `Temperature:`, `WebSearch:`). Missing trailers show up as `Unknown`.
