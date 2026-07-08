"""Enum vocabulary for the .fsf judge + reclassifier.

The judge's job is to characterise *what the content is* and *what languages/
notations it relates to* — not to confirm a single preconceived language. An
extension is polysemous: `.fsf` is dominantly FSL FEAT, but a FEAT file is
expressed in Tcl `set`-syntax (so it *relates to* Tcl), and other `.fsf` files
may be something else entirely.
"""

# Coarse "what kind of content is this" — the primary aggregation axis.
CONTENT_TYPES = [
    "config-or-dsl",   # a configuration / domain-specific language (FEAT etc.)
    "source-code",     # a general-purpose program
    "script",          # a shell/interpreter script
    "data",            # tabular / serialized data
    "markup",          # XML/HTML/Markdown-like
    "schema",          # a schema / interface definition
    "docs", "log", "binary", "mixed", "other",
]

ARTIFACT_KINDS = [   # kept for FEAT-specific detail
    "fsl-feat-design", "fsl-melodic-config", "tcl-script",
    "config-other", "data", "docs", "binary", "other",
]
FEAT_LEVELS = ["first-level", "higher-level", "not-applicable", "unknown"]
ANALYSIS_TYPES = ["task-glm", "resting-state-ica", "registration-only",
                  "group-stats", "not-applicable", "unknown"]
GENERATED = ["gui-generated", "hand-edited", "unknown"]
DOMAINS = ["neuroimaging-fmri", "other", "unknown"]
NOT_FSF_LABELS = ["none", "data", "docs", "other-format", "binary"]
CONFIDENCES = ["high", "medium", "low"]

# reclassifier content-label vocabulary
RECLASS_LABELS = ["fsl-feat", "tcl-other", "config-other", "data",
                  "binary", "other"]
FEAT_LABELS = {"fsl-feat"}


def coerce(value, allowed, default="unknown"):
    return value if value in allowed else default
