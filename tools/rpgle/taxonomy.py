"""Enum vocabulary for the `.rpgle` (IBM i / ILE RPG) judge + reclassifier.

The judge is asked "what IS this content, and which languages/notations does it
relate to?" — not merely "is it RPG?". `.rpgle` is RPG IV / ILE RPG source on
IBM i (AS/400); it can be a program, a module, a service-program procedure, or a
**copy/header member** of prototypes, and it commonly *embeds* SQL and calls CL.
"""

CONTENT_TYPES = [
    "source-code",             # a program / module / procedure
    "copybook-or-header",      # /copy or /include member: prototypes, constants
    "config", "data", "docs", "script", "binary", "other",
]

# RPG IV source formats — the central dialect axis.
SOURCE_FORMATS = [
    "fully-free",    # `**FREE` on line 1, modern free-form throughout
    "hybrid-free",   # fixed-format skeleton with /free … /end-free blocks
    "fixed-format",  # classic column-oriented spec letters (H F D C P O)
    "not-applicable", "unknown",
]

UNIT_KINDS = [
    "program",                       # has a main entry / cycle
    "module",                        # compiled unit, no main
    "procedure-or-service-program",  # exported procedures
    "copybook-prototype-header",     # /copy member of dcl-pr etc.
    "test", "snippet", "unknown",
]

DOMAINS = [
    "business-erp", "library-framework", "tooling-devtools",
    "web-api", "database", "education-tutorial", "demo-example",
    "test-suite", "utility", "other", "unknown",
]

MATURITIES = ["production-like", "library-quality", "student-exercise",
              "toy-or-hello-world", "snippet", "unknown"]

PLATFORMS = ["ibm-i-as400", "other", "unknown"]

NOT_RPGLE_LABELS = ["none", "data", "docs", "other-language", "binary",
                    "generated", "ambiguous"]

CONFIDENCES = ["high", "medium", "low"]

# reclassifier content-label vocabulary
RECLASS_LABELS = ["rpgle", "rpgle-copybook", "other", "data", "docs", "binary"]
RPGLE_LABELS = {"rpgle", "rpgle-copybook"}


def coerce(value, allowed, default="unknown"):
    return value if value in allowed else default
