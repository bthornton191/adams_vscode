"""CLI entry point for adams-cmd-lint."""

import argparse
import json
import os
import sys
from pathlib import Path

from .linter import lint_text
from .schema import Schema
from .diagnostics import Severity
from .macros import scan_macro_files, DEFAULT_MACRO_PATTERNS


def _output_text(filepath, diagnostics, file=None):
    """Human-readable output."""
    if file is None:
        file = sys.stdout
    for d in diagnostics:
        # 1-based lines/columns for human output
        print(
            f"{filepath}:{d.line + 1}:{d.column + 1}: {d.code} {d.message}",
            file=file,
        )
    errors = sum(1 for d in diagnostics if d.severity == Severity.ERROR)
    warnings = sum(1 for d in diagnostics if d.severity == Severity.WARNING)
    info = sum(1 for d in diagnostics if d.severity == Severity.INFO)
    print(f"\n{errors} error(s), {warnings} warning(s), {info} info", file=file)


def _output_json(filepath, diagnostics, file=None):
    """JSON output for agent/tool consumption."""
    if file is None:
        file = sys.stdout
    errors = sum(1 for d in diagnostics if d.severity == Severity.ERROR)
    warnings = sum(1 for d in diagnostics if d.severity == Severity.WARNING)
    info = sum(1 for d in diagnostics if d.severity == Severity.INFO)
    result = {
        "file": filepath,
        "diagnostics": [
            {
                "line": d.line + 1,
                "column": d.column + 1,
                "end_line": d.end_line + 1,
                "end_column": d.end_column + 1,
                "code": d.code,
                "message": d.message,
                "severity": d.severity.value,
            }
            for d in diagnostics
        ],
        "summary": {"errors": errors, "warnings": warnings, "info": info},
    }
    print(json.dumps(result, indent=2), file=file)


def _output_gcc(filepath, diagnostics, file=None):
    """GCC-style output for editor integration."""
    if file is None:
        file = sys.stdout
    for d in diagnostics:
        print(
            f"{filepath}:{d.line + 1}:{d.column + 1}: {d.severity.value}: {d.message} [{d.code}]",
            file=file,
        )


def main():
    """Main entry point for the adams-cmd-lint CLI."""
    parser = argparse.ArgumentParser(
        prog="adams-cmd-lint",
        description="Lint MSC Adams CMD files",
    )
    parser.add_argument("files", nargs="+", help="CMD files to lint")
    parser.add_argument(
        "--format",
        choices=["text", "json", "gcc"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="info",
        help="Minimum severity to report (default: info)",
    )
    parser.add_argument(
        "--schema",
        metavar="PATH",
        help="Path to command_schema.json (default: bundled)",
    )
    parser.add_argument(
        "--macro-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help=(
            "Glob patterns for macro file discovery, resolved relative to "
            "--macro-base-dir (default: current directory). "
            "Example: '**/*.mac' 'macros/*'. "
            "If omitted, no macro scanning is performed."
        ),
    )
    parser.add_argument(
        "--macro-base-dir",
        metavar="DIR",
        default=None,
        help=(
            "Base directory for resolving relative --macro-paths globs "
            "(default: current working directory)."
        ),
    )
    parser.add_argument(
        "--macro-ignore-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns (relative to base dir) to exclude from macro scanning.",
    )

    args = parser.parse_args()

    try:
        schema = Schema.load(args.schema) if args.schema else Schema.load()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error loading schema: {exc}", file=sys.stderr)
        sys.exit(2)

    macro_registry = None
    if args.macro_paths:
        base_dir = args.macro_base_dir or os.getcwd()
        macro_registry = scan_macro_files(
            [base_dir],
            patterns=args.macro_paths,
            ignore_patterns=args.macro_ignore_paths or None,
        )

    exit_code = 0
    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            sys.exit(2)

        text = path.read_text(encoding="utf-8", errors="replace")
        diagnostics = lint_text(
            text,
            schema=schema,
            min_severity=args.severity,
            macro_registry=macro_registry,
        )

        if any(d.severity == Severity.ERROR for d in diagnostics):
            exit_code = 1

        if args.format == "json":
            _output_json(filepath, diagnostics)
        elif args.format == "gcc":
            _output_gcc(filepath, diagnostics)
        else:
            _output_text(filepath, diagnostics)

    sys.exit(exit_code)
