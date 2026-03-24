"""Lint rules for Adams CMD files.

Each rule is a callable:
    rule(statements, schema, symbols) -> list[Diagnostic]

Rules are collected in ALL_RULES at the bottom of this module.
"""

from .diagnostics import Diagnostic, Severity
from .parser import Statement, _char_to_line_col


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _canonical_key(stmt):
    """Return the resolved command key if available, otherwise raw key."""
    return stmt.resolved_command_key or stmt.command_key


# ---------------------------------------------------------------------------
# Structural / command-level rules
# ---------------------------------------------------------------------------

def rule_unknown_command(statements, schema, symbols):
    """E001 — Unknown command.

    Attempts abbreviation resolution via the command tree.
    On success, sets stmt.resolved_command_key as a side-effect so that
    downstream rules can use the canonical key without re-resolving.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key:
            continue

        # Already resolved (e.g. exact match from a previous run)
        if stmt.resolved_command_key:
            continue

        # Exact match → no resolution needed
        if schema.has_command(stmt.command_key):
            stmt.resolved_command_key = stmt.command_key
            continue

        # Try abbreviation resolution
        tokens = stmt.command_key.split()
        resolved_key, error_index = schema.resolve_command_key(tokens)

        if resolved_key:
            stmt.resolved_command_key = resolved_key
            continue

        # Report the problematic token position
        col = sum(len(t) + 1 for t in tokens[:error_index]) if error_index else 0
        bad_token = tokens[error_index] if error_index is not None and error_index < len(tokens) else stmt.command_key
        diagnostics.append(Diagnostic(
            line=stmt.line_start,
            column=col,
            end_line=stmt.line_start,
            end_column=col + len(bad_token),
            code="E001",
            message=f"Unknown command: '{stmt.command_key}'",
            severity=Severity.ERROR,
        ))

    return diagnostics


def rule_invalid_argument(statements, schema, symbols):
    """E002 — Invalid argument for this command."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue  # E001 already fired for unknown command

        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            if canonical is None:
                diagnostics.append(Diagnostic(
                    line=arg.name_line,
                    column=arg.name_column,
                    end_line=arg.name_line,
                    end_column=arg.name_column + len(arg.name),
                    code="E002",
                    message=f"Invalid argument '{arg.name}' for command '{cmd_key}'",
                    severity=Severity.ERROR,
                ))

    return diagnostics


def rule_duplicate_argument(statements, schema, symbols):
    """E003 — Same argument provided twice in one statement.

    Checks both exact duplicates and abbreviation-resolved duplicates.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)

        seen = {}  # canonical_name → first Argument
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name) if cmd_key else None
            key = canonical or arg.name
            if key in seen:
                diagnostics.append(Diagnostic(
                    line=arg.name_line,
                    column=arg.name_column,
                    end_line=arg.name_line,
                    end_column=arg.name_column + len(arg.name),
                    code="E003",
                    message=f"Duplicate argument: '{arg.name}'",
                    severity=Severity.ERROR,
                ))
            else:
                seen[key] = arg

    return diagnostics


def rule_invalid_enum_value(statements, schema, symbols):
    """E004 — Argument value not in the allowed enum list."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_def = cmd["args"].get(canonical or arg.name)
            if not arg_def:
                continue
            enum_values = arg_def.get("enum_values")
            if not enum_values:
                continue

            # Skip runtime expressions
            val = arg.value.strip().lower()
            if "$" in val or val.startswith("(") or "eval(" in val:
                continue

            # Adams accepts unique prefixes for enum values too.
            # Resolve val against enum_values using same prefix logic as arg names.
            enum_lower = [v.lower() for v in enum_values]
            if val in enum_lower:
                continue  # exact match

            # Adams accepts unique prefixes for enum values — find the shortest
            # unique prefix for each value among its siblings, then check if val
            # is a valid (unambiguous) prefix of exactly one enum value.
            def _enum_min_prefix(candidate, others):
                for plen in range(1, len(candidate) + 1):
                    if sum(1 for o in others if o != candidate and o.startswith(candidate[:plen])) == 0:
                        return plen
                return len(candidate)

            matched = [
                ev for ev in enum_lower
                if ev.startswith(val) and len(val) >= _enum_min_prefix(ev, enum_lower)
            ]
            if len(matched) == 1:
                continue  # valid prefix abbreviation

            if not matched or len(matched) > 1:
                diagnostics.append(Diagnostic(
                    line=arg.value_line,
                    column=arg.value_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(arg.value),
                    code="E004",
                    message=(
                        f"Invalid value '{arg.value}' for argument '{arg.name}'. "
                        f"Expected one of: {', '.join(enum_values)}"
                    ),
                    severity=Severity.ERROR,
                ))

    return diagnostics


