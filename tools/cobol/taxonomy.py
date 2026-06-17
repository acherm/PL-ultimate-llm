"""Canonical vocabularies for the COBOL judge + normalizers.

Single source of truth shared by:
- `judge.py`   — builds an enum-constrained JSON Schema (cobol-judge/2) so the
                 model must pick from these values (with a free-text *detail*
                 field for nuance);
- `run_study.py` — normalizes verdicts for aggregation. The normalizers also
                 canonicalize the older free-text (cobol-judge/1) verdicts, so
                 a v1 run's distributions can be cleaned up with no re-judge.

Keep the lists short and stable; nuance lives in the `*_detail` free-text
fields, not in an ever-growing enum.
"""

from __future__ import annotations

# Compiler/vendor lineage. The "family" answers "which COBOL toolchain", the
# free-text detail captures the specific product/system (e.g. "JMA ORCA").
DIALECT_FAMILIES = [
    "ibm-mainframe",   # IBM Enterprise COBOL / OS/VS COBOL / z/OS
    "gnucobol",        # GnuCOBOL / OpenCOBOL
    "micro-focus",     # Micro Focus / Visual COBOL / Net Express
    "acucobol",        # ACUCOBOL-GT (Micro Focus extend)
    "rm-cobol",        # RM/COBOL (Liant)
    "fujitsu-nec",     # Fujitsu / NEC (Japanese mainframe & open systems)
    "other-vendor",
    "unknown",
]

STANDARDS = ["COBOL-68", "COBOL-74", "COBOL-85", "COBOL-2002", "COBOL-2014", "unknown"]
SOURCE_FORMATS = ["fixed", "free", "tab", "mixed", "unknown"]
PROGRAM_TYPES = ["batch", "online-cics", "subprogram", "copybook", "demo", "test", "unknown"]
MATURITIES = ["toy-or-hello-world", "student-exercise", "snippet", "production-like", "unknown"]
CONFIDENCES = ["high", "medium", "low"]

# "none" = the file IS COBOL (so there is no not-COBOL label).
NOT_COBOL_LABELS = [
    "none", "data", "docs", "copybook-only", "jcl",
    "other-language", "binary", "generated", "ambiguous",
]

DOMAINS = [
    "banking-finance", "insurance", "healthcare-medical", "government-public",
    "payroll-hr", "accounting-erp", "retail-commerce", "telecom",
    "manufacturing-logistics", "education-tutorial", "demo-example",
    "test-suite", "utility-tooling", "other", "unknown",
]

# --- normalizers: free-text -> canonical enum --------------------------------
# Keyword rules are checked in priority order; the first hit wins. Tuned to the
# v1 verdicts actually observed in this corpus.

_DIALECT_RULES = [
    ("gnucobol", ("gnucobol", "open cobol", "opencobol")),
    ("micro-focus", ("micro focus", "microfocus", "visual cobol", "net express", "mf cobol")),
    ("acucobol", ("acucobol", "acu cobol")),
    ("rm-cobol", ("rm/cobol", "rm-cobol", "rmcobol", "liant")),
    ("fujitsu-nec", ("fujitsu", "nec ")),
    ("ibm-mainframe", ("ibm", "enterprise cobol", "z/os", "os/vs", "mainframe", "cics")),
]

_DOMAIN_RULES = [
    ("healthcare-medical", ("medical", "health", "receipt", "orca", "jma",
                            "patient", "hospital", "dpc", "pdps")),
    ("insurance", ("insurance compan", "life insurance", "property insurance",
                   "actuar", "underwrit", "policy admin")),
    ("payroll-hr", ("payroll", "human resource", " hr ", "salary", "wage")),
    ("banking-finance", ("bank", "atm", "credit card", "securities", "trading",
                         "loan", "mortgage")),
    ("accounting-erp", ("accounting", "account payable", "accounts payable",
                        "accounts receivable", "ledger", "erp", "creditor",
                        "debtor", "invoic", "vat", "billing", "purchase ledger",
                        "general ledger", "finance")),
    ("retail-commerce", ("retail", "point of sale", " pos ", "commerce",
                         "inventory", "sales order", "warehouse")),
    ("telecom", ("telecom", "telephon", "billing call", "switch")),
    ("manufacturing-logistics", ("manufactur", "logistic", "supply chain",
                                 "shipping", "production planning")),
    ("government-public", ("government", "public sector", "municipal", "tax ",
                           "census", "social security")),
    ("test-suite", ("test suite", "ccvs", "validation suite", "conformance",
                    "test program")),
    ("education-tutorial", ("education", "tutorial", "training", "student",
                            "learn", "exercise", "academic", "course", "teaching")),
    ("demo-example", ("demo", "example", "hello world", "sample", "playpen",
                      "snippet", "rosetta")),
    ("utility-tooling", ("utility", "tooling", "helper", "library routine",
                         "conversion", "format")),
]


def _match(text: str, rules) -> str | None:
    t = (text or "").lower()
    for canon, kws in rules:
        if any(kw in t for kw in kws):
            return canon
    return None


def normalize_dialect_family(value: str) -> str:
    """Map a free-text dialect/family string to a canonical family."""
    if value in DIALECT_FAMILIES:
        return value
    return _match(value, _DIALECT_RULES) or "unknown"


def normalize_domain(value: str) -> str:
    if value in DOMAINS:
        return value
    return _match(value, _DOMAIN_RULES) or ("unknown" if not value else "other")


def coerce_enum(value: str, allowed: list[str], default: str = "unknown") -> str:
    """Exact-match coercion (used as a safety net on enum-native v2 output)."""
    return value if value in allowed else default
