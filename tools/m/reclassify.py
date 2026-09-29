"""Zero-API language identifier for `.m` contents (our deterministic labeller).

A decision cascade over `indicators.py`. Unambiguous markers go first
(Mercury `:-` declarations, Objective-C `@` directives, Wolfram package
cells, MUMPS routine structure, Magma/Maple block terminators), then the
MATLAB family is scored, and Octave is chosen *only* on Octave-only syntax —
MATLAB-compatible code stays "matlab" (the portability question is separate).

VERSION history is recorded so the held-out evaluation stays honest:
  v1  written before any judge label was seen (prospective) — frozen in
      `reclassify_v1.py`, used for the PPI estimates
  v2  revised after reading the 7 disagreements on the TUNING split only
      (U ranks 1–300): (a) Wolfram *expressions* with no package cell
      (`Log[`, `Zeta[`, `^n … \\` continuations) → mathematica-wolfram;
      (b) marker-less MATLAB scripts (control toolbox calls, `;`-terminated
      assignments, struct/cell literals) → matlab via a residual rule that
      fires only when no other language has any marker. Octave logic is
      deliberately unchanged: `octave` stays tied to Octave-only *syntax*.
"""

from __future__ import annotations

from tools.m import indicators as ind_mod

VERSION = "m-reclass/2"


def _is_binary(raw: bytes) -> bool:
    if b"\x00" in raw[:8192]:
        return True
    if not raw:
        return False
    s = raw[:4096]
    printable = sum(1 for b in s if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return printable / len(s) < 0.75


def classify_ind(i: ind_mod.Indicators, text: str) -> tuple[str, str, str]:
    """Return (language, content_hint, reason)."""
    if not i.is_text:
        return "not-code", "binary", "non-text bytes"
    if i.nonblank_lines == 0:
        return "not-code", "empty-or-trivial", "empty"
    if i.mercury_decls >= 2 or text.lstrip().startswith(":- module"):
        return "mercury", "source-code", f"mercury decls={i.mercury_decls}"
    if i.mason_markers >= 2:
        return "mason", "source-code", f"mason markers={i.mason_markers}"
    if i.starts_xml and i.objc_directives == 0 and i.ml_function_hdrs == 0:
        return "not-code", "markup-or-xml", "starts with XML/markup"
    if i.objc_directives >= 1 or i.objc_import_h >= 1 or i.objc_app_main or i.cocoapods_dummy:
        return "objective-c", "source-code", (f"objc directives={i.objc_directives} "
                                              f"#import={i.objc_import_h}")
    if i.limbo_markers >= 1 and i.ml_function_hdrs == 0:
        return "limbo", "source-code", f"limbo markers={i.limbo_markers}"
    if i.mma_package_marks >= 1 or i.mma_begin >= 1 or (i.mma_defs >= 2 and i.mma_calls >= 5
                                                          and i.ml_pct_comments == 0) \
            or (i.ml_pct_comments == 0 and i.ml_function_hdrs == 0
                and (i.mma_builtin_calls >= 3 or i.mma_pow_continuations >= 3)):
        return "mathematica-wolfram", "source-code", (f"pkg={i.mma_package_marks} "
                                                      f"defs={i.mma_defs} calls={i.mma_calls}")
    if i.mumps_labels >= 1 and (i.mumps_cmd_lines >= 3 or i.mumps_fns >= 3) and i.ml_function_hdrs == 0:
        return "mumps-m", "source-code", (f"labels={i.mumps_labels} cmd-lines={i.mumps_cmd_lines} "
                                          f"$fn={i.mumps_fns}")
    if i.magma_markers >= 2 and i.colon_assign >= 1 and i.ml_pct_comments == 0:
        return "magma", "source-code", f"magma markers={i.magma_markers}"
    if i.maple_markers >= 2 and i.colon_assign >= 1 and i.ml_pct_comments == 0:
        return "maple", "source-code", f"maple markers={i.maple_markers}"
    if i.scilab_markers >= 2 and i.oct_block_ends == 0:
        return "scilab", "source-code", f"scilab markers={i.scilab_markers}"

    ml = (3 * i.ml_function_hdrs + 2 * min(i.ml_pct_comments, 5) + i.ml_builtins
          + min(i.ml_end_lines, 5) + i.ml_elementwise + 3 * i.ml_classdef + 2 * i.ml_cell_marks)
    if ml >= 3 or i.octave_only_markers >= 2:
        oct_strong = i.oct_block_ends + i.oct_hash_comments + i.oct_printf + i.oct_ne \
            + int(i.oct_script_marker)
        if oct_strong >= 2 or i.oct_block_ends >= 1:
            return "octave", "source-code", f"octave-only markers={oct_strong}"
        return "matlab", "source-code", f"matlab score={ml}"
    if i.c_preproc >= 1 and i.c_main:
        return "c-or-cpp", "source-code", "C preprocessor + main"
    if i.colon_assign >= 3 and i.magma_markers >= 1:
        return "magma", "source-code", "':=' + magma marker"
    # a short MATLAB script without any tell-tale is still the likeliest reading
    if 0 < ml and i.nonblank_lines <= 30 and i.objc_msg_sends == 0:
        return "matlab", "source-code", f"weak matlab score={ml}"
    # v2 residual rule: no marker of any other language, but MATLAB-shaped statements
    others = (i.objc_directives + i.objc_import_h + i.c_preproc + i.mercury_decls + i.mumps_labels
              + i.magma_markers + i.maple_markers + i.limbo_markers + i.mason_markers + i.mma_builtin_calls)
    if others == 0 and (i.ml_builtins_ext >= 2 or i.ml_assign_lines >= 3):
        return "matlab", "source-code", (f"residual: builtins={i.ml_builtins_ext} "
                                         f"assignments={i.ml_assign_lines}")
    return "unknown", "other", "no decisive marker"


def classify(filename: str, raw: bytes) -> dict:
    if _is_binary(raw):
        return {"lang": "not-code", "content": "binary", "reason": "non-text bytes", "version": VERSION}
    text = raw.decode("utf-8", "replace")
    i = ind_mod.compute(text)
    lang, content, reason = classify_ind(i, text)
    if lang != "not-code" and (i.generated_marker or i.cocoapods_dummy or i.flutter_registrant):
        content = "generated-code"
    return {"lang": lang, "content": content, "reason": reason, "version": VERSION}
