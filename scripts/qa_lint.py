"""qa_lint.py — Batch-lint all Adams CMD files in a directory.

Runs the adams-cmd-lsp linter over every .cmd file, aggregates results by
rule code, and writes a CSV for detailed analysis.

Usage:
    python scripts/qa_lint.py [options]

Options:
    --dir PATH       Directory to scan recursively (default: hard-coded QA path)
    --out PATH       Output CSV file path (default: qa_lint_results.csv)
    --severity LEVEL Minimum severity: error | warning | info  (default: info = all)
    --top N          Number of example occurrences to show per rule (default: 5)
    --rules CODES    Comma-separated rule codes to INCLUDE (e.g. E001,E005).
                     Omit to include all rules.
    --exclude CODES  Comma-separated rule codes to EXCLUDE from the console
                     summary (they still appear in the CSV).
    --no-csv         Skip writing the CSV file.

Expected-error detection:
    Lines matching /^\\s*!\\s*ERROR/i in the source file are treated as
    "expected error markers".  Any diagnostic whose command start-line falls
    within 3 lines after such a marker is tagged expected=true in the CSV
    and excluded from the "unexpected" count shown in the console summary.
    This filters out intentional Adams error-test sections (e.g. in the
    stnd_regs QA suite) without hiding them entirely.
"""

import sys
import os
import re
import csv
import argparse
import time

# ---------------------------------------------------------------------------
# Bootstrap: allow running from repo root or from scripts/
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
_LSP_SRC = os.path.join(_REPO_ROOT, "adams-cmd-lsp")
if _LSP_SRC not in sys.path:
    sys.path.insert(0, _LSP_SRC)

from adams_cmd_lsp.linter import lint_text
from adams_cmd_lsp.schema import Schema
from adams_cmd_lsp.diagnostics import Severity

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_DIR = r"C:\Users\ben.thornton\code\hexagon\Adams\qa\aview\stnd_regs\cmd"
DEFAULT_OUT = "qa_lint_results.csv"

# Rule code → human-readable short description (for the summary table)
RULE_LABELS = {
    "E001": "Unknown command",
    "E002": "Unknown argument",
    "E003": "Duplicate argument",
    "E004": "Invalid enum value",
    "E005": "Missing required argument",
    "W005": "Object name omitted (auto-generated)",
    "I006": "Manual adams_id (prefer auto)",
    "E006": "Mutual exclusion conflict",
    "E101": "Unbalanced parentheses",
    "E102": "Unclosed quote",
    "W103": "Dangling continuation / merged commands",
    "E104": "Unbalanced if/end",
    "W201": "Type mismatch",
    "I202": "Unresolved reference",
}

