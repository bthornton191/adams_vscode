"""Linter orchestrator for Adams CMD files."""

from .parser import parse, _is_comment_only, _is_continuation, _strip_comment
from .schema import Schema
from .symbols import build_symbol_table
from .rules import ALL_RULES
from .diagnostics import Diagnostic, Severity


_SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def lint_text(text, schema=None, min_severity=None, macro_registry=None, show_macro_hint=True,
              ude_registry=None):
    """Lint a CMD text string and return sorted diagnostics.

    Args:
        text: raw .cmd file content
        schema: Schema object (loads bundled default if None)
        min_severity: minimum severity string to include: "error", "warning", "info"
                      (None means include all)
        macro_registry: optional MacroRegistry for workspace-wide user macro lookup
        show_macro_hint: if True, E001 messages include a hint about scanWorkspaceMacros
                         when no macro registry is active
        ude_registry: optional UdeRegistry for user-defined element lookup

    Returns:
        list[Diagnostic] sorted by (line, column)
    """
    schema = schema or Schema.load()
    statements = parse(text)
    symbols = build_symbol_table(
        statements, schema, macro_registry=macro_registry, show_macro_hint=show_macro_hint,
        ude_registry=ude_registry,
    )

    diagnostics = []
    for rule in ALL_RULES:
        diagnostics.extend(rule(statements, schema, symbols))

    # W103 — dangling '&' at end of file.
    # If the last non-blank, non-comment physical line ends with a continuation
    # marker '&', Adams would silently absorb the (non-existent) next line.
    # This is almost always a mistake — flag it.
    eof_diag = _check_dangling_eof(text)
    if eof_diag:
        diagnostics.append(eof_diag)

    # W103 — dangling '&' before a blank line mid-file.
    # A continuation group terminated by a blank line when its last physical
    # line still carries '&' indicates an incomplete or split command.
    diagnostics.extend(_check_dangling_continuations(text))

    if min_severity is not None:
        threshold = _SEVERITY_ORDER.get(min_severity.lower(), 2)
        diagnostics = [
            d for d in diagnostics
            if _SEVERITY_ORDER.get(d.severity.value, 2) <= threshold
        ]

    return sorted(diagnostics, key=lambda d: (d.line, d.column))


def _check_dangling_continuations(text):
    """Return W103 Diagnostics for each continuation group terminated by a blank
    line mid-file whose last physical line still ends with '&'.

    This catches the pattern:
        some_command arg1 = val1 &
            arg2 = val2 &
                            ← blank line silently ends the group
        else               ← next statement

    The EOF case is deliberately excluded here — it is handled by
    _check_dangling_eof so that function retains its standalone semantics.
    """
    lines = text.splitlines()
    n = len(lines)
    diagnostics = []

    # Pre-compute the index of the last meaningful line so that the inner loop
    # can cheaply exclude the EOF case (already handled by _check_dangling_eof).
    last_meaningful_idx = None
    for j in range(n - 1, -1, -1):
        if lines[j].strip() and not _is_comment_only(lines[j]):
            last_meaningful_idx = j
            break

    i = 0
    while i < n:
        raw = lines[i]

        # Skip comment-only lines and blank lines outside a continuation group
        if not raw.strip() or _is_comment_only(raw):
            i += 1
            continue

        if not _is_continuation(raw):
            i += 1
            continue

        # We are at the start of a continuation group.  Walk forward tracking
        # the last non-comment line that ends with '&'.
        last_cont_line_idx = i  # index of the most-recent line ending with '&'
        i += 1

        while i < n:
            raw2 = lines[i]

            # Comment-only lines are absorbed inside a continuation group
            if _is_comment_only(raw2):
                i += 1
                continue

            # Blank line — terminates the group
            if not raw2.strip():
                # Only flag if this is NOT the end of the file (EOF is handled
                # by _check_dangling_eof).
                if last_cont_line_idx != last_meaningful_idx:
                    line_text = lines[last_cont_line_idx]
                    # Strip comment before calculating '&' column so lines like
                    # "  arg = val & ! comment" point at the '&', not the comment.
                    stripped = _strip_comment(line_text).rstrip()
                    amp_col = len(stripped) - 1  # 0-based column of '&'
                    diagnostics.append(Diagnostic(
                        line=last_cont_line_idx,
                        column=amp_col,
                        end_line=last_cont_line_idx,
                        end_column=amp_col + 1,
                        code="W103",
                        message=(
                            "Dangling continuation '&' — command continuation "
                            "was terminated by a blank line"
                        ),
                        severity=Severity.WARNING,
                    ))
                i += 1
                break

            # Line ends with '&' — still in continuation
            if _is_continuation(raw2):
                last_cont_line_idx = i
                i += 1
                continue

            # Non-blank, non-comment line without '&' — normal group end
            i += 1
            break

    return diagnostics


def _check_dangling_eof(text):
    """Return a W103 Diagnostic if the last meaningful line ends with '&', else None."""
    lines = text.splitlines()
    last_line_idx = None
    for i in range(len(lines) - 1, -1, -1):
        raw = lines[i]
        if raw.strip() and not _is_comment_only(raw):
            last_line_idx = i
            break
    if last_line_idx is None:
        return None
    if _is_continuation(lines[last_line_idx]):
        return Diagnostic(
            line=last_line_idx,
            column=0,
            end_line=last_line_idx,
            end_column=len(lines[last_line_idx]),
            code="W103",
            message="Dangling continuation '&' at end of file — command is incomplete",
            severity=Severity.WARNING,
        )
    return None
