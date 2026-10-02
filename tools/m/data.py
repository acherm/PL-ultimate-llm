"""Merge every label layer of the `.m` study into one record per content.

    from tools.m.data import load
    recs = load()          # {sha: Rec}

A record carries the worklist row (frames, ranks, population weights), the
deterministic labels, Synid, every judge layer present on disk, and the human
reviews / group rules from `reviews_m/` (local review app) and `reviews/`
(online review page → GitHub issue → tools/ingest_reviews.py). Each *labeller* is exposed under a
uniform name → language label, so agreement code never special-cases a tool.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "data" / "derived" / "m_study"
WORKLIST = STUDY / "worklist_all.csv"
LABELS = STUDY / "labels"
JUDGE = STUDY / "judge"
SYNID = STUDY / "synid.jsonl"
REVIEWS = ROOT / "reviews_m"
RULES_FILE = REVIEWS / "_rules.jsonl"
# The encyclopedia's review store. Reviews submitted through the online review
# page land there (one record per review, `study.id == "m"`, `shown.via ==
# "review-page"`); the study reads them back in its own m-review/1 shape.
ONLINE_REVIEWS = ROOT / "reviews"
ONLINE_VIA = "review-page"

J1 = "anthropic__claude-sonnet-4.6"
J2 = "google__gemini-3.8-flash"
J1_IND = "anthropic__claude-sonnet-4.6+ind"

NON_CODE_TYPES = {"markup-or-xml", "docs-or-text", "binary", "empty-or-trivial", "config"}

SYNID_MAP = {
    "Objective-C": "objective-c", "MATLAB": "matlab", "Mercury": "mercury", "M": "mumps-m",
    "MUF": "muf", "Limbo": "limbo", "Mason": "mason", "Wolfram Language": "mathematica-wolfram",
    "Mathematica": "mathematica-wolfram", "Text": "unknown", "Octave": "octave",
}

# Labeller registry: name → (kind, short description)
LABELLERS = {
    "judge": ("llm", "claude-sonnet-4.6, blind"),
    "judge2": ("llm", "gemini-3.8-flash, blind"),
    "judge_ind": ("llm", "claude-sonnet-4.6 shown indicators (ablation)"),
    "ours": ("rules", "m-reclass/2 (this study, tuned on U ranks 1-300)"),
    "ours_v1": ("rules", "m-reclass/1 (frozen before any judge label)"),
    "linguist": ("rules", "Linguist .m heuristics (abstain → unknown)"),
    "pygments": ("rules", "Pygments guess_lexer_for_filename"),
    "synid": ("tool", "SWH Synid 9bc1c32, default content strategies"),
    "synid_nc": ("tool", "SWH Synid, without the comment strategy"),
}


def synid_lang(v) -> str:
    if not v:
        return "unknown"
    if len(v) > 1:
        return "unresolved"
    return SYNID_MAP.get(v[0], "other-programming-language")


@dataclass
class Rec:
    sha: str
    row: dict
    labels: dict | None = None
    synid: dict | None = None
    judges: dict = field(default_factory=dict)      # layer-name → verdict dict
    judge_meta: dict = field(default_factory=dict)  # layer-name → full record (usage…)
    reviews: list = field(default_factory=list)
    rule: dict | None = None

    # --- frames -------------------------------------------------------------
    @property
    def u_rank(self):
        return int(self.row["u_rank"]) if self.row.get("u_rank") else None

    @property
    def d_rank(self):
        return int(self.row["d_rank"]) if self.row.get("d_rank") else None

    @property
    def t_rank(self):
        return int(self.row["t_rank"]) if self.row.get("t_rank") else None

    def in_frame(self, frame: str, n: int | None = None) -> bool:
        r = {"U": self.u_rank, "R": self.d_rank, "T": self.t_rank}.get(frame)
        return r is not None and (n is None or r <= n)

    # --- labels -------------------------------------------------------------
    def v(self, layer="judge") -> dict | None:
        key = {"judge": J1, "judge2": J2, "judge_ind": J1_IND}.get(layer, layer)
        return self.judges.get(key)

    def lang(self, labeller: str) -> str | None:
        """Language label from one labeller, or None if that layer is absent."""
        if labeller in ("judge", "judge2", "judge_ind"):
            v = self.v(labeller)
            if not v:
                # binary contents are never sent to the judges: they are, by construction, not code
                if self.labels is not None and not self.labels["indicators"].get("is_text", True) \
                        and labeller in ("judge", "judge2"):
                    return "not-code"
                return None
            lang = v.get("language")
            # normalisation (documented in the report): a judge that says language
            # "unknown" while typing the content as markup/text/binary/empty means "not code"
            if lang == "unknown" and v.get("content_type") in NON_CODE_TYPES:
                return "not-code"
            # ...and one that names "other"/"unknown" while its own is_programming_language
            # field says False (treebank XML, data matrices) is taken at its word: not code
            if lang in ("other-programming-language", "unknown") and v.get("is_programming_language") is False:
                return "not-code"
            return lang
        if labeller == "human":
            h = self.human()
            return h.get("language") if h else None
        if self.labels is None:
            return None
        if labeller in ("ours", "ours_v1", "linguist", "pygments"):
            return self.labels[labeller]["lang"]
        if labeller == "synid":
            return synid_lang(self.synid.get("default")) if self.synid else None
        if labeller == "synid_nc":
            return synid_lang(self.synid.get("nocomment")) if self.synid else None
        raise KeyError(labeller)

    def human_latest(self) -> list[dict]:
        """Each human reviewer's latest review (a reviewer revises by writing a new one)."""
        latest: dict[str, dict] = {}
        for rv in self.reviews:
            if rv.get("human"):
                latest[(rv.get("reviewer") or {}).get("id") or "?"] = rv
        return sorted(latest.values(), key=lambda rv: rv.get("created_at") or "")

    def human(self) -> dict | None:
        """The human reference label: one reviewer → their latest review; several →
        the label they agree on (`unsure` abstains), or `unsure` with `_disputed`
        when they disagree, so a disputed file drops out of accuracy estimates."""
        latest = self.human_latest()
        if latest:
            langs = {rv["human"].get("language") for rv in latest} - {"unsure", "", None}
            if len(langs) <= 1:
                agreeing = [rv for rv in latest if rv["human"].get("language") in langs] or latest
                return agreeing[-1]["human"]
            return {"language": "unsure", "_disputed": sorted(langs)}
        if self.rule:
            return {"language": self.rule.get("label"), "_rule": True}
        return None

    def human_reviewers(self) -> list[str]:
        """Reviewers whose latest label is the reference label (for `verified_by`)."""
        h = self.human()
        if not h or h.get("_rule") or h.get("_disputed"):
            return []
        return [(rv.get("reviewer") or {}).get("id") for rv in self.human_latest()
                if rv["human"].get("language") == h.get("language")]

    @property
    def ind(self) -> dict:
        return (self.labels or {}).get("indicators", {})