SEV_LABEL = {
    Severity.ERROR:   "ERR ",
    Severity.WARNING: "WARN",
    Severity.INFO:    "INFO",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ERROR_MARKER_RE = re.compile(r"^\s*!\s*ERROR", re.IGNORECASE)
# Inline marker: ! ERROR appearing anywhere in the line (e.g. "end  ! ERROR")
_INLINE_ERROR_RE = re.compile(r"!\s*ERROR", re.IGNORECASE)


def build_expected_lines(text):
    """Return a set of 1-based line numbers that follow a '! ERROR' marker.

    Adams QA test files use ``! ERROR`` (optionally ``! ERROR: <reason>``) in
    two positions:

    1. **Stand-alone comment line** (``! ERROR`` at start-of-line): the next 3
       lines are marked expected — covers the common pattern where the marker
       precedes a deliberately-failing command.

    2. **Inline comment** (``end  ! ERROR`` or ``else !ERROR``): the line itself
       is marked expected — covers test files like avt27108 where the faulty
       keyword and the marker are on the same line.

    Both patterns are recognised so that diagnostics on those lines are tagged
    as intentional rather than false positives.
    """
    expected = set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if _ERROR_MARKER_RE.match(line):
            # Stand-alone marker: mark the next 3 lines (1-based)
            for offset in range(1, 4):
                expected.add(i + 1 + offset)   # i is 0-based, CSV uses 1-based
        elif _INLINE_ERROR_RE.search(line):
            # Inline marker: the line itself carries the bad token
            expected.add(i + 1)                # 1-based line number
    return expected


def collect_cmd_files(directory):
    """Recursively collect all .cmd files under directory."""
    files = []
    for root, _dirs, filenames in os.walk(directory):
        for fn in filenames:
            if fn.lower().endswith(".cmd"):
                files.append(os.path.join(root, fn))
    return sorted(files)


def read_file(path):
    """Read a file, trying UTF-8 then latin-1 as fallback."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            return f.read()


def progress(current, total, start_time, errors):
    """Print a compact progress line (overwrites in-place)."""
    pct = 100 * current // total
    elapsed = time.time() - start_time
    rate = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / rate if rate > 0 else 0
    bar_len = 30
    filled = bar_len * current // total
    bar = "#" * filled + "." * (bar_len - filled)
    sys.stdout.write(
        f"\r  [{bar}] {pct:3d}%  {current}/{total}"
        f"  {rate:.0f} files/s  ETA {eta:.0f}s  read-errors: {errors}  "
    )
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Batch-lint Adams CMD files and report diagnostics by rule."
    )
    parser.add_argument("--dir", default=DEFAULT_DIR,
                        help="Directory to scan (default: QA stnd_regs/cmd)")
    parser.add_argument("--out", default=DEFAULT_OUT,
                        help="Output CSV path (default: qa_lint_results.csv)")
    parser.add_argument("--severity", default="info",
                        choices=["error", "warning", "info"],
                        help="Minimum severity to report (default: info = all)")
    parser.add_argument("--top", type=int, default=5,
                        help="Examples to show per rule in console (default: 5)")
    parser.add_argument("--rules", default=None,
                        help="Only show these rule codes (comma-separated)")
    parser.add_argument("--exclude", default=None,
                        help="Hide these rule codes from console (still in CSV)")
    parser.add_argument("--no-csv", action="store_true",
                        help="Skip writing CSV output")
    args = parser.parse_args()

    include_rules = set(args.rules.upper().split(",")) if args.rules else None
    exclude_rules = set(args.exclude.upper().split(",")) if args.exclude else set()

    # ------------------------------------------------------------------
    # 1. Find files
    # ------------------------------------------------------------------
    print(f"\nScanning: {args.dir}")
    cmd_files = collect_cmd_files(args.dir)
    if not cmd_files:
        print("  No .cmd files found.")
        sys.exit(1)
    print(f"  Found {len(cmd_files)} .cmd files\n")

    # ------------------------------------------------------------------
    # 2. Load schema once
    # ------------------------------------------------------------------
    print("Loading schema...", end=" ", flush=True)
    schema = Schema.load()
    print("done\n")

    # ------------------------------------------------------------------
    # 3. Lint all files
    # ------------------------------------------------------------------
    # Each entry: {"file": rel_path, "line": 1-based, "col": 1-based,
    #              "code": ..., "severity": ..., "message": ...}
    all_diags = []
    read_errors = 0
    lint_errors = 0
    start = time.time()

    for i, filepath in enumerate(cmd_files):
        progress(i + 1, len(cmd_files), start, read_errors)

        rel = os.path.relpath(filepath, args.dir)
        try:
            text = read_file(filepath)
        except OSError as e:
            read_errors += 1
            continue

        expected_lines = build_expected_lines(text)

        try:
            diags = lint_text(text, schema=schema, min_severity=args.severity)
        except Exception as e:
            lint_errors += 1
            # Record a synthetic diagnostic so we can see which files crash the linter
            all_diags.append({
                "file": rel,
                "line": 1,
                "col": 1,
                "code": "CRASH",
                "severity": "error",
                "message": f"Linter raised an exception: {e}",
                "expected": False,
            })
            continue

        for d in diags:
            line_1based = d.line + 1
            all_diags.append({
                "file": rel,
                "line": line_1based,        # convert to 1-based
                "col": d.column + 1,
                "code": d.code,
                "severity": d.severity.value,
                "message": d.message,
                "expected": line_1based in expected_lines,
            })

    elapsed = time.time() - start
    print(f"\n\nFinished in {elapsed:.1f}s")
    if read_errors:
        print(f"  Warning: {read_errors} file(s) could not be read (skipped)")
    if lint_errors:
        print(f"  Warning: {lint_errors} file(s) crashed the linter (recorded as CRASH)")

    # ------------------------------------------------------------------
    # 4. Aggregate by rule code
    # ------------------------------------------------------------------
    from collections import defaultdict

    # count: {code: int}
    counts = defaultdict(int)
    unexpected_counts = defaultdict(int)
    # files affected: {code: set of file paths}
    affected_files = defaultdict(set)
    # first-seen severity: {code: str}
    sev_map = {}
    # example occurrences (unexpected only): {code: list of (file, line, message)}
    examples = defaultdict(list)

    for d in all_diags:
        code = d["code"]
        counts[code] += 1
        if not d["expected"]:
            unexpected_counts[code] += 1
        affected_files[code].add(d["file"])
        if code not in sev_map:
            sev_map[code] = d["severity"]
        if not d["expected"] and len(examples[code]) < args.top:
            examples[code].append((d["file"], d["line"], d["message"]))

    total_diags = len(all_diags)
    total_unexpected = sum(1 for d in all_diags if not d["expected"])
    total_expected = total_diags - total_unexpected
    clean_files = len(cmd_files) - len({d["file"] for d in all_diags})

    # ------------------------------------------------------------------
    # 5. Console summary
    # ------------------------------------------------------------------
    print(f"\n{'='*72}")
    print(f"  Adams CMD Linter — QA Batch Results")
    print(f"{'='*72}")
    print(f"  Files scanned : {len(cmd_files)}")
    print(f"  Files clean   : {clean_files}  ({100*clean_files//len(cmd_files)}%)")
    print(f"  Total diags   : {total_diags}  (unexpected: {total_unexpected}, expected/tagged: {total_expected})")
    print(f"  Elapsed       : {elapsed:.1f}s")
    print(f"{'='*72}\n")

    # Sort by count descending
    sorted_codes = sorted(counts.keys(), key=lambda c: -counts[c])

    # Filter for console display
    display_codes = [
        c for c in sorted_codes
        if c not in exclude_rules
        and (include_rules is None or c in include_rules)
    ]

    # Column widths
    W_CODE = 6
    W_SEV  = 5
    W_COUNT = 7
    W_UNEXP = 8
    W_FILES = 7
    W_DESC = 35

    header = (
        f"  {'Code':<{W_CODE}} {'Sev':<{W_SEV}} {'Total':>{W_COUNT}} "
        f"{'Unexpect':>{W_UNEXP}} {'Files':>{W_FILES}}  {'Description':<{W_DESC}}"
    )
    sep = "  " + "-" * (W_CODE + W_SEV + W_COUNT + W_UNEXP + W_FILES + W_DESC + 10)
    print(header)
    print(sep)

    for code in display_codes:
        sev = sev_map.get(code, "?")
        sev_short = {"error": "ERR", "warning": "WARN", "info": "INFO"}.get(sev, sev[:4])
        desc = RULE_LABELS.get(code, "")
        n_files = len(affected_files[code])
        unexp = unexpected_counts[code]
        print(
            f"  {code:<{W_CODE}} {sev_short:<{W_SEV}} {counts[code]:>{W_COUNT},} "
            f"{unexp:>{W_UNEXP},} {n_files:>{W_FILES},}  {desc:<{W_DESC}}"
        )

    print(sep)
    print()

    # Per-rule examples (unexpected only)
    if args.top > 0:
        for code in display_codes:
            sev = sev_map.get(code, "?")
            sev_short = {"error": "ERR", "warning": "WARN", "info": "INFO"}.get(sev, sev[:4])
            desc = RULE_LABELS.get(code, code)
            unexp = unexpected_counts[code]
            tag = f"  [{unexp:,} unexpected / {counts[code]:,} total in {len(affected_files[code]):,} files]"
            print(f"  {code} ({sev_short}) — {desc}{tag}")
            for file, line, msg in examples[code]:
                # Truncate long paths from the left
                short_file = file if len(file) <= 55 else "..." + file[-52:]
                short_msg = msg if len(msg) <= 80 else msg[:77] + "..."
                print(f"    {short_file}:{line}  {short_msg}")
            print()

    # ------------------------------------------------------------------
    # 6. Write CSV
    # ------------------------------------------------------------------
    if not args.no_csv:
        out_path = args.out
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["file", "line", "col", "code", "severity", "message", "expected"])
            writer.writeheader()
            writer.writerows(all_diags)
        print(f"  CSV written -> {os.path.abspath(out_path)}")
        print(f"  ({total_diags:,} rows, {total_unexpected:,} unexpected)\n")


if __name__ == "__main__":
    main()
