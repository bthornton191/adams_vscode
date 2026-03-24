"""Linter orchestrator for Adams CMD files."""

from .parser import parse
from .schema import Schema
from .symbols import build_symbol_table
from .rules import ALL_RULES
from .diagnostics import Severity


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

    if min_severity is not None:
        threshold = _SEVERITY_ORDER.get(min_severity.lower(), 2)
        diagnostics = [
            d for d in diagnostics
            if _SEVERITY_ORDER.get(d.severity.value, 2) <= threshold
        ]

    return sorted(diagnostics, key=lambda d: (d.line, d.column))
