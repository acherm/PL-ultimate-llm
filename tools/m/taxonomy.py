"""Enum vocabulary for the `.m` judge, labellers and review tool.

`.m` is the most polysemous extension studied so far. The mapping
(`data/derived/pl_taxonomy/ext_claim.csv`) lets it claim MATLAB, Octave,
Objective-C, Mercury, Wolfram/Mathematica, M (MUMPS), Limbo and MUF — and, via
a join bug, M4 / Monkey C / Win32 Message File (Pygments' *Mason*). Content
reading added **Magma**, **Maple** and non-code (treebank XML, generated
expressions) to the list. So the central axis is `language`, not "is it X?".
"""

# The language axis. "matlab" means MATLAB-family syntax that runs in MATLAB
# (and usually Octave); "octave" is reserved for files using Octave-only syntax.
LANGUAGES = [
    "objective-c",
    "matlab",
    "octave",
    "mathematica-wolfram",
    "mercury",
    "mumps-m",
    "magma",
    "maple",
    "scilab",
    "limbo",
    "muf",
    "mason",
    "c-or-cpp",
    "other-programming-language",
    "not-code",
    "unknown",
]

# What the extension→PL mapping claims (pl_id in ext_claim.csv) per language.
MAPPING_CLAIMS = {
    "objective-c": "pl/objective-c", "matlab": "pl/matlab", "octave": "pl/octave",
    "mathematica-wolfram": "pl/wolfram-language", "mercury": "pl/mercury",
    "mumps-m": "pl/m", "limbo": "pl/limbo", "muf": "pl/muf",
}
UNCLAIMED = {"magma", "maple", "scilab", "mason", "c-or-cpp",
             "other-programming-language"}

CONTENT_TYPES = [
    "source-code",           # hand-written program/function/class/module
    "generated-code",        # emitted by a tool: templates, codegen, symbolic output
    "data-or-expression",    # numbers/expressions/tables with no control flow
    "markup-or-xml",
    "docs-or-text",
    "config",
    "binary",
    "empty-or-trivial",
    "other",
]

# How the file came to exist — the axis that explains duplication in `.m`.
PROVENANCE_KINDS = [
    "hand-written",
    "ide-or-framework-template",   # Xcode/RN/Flutter/CocoaPods boilerplate
    "tool-generated",              # codegen, symbolic export, GUIDE, class-dump
    "vendored-third-party",        # a copy of a known library inside an app
    "decompiled-or-dumped",
    "unknown",
]

UNIT_KINDS = [
    "class-implementation",   # ObjC @implementation / MATLAB classdef / category
    "function-file",          # MATLAB function file
    "script",                 # MATLAB script (no function header)
    "program-entry",          # ObjC main.m
    "test",
    "module-or-package",      # Mercury/Limbo module, Mathematica package, Magma package
    "routine",                # MUMPS routine
    "declarations-only",
    "data",
    "other",
    "unknown",
]

# MATLAB vs Octave is a *portability* question, not an identity one.
MATLAB_DIALECTS = [
    "portable-matlab-octave",  # nothing ties it to one implementation
    "matlab-specific",         # classdef-only features, toolboxes, App Designer, `arguments`
    "octave-specific",         # `#` comments, endfunction/endif, printf, ++, !=, `1;`
    "not-applicable",
    "unclear",
]

DOMAINS = [
    "mobile-desktop-app",          # iOS/macOS apps
    "mobile-library-framework",    # iOS/macOS SDKs, UI components
    "numerical-scientific",
    "signal-image-processing",
    "machine-learning-data",
    "control-robotics",
    "engineering-simulation",
    "neuro-psych-bio-medical",
    "computer-algebra-math",
    "education-coursework",
    "healthcare-records",          # MUMPS/VistA
    "linguistics-nlp",
    "compiler-language-tooling",
    "games-graphics",
    "test-suite",
    "utility",
    "other",
    "unknown",
]

MATURITIES = ["production-like", "library-quality", "research-code",
              "student-exercise", "toy-or-hello-world", "snippet", "unknown"]

CONFIDENCES = ["high", "medium", "low"]

# Labels produced by the deterministic labellers → our LANGUAGES vocabulary.
LINGUIST_TO_LANG = {
    "Objective-C": "objective-c", "Mercury": "mercury", "MUF": "muf", "M": "mumps-m",
    "Mathematica": "mathematica-wolfram", "MATLAB": "matlab", "Limbo": "limbo",
}
PYGMENTS_TO_LANG = {
    "Objective-C": "objective-c", "Matlab": "matlab", "MATLAB": "matlab",
    "Octave": "octave", "Mason": "mason", "Mathematica": "mathematica-wolfram",
    "Mercury": "mercury", "Limbo": "limbo", "Objective-C++": "objective-c",
    "Text only": "unknown", "Text": "unknown",
}
SYNID_TO_LANG = dict(LINGUIST_TO_LANG) | {
    "Wolfram Language": "mathematica-wolfram", "Octave": "octave", "Matlab": "matlab",
    "Objective-C++": "objective-c", "Mason": "mason", "Magma": "magma",
    "Maple": "maple", "Scilab": "scilab", "XML": "not-code", "Text": "unknown",
    "C": "c-or-cpp", "C++": "c-or-cpp",
}

# Families used for coarse agreement (MATLAB and Octave are one family).
FAMILY = {"matlab": "matlab-family", "octave": "matlab-family"}


def family(lang: str) -> str:
    return FAMILY.get(lang, lang)


def coerce(value, allowed, default="unknown"):
    return value if value in allowed else default
