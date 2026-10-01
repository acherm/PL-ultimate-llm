#!/usr/bin/env python3
"""Ingest reviews submitted through the online review page (GitHub issues).

The review page (/review/study/<study>/, web/build_site.py) lets anyone with a
GitHub account review the files a study publishes in
`data/derived/study_exports/<study>/review_items.json`. Reviews are submitted as
a GitHub issue (form `.github/ISSUE_TEMPLATE/review.yml`, label `review`) whose
body carries a JSON batch:

    {"schema": "review-batch/1", "study": "m", "expertise": {...},
     "reviews": [{"sha1_git": "...", "language": "matlab", "confidence": "high",
                  "content_type": "...", ..., "notes": "...", "saved_at": "..."}]}

This script turns a batch into review-store records — one immutable file per
review in `reviews/<sha1_git>/` (tools/reviewstore.py, docs/reviews.md) — with
the exact study answer kept in a `study` block, so the study reads them back
(tools/m/data.py) and the site shows them on sample cards.

Who may submit: GitHub logins listed in `data/curated/reviewers.csv` are
ingested directly; a newcomer's first batch waits until a maintainer adds the
label `review-approved`, which adds the login to that file.

After ingesting, the bot replies on the issue with the study's machine labels
for the same files (the reveal — the page itself never shows them), labels the
issue `review-ingested` and closes it.

    python3 tools/ingest_reviews.py --issue 123            # CI (GH_TOKEN set)
    python3 tools/ingest_reviews.py --all                  # every open `review` issue
    python3 tools/ingest_reviews.py --body-file b.md --author acherm --dry-run   # local test
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
import reviewstore as RS  # noqa: E402

REPO = os.environ.get("GITHUB_REPOSITORY", "acherm/PL-ultimate-llm")
EXPORTS = ROOT / "data" / "derived" / "study_exports"
REVIEWERS_CSV = ROOT / "data" / "curated" / "reviewers.csv"
REVIEWER_FIELDS = ["login", "reviewer_id", "approved_by", "approved_at", "note"]
BATCH_SCHEMA = "review-batch/1"
VIA = "review-page"
LABEL_SUBMIT, LABEL_APPROVED, LABEL_DONE = "review", "review-approved", "review-ingested"
MAX_REVIEWS, MAX_NOTES = 200, 4000
MARK_WAIT = "<!-- review-bot:awaiting-approval -->"
MARK_DONE = "<!-- review-bot:ingested -->"
_JSON_BLOCK = re.compile(r"```(?:json)?\s*\n(.*?)\n```", re.S)


# ---------------------------------------------------------------- GitHub
def gh(*args: str, input_text: str | None = None) -> str:
    return subprocess.run(["gh", *args], input=input_text, capture_output=True, text=True, check=True).stdout


def fetch_issue(number: int) -> dict:
    d = json.loads(gh("api", f"repos/{REPO}/issues/{number}"))
    comments = json.loads(gh("api", f"repos/{REPO}/issues/{number}/comments?per_page=100"))
    return {"number": d["number"], "body": d.get("body") or "", "author": d["user"]["login"],
            "labels": [x["name"] for x in d.get("labels", [])], "url": d["html_url"],
            "created_at": d["created_at"], "state": d["state"],
            "comments": [c.get("body") or "" for c in comments]}


def open_review_issues() -> list[int]:
    out = json.loads(gh("api", f"repos/{REPO}/issues?labels={LABEL_SUBMIT}&state=open&per_page=100"))
    return [d["number"] for d in out if "pull_request" not in d]


def comment(number: int, body: str) -> None:
    gh("api", "-X", "POST", f"repos/{REPO}/issues/{number}/comments", "-F", "body=@-", input_text=body)


def finish(number: int) -> None:
    gh("api", "-X", "POST", f"repos/{REPO}/issues/{number}/labels", "-f", f"labels[]={LABEL_DONE}")
    gh("api", "-X", "PATCH", f"repos/{REPO}/issues/{number}", "-f", "state=closed", "-f", "state_reason=completed")


# ---------------------------------------------------------------- reviewers
def reviewers() -> dict[str, dict]:
    if not REVIEWERS_CSV.exists():
        return {}
    with REVIEWERS_CSV.open(encoding="utf-8") as f:
        return {r["login"].lower(): r for r in csv.DictReader(f)}


def approve(login: str, approved_by: str) -> str:
    """Add a newcomer to reviewers.csv; returns their reviewer id."""
    known = reviewers()
    taken = {r["reviewer_id"] for r in known.values()}
    rid = RS.slugify(login) or "reviewer"
    if rid in taken:
        rid = "gh-" + rid
    with REVIEWERS_CSV.open("a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=REVIEWER_FIELDS).writerow(
            {"login": login, "reviewer_id": rid, "approved_by": approved_by,
             "approved_at": dt.date.today().isoformat(), "note": "approved via the review-approved label"})
    return rid


# ---------------------------------------------------------------- batch
def parse_batch(body: str) -> dict:
    m = _JSON_BLOCK.search(body)
    raw = m.group(1) if m else body.strip()
    try:
        batch = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"the issue body has no valid JSON batch ({e.msg} at line {e.lineno})") from None
    if not isinstance(batch, dict) or batch.get("schema") != BATCH_SCHEMA:
        raise ValueError(f"the JSON batch must have \"schema\": \"{BATCH_SCHEMA}\"")
    if not re.fullmatch(r"[a-z0-9_]+", str(batch.get("study", ""))):
        raise ValueError("the JSON batch names no valid study")
    if not isinstance(batch.get("reviews"), list) or not batch["reviews"]:
        raise ValueError("the JSON batch has no reviews")
    if len(batch["reviews"]) > MAX_REVIEWS:
        raise ValueError(f"at most {MAX_REVIEWS} reviews per issue")
    return batch


def load_spec(study: str) -> dict:
    p = EXPORTS / study / "review_items.json"
    if not p.exists():
        raise ValueError(f"study {study!r} publishes no review items")
    return json.loads(p.read_text(encoding="utf-8"))


def check(rv: dict, spec: dict, items: dict) -> tuple[dict | None, str | None]:
    """Validate one review against the published fields; returns (answer, error)."""
    if not isinstance(rv, dict):
        return None, "not an object"
    sha = str(rv.get("sha1_git", ""))
    if sha not in items:
        return None, f"`{sha[:12]}` is not in the published review queue"
    ans = {}
    for f in spec["fields"]:
        v = rv.get(f["id"], "")
        v = "" if v is None else str(v).strip()
        if f.get("type") == "text":
            if len(v) > MAX_NOTES:
                return None, f"`{items[sha]['filename']}`: {f['id']} longer than {MAX_NOTES} characters"
        elif v and v not in {o["value"] for o in f.get("options", [])}:
            return None, f"`{items[sha]['filename']}`: {f['id']} = {v!r} is not a listed option"
        if f.get("required") and not v:
            return None, f"`{items[sha]['filename']}`: {f['id']} is required"
        ans[f["id"]] = v
    return ans, None


def ingest(issue: dict, *, dry_run: bool, approved_by: str) -> dict:
    """Returns {"status", "written", "skipped", "errors", "reply"}."""
    try:
        batch = parse_batch(issue["body"])
        spec = load_spec(batch["study"])
        mod = importlib.import_module(f"tools.{batch['study']}.export")
    except (ValueError, ModuleNotFoundError) as e:
        return {"status": "invalid", "errors": [str(e)], "written": 0, "skipped": 0,
                "reply": f"{MARK_DONE}\nThis issue could not be read: {e}. Please submit from the review page."}

    login = issue["author"]
    who = reviewers().get(login.lower())
    if who is None:
        if LABEL_APPROVED not in issue["labels"]:
            return {"status": "awaiting-approval", "errors": [], "written": 0, "skipped": 0,
                    "reply": None if any(MARK_WAIT in c for c in issue["comments"]) else
                    f"{MARK_WAIT}\nThanks @{login}! This is your first batch: a maintainer will look at it and "
                    f"add the `{LABEL_APPROVED}` label, after which your reviews are ingested automatically "
                    f"(and your next batches directly)."}
        rid = "gh-" + RS.slugify(login) if dry_run else approve(login, approved_by)
    else:
        rid = who["reviewer_id"]

    items = {it["sha1_git"]: it for it in spec["items"]}
    answers, errors = {}, []
    for rv in batch["reviews"]:
        ans, err = check(rv, spec, items)
        if err:
            errors.append(err)
        else:
            answers[rv["sha1_git"]] = (ans, rv)          # last review of a file in the batch wins

    known = set(RS.load_pl_index())
    written = skipped = 0
    for sha, (ans, rv) in answers.items():
        rec = RS.new_review(
            subject={"sha1_git": sha, "filename": items[sha]["filename"], "ext": spec.get("ext", "")},
            reviewer={"kind": "human", "id": rid},
            label=mod.review_label(ans), confidence=ans.get("confidence") or "medium",
            comment=ans.get("notes"),
            shown={"study": batch["study"], "via": VIA, "blind": True, "machine_labels_shown": False,
                   "audit": spec.get("queue") == "audit", "issue": issue["url"],
                   "expertise": batch.get("expertise") if isinstance(batch.get("expertise"), dict) else None,
                   "saved_at": str(rv.get("saved_at", ""))[:32] or None})
        rec["created_at"] = issue["created_at"]            # deterministic: re-runs write nothing new
        rec["study"] = {"id": batch["study"], "schema": f"{batch['study']}-review/1",
                        "human": {k: v for k, v in ans.items()}}
        problems = RS.validate_review(rec, known)
        if problems:
            errors.append(f"`{items[sha]['filename']}`: " + "; ".join(problems))
            continue
        if dry_run:
            written += 1
            continue
        try:
            RS.write_review(rec, known_pl_ids=known)
            written += 1
        except FileExistsError:
            skipped += 1

    reply = None
    if written or errors:
        reply = reveal(mod, answers, items, rid, written, skipped, errors)
    return {"status": "ingested", "written": written, "skipped": skipped, "errors": errors, "reply": reply}


def reveal(mod, answers: dict, items: dict, rid: str, written: int, skipped: int, errors: list[str]) -> str:
    lines = [MARK_DONE, f"Thanks! **{written}** review(s) recorded as `{rid}` in `reviews/`"
             + (f" ({skipped} already there)" if skipped else "") + "."]
    labels = mod.judge_labels(list(answers)) if hasattr(mod, "judge_labels") else {}
    if labels and answers:
        models = sorted({m for v in labels.values() for m in v})
        both = sum(1 for sha, (ans, _) in answers.items()
                   if labels.get(sha) and all(labels[sha].get(m) == ans["language"] for m in models))
        lines += ["", f"**How the study's LLM judges labelled the same files** — you agree with both on "
                      f"{both} of {len(answers)}:", "",
                  "| file | you | " + " | ".join(models) + " |", "|---|---|" + "---|" * len(models)]
        for sha, (ans, _) in answers.items():
            cells = [f"`{labels.get(sha, {}).get(m) or '—'}`" + (" ✓" if labels.get(sha, {}).get(m) == ans["language"] else "")
                     for m in models]
            lines.append(f"| `{items[sha]['filename']}` | `{ans['language']}` | " + " | ".join(cells) + " |")
        lines += ["", "Disagreeing is fine: the audit measures the judges against you, not the other way round."]
    if errors:
        lines += ["", "**Not recorded:**"] + [f"- {e}" for e in errors]
    return "\n".join(lines)


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--issue", type=int, help="issue number")
    g.add_argument("--all", action="store_true", help="every open issue labelled `review`")
    g.add_argument("--body-file", type=Path, help="local test: an issue body")
    ap.add_argument("--author", default="acherm", help="with --body-file: the issue author")
    ap.add_argument("--dry-run", action="store_true", help="validate and print, write nothing")
    a = ap.parse_args()
    approved_by = os.environ.get("GITHUB_ACTOR", "maintainer")

    if a.body_file:
        issue = {"number": 0, "body": a.body_file.read_text(encoding="utf-8"), "author": a.author,
                 "labels": [LABEL_SUBMIT], "url": "local:" + a.body_file.name,
                 "created_at": RS.utc_now_iso(), "state": "open", "comments": []}
        res = ingest(issue, dry_run=a.dry_run, approved_by=approved_by)
        print(json.dumps({k: v for k, v in res.items() if k != "reply"}, indent=1))
        print("\n--- reply ---\n" + (res["reply"] or "(none)"))
        return 0 if res["status"] != "invalid" else 1

    numbers = open_review_issues() if a.all else [a.issue]
    for n in numbers:
        issue = fetch_issue(n)
        if LABEL_SUBMIT not in issue["labels"] or LABEL_DONE in issue["labels"]:
            print(f"#{n}: not a pending review issue — skipped")
            continue
        res = ingest(issue, dry_run=a.dry_run, approved_by=approved_by)
        print(f"#{n}: {res['status']} · written {res['written']} · already there {res['skipped']} · "
              f"errors {len(res['errors'])}")
        if a.dry_run:
            print(res["reply"] or "")
            continue
        if res["reply"] and res["reply"] not in issue["comments"]:      # no duplicate replies on re-runs
            comment(n, res["reply"])
        if res["status"] == "ingested" and (res["written"] or res["skipped"]) and not res["errors"]:
            finish(n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