def rule_missing_required(statements, schema, symbols):
    """E005 / W005 — Missing required argument (two-tier severity).

    - adams_id type: no diagnostic (omitting is preferred behaviour)
    - NDBWD_*/NDB_* type (new_object): W005 warning (Adams auto-generates names)
    - All other required args: E005 error
    - Suppressed if another member of the same exclusive group is provided
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        # Build set of provided argument canonical names
        provided = set()
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            provided.add(canonical if canonical else arg.name)

        # Determine which required args are "covered" by exclusive groups
        groups = schema.get_exclusive_groups(cmd_key)
        covered_by_group = set()
        for group in groups:
            members = group.get("members", [])
            if any(m in provided for m in members):
                covered_by_group.update(members)

        for arg_name, arg_def in cmd["args"].items():
            if not arg_def.get("required"):
                continue
            if arg_name in provided:
                continue
            if arg_name in covered_by_group:
                continue  # suppressed: another group member satisfies this slot

            arg_type = arg_def.get("type", "")
            db_type = arg_def.get("db_type", "")

            if arg_type == "adams_id" or db_type == "ADAMS_ID":
                continue  # omitting adams_id is the preferred behaviour

            if db_type.startswith("NDBWD_") or db_type.startswith("NDB_") or arg_type == "new_object":
                code, sev = "W005", Severity.WARNING
                msg = f"Object name '{arg_name}' omitted — Adams will auto-generate a name. Explicit names are recommended."
            else:
                code, sev = "E005", Severity.ERROR
                msg = f"Missing required argument: '{arg_name}'"

            diagnostics.append(Diagnostic(
                line=stmt.line_start,
                column=0,
                end_line=stmt.line_start,
                end_column=len(stmt.command_key),
                code=code,
                message=msg,
                severity=sev,
            ))

    return diagnostics


def rule_manual_adams_id(statements, schema, symbols):
    """I006 — Manual adams_id assignment detected.

    Best practice is to let Adams auto-assign IDs. Manual assignment
    can cause ID conflicts and maintenance headaches.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_name = canonical or arg.name
            arg_def = cmd["args"].get(arg_name)
            if arg_def and (
                arg_def.get("type") == "adams_id"
                or arg_def.get("db_type") == "ADAMS_ID"
            ):
                diagnostics.append(Diagnostic(
                    line=arg.name_line,
                    column=arg.name_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(arg.value),
                    code="I006",
                    message="Manual adams_id assignment — consider letting Adams auto-assign",
                    severity=Severity.INFO,
                ))

    return diagnostics


def rule_exclusive_conflict(statements, schema, symbols):
    """E006 — Two mutually exclusive arguments both provided."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        groups = schema.get_exclusive_groups(cmd_key)
        provided_map = {}  # canonical_name → Argument
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name) if cmd_key else None
            provided_map[canonical or arg.name] = arg

        for group in groups:
            members = group.get("members", [])
            used = [m for m in members if m in provided_map]
            if len(used) > 1:
                # Flag the second (and beyond) conflict
                for conflict_name in used[1:]:
                    arg = provided_map[conflict_name]
                    diagnostics.append(Diagnostic(
                        line=arg.name_line,
                        column=arg.name_column,
                        end_line=arg.name_line,
                        end_column=arg.name_column + len(arg.name),
                        code="E006",
                        message=f"'{conflict_name}' conflicts with '{used[0]}' (mutually exclusive)",
                        severity=Severity.WARNING,
                    ))

    return diagnostics


# ---------------------------------------------------------------------------
# Syntax rules
# ---------------------------------------------------------------------------

def rule_unbalanced_parens(statements, schema, symbols):
    """E101 — Unbalanced parentheses in a statement."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank:
            continue
        depth = 0
        in_double = False
        in_single = False
        text = stmt.raw_text
        for i, ch in enumerate(text):
            if ch == '"' and not in_single:
                in_double = not in_double
            elif ch == "'" and not in_double:
                in_single = not in_single
            elif not in_double and not in_single:
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth < 0:
                        diagnostics.append(Diagnostic(
                            line=stmt.line_start,
                            column=i,
                            end_line=stmt.line_start,
                            end_column=i + 1,
                            code="E101",
                            message="Unexpected closing parenthesis ')'",
                            severity=Severity.ERROR,
                        ))
                        depth = 0  # reset and continue scanning
        if depth > 0:
            diagnostics.append(Diagnostic(
                line=stmt.line_end,
                column=0,
                end_line=stmt.line_end,
                end_column=0,
                code="E101",
                message=f"Unbalanced parentheses: {depth} unclosed '('",
                severity=Severity.ERROR,
            ))

    return diagnostics


