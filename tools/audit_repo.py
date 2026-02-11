#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from util import canonical_name, code_hash

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES_DIR = ROOT / "languages"


@dataclass(frozen=True)
class Finding:
    kind: str  # e.g., integrity.hash_mismatch
    severity: str  # info|warn|error
    language: str | None = None
    language_folder: str | None = None
    program_sha256: str | None = None
    program_folder: str | None = None
    message: str = ""
    details: dict[str, Any] | None = None


@dataclass(frozen=True)
class ProgramRec:
    sha256: str
    title: str
    origin_url: str
    license_guess: str | None
    added_at: str
    code_path: str | None
    code_text: str | None


@dataclass(frozen=True)
class LangRec:
    name: str
    aliases: list[str]
    evidence_url: str
    added_at: str
    folder_rel: str
    programs: list[ProgramRec]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


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


def load_repo() -> list[LangRec]:
    langs: list[LangRec] = []
    for meta_path in sorted(LANGUAGES_DIR.rglob("meta.json")):
        meta = safe_read_json(meta_path)
        if not meta:
            continue
        name = str(meta.get("name") or "").strip()
        if not name:
            continue
        folder = meta_path.parent
        folder_rel = folder.relative_to(LANGUAGES_DIR).as_posix()
        programs: list[ProgramRec] = []
        programs_dir = folder / "programs"
        if programs_dir.is_dir():
            for prog_dir in sorted([p for p in programs_dir.iterdir() if p.is_dir()]):
                manifest_path = prog_dir / "manifest.json"
                manifest = safe_read_json(manifest_path) if manifest_path.exists() else None
                if not manifest:
                    continue
                sha256 = str(manifest.get("code_sha256") or prog_dir.name)
                code_file = find_program_code_file(prog_dir)
                code_text = None
                code_path = None
                if code_file and code_file.exists():
                    code_path = code_file.relative_to(ROOT).as_posix()
                    code_text = code_file.read_text(encoding="utf-8", errors="replace")
                programs.append(
                    ProgramRec(
                        sha256=sha256,
                        title=str(manifest.get("title") or ""),
                        origin_url=str(manifest.get("origin_url") or ""),
                        license_guess=str(manifest.get("license_guess")) if manifest.get("license_guess") else None,
                        added_at=str(manifest.get("added_at") or ""),
                        code_path=code_path,
                        code_text=code_text,
                    )
                )

        langs.append(
            LangRec(
                name=name,
                aliases=list(meta.get("aliases") or []),
                evidence_url=str(meta.get("evidence_url") or ""),
                added_at=str(meta.get("added_at") or ""),
                folder_rel=folder_rel,
                programs=programs,
            )
        )

    langs.sort(key=lambda l: l.name.lower())
    return langs


def nonempty_line_count(text: str) -> int:
    return sum(1 for ln in text.splitlines() if ln.strip())


