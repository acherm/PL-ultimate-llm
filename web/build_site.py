#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.util import canonical_name, slugify  # noqa: E402

LANGUAGES_DIR = ROOT / "languages"


@dataclass(frozen=True)
class Program:
    sha256: str
    title: str
    origin_url: str
    license_guess: str | None
    added_at: str
    code_source_path: Path | None
    code_bytes: bytes | None
    code_text: str | None
    code_out_name: str | None


@dataclass(frozen=True)
class Language:
    name: str
    aliases: list[str]
    evidence_url: str
    added_at: str
    folder_rel: str
    slug: str
    programs: list[Program]
    # Provenance from git commit trailers (best-effort).
    turn_commit: str | None
    turn_authored_at: str | None
    agent: str | None
    model: str | None
    temperature: float | None
    web_search: str | None


@dataclass(frozen=True)
class TurnInfo:
    commit: str
    authored_at: str
    language: str
    trailers: dict[str, str]


def parse_iso8601(s: str) -> datetime | None:
    if not s:
        return None
    s = s.strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


TURN_PREFIX = "turn: add "
TURN_SUFFIX = " (+1 program)"
TRAILER_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")


def parse_trailers(message_body: str) -> dict[str, str]:
    trailers: dict[str, str] = {}
    for raw_line in (message_body or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = TRAILER_RE.match(line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        trailers[key] = value
    return trailers


def parse_temperature(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.strip())
    except Exception:
        return None


def normalize_web_search(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip().lower()
    if v in {"enabled", "true", "yes", "1", "on"}:
        return "enabled"
    if v in {"disabled", "false", "no", "0", "off"}:
        return "disabled"
    return value.strip()


def read_turns_from_git() -> list[TurnInfo]:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        return []
    try:
        proc = subprocess.run(
            ["git", "--no-pager", "log", "--pretty=format:%H%x1f%aI%x1f%s%x1f%b%x1e"],
            cwd=str(ROOT),
            check=True,
            text=True,
            capture_output=True,
        )
    except Exception:
        return []

    turns: list[TurnInfo] = []
    for record in proc.stdout.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 4:
            continue
        commit, authored_at, subject, body = parts[0], parts[1], parts[2], parts[3]
        if not (subject.startswith(TURN_PREFIX) and subject.endswith(TURN_SUFFIX)):
            continue
        lang_raw = subject[len(TURN_PREFIX) : -len(TURN_SUFFIX)]
        lang = canonical_name(lang_raw)
        trailers = parse_trailers(body)
        turns.append(TurnInfo(commit=commit, authored_at=authored_at, language=lang, trailers=trailers))

    return turns


def index_turns_by_language(turns: list[TurnInfo]) -> dict[str, TurnInfo]:
    # git log returns newest-first; we want first (oldest) per language if duplicates exist.
    by_lang: dict[str, TurnInfo] = {}
    for turn in reversed(turns):
        key = canonical_name(turn.language).lower()
        if key not in by_lang:
            by_lang[key] = turn
    return by_lang


def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def make_lang_slug(name: str) -> str:
    base = slugify(name) or "lang"
    return f"{base}-{short_hash(name)}"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_lossy(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def find_program_code_file(program_dir: Path) -> Path | None:
    if not program_dir.is_dir():
        return None
    candidates = [p for p in program_dir.iterdir() if p.is_file() and p.name != "manifest.json"]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    codeish = [p for p in candidates if p.name.startswith("code")]
    if len(codeish) == 1:
        return codeish[0]
    return sorted(candidates, key=lambda p: (0 if p.name.startswith("code") else 1, len(p.name), p.name))[0]


def derive_code_out_name(code_source_name: str) -> str:
    # Normalize historical variants:
    # - code.abap      -> code.abap
    # - codepy         -> code.py
    # - coders         -> code.rs
    # - <other file>   -> <other file>
    if "." in code_source_name:
        return code_source_name
    if code_source_name.startswith("code") and len(code_source_name) > 4:
        ext = code_source_name[4:]
        ext = "".join(ch for ch in ext if ch.isalnum() or ch in ("+", "-", "_"))
        if not ext:
            return "code.txt"
        return f"code.{ext}"
    return code_source_name


def rel_prefix(page: Path, dist_root: Path) -> str:
    rel = page.parent.relative_to(dist_root)
    return "../" * len(rel.parts)


def layout(*, title: str, rel: str, body: str, generated_at: str, description: str = "") -> str:
    safe_title = html.escape(title)
    safe_desc = html.escape(description or "Browse programming languages and their example programs.")
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <meta name="description" content="{safe_desc}" />
    <link rel="stylesheet" href="{rel}assets/style.css" />
    <script>
      window.__SITE_ROOT__ = {json.dumps(rel)};
      window.__DATA_BASE__ = {json.dumps(rel + "data")};
    </script>
    <script src="{rel}assets/app.js" defer></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container header-inner">
        <a class="brand" href="{rel}index.html">PL Catalog</a>
        <nav class="nav">
          <a href="{rel}browse/index.html">Browse</a>
          <a href="{rel}stats/index.html">Stats</a>
          <button id="randomBtn" class="nav-btn" type="button">Random</button>
        </nav>
      </div>
    </header>
    <main class="container">
      {body}
    </main>
    <footer class="site-footer">
      <div class="container">
        Generated at <span class="muted">{html.escape(generated_at)}</span> from this repository.
      </div>
    </footer>
  </body>
</html>
"""


def letter_counts(languages: list[Language]) -> dict[str, int]:
    counts: dict[str, int] = {chr(c): 0 for c in range(ord("A"), ord("Z") + 1)}
    for lang in languages:
        if not lang.name:
            continue
        ch = lang.name[0].upper()
        if ch in counts:
            counts[ch] += 1
    return counts


def first_letter(name: str) -> str:
    if not name:
        return ""
    ch = name[0].upper()
    return ch if "A" <= ch <= "Z" else "#"


def render_letter_grid(*, rel: str, counts: dict[str, int]) -> str:
    tiles = []
    for letter in sorted(counts.keys()):
        c = counts[letter]
        tiles.append(
            f'<a href="{rel}browse/index.html?letter={letter}" data-letter="{letter}">{letter}<span>{c}</span></a>'
        )
    return f'<div class="letter-grid" id="browseLetters">{"".join(tiles)}</div>'


def safe(s: str) -> str:
    return html.escape(s or "")


def render_home_page(
    *,
    dist_root: Path,
    languages: list[Language],
    counts: dict[str, int],
    generated_at: str,
    programs_total: int,
) -> None:
    page = dist_root / "index.html"
    rel = rel_prefix(page, dist_root)

    newest = sorted(
        languages,
        key=lambda l: parse_iso8601(l.added_at) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:12]

    recent_items = "\n".join(
        f'<li><a href="{rel}l/{lang.slug}/">{safe(lang.name)}</a><span class="muted">{safe(lang.added_at)}</span></li>'
        for lang in newest
    )

    stats_html = f"""
    <div class="stats">
      <div class="stat"><div class="num">{len(languages)}</div><div class="muted">languages</div></div>
      <div class="stat"><div class="num">{programs_total}</div><div class="muted">programs</div></div>
      <div class="stat"><div class="num">{generated_at.split('T')[0]}</div><div class="muted">last build (UTC)</div></div>
    </div>
    """

    body = f"""
    <section class="panel hero">
      <h1>Programming languages + example programs</h1>
      <p>Browse the repository without dumping everything on one page.</p>
      {stats_html}
      <div class="search-box" style="margin-top:14px;">
        <input id="homeSearch" type="search" placeholder="Search (e.g., Haskell, C#, Prolog, ML/I…)" autocomplete="off" />
        <div id="homeResults" style="margin-top:10px;"></div>
      </div>
    </section>

    <div class="grid" style="margin-top:18px;">
      <section class="panel section">
        <h2>Browse by letter</h2>
        <p class="muted" style="margin: 0 0 12px;">Pick a letter to jump into a manageable list.</p>
        {render_letter_grid(rel=rel, counts=counts)}
      </section>
      <section class="panel section">
        <h2>Recently added</h2>
        <ul class="recent">
          {recent_items}
        </ul>
      </section>
    </div>
    """

    page.write_text(
        layout(
            title="PL Catalog",
            rel=rel,
            body=body,
            generated_at=generated_at,
            description="Browse programming languages with example programs.",
        ),
        encoding="utf-8",
    )


def render_browse_page(*, dist_root: Path, languages: list[Language], counts: dict[str, int], generated_at: str) -> None:
    page = dist_root / "browse" / "index.html"
    rel = rel_prefix(page, dist_root)
    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Browse</h1>
      <p class="muted" style="margin:0 0 14px;">Pick a letter or search. Results are paged (no 800+ item dump).</p>
      <div class="search-box" style="margin-bottom: 14px;">
        <input id="browseSearch" type="search" placeholder="Search languages or aliases…" autocomplete="off" />
      </div>
      {render_letter_grid(rel=rel, counts=counts)}
      <div id="browseSummary" class="muted" style="margin-top: 12px;"></div>
      <div id="browseResults" style="margin-top: 10px;"></div>
      <button id="browseMore" class="btn" type="button" style="margin-top: 12px;" hidden>Load more</button>
      <noscript>
        <p class="muted" style="margin-top: 12px;">This page uses a small amount of JavaScript for search/paging.</p>
      </noscript>
    </section>
    """
    page.write_text(layout(title="Browse · PL Catalog", rel=rel, body=body, generated_at=generated_at), encoding="utf-8")


def render_stats_page(
    *,
    dist_root: Path,
    languages: list[Language],
    counts: dict[str, int],
    programs_total: int,
    generated_at: str,
    top_domains: list[tuple[str, int]],
    top_licenses: list[tuple[str, int]],
    top_exts: list[tuple[str, int]],
    langs_added_by_day: list[tuple[str, int]],
    turns_total: int,
    unique_agents: int,
    unique_models: int,
    top_agents: list[tuple[str, int]],
    top_models: list[tuple[str, int]],
    web_search_counts: list[tuple[str, int]],
    temps_count: int,
    temps_min: float | None,
    temps_max: float | None,
    temps_avg: float | None,
    temp_buckets: list[tuple[str, int]],
) -> None:
    page = dist_root / "stats" / "index.html"
    rel = rel_prefix(page, dist_root)

    max_letter = max(counts.values()) if counts else 1
    letter_rows = "\n".join(
        f'<li class="bar-row"><div class="muted">{letter}</div><div class="bar" style="--w:{(counts[letter]/max_letter)*100:.1f}%"><div></div></div><div class="muted" style="text-align:right;">{counts[letter]}</div></li>'
        for letter in sorted(counts.keys())
        if counts[letter] > 0
    )

    def bar_rows(items: list[tuple[str, int]]) -> str:
        maxv = max((c for _, c in items), default=1)
        return "\n".join(
            f'<li class="bar-row"><div class="muted">{safe(label)}</div><div class="bar" style="--w:{(count/maxv)*100:.1f}%"><div></div></div><div class="muted" style="text-align:right;">{count}</div></li>'
            for label, count in items
        )

    last_30_days = langs_added_by_day[-30:] if len(langs_added_by_day) > 30 else langs_added_by_day

    if turns_total > 0:
        if temps_count > 0 and temps_min is not None and temps_max is not None and temps_avg is not None:
            temp_summary = f"{temps_count} commits include Temperature · avg {temps_avg:.2f} (min {temps_min:.2f}, max {temps_max:.2f})"
            temp_bucket_html = f"<ul class='bar-list'>{bar_rows(temp_buckets)}</ul>" if temp_buckets else "<div class='muted'>No temperature buckets.</div>"
        else:
            temp_summary = "No Temperature trailers found."
            temp_bucket_html = "<div class='muted'>—</div>"

        llm_section = f"""
        <section class="panel section" style="margin-top: 18px;">
          <h2>Agents &amp; LLMs</h2>
          <p class="muted" style="margin:0 0 14px;">Derived from git commit trailers in <code>turn: add …</code> commits.</p>
          <div class="stats">
            <div class="stat"><div class="num">{turns_total}</div><div class="muted">turn commits</div></div>
            <div class="stat"><div class="num">{unique_agents}</div><div class="muted">agents</div></div>
            <div class="stat"><div class="num">{unique_models}</div><div class="muted">models</div></div>
          </div>
        </section>

        <div class="grid" style="margin-top: 18px;">
          <section class="panel section">
            <h2>Top agents</h2>
            <ul class="bar-list">{bar_rows(top_agents)}</ul>
          </section>
          <section class="panel section">
            <h2>Top models</h2>
            <ul class="bar-list">{bar_rows(top_models)}</ul>
          </section>
        </div>

        <div class="grid" style="margin-top: 18px;">
          <section class="panel section">
            <h2>WebSearch usage</h2>
            <ul class="bar-list">{bar_rows(web_search_counts)}</ul>
          </section>
          <section class="panel section">
            <h2>Temperature (where recorded)</h2>
            <p class="muted" style="margin:0 0 10px;">{safe(temp_summary)}</p>
            {temp_bucket_html}
          </section>
        </div>
        """
    else:
        llm_section = """
        <section class="panel section" style="margin-top: 18px;">
          <h2>Agents &amp; LLMs</h2>
          <p class="muted" style="margin:0;">Git history not available; cannot compute agent/model statistics.</p>
        </section>
        """

    body = f"""
    <section class="panel section">
      <h1 style="margin:0 0 8px;">Statistics</h1>
      <p class="muted" style="margin:0 0 14px;">Quick aggregates computed from `languages/**/meta.json` and program manifests.</p>

      <div class="stats">
        <div class="stat"><div class="num">{len(languages)}</div><div class="muted">languages</div></div>
        <div class="stat"><div class="num">{programs_total}</div><div class="muted">programs</div></div>
        <div class="stat"><div class="num">{(programs_total / max(1, len(languages))):.2f}</div><div class="muted">avg programs / language</div></div>
      </div>
    </section>

    {llm_section}

    <section class="panel section">
      <h2>Languages by first letter</h2>
      <ul class="bar-list">{letter_rows}</ul>
    </section>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Top origin domains</h2>
        <ul class="bar-list">{bar_rows(top_domains)}</ul>
      </section>
      <section class="panel section">
        <h2>Top license guesses</h2>
        <ul class="bar-list">{bar_rows(top_licenses)}</ul>
      </section>
    </div>

    <div class="grid" style="margin-top: 18px;">
      <section class="panel section">
        <h2>Top code file extensions</h2>
        <ul class="bar-list">{bar_rows([(f'.{e}' if e and e != 'unknown' else e, c) for e, c in top_exts])}</ul>
      </section>
      <section class="panel section">
        <h2>Languages added (last 30 days)</h2>
        <ul class="bar-list">{bar_rows(last_30_days)}</ul>
      </section>
    </div>
    """

    page.write_text(layout(title="Stats · PL Catalog", rel=rel, body=body, generated_at=generated_at), encoding="utf-8")


def render_language_pages(
    *,
    dist_root: Path,
    languages: list[Language],
    generated_at: str,
    slug_to_prev_next: dict[str, tuple[Language | None, Language | None]],
) -> None:
    for lang in languages:
        page = dist_root / "l" / lang.slug / "index.html"
        rel = rel_prefix(page, dist_root)

        alias_html = (
            f"<div class='muted'>Aliases: {safe(', '.join(lang.aliases))}</div>" if lang.aliases else "<div class='muted'>Aliases: —</div>"
        )
        prov_pills: list[str] = []
        if lang.agent:
            prov_pills.append(f"<span class='pill'>Agent: {safe(lang.agent)}</span>")
        if lang.model:
            prov_pills.append(f"<span class='pill'>Model: {safe(lang.model)}</span>")
        if lang.temperature is not None:
            prov_pills.append(f"<span class='pill'>Temp: {lang.temperature:g}</span>")
        if lang.web_search:
            prov_pills.append(f"<span class='pill'>WebSearch: {safe(lang.web_search)}</span>")

        prov_bits: list[str] = []
        if lang.turn_commit:
            prov_bits.append(f"commit {lang.turn_commit[:10]}")
        if lang.turn_authored_at:
            prov_bits.append(f"authored {lang.turn_authored_at}")
        prov_line = f"<div class='muted'>Provenance: {safe(' · '.join(prov_bits))}</div>" if prov_bits else ""

        programs_html = []
        if not lang.programs:
            programs_html.append("<p class='muted'>No programs recorded for this language yet.</p>")
        else:
            for idx, prog in enumerate(lang.programs):
                code_id = f"code-{idx}"
                manifest_link = f"{rel}code/{prog.sha256}/manifest.json"
                download_link = f"{rel}code/{prog.sha256}/{safe(prog.code_out_name or 'code.txt')}" if prog.code_out_name else ""

                links = [f"<a href='{safe(prog.origin_url)}' target='_blank' rel='noopener'>Origin</a>"]
                if prog.code_out_name:
                    links.append(f"<a href='{download_link}' download>Download</a>")
                links.append(f"<a href='{manifest_link}'>manifest.json</a>")
                links_html = " · ".join(links)

                meta_bits = []
                if prog.license_guess:
                    meta_bits.append(f"license: {safe(prog.license_guess)}")
                meta_bits.append(f"added: {safe(prog.added_at)}")
                meta_str = " · ".join(meta_bits)

                code_block = ""
                if prog.code_text is not None:
                    code_block = f"""
                    <div class="codeblock" style="margin-top: 10px;">
                      <div class="codebar">
                        <div class="meta">{safe(prog.code_out_name or '')} · {meta_str}</div>
                        <button class="btn copy-btn" type="button" data-copy-target="#{code_id}">Copy</button>
                      </div>
                      <pre><code id="{code_id}">{safe(prog.code_text)}</code></pre>
                    </div>
                    """
                else:
                    code_block = "<p class='muted'>Code file missing.</p>"

                programs_html.append(
                    f"""
                    <section class="panel section" style="margin-top: 18px;">
                      <h2 style="margin:0 0 8px;">{safe(prog.title)}</h2>
                      <div class="muted">{links_html}</div>
                      {code_block}
                    </section>
                    """
                )

        prev_lang, next_lang = slug_to_prev_next.get(lang.slug, (None, None))
        prev_href = f"{rel}l/{prev_lang.slug}/" if prev_lang else f"{rel}index.html"
        prev_label = f"← {safe(prev_lang.name)}" if prev_lang else "← Home"
        next_href = f"{rel}l/{next_lang.slug}/" if next_lang else f"{rel}browse/index.html"
        next_label = f"{safe(next_lang.name)} →" if next_lang else "Browse →"
        pager = f"""
        <div class="pager">
          <a href="{prev_href}" aria-label="Previous language">{prev_label}</a>
          <a href="{next_href}" aria-label="Next language">{next_label}</a>
        </div>
        """

        body = f"""
        <div class="breadcrumbs">
          <a href="{rel}index.html">Home</a> · <a href="{rel}browse/index.html?letter={first_letter(lang.name)}">Browse</a> · {safe(lang.name)}
        </div>
        <section class="panel section">
          <h1 style="margin:0 0 8px;">{safe(lang.name)}</h1>
          <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <span class="pill">{len(lang.programs)} program{'' if len(lang.programs)==1 else 's'}</span>
            <span class="pill">Added {safe(lang.added_at)}</span>
            {"".join(prov_pills)}
            <a class="pill" href="{safe(lang.evidence_url)}" target="_blank" rel="noopener">Evidence</a>
          </div>
          {alias_html}
          {prov_line}
        </section>
        {"".join(programs_html)}
        {pager}
        """

        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(layout(title=f"{lang.name} · PL Catalog", rel=rel, body=body, generated_at=generated_at), encoding="utf-8")


def build_languages(*, turns_by_language: dict[str, TurnInfo]) -> list[Language]:
    meta_paths = sorted(LANGUAGES_DIR.rglob("meta.json"))
    languages: list[Language] = []
    for meta_path in meta_paths:
        try:
            meta = read_json(meta_path)
        except Exception as e:
            raise SystemExit(f"Failed to parse {meta_path}: {e}") from e

        name = str(meta.get("name") or "").strip()
        if not name:
            continue
        aliases = list(meta.get("aliases") or [])
        evidence_url = str(meta.get("evidence_url") or "").strip()
        added_at = str(meta.get("added_at") or "").strip()

        folder = meta_path.parent
        folder_rel = folder.relative_to(LANGUAGES_DIR).as_posix()
        slug = make_lang_slug(name)

        turn = turns_by_language.get(canonical_name(name).lower())
        agent = turn.trailers.get("Agent") if turn else None
        model = turn.trailers.get("Model") if turn else None
        temperature = parse_temperature(turn.trailers.get("Temperature") if turn else None)
        web_search = normalize_web_search(turn.trailers.get("WebSearch") if turn else None)

        programs: list[Program] = []
        programs_dir = folder / "programs"
        if programs_dir.is_dir():
            for prog_dir in sorted([p for p in programs_dir.iterdir() if p.is_dir()]):
                manifest_path = prog_dir / "manifest.json"
                if not manifest_path.exists():
                    continue
                manifest = read_json(manifest_path)
                sha256 = str(manifest.get("code_sha256") or prog_dir.name)
                title = str(manifest.get("title") or "Untitled program")
                origin_url = str(manifest.get("origin_url") or "")
                license_guess = manifest.get("license_guess")
                license_guess = str(license_guess) if license_guess else None
                prog_added_at = str(manifest.get("added_at") or "")

                code_path = find_program_code_file(prog_dir)
                code_bytes = None
                code_text = None
                code_out_name = None
                if code_path is not None and code_path.exists():
                    code_bytes = code_path.read_bytes()
                    code_text = code_bytes.decode("utf-8", errors="replace")
                    code_out_name = derive_code_out_name(code_path.name)

                programs.append(
                    Program(
                        sha256=sha256,
                        title=title,
                        origin_url=origin_url,
                        license_guess=license_guess,
                        added_at=prog_added_at,
                        code_source_path=code_path,
                        code_bytes=code_bytes,
                        code_text=code_text,
                        code_out_name=code_out_name,
                    )
                )

        languages.append(
            Language(
                name=name,
                aliases=aliases,
                evidence_url=evidence_url,
                added_at=added_at,
                folder_rel=folder_rel,
                slug=slug,
                programs=programs,
                turn_commit=turn.commit if turn else None,
                turn_authored_at=turn.authored_at if turn else None,
                agent=agent,
                model=model,
                temperature=temperature,
                web_search=web_search,
            )
        )

    languages.sort(key=lambda l: l.name.lower())
    return languages


def copy_assets(*, out: Path) -> None:
    assets_src = Path(__file__).parent / "assets"
    assets_dst = out / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)
    for p in assets_src.iterdir():
        if p.is_file():
            shutil.copy2(p, assets_dst / p.name)


def write_index_json(*, out: Path, languages: list[Language], generated_at: str) -> None:
    payload = {
        "generated_at": generated_at,
        "languages": [
            {
                "name": l.name,
                "slug": l.slug,
                "aliases": l.aliases,
                "evidence_url": l.evidence_url,
                "added_at": l.added_at,
                "program_count": len(l.programs),
                "first_letter": first_letter(l.name),
                "turn_commit": l.turn_commit,
                "turn_authored_at": l.turn_authored_at,
                "agent": l.agent,
                "model": l.model,
                "temperature": l.temperature,
                "web_search": l.web_search,
            }
            for l in languages
        ],
    }
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "data" / "index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def copy_program_files(*, out: Path, languages: list[Language]) -> None:
    code_root = out / "code"
    for lang in languages:
        for prog in lang.programs:
            if not prog.sha256:
                continue
            out_dir = code_root / prog.sha256
            out_dir.mkdir(parents=True, exist_ok=True)

            # Copy manifest if it exists in the source folder.
            if prog.code_source_path is not None:
                prog_dir = prog.code_source_path.parent
                manifest_src = prog_dir / "manifest.json"
                if manifest_src.exists():
                    shutil.copy2(manifest_src, out_dir / "manifest.json")

            if prog.code_bytes is None:
                continue

            out_name = prog.code_out_name or "code.txt"
            (out_dir / out_name).write_bytes(prog.code_bytes)


def compute_top_domains_licenses_exts(
    languages: list[Language],
) -> tuple[list[tuple[str, int]], list[tuple[str, int]], list[tuple[str, int]]]:
    domains = Counter()
    licenses = Counter()
    exts = Counter()
    for lang in languages:
        for prog in lang.programs:
            if prog.origin_url:
                try:
                    domains[urlparse(prog.origin_url).netloc.lower() or "(unknown)"] += 1
                except Exception:
                    domains["(invalid url)"] += 1
            licenses[prog.license_guess or "Unknown"] += 1
            if prog.code_out_name:
                suffix = Path(prog.code_out_name).suffix.lower().lstrip(".")
                exts[suffix or "unknown"] += 1
            else:
                exts["unknown"] += 1
    return domains.most_common(12), licenses.most_common(12), exts.most_common(12)


def compute_added_by_day(languages: list[Language]) -> list[tuple[str, int]]:
    ctr = Counter()
    for lang in languages:
        dt = parse_iso8601(lang.added_at)
        if dt is None:
            continue
        ctr[dt.date().isoformat()] += 1
    return sorted(ctr.items())


def temperature_bucket(temp: float) -> str:
    if temp < 0:
        return "<0"
    if temp < 0.2:
        return "0.0–0.2"
    if temp < 0.4:
        return "0.2–0.4"
    if temp < 0.6:
        return "0.4–0.6"
    if temp < 0.8:
        return "0.6–0.8"
    if temp < 1.0:
        return "0.8–1.0"
    return "≥1.0"


def compute_turn_stats(turns: list[TurnInfo]) -> dict[str, Any]:
    models = Counter()
    agents = Counter()
    web_search = Counter()
    temps: list[float] = []
    temp_buckets = Counter()

    for turn in turns:
        model = (turn.trailers.get("Model") or "").strip() or "Unknown"
        agent = (turn.trailers.get("Agent") or "").strip() or "Unknown"
        ws = normalize_web_search(turn.trailers.get("WebSearch"))
        ws = (ws or "").strip() or "Unknown"

        models[model] += 1
        agents[agent] += 1
        web_search[ws] += 1

        temp = parse_temperature(turn.trailers.get("Temperature"))
        if temp is not None:
            temps.append(temp)
            temp_buckets[temperature_bucket(temp)] += 1

    bucket_order = ["<0", "0.0–0.2", "0.2–0.4", "0.4–0.6", "0.6–0.8", "0.8–1.0", "≥1.0"]
    temp_bucket_rows = [(b, int(temp_buckets.get(b, 0))) for b in bucket_order if temp_buckets.get(b, 0)]

    if temps:
        temps_min = min(temps)
        temps_max = max(temps)
        temps_avg = sum(temps) / len(temps)
    else:
        temps_min = temps_max = temps_avg = None

    return {
        "turns_total": len(turns),
        "unique_models": len(models),
        "unique_agents": len(agents),
        "top_models": models.most_common(12),
        "top_agents": agents.most_common(12),
        "web_search": web_search.most_common(12),
        "temps_count": len(temps),
        "temps_min": temps_min,
        "temps_max": temps_max,
        "temps_avg": temps_avg,
        "temp_buckets": temp_bucket_rows,
    }


def compute_prev_next(languages: list[Language]) -> dict[str, tuple[Language | None, Language | None]]:
    if not languages:
        return {}
    mapping: dict[str, tuple[Language | None, Language | None]] = {}
    for i, lang in enumerate(languages):
        prev_lang = languages[i - 1] if i > 0 else None
        next_lang = languages[i + 1] if i + 1 < len(languages) else None
        mapping[lang.slug] = (prev_lang, next_lang)
    return mapping


def build_site(*, out: Path) -> None:
    if not LANGUAGES_DIR.exists():
        raise SystemExit(f"Missing {LANGUAGES_DIR}")

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    turns = read_turns_from_git()
    turns_by_language = index_turns_by_language(turns)
    turn_stats = compute_turn_stats(turns)

    languages = build_languages(turns_by_language=turns_by_language)
    counts = letter_counts(languages)
    programs_total = sum(len(l.programs) for l in languages)
    top_domains, top_licenses, top_exts = compute_top_domains_licenses_exts(languages)
    langs_added_by_day = compute_added_by_day(languages)
    slug_to_prev_next = compute_prev_next(languages)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "browse").mkdir(parents=True, exist_ok=True)
    (out / "stats").mkdir(parents=True, exist_ok=True)

    copy_assets(out=out)
    write_index_json(out=out, languages=languages, generated_at=generated_at)
    copy_program_files(out=out, languages=languages)

    render_home_page(
        dist_root=out,
        languages=languages,
        counts=counts,
        generated_at=generated_at,
        programs_total=programs_total,
    )
    render_browse_page(dist_root=out, languages=languages, counts=counts, generated_at=generated_at)
    render_stats_page(
        dist_root=out,
        languages=languages,
        counts=counts,
        programs_total=programs_total,
        generated_at=generated_at,
        top_domains=top_domains,
        top_licenses=top_licenses,
        top_exts=top_exts,
        langs_added_by_day=langs_added_by_day,
        turns_total=int(turn_stats["turns_total"]),
        unique_agents=int(turn_stats["unique_agents"]),
        unique_models=int(turn_stats["unique_models"]),
        top_agents=list(turn_stats["top_agents"]),
        top_models=list(turn_stats["top_models"]),
        web_search_counts=list(turn_stats["web_search"]),
        temps_count=int(turn_stats["temps_count"]),
        temps_min=turn_stats["temps_min"],
        temps_max=turn_stats["temps_max"],
        temps_avg=turn_stats["temps_avg"],
        temp_buckets=list(turn_stats["temp_buckets"]),
    )
    render_language_pages(dist_root=out, languages=languages, generated_at=generated_at, slug_to_prev_next=slug_to_prev_next)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build a static website from languages/* data.")
    parser.add_argument("--out", default=str(Path("web") / "dist"), help="Output directory (default: web/dist)")
    args = parser.parse_args(argv)

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out

    # Safety: refuse to delete something that doesn't look like a build dir.
    out_str = str(out)
    if os.path.abspath(out_str) in ("/", str(ROOT)):
        raise SystemExit(f"Refusing to use --out={out}")

    build_site(out=out)
    print(f"[web] built site at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
