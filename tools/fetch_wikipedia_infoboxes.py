#!/usr/bin/env python3
"""Enrich Wikidata extension records with Wikipedia infobox data via live MW API.

For each Wikidata item with an enwiki sitelink, fetch the article wikitext,
look for any `{{Infobox …}}` template, and extract candidate file-extension
fields. The value is normalized: `<br/>` becomes a newline, references are
stripped, then we split per-line into `(extension, note)`.

Reproducibility model: the live MediaWiki API is used as a refresh
mechanism — its output is captured into a per-title wikitext cache under
`.cache/wikipedia_pages/` and into the pinned JSONL under `data/raw/`.
Once committed, the JSONL defines the truth for the downstream build until
the next intentional refresh. This mirrors how `data/raw/linguist_languages.yml`
is pinned in this repo.

Output: data/raw/wikipedia_infobox.<YYYY-MM-DD>.jsonl  (one record per page)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import mwparserfromhell  # type: ignore

UA = "PL-ext-explorer/0.1 (https://github.com/acherm/PL-ultimate; mathieu.acher@irisa.fr)"
MWAPI = "https://en.wikipedia.org/w/api.php"
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
CACHE_DIR = ROOT / ".cache" / "wikipedia_pages"

# Heuristic field-name whitelist. Any infobox parameter whose normalized name
# matches one of these is treated as a "filename extension" field. We collapse
# runs of `[\s_\-]+` to a single underscore before matching, so `file ext`,
# `file_ext`, and `file-ext` all reach the same regex.
EXT_FIELD_PAT = re.compile(
    r"^(file_?ext(ension)?s?|extensions?|filename_?ext(ension)?s?|suffix(es)?)$",
    re.IGNORECASE,
)


def normalize_field_name(name: str) -> str:
    return re.sub(r"[\s_\-]+", "_", name.strip().lower())

# Infobox templates we definitely care about — others (Infobox software,
# Infobox album, …) may still incidentally carry an extension field, so we
# do not hard-filter the template name; we record it.
EXPECTED_INFOBOXES = re.compile(
    r"^infobox\s+(file format|programming language|markup language|software|"
    r"file system|character encoding|graphics file format)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# HTTP / MediaWiki API
# ---------------------------------------------------------------------------

def http_get(params: dict) -> dict:
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{MWAPI}?{qs}",
        headers={"Accept": "application/json", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fetch_wikitext_batch(titles: list[str]) -> dict[str, str | None]:
    """Return {requested_title: wikitext or None}. Follows redirects.

    The MW API may canonicalize titles (spaces/underscores) and resolve
    redirects; we map every requested title back to the page we actually got.
    """
    if not titles:
        return {}
    res = http_get({
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "titles": "|".join(titles),
        "redirects": 1,
        "format": "json",
        "formatversion": 2,
    })

    # Build canonical-title → wikitext.
    canon_to_text: dict[str, str | None] = {}
    for page in res.get("query", {}).get("pages", []):
        title = page.get("title")
        if "missing" in page or not title:
            continue
        revs = page.get("revisions") or []
        if not revs:
            continue
        content = revs[0].get("slots", {}).get("main", {}).get("content")
        canon_to_text[title] = content

    # Replay redirect/normalization tables so requesters see their input title.
    requested_to_canon: dict[str, str] = {t: t for t in titles}
    for n in res.get("query", {}).get("normalized", []) or []:
        requested_to_canon[n["from"]] = n["to"]
    for r in res.get("query", {}).get("redirects", []) or []:
        for k, v in requested_to_canon.items():
            if v == r["from"]:
                requested_to_canon[k] = r["to"]

    return {req: canon_to_text.get(canon) for req, canon in requested_to_canon.items()}


def cached_or_fetch(titles: list[str], batch_size: int = 30, sleep: float = 0.5) -> dict[str, str | None]:
    """Fetch wikitext for `titles`, using on-disk JSON cache per title."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, str | None] = {}
    todo: list[str] = []
    for t in titles:
        cf = CACHE_DIR / f"{safe_filename(t)}.json"
        if cf.exists():
            try:
                out[t] = json.loads(cf.read_text()).get("wikitext")
                continue
            except Exception:
                pass
        todo.append(t)

    print(f"[mw]   cache hit: {len(out)}  miss: {len(todo)}", flush=True)
    for i in range(0, len(todo), batch_size):
        chunk = todo[i : i + batch_size]
        try:
            got = fetch_wikitext_batch(chunk)
        except Exception as e:
            print(f"       batch error: {e!r} — sleeping 5s and retrying once", flush=True)
            time.sleep(5)
            got = fetch_wikitext_batch(chunk)
        for t in chunk:
            wt = got.get(t)
            out[t] = wt
            cf = CACHE_DIR / f"{safe_filename(t)}.json"
            cf.write_text(json.dumps({"title": t, "wikitext": wt, "fetched_at": dt.datetime.utcnow().isoformat() + "Z"}, ensure_ascii=False))
        if (i // batch_size) % 5 == 0:
            print(f"       fetched {min(i + batch_size, len(todo))}/{len(todo)}", flush=True)
        time.sleep(sleep)
    return out


def safe_filename(title: str) -> str:
    s = title.replace("/", "_")
    return re.sub(r"[^\w\-. ]", "_", s)[:200]


# ---------------------------------------------------------------------------
# Infobox extraction
# ---------------------------------------------------------------------------

def normalize_value(raw: str) -> str:
    """Replace <br/> with newlines and strip <ref>…</ref> footnotes."""
    # <br>, <br/>, <br /> in any case → newline
    s = re.sub(r"<\s*br\s*/?\s*>", "\n", raw, flags=re.IGNORECASE)
    # strip ref tags (paired and self-closing)
    s = re.sub(r"<ref\b[^/]*?/\s*>", "", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<ref\b.*?</\s*ref\s*>", "", s, flags=re.IGNORECASE | re.DOTALL)
    # HTML comments
    s = re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)
    return s


# Display/formatting templates that wrap their first positional arg as the
# visible text. We unwrap them so strip_code() does not discard the extension
# token. e.g. {{code|.mp3}} → .mp3
DISPLAY_TEMPLATES = {
    "code", "mono", "tt", "kbd", "samp", "var", "nowrap", "nobr",
    "small", "big", "smaller", "larger", "font", "color", "fontcolor",
    "smallcaps", "sc", "no wrap",
}


def unwrap_display_templates(code) -> None:
    """In-place: replace {{code|X}} (and friends) with the literal X."""
    for _ in range(3):  # a couple of passes for nesting
        changed = False
        for tmpl in list(code.filter_templates()):
            name = str(tmpl.name).strip().lower()
            if name not in DISPLAY_TEMPLATES or not tmpl.params:
                continue
            try:
                code.replace(tmpl, str(tmpl.params[0].value))
                changed = True
            except ValueError:
                pass  # node already removed by a prior replacement
        if not changed:
            break


# extension token: optional leading dot, letters/digits/+/-, 1..20 chars
EXT_TOKEN = re.compile(r"^\.?([A-Za-z0-9][A-Za-z0-9+\-_]{0,19})\b\s*(.*)$")


def parse_ext_field(raw_value: str) -> list[dict]:
    """Parse an infobox extension-field value into [{value, note, raw_line}]."""
    norm = normalize_value(raw_value)
    code = mwparserfromhell.parse(norm)
    unwrap_display_templates(code)
    plain = code.strip_code(normalize=True, collapse=False)

    out: list[dict] = []
    seen: set[str] = set()
    # Split on newlines, semicolons, AND commas. Some infoboxes inline-list
    # extensions: ".mpeg, .mpg, .mpe, .mp1, .mp2, .mp3" (MPEG-1).
    for raw_line in re.split(r"[\n;,]+", plain):
        line = raw_line.strip()
        # Strip leading bullet/list markers and quotes
        line = re.sub(r"^[\*\-•\s,]+", "", line)
        line = line.strip()
        if not line:
            continue
        m = EXT_TOKEN.match(line)
        if not m:
            continue
        ext = m.group(1).lower()
        note = m.group(2).strip()
        # Strip wrapping parens on a leading parenthetical note
        note = note.strip(" ,.;").lstrip("(").rstrip(")").strip()
        if ext in seen:
            continue
        seen.add(ext)
        out.append({"value": ext, "note": note or None, "raw_line": raw_line.strip()})
    return out


def find_infobox_extensions(wikitext: str) -> list[dict]:
    """Return a list of {template, field, parsed: [...]} entries."""
    if not wikitext:
        return []
    code = mwparserfromhell.parse(wikitext)
    out: list[dict] = []
    for tmpl in code.filter_templates():
        name = str(tmpl.name).strip()
        if not name.lower().startswith("infobox"):
            continue
        for param in tmpl.params:
            pname = normalize_field_name(str(param.name))
            if not EXT_FIELD_PAT.match(pname):
                continue
            raw = str(param.value)
            parsed = parse_ext_field(raw)
            if not parsed:
                continue
            out.append({
                "template": name,
                "template_known": bool(EXPECTED_INFOBOXES.match(name)),
                "field": pname,
                "raw": raw.strip(),
                "parsed": parsed,
            })
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def load_enwiki_items(jsonl_path: Path) -> list[dict]:
    items = []
    with jsonl_path.open() as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("enwiki_title"):
                items.append(rec)
    return items


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="wikidata_p1195.<date>.jsonl path")
    p.add_argument("--limit", type=int, default=None, help="Only process N items (smoke test)")
    p.add_argument("--titles", nargs="*", help="Specific titles to process (smoke test)")
    p.add_argument("--out-suffix", default="", help="Optional suffix for output filename")
    args = p.parse_args()

    in_path = Path(args.input)
    items = load_enwiki_items(in_path)
    print(f"[load] {len(items)} items have enwiki_title", flush=True)

    if args.titles:
        wanted = {t for t in args.titles}
        items = [i for i in items if i["enwiki_title"] in wanted]
        print(f"       filtered to {len(items)} by --titles", flush=True)
    if args.limit:
        items = items[: args.limit]
        print(f"       capped to {len(items)} by --limit", flush=True)

    titles = [it["enwiki_title"] for it in items]
    wt_map = cached_or_fetch(titles)

    today = dt.date.today().isoformat()
    suffix = f".{args.out_suffix}" if args.out_suffix else ""
    out_path = DATA_DIR / f"wikipedia_infobox.{today}{suffix}.jsonl"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    n_with_box = 0
    n_extra = 0
    with out_path.open("w") as f:
        for it in items:
            t = it["enwiki_title"]
            wt = wt_map.get(t)
            boxes = find_infobox_extensions(wt) if wt else []

            wd_exts = {e["value"].lower() for e in it.get("extensions", [])}
            wp_exts = {p["value"] for b in boxes for p in b["parsed"]}
            extra = sorted(wp_exts - wd_exts)
            missing = sorted(wd_exts - wp_exts)

            rec = {
                "qid": it["qid"],
                "label": it["label"],
                "enwiki_title": t,
                "had_wikitext": wt is not None,
                "infobox_hits": boxes,
                "wikidata_extensions": sorted(wd_exts),
                "wikipedia_extensions": sorted(wp_exts),
                "wikipedia_extra": extra,
                "wikipedia_missing": missing,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if boxes:
                n_with_box += 1
            if extra:
                n_extra += 1

    print(f"[done] wrote {out_path}", flush=True)
    print(f"       items processed:       {len(items)}", flush=True)
    print(f"       with ≥1 infobox match: {n_with_box}", flush=True)
    print(f"       Wikipedia adds extras: {n_extra}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