def trigrams(s: str) -> set[str]:
    s = re.sub(r"\s+", " ", (s or "").strip().lower())
    if len(s) <= 3:
        return {s} if s else set()
    pad = f"  {s}  "
    return {pad[i : i + 3] for i in range(0, len(pad) - 2)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    union = len(a) + len(b) - inter
    return inter / union


def connected_components(nodes: list[str], edges: Iterable[tuple[str, str]]) -> list[list[str]]:
    parent = {n: n for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edges:
        if a in parent and b in parent:
            union(a, b)

    groups: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        groups[find(n)].append(n)
    return [sorted(g, key=str.lower) for g in groups.values()]


EXT_ALLOW: dict[str, set[str]] = {
    ".rs": {"rust"},
    ".py": {"python"},
    ".c": {"c"},
    ".cc": {"c++", "cpp"},
    ".cpp": {"c++", "cpp"},
    ".java": {"java"},
    ".js": {"javascript"},
    ".ts": {"typescript"},
    ".go": {"go"},
    ".ml": {"ocaml"},
    ".hs": {"haskell"},
    ".rb": {"ruby"},
    ".pl": {"perl"},
    ".php": {"php"},
    ".scala": {"scala"},
    ".r": {"r"},
    ".lua": {"lua"},
    ".kt": {"kotlin"},
    ".swift": {"swift"},
    ".cs": {"c#", "csharp"},
    ".jl": {"julia"},
    ".erl": {"erlang"},
    ".ex": {"elixir"},
    ".exs": {"elixir"},
    ".nim": {"nim"},
    ".zig": {"zig"},
    ".f90": {"fortran"},
    ".m": {"matlab"},
    ".wl": {"wolfram"},
    ".ijs": {"j"},
    ".rex": {"rexx", "oorexx", "netrexx"},
}


def ext_language_compatible(lang_name: str, ext: str) -> bool:
    ln = (lang_name or "").strip().lower()
    ok = EXT_ALLOW.get((ext or "").strip().lower())
    return (ok is None) or (ln in ok)


def audit_integrity(langs: list[LangRec]) -> list[Finding]:
    findings: list[Finding] = []
    for lang in langs:
        lang_folder = f"languages/{lang.folder_rel}"
        if not (lang.evidence_url or "").startswith(("http://", "https://")):
            findings.append(
                Finding(
                    kind="meta.bad_evidence_url",
                    severity="warn",
                    language=lang.name,
                    language_folder=lang_folder,
                    message="Evidence URL is missing or not http(s).",
                    details={"evidence_url": lang.evidence_url},
                )
            )
        for prog in lang.programs:
            prog_folder = f"{lang_folder}/programs/{prog.sha256}"
            if not prog.code_text:
                findings.append(
                    Finding(
                        kind="integrity.missing_code",
                        severity="error",
                        language=lang.name,
                        language_folder=lang_folder,
                        program_sha256=prog.sha256,
                        program_folder=prog_folder,
                        message="Program directory has no readable code file.",
                    )
                )
                continue

            if nonempty_line_count(prog.code_text) < 3:
                findings.append(
                    Finding(
                        kind="quality.trivial_code",
                        severity="warn",
                        language=lang.name,
                        language_folder=lang_folder,
                        program_sha256=prog.sha256,
                        program_folder=prog_folder,
                        message="Program code looks trivial (<3 non-empty lines).",
                    )
                )

            actual_sha = code_hash(prog.code_text)
            if actual_sha != prog.sha256:
                findings.append(
                    Finding(
                        kind="integrity.hash_mismatch",
                        severity="error",
                        language=lang.name,
                        language_folder=lang_folder,
                        program_sha256=prog.sha256,
                        program_folder=prog_folder,
                        message="Manifest code_sha256 does not match computed code hash.",
                        details={"manifest": prog.sha256, "computed": actual_sha, "code_path": prog.code_path},
                    )
                )

            if prog.code_path:
                ext = Path(prog.code_path).suffix
                if ext and not ext_language_compatible(lang.name, ext):
                    findings.append(
                        Finding(
                            kind="quality.ext_mismatch",
                            severity="warn",
                            language=lang.name,
                            language_folder=lang_folder,
                            program_sha256=prog.sha256,
                            program_folder=prog_folder,
                            message="File extension looks incompatible with language (heuristic; limited map).",
                            details={"ext": ext, "code_path": prog.code_path},
                        )
                    )

            try:
                u = urlparse(prog.origin_url or "")
                if u.netloc.lower() == "en.wikipedia.org":
                    findings.append(
                        Finding(
                            kind="quality.origin_is_wikipedia",
                            severity="info",
                            language=lang.name,
                            language_folder=lang_folder,
                            program_sha256=prog.sha256,
                            program_folder=prog_folder,
                            message="Origin URL is a Wikipedia page (may be fine, but often a smell).",
                            details={"origin_url": prog.origin_url},
                        )
                    )
            except Exception:
                pass
    return findings


def audit_duplicates(
    langs: list[LangRec],
    *,
    duplicate_threshold: float,
    max_pairs: int,
) -> tuple[list[Finding], list[dict[str, Any]]]:
    """
    Returns:
      - findings (definite duplicates: evidence_url duplicates, alias/name collisions)
      - fuzzy_pairs (candidates based on trigram Jaccard)
    """
    findings: list[Finding] = []
    evidence_map: dict[str, list[LangRec]] = defaultdict(list)
    name_map: dict[str, LangRec] = {}
    alias_map: dict[str, list[LangRec]] = defaultdict(list)

    for lang in langs:
        evidence = (lang.evidence_url or "").strip()
        if evidence:
            evidence_map[evidence].append(lang)
        name_map[canonical_name(lang.name).lower()] = lang
        for a in lang.aliases:
            aa = canonical_name(a).lower()
            if aa:
                alias_map[aa].append(lang)

    for evidence, ls in evidence_map.items():
        if len(ls) > 1:
            findings.append(
                Finding(
                    kind="dupe.evidence_url",
                    severity="warn",
                    message="Same evidence_url appears in multiple languages.",
                    details={"evidence_url": evidence, "languages": [l.name for l in ls]},
                )
            )

    for alias_norm, owners in alias_map.items():
        if alias_norm in name_map and name_map[alias_norm] not in owners:
            findings.append(
                Finding(
                    kind="dupe.alias_matches_name",
                    severity="warn",
                    message="An alias matches another canonical language name.",
                    details={
                        "alias": alias_norm,
                        "alias_of": [o.name for o in owners],
                        "matches_language": name_map[alias_norm].name,
                    },
                )
            )

    # Fuzzy candidates
    texts = []
    for lang in langs:
        blob = " ".join([lang.name] + list(lang.aliases or []))
        texts.append((lang.name, trigrams(blob)))

    pairs: list[dict[str, Any]] = []
    for i in range(len(texts)):
        n1, t1 = texts[i]
        for j in range(i + 1, len(texts)):
            n2, t2 = texts[j]
            sim = jaccard(t1, t2)
            if sim >= duplicate_threshold:
                pairs.append({"a": n1, "b": n2, "score": round(sim, 4)})

    pairs.sort(key=lambda x: x["score"], reverse=True)
    return findings, pairs[:max_pairs]


def build_related_and_clusters(
    langs: list[LangRec],
    *,
    related_k: int,
    cluster_threshold: float,
) -> tuple[dict[str, list[dict[str, Any]]], list[list[str]]]:
    """
    - related: per-language top-K neighbors (by trigram Jaccard on name+aliases)
    - clusters: connected components at similarity >= cluster_threshold
    """
    names = [l.name for l in langs]
    trig = {l.name: trigrams(" ".join([l.name] + list(l.aliases or []))) for l in langs}

    related: dict[str, list[dict[str, Any]]] = {n: [] for n in names}
    edges: list[tuple[str, str]] = []
    for i, a in enumerate(names):
        ta = trig[a]
        for j in range(i + 1, len(names)):
            b = names[j]
            sim = jaccard(ta, trig[b])
            if sim >= cluster_threshold:
                edges.append((a, b))
            if related_k > 0 and sim > 0:
                # Keep small neighbor lists; we'll trim later.
                related[a].append({"name": b, "score": sim})
                related[b].append({"name": a, "score": sim})

    for n in names:
        related[n].sort(key=lambda x: x["score"], reverse=True)
        related[n] = [{"name": x["name"], "score": round(x["score"], 4)} for x in related[n][:related_k]]

    clusters = [c for c in connected_components(names, edges) if len(c) > 1]
    clusters.sort(key=len, reverse=True)
    return related, clusters


def git_head() -> str | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            check=True,
            text=True,
            capture_output=True,
        )
        return (proc.stdout or "").strip() or None
    except Exception:
        return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Audit repository data quality (duplicates, integrity, clustering hints).")
    ap.add_argument("--out", default=str(ROOT / "web" / "dist" / "data" / "audit.json"), help="Output JSON path.")
    ap.add_argument("--duplicate-threshold", type=float, default=0.92, help="Trigram Jaccard threshold for dupe candidates.")
    ap.add_argument("--max-duplicate-pairs", type=int, default=80, help="Max fuzzy dupe candidate pairs to keep.")
    ap.add_argument("--related-k", type=int, default=5, help="Related languages to keep per language.")
    ap.add_argument("--cluster-threshold", type=float, default=0.62, help="Similarity threshold for clustering graph.")
    args = ap.parse_args(argv)

    if not LANGUAGES_DIR.exists():
        raise SystemExit(f"Missing {LANGUAGES_DIR}")

    langs = load_repo()

    integrity = audit_integrity(langs)
    dup_findings, dup_pairs = audit_duplicates(
        langs,
        duplicate_threshold=float(args.duplicate_threshold),
        max_pairs=int(args.max_duplicate_pairs),
    )
    related, clusters = build_related_and_clusters(
        langs,
        related_k=int(args.related_k),
        cluster_threshold=float(args.cluster_threshold),
    )

    # Small, aggregated stats for quick triage.
    origin_domains = Counter()
    license_guess = Counter()
    for lang in langs:
        for prog in lang.programs:
            if prog.origin_url:
                try:
                    origin_domains[urlparse(prog.origin_url).netloc.lower() or "(unknown)"] += 1
                except Exception:
                    origin_domains["(invalid url)"] += 1
            license_guess[prog.license_guess or "Unknown"] += 1

    payload: dict[str, Any] = {
        "generated_at": now_iso(),
        "repo_head": git_head(),
        "summary": {
            "languages": len(langs),
            "programs": sum(len(l.programs) for l in langs),
            "findings": len(integrity) + len(dup_findings),
        },
        "stats": {
            "top_origin_domains": origin_domains.most_common(15),
            "top_license_guess": license_guess.most_common(15),
        },
        "findings": [asdict(f) for f in (integrity + dup_findings)],
        "duplicate_candidates": dup_pairs,
        "clusters": clusters,
        "related": related,
    }

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[audit] wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
