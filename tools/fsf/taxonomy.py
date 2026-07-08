"""Enum vocabulary for the .fsf (FSL FEAT) judge + reclassifier."""

ARTIFACT_KINDS = [
    "fsl-feat-design",       # a FEAT first/higher-level design
    "fsl-melodic-config",    # MELODIC ICA config
    "tcl-script",            # generic Tcl `set` config, not FEAT
    "config-other",
    "data", "docs", "binary", "other",
]
FEAT_LEVELS = ["first-level", "higher-level", "not-applicable", "unknown"]
ANALYSIS_TYPES = ["task-glm", "resting-state-ica", "registration-only",
                  "group-stats", "unknown"]
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
