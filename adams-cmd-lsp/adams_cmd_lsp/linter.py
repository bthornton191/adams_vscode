"""Linter orchestrator for Adams CMD files."""

from .parser import parse, _is_comment_only, _is_continuation
from .schema import Schema
from .symbols import build_symbol_table
from .rules import ALL_RULES
from .diagnostics import Diagnostic, Severity


_SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def lint_text(text, schema=None, min_severity=None):
    """Lint a CMD text string and return sorted diagnostics.

    Args:
        text: raw .cmd file content
        schema: Schema object (loads bundled default if None)
        min_severity: minimum severity string to include: "error", "warning", "info"
                      (None means include all)

    Returns:
        list[Diagnostic] sorted by (line, column)
    """
    schema = schema or Schema.load()
    statements = parse(text)
    symbols = build_symbol_table(statements, schema)

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

    if min_severity is not None:
        threshold = _SEVERITY_ORDER.get(min_severity.lower(), 2)
        diagnostics = [
            d for d in diagnostics
            if _SEVERITY_ORDER.get(d.severity.value, 2) <= threshold
        ]

    return sorted(diagnostics, key=lambda d: (d.line, d.column))


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
