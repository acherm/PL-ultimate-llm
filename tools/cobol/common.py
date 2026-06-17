"""Shared helpers for the COBOL-in-SWH study: paths, SWH fetch, caching.

Design notes
------------
- A *content* in these CSVs is a bare ``swh:1:cnt:<sha1_git>`` plus a
  filename. SWH serves the raw bytes anonymously by sha1_git:
      GET /api/1/content/sha1_git:<sha>/        -> metadata (length, checksums)
      GET /api/1/content/sha1_git:<sha>/raw/    -> the bytes
  We cache both under ``.cache/cobol/`` (gitignored) so re-runs are free.
- Anonymous access is rate-limited; set ``SWH_TOKEN`` for higher limits.
  We back off on HTTP 429 and honour ``X-RateLimit-Reset`` when present.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY_DIR = ROOT / "data" / "derived" / "cobol_study"
CACHE_DIR = ROOT / ".cache" / "cobol"
CSV_DIR = ROOT / "COBOL-SWH-extracted"

SWH_BASE = "https://archive.softwareheritage.org"
USER_AGENT = "PL-ultimate-llm/cobol-study"

# SWHID prefix for content objects.
CNT_PREFIX = "swh:1:cnt:"


def ensure_dirs() -> None:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    (STUDY_DIR / "reports").mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def sha1_git_of(swhid: str) -> str:
    """Extract the 40-hex sha1_git from a ``swh:1:cnt:<hex>`` SWHID."""
    s = swhid.strip()
    if s.startswith(CNT_PREFIX):
        s = s[len(CNT_PREFIX):]
    # Drop any qualifiers (;origin=…) if present.
    return s.split(";", 1)[0].strip()


def swh_headers() -> dict[str, str]:
    h = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    tok = os.environ.get("SWH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


# Upper bound on any single rate-limit sleep (a bit over one hour, since the
# SWH anonymous window is hourly). Lets a long background fetch ride out a full
# reset instead of failing, without risk of an unbounded stall.
_MAX_RL_SLEEP = 3700.0


def _reset_wait(headers, *, default: float = 0.0) -> float:
    reset = headers.get("X-RateLimit-Reset")
    if not reset:
        return default
    try:
        return max(0.0, float(reset) - time.time())
    except ValueError:
        return default


def _http_get(url: str, *, accept_json: bool, timeout: float = 30.0,
              max_retries: int = 4) -> bytes:
    """GET with rate-limit-aware backoff. Returns raw response body bytes.

    Proactively self-paces: when the response says few requests remain in the
    window, it sleeps until the window resets *before* returning — so a long
    sequential fetch never trips a 429. On an actual 429/5xx it honours the
    full ``X-RateLimit-Reset`` (capped at ~1h) and retries.
    """
    headers = swh_headers()
    if not accept_json:
        headers["Accept"] = "*/*"
    last_err: Exception | None = None
    for attempt in range(max_retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                remaining = r.headers.get("X-RateLimit-Remaining")
                if remaining is not None:
                    try:
                        if int(remaining) <= 2:
                            wait = min(_reset_wait(r.headers) + 1.0, _MAX_RL_SLEEP)
                            if wait > 0:
                                time.sleep(wait)
                    except ValueError:
                        pass
                return body
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504):
                wait = _reset_wait(e.headers, default=2.0 * (attempt + 1))
                time.sleep(min(wait, _MAX_RL_SLEEP) + 0.5)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
            continue
    raise RuntimeError(f"GET failed after {max_retries} tries: {url}: {last_err}")


@dataclass
class Content:
    sha1_git: str
    swhid: str
    filename: str
    raw: bytes
    length: int
    status: str = "visible"
    meta: dict = field(default_factory=dict)
    from_cache: bool = False

    @property
    def text(self) -> str:
        """Best-effort decode (COBOL sources are often latin-1/EBCDIC-origin)."""
        for enc in ("utf-8", "latin-1"):
            try:
                return self.raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return self.raw.decode("utf-8", errors="replace")

    @property
    def is_text(self) -> bool:
        # Heuristic: a NUL byte or a high ratio of non-printable bytes => binary.
        if b"\x00" in self.raw:
            return False
        if not self.raw:
            return True
        sample = self.raw[:4096]
        printable = sum(1 for b in sample if 9 <= b <= 13 or 32 <= b <= 126 or b >= 160)
        return printable / len(sample) > 0.85


def fetch_content(swhid: str, filename: str = "", *,
                  use_cache: bool = True, polite_delay: float = 0.0,
                  fetch_meta: bool = False) -> Content:
    """Fetch raw bytes for a content SWHID, with on-disk cache.

    SWH's anonymous quota is only ~120 req/h, so by default we make ONE
    request per content: ``/api/1/content/sha1_git:<sha>/raw/``. The
    sha1_git in our CSVs *is* the content identifier, so the bytes are
    self-verifying (length is derived locally). Pass ``fetch_meta=True``
    to also pull the metadata endpoint (status/checksums) at +1 request.
    """
    ensure_dirs()
    sha = sha1_git_of(swhid)
    raw_path = CACHE_DIR / f"{sha}.bin"
    meta_path = CACHE_DIR / f"{sha}.meta.json"

    if use_cache and raw_path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        raw = raw_path.read_bytes()
        return Content(sha1_git=sha, swhid=f"{CNT_PREFIX}{sha}",
                       filename=filename or meta.get("filename", ""),
                       raw=raw, length=meta.get("length", len(raw)),
                       status=meta.get("status", "visible"), meta=meta,
                       from_cache=True)

    meta_extra: dict = {}
    if fetch_meta:
        meta_url = f"{SWH_BASE}/api/1/content/sha1_git:{sha}/"
        m = json.loads(_http_get(meta_url, accept_json=True).decode("utf-8"))
        meta_extra = {"status": m.get("status", "visible"),
                      "checksums": m.get("checksums", {})}
        if polite_delay:
            time.sleep(polite_delay)

    raw_url = f"{SWH_BASE}/api/1/content/sha1_git:{sha}/raw/"
    raw = _http_get(raw_url, accept_json=False)
    if polite_delay:
        time.sleep(polite_delay)

    meta_out = {
        "sha1_git": sha,
        "filename": filename,
        "length": len(raw),
        "status": meta_extra.get("status", "visible"),
        "checksums": meta_extra.get("checksums", {}),
        "fetched_at": _now(),
    }
    raw_path.write_bytes(raw)
    meta_path.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")
    return Content(sha1_git=sha, swhid=f"{CNT_PREFIX}{sha}",
                   filename=filename, raw=raw,
                   length=meta_out["length"], status=meta_out["status"],
                   meta=meta_out, from_cache=False)


def _now() -> str:
    # Avoid argless datetime.now() restrictions; use time.time().
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))


def now_iso() -> str:
    return _now()