def _load_json_dir(d: Path) -> dict:
    out = {}
    if d.is_dir():
        for p in d.glob("*.json"):
            try:
                out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return out


def load_rules() -> list[dict]:
    out = []
    if RULES_FILE.exists():
        for line in RULES_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def rule_for(row: dict, rules: list[dict]) -> dict | None:
    for rule in reversed(rules):              # latest assertion wins
        v = rule.get("value") or ""
        if rule.get("scope") == "origin" and row.get("origin") == v:
            return rule
        if rule.get("scope") in ("filename", "path") and v:
            target = row.get("name", "") if rule["scope"] == "filename" else row.get("path", "")
            try:
                if re.search(v, target or ""):
                    return rule
            except re.error:
                pass
    return None


def _online_reviews(sha: str) -> list[dict]:
    """Online reviews of this content from the encyclopedia store, as m-review/1 dicts."""
    d = ONLINE_REVIEWS / sha
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        study, shown = rec.get("study") or {}, rec.get("shown") or {}
        # reviews from the review page, and corrections recorded at a reviewer's
        # request (shown.via == "correction"); copies propagated from reviews_m/
        # carry no `study` block and are skipped
        if study.get("id") != "m" or not study.get("human"):
            continue
        out.append({"schema": "m-review/1", "subject": rec.get("subject"),
                    "reviewer": {"kind": "human", "id": (rec.get("reviewer") or {}).get("id")},
                    "blind": bool(shown.get("blind")), "audit": bool(shown.get("audit")),
                    "human": study["human"], "created_at": rec.get("created_at"),
                    "source": shown.get("issue"), "online": True})
    return out


def reviews_for(sha: str) -> list[dict]:
    d = REVIEWS / sha
    out = []
    if d.is_dir():
        for p in sorted(d.glob("*.json")):
            try:
                out.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                pass
    out += _online_reviews(sha)
    return sorted(out, key=lambda rv: rv.get("created_at") or "")


def load(with_reviews: bool = True) -> dict[str, Rec]:
    from tools.m.study import worklist
    rows = {r["sha1_git"]: r for r in worklist()}
    labels = _load_json_dir(LABELS)
    syn = {}
    if SYNID.exists():
        for line in SYNID.open(encoding="utf-8"):
            d = json.loads(line)
            syn[d["sha1_git"]] = d
    judges = {}
    if JUDGE.is_dir():
        for d in JUDGE.iterdir():
            if d.is_dir():
                judges[d.name] = _load_json_dir(d)
    rules = load_rules() if with_reviews else []
    recs = {}
    for sha, row in rows.items():
        r = Rec(sha=sha, row=row, labels=labels.get(sha), synid=syn.get(sha))
        for layer, by in judges.items():
            j = by.get(sha)
            if j and j.get("parse_ok") and isinstance(j.get("verdict"), dict):
                r.judges[layer] = j["verdict"]
                r.judge_meta[layer] = j
        if with_reviews:
            r.reviews = reviews_for(sha)
            r.rule = rule_for(row, rules)
        recs[sha] = r
    return recs
