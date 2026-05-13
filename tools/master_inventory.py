#!/usr/bin/env python3
"""Build and compare a master programming-language inventory.

This reproduces the core idea from `acherm/PL-ultimate` inside this repo:
- build a master inventory from PLDB, GitHub Linguist, Wikipedia, optional Esolang
- augment it with Hyperpolyglot, local Pygments, and Rosetta Code support flags
- compare the resulting inventory against `data/pl_list.txt`

The implementation intentionally stays dependency-light:
- stdlib
- PyYAML
- installed Pygments
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import html as html_lib
import json
import re
import string
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Missing dependency: PyYAML is required to run this script.") from exc

try:
    from pygments.lexers._mapping import LEXERS
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Missing dependency: Pygments is required to run this script.") from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DERIVED_DIR = DATA_DIR / "derived"
REPORTS_DIR = ROOT / "reports" / "master_inventory"

LINGUIST_URL = (
    "https://raw.githubusercontent.com/github-linguist/linguist/master/"
    "lib/linguist/languages.yml"
)
WIKIPEDIA_LIST_URL = "https://en.wikipedia.org/wiki/List_of_programming_languages"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
ESOLANG_API = "https://esolangs.org/w/api.php"
HYPERPOLYGLOT_LANGS_URL = (
    "https://raw.githubusercontent.com/monkslc/hyperpolyglot/master/src/codegen/languages.rs"
)
HYPERPOLYGLOT_INFO_URL = (
    "https://raw.githubusercontent.com/monkslc/hyperpolyglot/master/"
    "src/codegen/language-info-map.rs"
)
ROSETTA_APIS = [
    "https://rosettacode.org/w/api.php",
    "https://rosettacode.org/mw/api.php",
]

HTTP_HEADERS = {
    "User-Agent": "PL-ultimate-llm/1.0 (+https://github.com/acherm/PL-ultimate)"
}

MASTER_FIELDS = [
    "lang_id",
    "canonical_name",
    "source_flags",
    "types",
    "extensions",
    "first_appeared",
    "homepage",
    "paradigms",
    "typing",
    "designed_by",
    "influenced_by",
    "hello_world",
    "linguist_key",
    "evidence_urls",
    "notes",
    "in_pldb",
    "in_linguist",
    "in_wikipedia",
    "in_esolang",
    "has_extensions",
    "has_paradigm",
    "has_typing",
    "has_hello_world",
    "source_count",
    "alias_count",
    "hyperpolyglot_name",
    "in_hyperpolyglot",
    "hp_type",
    "hp_group",
    "hp_color",
    "pygments_name",
    "in_pygments",
    "pygments_module",
    "pygments_class",
    "pygments_aliases",
    "pygments_filenames",
    "pygments_mimetypes",
    "in_rosettacode",
    "rosettacode_name",
    "rosettacode_url",
    "rosettacode_summary",
    "rosettacode_tasks_count",
]

BOOLEAN_FIELDS = {
    "hello_world",
    "in_pldb",
    "in_linguist",
    "in_wikipedia",
    "in_esolang",
    "has_extensions",
    "has_paradigm",
    "has_typing",
    "has_hello_world",
    "in_hyperpolyglot",
    "in_pygments",
    "in_rosettacode",
}

INT_FIELDS = {"source_count", "alias_count", "rosettacode_tasks_count"}

SOURCE_PRIORITY = {
    "pldb": 0,
    "linguist": 1,
    "wikipedia": 2,
    "esolang": 3,
}

KV_HEAD = re.compile(r"^\s*([A-Za-z0-9_][\w\s/-]*?)\s*:\s*(.*?)\s*$")
LIST_ITEM = re.compile(r"^\s*-\s*(.*?)\s*$")
WIKI_BAD_PAT = re.compile(
    r"(list of|disambiguation|help:|user:|talk:|wikipedia:|category:)",
    re.IGNORECASE,
)
WIKI_TITLE_PAT = re.compile(r'<a\b[^>]*\btitle="([^"]+)"', re.IGNORECASE)
BAD_PATH_TOKENS = re.compile(
    r"/(authors|author|build|books?|measures?|metrics?|scripts?|readme|data|csv|tsv|json|assets?)/",
    re.IGNORECASE,
)
BAD_NAME_TOKENS = re.compile(
    r"^(authors?|build|books?|measures?|metrics?|readme|csv|tsv|json)\b",
    re.IGNORECASE,
)
LANG_PROPS_HINTS = {
    "paradigm",
    "paradigms",
    "typing",
    "type system",
    "influenced by",
    "influenced",
    "influenced-by",
    "designed by",
    "designed",
    "filename extension",
    "file extension",
    "file extensions",
    "extensions",
    "hello world",
    "hello-world",
    "hello_world",
    "hello",
    "clocextensions",
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            out.append(value)
            seen.add(value)
    return out


def ascii_fold(value: str) -> str:
    return (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def normalize_token(value: str) -> str:
    text = (value or "").strip()
    text = (
        text.replace("–", "-")
        .replace("—", "-")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("♯", "#")
    )
    return re.sub(r"\s+", " ", text)


def normalize_key(value: str) -> str:
    text = ascii_fold(normalize_token(value)).lower().strip()
    text = text.replace("++", " plus plus ")
    text = re.sub(r"[^a-z0-9+#.\- ]+", " ", text)
    text = text.replace("#", " sharp ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_id(name: str) -> str:
    key = normalize_key(name).replace(" ", "-").strip("-")
    if key:
        return key
    digest = hashlib.sha1((name or "").encode("utf-8", "ignore")).hexdigest()[:8]
    return f"id-{digest}"


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    return text in {"1", "true", "yes", "y"}


def parse_int(value: Any) -> int:
    text = str(value or "").strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


def split_semicolon(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"[;|]", value) if part.strip()]


def split_extension_tokens(value: str) -> list[str]:
    if not value:
        return []
    tokens: list[str] = []
    for part in re.split(r"[\s,;|/]+", value):
        token = part.strip()
        if not token:
            continue
        if token.startswith("*."):
            token = "." + token[2:]
        if not token.startswith("."):
            token = "." + token
        token = re.sub(r"[^.\w+-]", "", token.lower())
        if len(token) > 1:
            tokens.append(token)
    return unique_preserve_order(tokens)


def first_non_empty(rows: list[dict[str, Any]], field: str) -> Any:
    for row in rows:
        value = row.get(field)
        if isinstance(value, bool):
            if value:
                return value
            continue
        if str(value or "").strip():
            return value
    return ""


def union_flags(rows: list[dict[str, Any]], field: str) -> str:
    values: list[str] = []
    for row in rows:
        values.extend(split_semicolon(str(row.get(field, ""))))
    return ";".join(sorted(set(values)))


def union_extensions(rows: list[dict[str, Any]]) -> str:
    tokens: list[str] = []
    for row in rows:
        tokens.extend(split_extension_tokens(str(row.get("extensions", ""))))
    return " ".join(sorted(set(tokens)))


def http_get_text(url: str, *, timeout: int = 60) -> str:
    request = Request(url, headers=HTTP_HEADERS)
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read().decode("utf-8", errors="replace")


def mediawiki_api_get(api_bases: list[str] | str, params: dict[str, str]) -> dict[str, Any]:
    bases = [api_bases] if isinstance(api_bases, str) else api_bases
    last_error: Exception | None = None
    for base in bases:
        for attempt in range(3):
            try:
                query = urlencode({"format": "json", **params})
                payload = http_get_text(f"{base}?{query}", timeout=45)
                return json.loads(payload)
            except Exception as exc:  # pragma: no cover - network variability
                last_error = exc
                time.sleep(0.25 * (attempt + 1))
    raise RuntimeError(f"MediaWiki API request failed: {last_error}") from last_error


def fetch_linguist_yaml(*, offline: bool) -> Path:
    ensure_dir(RAW_DIR)
    out = RAW_DIR / "linguist_languages.yml"
    if offline and out.exists():
        return out
    out.write_text(http_get_text(LINGUIST_URL), encoding="utf-8")
    return out


def extract_wikipedia_titles_from_html(page_html: str) -> list[str]:
    titles: list[str] = []
    for match in WIKI_TITLE_PAT.finditer(page_html):
        title = html_lib.unescape(match.group(1)).strip()
        if not title or WIKI_BAD_PAT.search(title):
            continue
        titles.append(title)
    return unique_preserve_order(titles)


def fetch_wikipedia_titles(*, offline: bool) -> Path:
    ensure_dir(RAW_DIR)
    out = RAW_DIR / "wikipedia_lang_titles.json"
    if offline and out.exists():
        return out

    titles: list[str] = []
    try:
        for suffix in [""] + [f":_{letter}" for letter in string.ascii_uppercase]:
            page = http_get_text(f"{WIKIPEDIA_LIST_URL}{suffix}", timeout=45)
            titles.extend(extract_wikipedia_titles_from_html(page))
            time.sleep(0.05)
    except Exception:
        titles = []

    if not titles:
        seen: set[str] = set()
        cont: str | None = None
        while True:
            params = {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": "Category:Programming languages",
                "cmnamespace": "0",
                "cmtype": "page",
                "cmlimit": "500",
            }
            if cont:
                params["cmcontinue"] = cont
            data = mediawiki_api_get(WIKIPEDIA_API, params)
            for item in data.get("query", {}).get("categorymembers", []):
                title = str(item.get("title", "")).strip()
                if title and not WIKI_BAD_PAT.search(title) and title not in seen:
                    seen.add(title)
                    titles.append(title)
            cont = data.get("continue", {}).get("cmcontinue")
            if not cont:
                break
            time.sleep(0.05)

    out.write_text(
        json.dumps(sorted(set(titles)), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out


def fetch_esolang_titles(*, offline: bool) -> Path:
    ensure_dir(RAW_DIR)
    out = RAW_DIR / "esolang_language_titles.json"
    if offline and out.exists():
        return out

    titles: list[str] = []
    cont: str | None = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Languages",
            "cmtype": "page",
            "cmlimit": "500",
        }
        if cont:
            params["cmcontinue"] = cont
        data = mediawiki_api_get(ESOLANG_API, params)
        for item in data.get("query", {}).get("categorymembers", []):
            title = str(item.get("title", "")).strip()
            if title:
                titles.append(title)
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        time.sleep(0.05)

    out.write_text(
        json.dumps(sorted(set(titles)), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out


def fetch_hyperpolyglot_sources(*, offline: bool) -> tuple[Path, Path]:
    ensure_dir(RAW_DIR)
    langs = RAW_DIR / "hyperpolyglot_languages.rs"
    info = RAW_DIR / "hyperpolyglot_language_info_map.rs"
    if not (offline and langs.exists()):
        langs.write_text(http_get_text(HYPERPOLYGLOT_LANGS_URL), encoding="utf-8")
    if not (offline and info.exists()):
        info.write_text(http_get_text(HYPERPOLYGLOT_INFO_URL), encoding="utf-8")
    return langs, info


def parse_blocks(text: str) -> dict[str, list[str]]:
    props: dict[str, list[str]] = {}
    current_key: str | None = None
    for line in text.splitlines():
        head = KV_HEAD.match(line)
        if head:
            current_key = head.group(1).strip().lower()
            value = (head.group(2) or "").strip()
            props.setdefault(current_key, [])
            if value:
                props[current_key].append(value)
            continue

        if current_key:
            item = LIST_ITEM.match(line)
            if item:
                value = item.group(1).strip()
                if value:
                    props[current_key].append(value)
                continue
            if line.startswith((" ", "\t")):
                value = line.strip()
                if value:
                    props[current_key].append(value)
                continue
            current_key = None

    return props


def collect_pldb_aliases(props: dict[str, list[str]]) -> list[str]:
    aliases: list[str] = []
    for key in (
        "alias",
        "aliases",
        "aka",
        "also known as",
        "short name",
        "short names",
    ):
        for value in props.get(key, []):
            if any(sep in value for sep in [",", ";", "|", "/"]):
                aliases.extend(
                    piece.strip()
                    for piece in re.split(r"[;,|/]", value)
                    if piece.strip()
                )
            else:
                aliases.append(value.strip())
    return sorted(
        {
            alias
            for alias in aliases
            if alias and not BAD_NAME_TOKENS.search(alias)
        },
        key=str.lower,
    )


def collect_pldb_extensions(props: dict[str, list[str]]) -> list[str]:
    tokens: list[str] = []
    for key in (
        "clocextensions",
        "cloc extensions",
        "cloc-ext",
        "cloc_ext",
        "filename extension",
        "file extension",
        "file extensions",
        "extensions",
    ):
        for value in props.get(key, []):
            tokens.extend(split_extension_tokens(value))
    return unique_preserve_order(tokens)


def parse_pldb_file(text: str, file_path: Path) -> dict[str, Any]:
    path_text = file_path.as_posix()
    if BAD_PATH_TOKENS.search("/" + path_text + "/"):
        return {}

    props = parse_blocks(text)
    is_concept = "/concepts/" in path_text or path_text.startswith("pldb/concepts/")
    has_lang_prop = any(key in props for key in LANG_PROPS_HINTS)
    if not (is_concept or has_lang_prop):
        return {}

    name = ""
    for key in ("name", "title"):
        if props.get(key):
            name = props[key][0].strip()
            break
    if not name:
        name = file_path.stem.strip()
    if not name or BAD_NAME_TOKENS.search(name):
        return {}

    first_appeared = ""
    for key in ("appeared", "first appeared", "first-appeared"):
        if props.get(key):
            first_appeared = props[key][0].strip()
            break

    homepage = ""
    for key in ("homepage", "home page", "url", "urls"):
        if props.get(key):
            homepage = props[key][0].strip()
            break

    return {
        "name": name,
        "aliases": collect_pldb_aliases(props),
        "first_appeared": first_appeared,
        "homepage": homepage,
        "paradigms": "; ".join(props.get("paradigm", []) + props.get("paradigms", [])),
        "typing": "; ".join(props.get("typing", []) + props.get("type system", [])),
        "designed_by": "; ".join(props.get("designed by", []) + props.get("designed", [])),
        "influenced_by": "; ".join(
            props.get("influenced by", [])
            + props.get("influenced", [])
            + props.get("influenced-by", [])
        ),
        "hello_world": bool(
            props.get("hello world")
            or props.get("hello-world")
            or props.get("hello_world")
            or props.get("hello")
        ),
        "extensions": " ".join(collect_pldb_extensions(props)),
    }


def scan_local_pldb(pldb_dir: Path) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for path in pldb_dir.rglob("*"):
        if path.suffix.lower() not in {".pldb", ".scroll"}:
            continue
        try:
            record = parse_pldb_file(
                path.read_text(encoding="utf-8", errors="ignore"), path
            )
        except Exception:
            continue
        if record:
            found.append(record)
    return found


def base_row(
    *,
    name: str,
    source_flags: str,
    evidence_url: str,
    row_type: str = "",
    extensions: str = "",
    first_appeared: str = "",
    homepage: str = "",
    paradigms: str = "",
    typing: str = "",
    designed_by: str = "",
    influenced_by: str = "",
    hello_world: bool = False,
    linguist_key: str = "",
    notes: str = "",
) -> dict[str, Any]:
    return {
        "lang_id": make_id(name),
        "canonical_name": name,
        "source_flags": source_flags,
        "types": row_type,
        "extensions": extensions,
        "first_appeared": first_appeared,
        "homepage": homepage,
        "paradigms": paradigms,
        "typing": typing,
        "designed_by": designed_by,
        "influenced_by": influenced_by,
        "hello_world": hello_world,
        "linguist_key": linguist_key,
        "evidence_urls": evidence_url,
        "notes": notes,
    }


def row_metadata_score(row: dict[str, Any]) -> int:
    fields = (
        "extensions",
        "first_appeared",
        "homepage",
        "paradigms",
        "typing",
        "designed_by",
        "influenced_by",
    )
    return sum(1 for field in fields if str(row.get(field, "")).strip())


def row_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    flags = set(split_semicolon(str(row.get("source_flags", ""))))
    source_rank = min((SOURCE_PRIORITY.get(flag, 99) for flag in flags), default=99)
    return (source_rank, -row_metadata_score(row), normalize_key(row["canonical_name"]))


def initialize_augmented_fields(row: dict[str, Any]) -> None:
    for field in MASTER_FIELDS:
        if field not in row:
            row[field] = False if field in BOOLEAN_FIELDS else 0 if field in INT_FIELDS else ""


def merge_base_rows(
    rows: list[dict[str, Any]], alias_records: list[dict[str, str]]
) -> tuple[list[dict[str, Any]], list[dict[str, str]], dict[str, list[str]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["lang_id"]].append(row)

    aliases_by_lang: dict[str, list[str]] = defaultdict(list)
    alias_sources: dict[tuple[str, str], set[str]] = defaultdict(set)
    for record in alias_records:
        aliases_by_lang[record["lang_id"]].append(record["alias"])
        alias_sources[(record["lang_id"], record["alias"])].add(record.get("source", ""))

    master_rows: list[dict[str, Any]] = []
    alias_rows_out: list[dict[str, str]] = []

    for lang_id, group in grouped.items():
        ordered = sorted(group, key=row_sort_key)
        merged = {
            "lang_id": lang_id,
            "canonical_name": first_non_empty(ordered, "canonical_name"),
            "source_flags": union_flags(ordered, "source_flags"),
            "types": first_non_empty(ordered, "types"),
            "extensions": union_extensions(ordered),
            "first_appeared": first_non_empty(ordered, "first_appeared"),
            "homepage": first_non_empty(ordered, "homepage"),
            "paradigms": first_non_empty(ordered, "paradigms"),
            "typing": first_non_empty(ordered, "typing"),
            "designed_by": first_non_empty(ordered, "designed_by"),
            "influenced_by": first_non_empty(ordered, "influenced_by"),
            "hello_world": any(parse_bool(row.get("hello_world")) for row in ordered),
            "linguist_key": first_non_empty(ordered, "linguist_key"),
            "evidence_urls": union_flags(ordered, "evidence_urls"),
            "notes": first_non_empty(ordered, "notes"),
        }

        flags = set(split_semicolon(merged["source_flags"]))
        merged["in_pldb"] = "pldb" in flags
        merged["in_linguist"] = "linguist" in flags
        merged["in_wikipedia"] = "wikipedia" in flags
        merged["in_esolang"] = "esolang" in flags
        merged["has_extensions"] = bool(merged["extensions"])
        merged["has_paradigm"] = bool(merged["paradigms"])
        merged["has_typing"] = bool(merged["typing"])
        merged["has_hello_world"] = bool(merged["hello_world"])
        merged["source_count"] = len(flags)

        alias_names = unique_preserve_order(
            sorted(
                set(aliases_by_lang.get(lang_id, [])) | {merged["canonical_name"]},
                key=str.lower,
            )
        )
        aliases_by_lang[lang_id] = alias_names
        merged["alias_count"] = len(alias_names)
        initialize_augmented_fields(merged)
        master_rows.append(merged)

        for alias in alias_names:
            alias_rows_out.append(
                {
                    "alias": alias,
                    "lang_id": lang_id,
                    "source": (
                        "self"
                        if alias == merged["canonical_name"]
                        else ";".join(
                            sorted(
                                source
                                for source in alias_sources.get((lang_id, alias), set())
                                if source
                            )
                        )
                    ),
                }
            )

    master_rows.sort(key=lambda row: normalize_key(row["canonical_name"]))
    alias_rows_out.sort(
        key=lambda row: (normalize_key(row["alias"]), normalize_key(row["lang_id"]))
    )
    return master_rows, alias_rows_out, aliases_by_lang


def parse_hyperpolyglot_languages(text: str) -> list[str]:
    match = re.search(
        r"static\s+LANGUAGES\s*:[\s\S]*?=\s*&\s*\[(?P<body>[\s\S]*?)\]\s*;", text
    )
    if not match:
        raise RuntimeError("Could not locate LANGUAGES array in Hyperpolyglot source.")
    body = match.group("body")
    names = re.findall(r'"((?:\\.|[^"\\])*)"', body)
    return [bytes(name, "utf-8").decode("unicode_escape") for name in names]


def parse_hyperpolyglot_info(text: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r'\("(?P<key>[^"]+)",\s*Language\s*\{\s*name:\s*"(?P<name>[^"]+)",\s*'
        r'language_type:\s*LanguageType::(?P<lang_type>\w+),\s*'
        r'color:\s*(?P<color>Some\("?#?[0-9A-Fa-f]+"?\)|None),\s*'
        r'group:\s*(?P<group>Some\(".*?"\)|None)\s*\}\s*\)',
        re.S,
    )
    for match in pattern.finditer(text):
        color = ""
        if match.group("color").startswith("Some"):
            color_match = re.search(r'"(#?[0-9A-Fa-f]+)"', match.group("color"))
            color = color_match.group(1) if color_match else ""
        group = ""
        if match.group("group").startswith("Some"):
            group_match = re.search(r'"(.*?)"', match.group("group"))
            group = group_match.group(1) if group_match else ""
        out[match.group("name")] = {
            "hp_type": match.group("lang_type"),
            "hp_group": group,
            "hp_color": color,
        }
    return out


def hyperpolyglot_alias_table() -> dict[str, str]:
    return {
        "c sharp": "C#",
        "c-sharp": "C#",
        "csharp": "C#",
        "f sharp": "F#",
        "f-sharp": "F#",
        "fsharp": "F#",
        "c plus plus": "C++",
        "cplusplus": "C++",
        "cpp": "C++",
        "objective c": "Objective-C",
        "objective-c": "Objective-C",
        "obj-c": "Objective-C",
        "objective c++": "Objective-C++",
        "objective-c++": "Objective-C++",
        "obj-c++": "Objective-C++",
        "golang": "Go",
        "wolfram language": "Mathematica",
        "wolfram": "Mathematica",
        "js": "JavaScript",
        "ts": "TypeScript",
        "vb.net": "Visual Basic .NET",
        "vb": "Visual Basic .NET",
        "shell": "Shell",
        "shell script": "Shell",
        "powershell core": "PowerShell",
        "pl/sql": "PLSQL",
        "pl/pgsql": "PLpgSQL",
    }


def build_name_index(names: list[str]) -> dict[str, str]:
    index: dict[str, str] = {}
    for name in names:
        key = normalize_key(name)
        for variant in (
            key,
            key.replace(" ", "-"),
            key.replace("-", " "),
            key.replace(" ", ""),
        ):
            if variant:
                index[variant] = name
    return index


def match_hyperpolyglot_name(
    name: str, index: dict[str, str], alias_map: dict[str, str]
) -> str | None:
    key = normalize_key(name)
    if key in index:
        return index[key]
    if key in alias_map:
        alias = alias_map[key]
        alias_key = normalize_key(alias)
        if alias_key in index:
            return index[alias_key]
    noise_filtered = " ".join(
        part for part in key.split() if part not in {"language", "programming", "script"}
    )
    return index.get(noise_filtered)


def augment_with_hyperpolyglot(
    master_rows: list[dict[str, Any]],
    aliases_by_lang: dict[str, list[str]],
    *,
    offline: bool,
) -> list[dict[str, str]]:
    langs_path, info_path = fetch_hyperpolyglot_sources(offline=offline)
    hp_names = parse_hyperpolyglot_languages(langs_path.read_text(encoding="utf-8"))
    hp_info = parse_hyperpolyglot_info(info_path.read_text(encoding="utf-8"))
    hp_index = build_name_index(hp_names)
    hp_alias_map = hyperpolyglot_alias_table()

    matched_names: set[str] = set()
    for row in master_rows:
        candidates = [row["canonical_name"], *aliases_by_lang.get(row["lang_id"], [])]
        match = None
        for candidate in unique_preserve_order(candidates):
            match = match_hyperpolyglot_name(candidate, hp_index, hp_alias_map)
            if match:
                break
        if not match:
            continue
        info = hp_info.get(match, {})
        row["hyperpolyglot_name"] = match
        row["in_hyperpolyglot"] = True
        row["hp_type"] = info.get("hp_type", "")
        row["hp_group"] = info.get("hp_group", "")
        row["hp_color"] = info.get("hp_color", "")
        matched_names.add(match)

    missing = []
    for name in sorted(set(hp_names) - matched_names, key=str.lower):
        info = hp_info.get(name, {})
        missing.append(
            {
                "hyperpolyglot_name": name,
                "hp_type": info.get("hp_type", ""),
                "hp_group": info.get("hp_group", ""),
                "hp_color": info.get("hp_color", ""),
            }
        )
    return missing


def pygments_alias_table() -> dict[str, str]:
    return {
        "c sharp": "csharp",
        "c-sharp": "csharp",
        "c#": "csharp",
        "f sharp": "fsharp",
        "f-sharp": "fsharp",
        "f#": "fsharp",
        "c plus plus": "cpp",
        "cplusplus": "cpp",
        "cpp": "cpp",
        "objective c": "objective-c",
        "objective-c": "objective-c",
        "obj-c": "objective-c",
        "objective c++": "objective-c++",
        "objective-c++": "objective-c++",
        "obj-c++": "objective-c++",
        "golang": "go",
        "js": "javascript",
        "ts": "typescript",
        "vb.net": "vbnet",
        "vb": "vbnet",
        "shell": "bash",
        "shell script": "bash",
        "unix shell": "bash",
        "wolfram language": "mathematica",
        "wolfram": "mathematica",
        "pl/sql": "plsql",
        "pl/pgsql": "postgresql",
        "vim script": "viml",
        "vimscript": "viml",
    }


def build_pygments_indexes() -> tuple[
    dict[str, dict[str, Any]], dict[str, str], dict[str, set[str]]
]:
    name_to_meta: dict[str, dict[str, Any]] = {}
    alias_index: dict[str, str] = {}
    filename_index: dict[str, set[str]] = defaultdict(set)

    for display_name, value in LEXERS.items():
        module, klass, aliases, filenames, mimetypes = value
        meta = {
            "pygments_name": display_name,
            "pygments_module": module,
            "pygments_class": klass,
            "pygments_aliases": ";".join(aliases),
            "pygments_filenames": ";".join(filenames),
            "pygments_mimetypes": ";".join(mimetypes),
        }
        name_to_meta[display_name] = meta

        keys = [display_name, *aliases]
        for key in keys:
            normalized = normalize_key(key)
            if normalized:
                alias_index[normalized] = display_name

        for filename in filenames:
            filename = filename.strip()
            if not filename:
                continue
            ext_match = re.match(r"^\*\.(?P<ext>[A-Za-z0-9_+\-.]+)$", filename)
            if ext_match:
                token = "." + ext_match.group("ext").lower().lstrip(".")
                if len(token) >= 3:
                    filename_index[token].add(display_name)
            else:
                bare = filename.lstrip("./").lower()
                if len(bare) >= 3:
                    filename_index[bare].add(display_name)

    return name_to_meta, alias_index, filename_index


def match_pygments_name(
    name: str,
    alias_index: dict[str, str],
    filename_index: dict[str, set[str]],
    ext_tokens: list[str],
) -> str | None:
    key = normalize_key(name)
    if key in alias_index:
        return alias_index[key]
    rewritten = pygments_alias_table().get(key)
    if rewritten and rewritten in alias_index:
        return alias_index[rewritten]

    candidates: list[tuple[int, str]] = []
    for ext in ext_tokens:
        for display_name in filename_index.get(ext, set()):
            candidates.append((len(ext), display_name))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return None


def augment_with_pygments(
    master_rows: list[dict[str, Any]], aliases_by_lang: dict[str, list[str]]
) -> list[dict[str, str]]:
    name_to_meta, alias_index, filename_index = build_pygments_indexes()
    matched_names: set[str] = set()

    for row in master_rows:
        ext_tokens = split_extension_tokens(row.get("extensions", ""))
        candidates = [row["canonical_name"], row.get("hyperpolyglot_name", "")]
        candidates.extend(aliases_by_lang.get(row["lang_id"], []))
        match = None
        for candidate in unique_preserve_order([c for c in candidates if c]):
            match = match_pygments_name(candidate, alias_index, filename_index, ext_tokens)
            if match:
                break
        if not match:
            continue

        meta = name_to_meta[match]
        row["in_pygments"] = True
        for key, value in meta.items():
            row[key] = value
        matched_names.add(match)

    missing = []
    for display_name in sorted(set(name_to_meta) - matched_names, key=str.lower):
        meta = name_to_meta[display_name]
        missing.append(
            {
                "pygments_name": display_name,
                "pygments_aliases": meta["pygments_aliases"],
                "pygments_filenames": meta["pygments_filenames"],
                "pygments_module": meta["pygments_module"],
            }
        )
    return missing


def fetch_rosetta_dump(*, offline: bool) -> list[dict[str, Any]]:
    out = DERIVED_DIR / "rosettacode_languages.csv"
    if offline and out.exists():
        return load_csv_rows(out)

    ensure_dir(DERIVED_DIR)
    category_titles: list[str] = []
    cont: str | None = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Programming Languages",
            "cmnamespace": "14",
            "cmtype": "subcat",
            "cmlimit": "500",
        }
        if cont:
            params["cmcontinue"] = cont
        data = mediawiki_api_get(ROSETTA_APIS, params)
        for item in data.get("query", {}).get("categorymembers", []):
            title = str(item.get("title", "")).strip()
            if title:
                category_titles.append(title)
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        time.sleep(0.05)

    main_titles = [
        title.split("Category:", 1)[1] if title.startswith("Category:") else title
        for title in category_titles
    ]

    extracts: dict[str, str] = {}
    counts: dict[str, int] = {}
    batch_size = 50
    for start in range(0, len(main_titles), batch_size):
        chunk_titles = main_titles[start : start + batch_size]
        data = mediawiki_api_get(
            ROSETTA_APIS,
            {
                "action": "query",
                "prop": "extracts",
                "exintro": "1",
                "explaintext": "1",
                "titles": "|".join(chunk_titles),
            },
        )
        for page in data.get("query", {}).get("pages", {}).values():
            title = str(page.get("title", "")).strip()
            if title:
                extracts[title] = str(page.get("extract", "")).strip()
        time.sleep(0.05)

    for start in range(0, len(category_titles), batch_size):
        chunk_titles = category_titles[start : start + batch_size]
        data = mediawiki_api_get(
            ROSETTA_APIS,
            {
                "action": "query",
                "prop": "categoryinfo",
                "titles": "|".join(chunk_titles),
            },
        )
        for page in data.get("query", {}).get("pages", {}).values():
            title = str(page.get("title", "")).strip()
            if title:
                counts[title] = parse_int(page.get("categoryinfo", {}).get("pages"))
        time.sleep(0.05)

    rows: list[dict[str, Any]] = []
    for category_title, title in zip(category_titles, main_titles):
        rows.append(
            {
                "rosettacode_name": title,
                "rosettacode_url": f"https://rosettacode.org/wiki/{quote(title.replace(' ', '_'))}",
                "rosettacode_summary": extracts.get(title, ""),
                "rosettacode_tasks_count": counts.get(category_title, 0),
            }
        )

    write_csv_rows(
        out,
        ["rosettacode_name", "rosettacode_url", "rosettacode_summary", "rosettacode_tasks_count"],
        rows,
    )
    return rows


def build_master_name_maps(
    master_rows: list[dict[str, Any]], aliases_by_lang: dict[str, list[str]]
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    exact: dict[str, dict[str, Any]] = {}
    normalized: dict[str, dict[str, Any]] = {}

    def better(existing: dict[str, Any] | None, candidate: dict[str, Any]) -> dict[str, Any]:
        if existing is None:
            return candidate
        existing_score = (
            parse_int(existing.get("source_count")),
            int(parse_bool(existing.get("has_extensions"))),
            int(parse_bool(existing.get("in_pygments"))),
            int(parse_bool(existing.get("in_rosettacode"))),
        )
        candidate_score = (
            parse_int(candidate.get("source_count")),
            int(parse_bool(candidate.get("has_extensions"))),
            int(parse_bool(candidate.get("in_pygments"))),
            int(parse_bool(candidate.get("in_rosettacode"))),
        )
        return candidate if candidate_score > existing_score else existing

    for row in master_rows:
        names = [row["canonical_name"]]
        names.extend(aliases_by_lang.get(row["lang_id"], []))
        for extra_field in (
            "linguist_key",
            "hyperpolyglot_name",
            "pygments_name",
            "rosettacode_name",
        ):
            extra = str(row.get(extra_field, "")).strip()
            if extra:
                names.append(extra)
        for name in unique_preserve_order([name for name in names if name]):
            exact_key = name.casefold()
            normalized_key = normalize_key(name)
            exact[exact_key] = better(exact.get(exact_key), row)
            if normalized_key:
                normalized[normalized_key] = better(normalized.get(normalized_key), row)
    return exact, normalized


def rosetta_alias_table() -> dict[str, str]:
    return {
        "c sharp": "c sharp",
        "c-sharp": "c sharp",
        "csharp": "c sharp",
        "f sharp": "f sharp",
        "f-sharp": "f sharp",
        "fsharp": "f sharp",
        "c plus plus": "c plus plus",
        "cplusplus": "c plus plus",
        "cpp": "c plus plus",
        "golang": "go",
        "js": "javascript",
        "ts": "typescript",
        "wolfram language": "mathematica",
        "pl/sql": "plsql",
        "pl/pgsql": "plpgsql",
        "objective c": "objective c",
        "objective-c": "objective c",
        "objective c++": "objective c plus plus",
        "objective-c++": "objective c plus plus",
    }


def augment_with_rosettacode(
    master_rows: list[dict[str, Any]],
    aliases_by_lang: dict[str, list[str]],
    *,
    offline: bool,
) -> list[dict[str, str]]:
    rosetta_rows = fetch_rosetta_dump(offline=offline)
    exact_map, normalized_map = build_master_name_maps(master_rows, aliases_by_lang)
    alias_map = rosetta_alias_table()
    matched_names: set[str] = set()

    for rosetta in rosetta_rows:
        name = str(rosetta.get("rosettacode_name", "")).strip()
        match = exact_map.get(name.casefold())
        if not match:
            normalized_name = normalize_key(name)
            match = normalized_map.get(normalized_name)
        if not match:
            rewritten = alias_map.get(normalize_key(name))
            if rewritten:
                match = normalized_map.get(rewritten)
        if not match:
            close = difflib.get_close_matches(
                normalize_key(name), list(normalized_map.keys()), n=1, cutoff=0.92
            )
            if close:
                match = normalized_map[close[0]]
        if not match:
            continue

        match["in_rosettacode"] = True
        match["rosettacode_name"] = name
        match["rosettacode_url"] = rosetta.get("rosettacode_url", "")
        match["rosettacode_summary"] = rosetta.get("rosettacode_summary", "")
        match["rosettacode_tasks_count"] = parse_int(rosetta.get("rosettacode_tasks_count"))
        matched_names.add(name)

    missing = [
        {
            "rosettacode_name": row["rosettacode_name"],
            "rosettacode_url": row["rosettacode_url"],
        }
        for row in sorted(rosetta_rows, key=lambda item: normalize_key(item["rosettacode_name"]))
        if row["rosettacode_name"] not in matched_names
    ]
    return missing


def compute_extension_inventory(master_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for row in master_rows:
        for ext in split_extension_tokens(str(row.get("extensions", ""))):
            record = stats.setdefault(
                ext,
                {
                    "extension": ext,
                    "count_total": 0,
                    "count_pldb": 0,
                    "count_linguist": 0,
                    "count_wikipedia": 0,
                    "count_esolang": 0,
                    "count_hyperpolyglot": 0,
                    "count_pygments": 0,
                    "count_rosettacode": 0,
                    "sample_lang": row["canonical_name"],
                },
            )
            record["count_total"] += 1
            record["count_pldb"] += int(parse_bool(row.get("in_pldb")))
            record["count_linguist"] += int(parse_bool(row.get("in_linguist")))
            record["count_wikipedia"] += int(parse_bool(row.get("in_wikipedia")))
            record["count_esolang"] += int(parse_bool(row.get("in_esolang")))
            record["count_hyperpolyglot"] += int(parse_bool(row.get("in_hyperpolyglot")))
            record["count_pygments"] += int(parse_bool(row.get("in_pygments")))
            record["count_rosettacode"] += int(parse_bool(row.get("in_rosettacode")))
    return sorted(
        stats.values(),
        key=lambda row: (-parse_int(row["count_total"]), row["extension"]),
    )


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def load_csv_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            converted: dict[str, Any] = dict(row)
            for field in BOOLEAN_FIELDS:
                if field in converted:
                    converted[field] = parse_bool(converted[field])
            for field in INT_FIELDS:
                if field in converted:
                    converted[field] = parse_int(converted[field])
            rows.append(converted)
    return rows


def write_master_snapshots(
    *,
    final_rows: list[dict[str, Any]],
    aliases: list[dict[str, str]],
    missing_hyper: list[dict[str, str]],
    missing_pygments: list[dict[str, str]],
    missing_rosetta: list[dict[str, str]],
) -> None:
    ensure_dir(DERIVED_DIR)
    write_csv_rows(
        DERIVED_DIR / "languages_master_augmented_rosettacode.csv", MASTER_FIELDS, final_rows
    )
    write_csv_rows(DERIVED_DIR / "aliases.csv", ["alias", "lang_id", "source"], aliases)
    write_csv_rows(
        DERIVED_DIR / "hyperpolyglot_missing_from_master.csv",
        ["hyperpolyglot_name", "hp_type", "hp_group", "hp_color"],
        missing_hyper,
    )
    write_csv_rows(
        DERIVED_DIR / "pygments_missing_from_master.csv",
        ["pygments_name", "pygments_aliases", "pygments_filenames", "pygments_module"],
        missing_pygments,
    )
    write_csv_rows(
        DERIVED_DIR / "rosettacode_missing_from_master.csv",
        ["rosettacode_name", "rosettacode_url"],
        missing_rosetta,
    )
    write_csv_rows(
        DERIVED_DIR / "extensions_inventory.csv",
        [
            "extension",
            "count_total",
            "count_pldb",
            "count_linguist",
            "count_wikipedia",
            "count_esolang",
            "count_hyperpolyglot",
            "count_pygments",
            "count_rosettacode",
            "sample_lang",
        ],
        compute_extension_inventory(final_rows),
    )


def build_inventory(args: argparse.Namespace) -> None:
    pldb_dir = Path(args.pldb_dir).expanduser().resolve()
    if not pldb_dir.exists():
        raise SystemExit(f"PLDB directory not found: {pldb_dir}")

    linguist_path = fetch_linguist_yaml(offline=args.offline)
    wikipedia_path = fetch_wikipedia_titles(offline=args.offline)
    esolang_path = fetch_esolang_titles(offline=args.offline) if args.include_esolang else None
    fetch_hyperpolyglot_sources(offline=args.offline)

    if getattr(args, "fetch_only", False):
        print("[ok] Raw sources refreshed under data/raw/")
        return

    rows: list[dict[str, Any]] = []
    alias_records: list[dict[str, str]] = []

    linguist = yaml.safe_load(linguist_path.read_text(encoding="utf-8"))
    for name, meta in sorted(linguist.items(), key=lambda item: normalize_key(item[0])):
        rows.append(
            base_row(
                name=name,
                source_flags="linguist",
                evidence_url=LINGUIST_URL,
                extensions=" ".join(meta.get("extensions") or []),
                linguist_key=name,
            )
        )
        for alias in meta.get("aliases") or []:
            alias_records.append(
                {"alias": str(alias).strip(), "lang_id": make_id(name), "source": "linguist"}
            )

    wikipedia_titles = json.loads(wikipedia_path.read_text(encoding="utf-8"))
    for title in wikipedia_titles:
        rows.append(
            base_row(
                name=title,
                source_flags="wikipedia",
                evidence_url=WIKIPEDIA_LIST_URL,
            )
        )

    if esolang_path is not None:
        esolang_titles = json.loads(esolang_path.read_text(encoding="utf-8"))
        for title in esolang_titles:
            rows.append(
                base_row(
                    name=title,
                    source_flags="esolang",
                    evidence_url="https://esolangs.org/wiki/Category:Languages",
                    row_type="esolang",
                )
            )

    for record in scan_local_pldb(pldb_dir):
        rows.append(
            base_row(
                name=record["name"],
                source_flags="pldb",
                evidence_url="https://github.com/breck7/pldb",
                extensions=record.get("extensions", ""),
                first_appeared=record.get("first_appeared", ""),
                homepage=record.get("homepage", ""),
                paradigms=record.get("paradigms", ""),
                typing=record.get("typing", ""),
                designed_by=record.get("designed_by", ""),
                influenced_by=record.get("influenced_by", ""),
                hello_world=bool(record.get("hello_world")),
            )
        )
        for alias in record.get("aliases", []):
            alias_records.append(
                {"alias": alias, "lang_id": make_id(record["name"]), "source": "pldb"}
            )

    master_rows, alias_rows, aliases_by_lang = merge_base_rows(rows, alias_records)
    base_snapshot = deepcopy(master_rows)

    missing_hyper = augment_with_hyperpolyglot(master_rows, aliases_by_lang, offline=args.offline)
    augmented_snapshot = deepcopy(master_rows)
    missing_pygments = augment_with_pygments(master_rows, aliases_by_lang)
    pygments_snapshot = deepcopy(master_rows)
    missing_rosetta = augment_with_rosettacode(
        master_rows, aliases_by_lang, offline=args.offline
    )

    write_csv_rows(DERIVED_DIR / "languages_master.csv", MASTER_FIELDS, base_snapshot)
    write_csv_rows(DERIVED_DIR / "languages_master_augmented.csv", MASTER_FIELDS, augmented_snapshot)
    write_csv_rows(
        DERIVED_DIR / "languages_master_augmented_pygments.csv",
        MASTER_FIELDS,
        pygments_snapshot,
    )
    write_master_snapshots(
        final_rows=master_rows,
        aliases=alias_rows,
        missing_hyper=missing_hyper,
        missing_pygments=missing_pygments,
        missing_rosetta=missing_rosetta,
    )

    print(
        f"[ok] Wrote master inventory with {len(master_rows)} rows "
        f"and {len(compute_extension_inventory(master_rows))} unique extensions."
    )
    print(
        "[ok] Outputs: "
        "data/derived/languages_master*.csv, aliases.csv, extensions_inventory.csv, "
        "tool-specific missing reports."
    )


def read_pl_list(path: Path) -> list[str]:
    lines: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            continue
        lines.append(line)
    return lines


def count_pl_list_conflict_markers(path: Path) -> int:
    return sum(
        1
        for raw_line in path.read_text(encoding="utf-8").splitlines()
        if raw_line.strip().startswith(("<<<<<<<", "=======", ">>>>>>>"))
    )


def load_aliases(path: Path) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            alias = str(row.get("alias", "")).strip()
            lang_id = str(row.get("lang_id", "")).strip()
            if alias and lang_id:
                aliases[lang_id].append(alias)
    return {lang_id: unique_preserve_order(names) for lang_id, names in aliases.items()}


def build_match_maps(
    master_rows: list[dict[str, Any]],
    aliases_by_lang: dict[str, list[str]],
) -> dict[str, dict[str, dict[str, Any]]]:
    maps: dict[str, dict[str, dict[str, Any]]] = {
        "exact_canonical": {},
        "exact_alias": {},
        "exact_tool": {},
        "normalized_canonical": {},
        "normalized_alias": {},
        "normalized_tool": {},
    }

    def update(kind: str, key: str, row: dict[str, Any]) -> None:
        existing = maps[kind].get(key)
        if existing is None:
            maps[kind][key] = row
            return
        existing_score = (
            parse_int(existing.get("source_count")),
            int(parse_bool(existing.get("has_extensions"))),
            int(parse_bool(existing.get("in_pygments"))),
            int(parse_bool(existing.get("in_rosettacode"))),
        )
        candidate_score = (
            parse_int(row.get("source_count")),
            int(parse_bool(row.get("has_extensions"))),
            int(parse_bool(row.get("in_pygments"))),
            int(parse_bool(row.get("in_rosettacode"))),
        )
        if candidate_score > existing_score:
            maps[kind][key] = row

    for row in master_rows:
        canonical = row["canonical_name"]
        update("exact_canonical", canonical.casefold(), row)
        update("normalized_canonical", normalize_key(canonical), row)

        for alias in aliases_by_lang.get(row["lang_id"], []):
            if alias == canonical:
                continue
            update("exact_alias", alias.casefold(), row)
            update("normalized_alias", normalize_key(alias), row)

        for field in ("linguist_key", "hyperpolyglot_name", "pygments_name", "rosettacode_name"):
            value = str(row.get(field, "")).strip()
            if value:
                update("exact_tool", value.casefold(), row)
                update("normalized_tool", normalize_key(value), row)

    return maps


def compare_inventory(args: argparse.Namespace) -> None:
    master_path = Path(args.master).expanduser().resolve()
    aliases_path = Path(args.aliases).expanduser().resolve()
    pl_list_path = Path(args.pl_list).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()

    master_rows = load_csv_rows(master_path)
    aliases_by_lang = load_aliases(aliases_path)
    pl_names = read_pl_list(pl_list_path)
    pl_conflict_markers = count_pl_list_conflict_markers(pl_list_path)
    match_maps = build_match_maps(master_rows, aliases_by_lang)

    matched_lang_ids: set[str] = set()
    match_counts: Counter[str] = Counter()
    match_rows: list[dict[str, Any]] = []
    pl_missing_rows: list[dict[str, Any]] = []

    for name in pl_names:
        matched_row = None
        match_kind = ""
        exact_key = name.casefold()
        normalized_key = normalize_key(name)

        for kind, key in (
            ("exact_canonical", exact_key),
            ("exact_alias", exact_key),
            ("exact_tool", exact_key),
            ("normalized_canonical", normalized_key),
            ("normalized_alias", normalized_key),
            ("normalized_tool", normalized_key),
        ):
            row = match_maps[kind].get(key)
            if row:
                matched_row = row
                match_kind = kind
                break

        fuzzy_candidates: list[str] = []
        if matched_row is None:
            close = difflib.get_close_matches(
                normalized_key,
                list(match_maps["normalized_canonical"].keys()),
                n=3,
                cutoff=0.92,
            )
            fuzzy_candidates = [
                match_maps["normalized_canonical"][candidate]["canonical_name"]
                for candidate in close
            ]

        result = {
            "pl_name": name,
            "matched": bool(matched_row),
            "match_kind": match_kind,
            "master_lang_id": matched_row.get("lang_id", "") if matched_row else "",
            "master_name": matched_row.get("canonical_name", "") if matched_row else "",
            "source_flags": matched_row.get("source_flags", "") if matched_row else "",
            "extensions": matched_row.get("extensions", "") if matched_row else "",
            "in_pldb": parse_bool(matched_row.get("in_pldb")) if matched_row else False,
            "in_linguist": parse_bool(matched_row.get("in_linguist")) if matched_row else False,
            "in_wikipedia": parse_bool(matched_row.get("in_wikipedia")) if matched_row else False,
            "in_esolang": parse_bool(matched_row.get("in_esolang")) if matched_row else False,
            "in_hyperpolyglot": parse_bool(matched_row.get("in_hyperpolyglot")) if matched_row else False,
            "in_pygments": parse_bool(matched_row.get("in_pygments")) if matched_row else False,
            "in_rosettacode": parse_bool(matched_row.get("in_rosettacode")) if matched_row else False,
            "fuzzy_candidates": ";".join(fuzzy_candidates),
        }
        match_rows.append(result)

        if matched_row:
            matched_lang_ids.add(str(matched_row["lang_id"]))
            match_counts[match_kind] += 1
        else:
            pl_missing_rows.append(result)

    master_missing_rows = [
        {
            "canonical_name": row["canonical_name"],
            "lang_id": row["lang_id"],
            "source_flags": row.get("source_flags", ""),
            "extensions": row.get("extensions", ""),
            "source_count": parse_int(row.get("source_count")),
            "alias_count": parse_int(row.get("alias_count")),
            "in_hyperpolyglot": parse_bool(row.get("in_hyperpolyglot")),
            "in_pygments": parse_bool(row.get("in_pygments")),
            "in_rosettacode": parse_bool(row.get("in_rosettacode")),
        }
        for row in master_rows
        if str(row["lang_id"]) not in matched_lang_ids
    ]
    master_missing_rows.sort(
        key=lambda row: (
            -parse_int(row["source_count"]),
            -int(parse_bool(row["in_pygments"])),
            -int(parse_bool(row["in_rosettacode"])),
            normalize_key(row["canonical_name"]),
        )
    )

    matched_rows = [row for row in match_rows if parse_bool(row["matched"])]
    summary = {
        "master_count": len(master_rows),
        "pl_list_count": len(pl_names),
        "pl_list_conflict_markers_ignored": pl_conflict_markers,
        "pl_list_matched": len(matched_rows),
        "pl_list_missing_from_master": len(pl_missing_rows),
        "master_missing_from_pl_list": len(master_missing_rows),
        "unique_master_lang_ids_matched": len(matched_lang_ids),
        "match_kind_counts": dict(match_counts),
        "matched_with_extensions": sum(1 for row in matched_rows if row["extensions"]),
        "matched_in_pygments": sum(1 for row in matched_rows if parse_bool(row["in_pygments"])),
        "matched_in_hyperpolyglot": sum(
            1 for row in matched_rows if parse_bool(row["in_hyperpolyglot"])
        ),
        "matched_in_rosettacode": sum(
            1 for row in matched_rows if parse_bool(row["in_rosettacode"])
        ),
        "matched_in_linguist": sum(1 for row in matched_rows if parse_bool(row["in_linguist"])),
        "matched_in_pldb": sum(1 for row in matched_rows if parse_bool(row["in_pldb"])),
        "sample_pl_list_missing": [row["pl_name"] for row in pl_missing_rows[:25]],
        "sample_master_missing": [row["canonical_name"] for row in master_missing_rows[:25]],
    }

    ensure_dir(out_dir)
    write_csv_rows(
        out_dir / "pl_list_matches_master.csv",
        [
            "pl_name",
            "matched",
            "match_kind",
            "master_lang_id",
            "master_name",
            "source_flags",
            "extensions",
            "in_pldb",
            "in_linguist",
            "in_wikipedia",
            "in_esolang",
            "in_hyperpolyglot",
            "in_pygments",
            "in_rosettacode",
            "fuzzy_candidates",
        ],
        match_rows,
    )
    write_csv_rows(
        out_dir / "pl_list_missing_from_master.csv",
        [
            "pl_name",
            "matched",
            "match_kind",
            "master_lang_id",
            "master_name",
            "source_flags",
            "extensions",
            "in_pldb",
            "in_linguist",
            "in_wikipedia",
            "in_esolang",
            "in_hyperpolyglot",
            "in_pygments",
            "in_rosettacode",
            "fuzzy_candidates",
        ],
        pl_missing_rows,
    )
    write_csv_rows(
        out_dir / "master_missing_from_pl_list.csv",
        [
            "canonical_name",
            "lang_id",
            "source_flags",
            "extensions",
            "source_count",
            "alias_count",
            "in_hyperpolyglot",
            "in_pygments",
            "in_rosettacode",
        ],
        master_missing_rows,
    )
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_lines = [
        "# Master Inventory vs pl_list",
        "",
        f"- Master rows: **{summary['master_count']}**",
        f"- `pl_list` rows: **{summary['pl_list_count']}**",
        f"- Ignored conflict-marker lines in `pl_list`: **{summary['pl_list_conflict_markers_ignored']}**",
        f"- `pl_list` matched to master: **{summary['pl_list_matched']}**",
        f"- `pl_list` missing from master: **{summary['pl_list_missing_from_master']}**",
        f"- Master rows missing from `pl_list`: **{summary['master_missing_from_pl_list']}**",
        f"- Unique master rows matched by `pl_list`: **{summary['unique_master_lang_ids_matched']}**",
        "",
        "## Match Kinds",
        "",
    ]
    for kind, count in sorted(summary["match_kind_counts"].items()):
        md_lines.append(f"- `{kind}`: {count}")

    md_lines.extend(
        [
            "",
            "## Coverage Across Matched pl_list Entries",
            "",
            f"- With extensions: {summary['matched_with_extensions']}",
            f"- In PLDB: {summary['matched_in_pldb']}",
            f"- In Linguist: {summary['matched_in_linguist']}",
            f"- In Hyperpolyglot: {summary['matched_in_hyperpolyglot']}",
            f"- In Pygments: {summary['matched_in_pygments']}",
            f"- In Rosetta Code: {summary['matched_in_rosettacode']}",
            "",
            "## Sample pl_list Names Missing From Master",
            "",
        ]
    )
    for name in summary["sample_pl_list_missing"]:
        md_lines.append(f"- {name}")

    md_lines.extend(["", "## Sample Master Rows Missing From pl_list", ""])
    for name in summary["sample_master_missing"]:
        md_lines.append(f"- {name}")

    (out_dir / "summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[ok] Wrote comparison report to {out_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build the master language inventory")
    build.add_argument("--pldb-dir", required=True, help="Path to a local PLDB clone")
    build.add_argument("--offline", action="store_true", help="Reuse cached raw files when available")
    build.add_argument("--fetch-only", action="store_true", help="Refresh raw files only")
    build.add_argument("--include-esolang", action="store_true", help="Include Esolang titles")
    build.set_defaults(func=build_inventory)

    compare = subparsers.add_parser(
        "compare", help="Compare the master inventory against data/pl_list.txt"
    )
    compare.add_argument(
        "--master",
        default=str(DERIVED_DIR / "languages_master_augmented_rosettacode.csv"),
        help="Path to the master inventory CSV",
    )
    compare.add_argument(
        "--aliases",
        default=str(DERIVED_DIR / "aliases.csv"),
        help="Path to aliases.csv",
    )
    compare.add_argument(
        "--pl-list",
        default=str(DATA_DIR / "pl_list.txt"),
        help="Path to pl_list.txt",
    )
    compare.add_argument(
        "--out-dir",
        default=str(REPORTS_DIR),
        help="Directory for comparison artifacts",
    )
    compare.set_defaults(func=compare_inventory)

    all_cmd = subparsers.add_parser("all", help="Run build then compare")
    all_cmd.add_argument("--pldb-dir", required=True, help="Path to a local PLDB clone")
    all_cmd.add_argument("--offline", action="store_true", help="Reuse cached raw files when available")
    all_cmd.add_argument("--include-esolang", action="store_true", help="Include Esolang titles")
    all_cmd.add_argument(
        "--out-dir",
        default=str(REPORTS_DIR),
        help="Directory for comparison artifacts",
    )

    def run_all(args: argparse.Namespace) -> None:
        build_inventory(args)
        compare_args = argparse.Namespace(
            master=str(DERIVED_DIR / "languages_master_augmented_rosettacode.csv"),
            aliases=str(DERIVED_DIR / "aliases.csv"),
            pl_list=str(DATA_DIR / "pl_list.txt"),
            out_dir=args.out_dir,
        )
        compare_inventory(compare_args)

    all_cmd.set_defaults(func=run_all)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