def rule_unclosed_quote(statements, schema, symbols):
    """E102 — Unclosed double-quoted string."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank:
            continue
        in_string = False
        string_start = -1
        for i, ch in enumerate(stmt.raw_text):
            if ch == '"':
                if not in_string:
                    in_string = True
                    string_start = i
                else:
                    in_string = False
                    string_start = -1
        if in_string:
            diagnostics.append(Diagnostic(
                line=stmt.line_end,
                column=string_start,
                end_line=stmt.line_end,
                end_column=string_start + 1,
                code="E102",
                message="Unclosed double-quoted string",
                severity=Severity.ERROR,
            ))

    return diagnostics


def rule_control_flow_balance(statements, schema, symbols):
    """E104 — Unbalanced if/for/while/end blocks."""
    diagnostics = []
    stack = []  # list of (keyword, line)

    for stmt in statements:
        if not stmt.is_control_flow:
            continue
        kw = stmt.control_flow_keyword

        if kw in ("if", "for", "while"):
            stack.append((kw, stmt.line_start))
        elif kw == "elseif":
            if not stack or stack[-1][0] not in ("if",):
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=0,
                    end_line=stmt.line_start,
                    end_column=len(kw),
                    code="E104",
                    message="'elseif' without matching 'if'",
                    severity=Severity.ERROR,
                ))
        elif kw == "else":
            if not stack or stack[-1][0] != "if":
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=0,
                    end_line=stmt.line_start,
                    end_column=len(kw),
                    code="E104",
                    message="'else' without matching 'if'",
                    severity=Severity.ERROR,
                ))
        elif kw == "end":
            if not stack:
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=0,
                    end_line=stmt.line_start,
                    end_column=len(kw),
                    code="E104",
                    message="'end' without matching 'if', 'for', or 'while'",
                    severity=Severity.ERROR,
                ))
            else:
                stack.pop()

    # Any unclosed blocks remaining in the stack
    for kw, line in stack:
        diagnostics.append(Diagnostic(
            line=line,
            column=0,
            end_line=line,
            end_column=len(kw),
            code="E104",
            message=f"'{kw}' block not closed with 'end'",
            severity=Severity.ERROR,
        ))

    return diagnostics


# ---------------------------------------------------------------------------
# Semantic rules
# ---------------------------------------------------------------------------

def rule_type_mismatch(statements, schema, symbols):
    """W201 / I202 — Wrong object type or unresolved reference."""
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = _canonical_key(stmt)
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_def = cmd["args"].get(canonical or arg.name)
            if not arg_def or arg_def.get("type") != "existing_object":
                continue

            # Skip runtime expressions
            val = arg.value
            if "$" in val or val.lower().startswith("(") or "eval(" in val.lower():
                continue

            symbol = symbols.lookup(val)
            expected_type = arg_def.get("object_type", "")

            if symbol:
                if expected_type and symbol.object_type.upper() != expected_type.upper():
                    diagnostics.append(Diagnostic(
                        line=arg.value_line,
                        column=arg.value_column,
                        end_line=arg.value_line,
                        end_column=arg.value_column + len(val),
                        code="W201",
                        message=(
                            f"Type mismatch: '{val}' is a {symbol.object_type}, "
                            f"expected {expected_type}"
                        ),
                        severity=Severity.WARNING,
                    ))
            else:
                diagnostics.append(Diagnostic(
                    line=arg.value_line,
                    column=arg.value_column,
                    end_line=arg.value_line,
                    end_column=arg.value_column + len(val),
                    code="I202",
                    message=f"Unresolved reference: '{val}'",
                    severity=Severity.INFO,
                ))

    return diagnostics


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

ALL_RULES = [
    rule_unknown_command,       # E001 — sets resolved_command_key as side-effect
    rule_invalid_argument,      # E002
    rule_duplicate_argument,    # E003
    rule_invalid_enum_value,    # E004
    rule_missing_required,      # E005 / W005
    rule_manual_adams_id,       # I006
    rule_exclusive_conflict,    # E006
    rule_unbalanced_parens,     # E101
    rule_unclosed_quote,        # E102
    rule_control_flow_balance,  # E104
    rule_type_mismatch,         # W201 / I202
]
