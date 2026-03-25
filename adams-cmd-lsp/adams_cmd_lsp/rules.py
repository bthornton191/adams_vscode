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
    """E001 — Unknown command.  W103 — Commands merged by dangling '&'.

    Attempts abbreviation resolution via the command tree.
    On success, sets stmt.resolved_command_key as a side-effect so that
    downstream rules can use the canonical key without re-resolving.

    When a command key fails to resolve AND the key appears to be two valid
    commands concatenated (a symptom of a trailing '&' merging two lines),
    W103 is emitted instead of E001.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key:
            continue

        # Suppress E001 for dot-path property assignments, e.g.:
        #   .plot_1.curve_2.y_history = "filter(...)"
        #   .model_1.spring_1.func = "vr(...)"
        # These are direct object-property setter statements in Adams CMD.
        # No Adams command begins with '.', so these are never false negatives.
        if stmt.command_key.startswith('.'):
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

        # Before emitting E001, check whether this looks like two commands
        # merged by a dangling '&'.  Try every split point in the token list:
        # if both halves independently resolve to valid commands, emit W103.
        w103_diag = _check_merged_commands(stmt, tokens, schema)
        if w103_diag:
            diagnostics.append(w103_diag)
            continue

        # Suppress E001 if the first token matches a user-defined macro name.
        # When `macro create macro_name=foo ...` is present earlier in the file,
        # a call `foo arg=val` should not be flagged as an unknown command.
        first_token = tokens[0] if tokens else ""
        if first_token and symbols.has(first_token):
            sym = symbols.lookup(first_token)
            if sym and sym.object_type.upper() == "MACRO":
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


def _check_merged_commands(stmt, tokens, schema):
    """Return a W103 Diagnostic if *tokens* appears to be two commands merged
    by a dangling '&', or None otherwise.

    Tries every split point (1..N-1) in the token list.  If both halves
    independently resolve to known commands, the statement is flagged.
    """
    for split in range(1, len(tokens)):
        left_tokens = tokens[:split]
        right_tokens = tokens[split:]
        left_key, left_err = schema.resolve_command_key(left_tokens)
        right_key, right_err = schema.resolve_command_key(right_tokens)
        if left_key and right_key:
            return Diagnostic(
                line=stmt.line_start,
                column=0,
                end_line=stmt.line_end,
                end_column=0,
                code="W103",
                message=(
                    f"Commands appear merged by trailing '&': "
                    f"'{left_key}' and '{right_key}'"
                ),
                severity=Severity.WARNING,
            )
    return None


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

        # If the command has no defined arguments (stub entry), skip E002
        # to avoid false positives on partially-documented commands.
        if not cmd.get("args"):
            continue

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

            # Adams allows quoting enum values (e.g. icon_visibility="off").
            # Strip a single layer of matching surrounding quotes before matching.
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]

            # Adams allows comma-separated lists of enum values for array-type
            # arguments (e.g. visibility_between_markers = on, on, off).
            # Adams also accepts single-character abbreviations like 'y'/'n' for
            # yes/no in pattern arguments.
            # If every element in the list is a valid (or abbreviated) enum value,
            # accept the whole list without further checking.
            if "," in val:
                elements = [e.strip() for e in val.split(",")]
                enum_lower = [v.lower() for v in enum_values]

                def _element_valid(e):
                    if e in enum_lower:
                        return True
                    # Accept unambiguous prefix of any enum value
                    matched_e = [
                        ev for ev in enum_lower
                        if ev.startswith(e)
                    ]
                    return len(matched_e) >= 1  # any match is fine for comma lists

                if all(_element_valid(e) for e in elements):
                    continue
                # At least one element is invalid — skip further E004 (already
                # confusing to report whole string); silently skip for now.
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
    - NDBWD_PART type (part name): E005 error (Adams requires an explicit name)
    - Other NDBWD_*/NDB_* type (new_object): W005 warning (Adams auto-generates names)
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

        # Build set of provided argument canonical names and a value map
        provided = set()
        provided_values = {}  # canonical_name -> raw value string
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            canon = canonical if canonical else arg.name
            provided.add(canon)
            provided_values[canon] = arg.value

        # Determine which required args are "covered" by exclusive groups
        groups = schema.get_exclusive_groups(cmd_key)
        covered_by_group = set()
        for group in groups:
            members = group.get("members", [])
            if any(m in provided for m in members):
                covered_by_group.update(members)

        # Special case: force create direct single_component_force with action_only=on.
        # In action-only mode the force has no reaction body; j_marker_name and
        # j_part_name are not applicable and must not be flagged as missing.
        if (cmd_key == "force create direct single_component_force"
                and provided_values.get("action_only", "").lower() == "on"):
            covered_by_group.update({"j_marker_name", "j_part_name"})

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
                if db_type == "NDBWD_PART":
                    # Adams requires an explicit part name — auto-generation is not supported
                    code, sev = "E005", Severity.ERROR
                    msg = f"Missing required argument: '{arg_name}' (Adams requires an explicit part name)"
                else:
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
    """E104 — Unbalanced if/for/while/end blocks.

    Python sections (between ``language switch_to python`` and
    ``Adams.switchToCmd()`` / ``language switch_to cmd``) are skipped because
    Python uses the same keywords (``for``, ``if``, ``else``, ``end``) with
    different semantics and no explicit ``end`` statement.
    """
    diagnostics = []
    stack = []  # list of (keyword, line)
    in_python = False  # True while inside a Python scripting section

    for stmt in statements:
        # Detect entry into Python mode
        ck = stmt.command_key.lower()
        if not stmt.is_control_flow:
            if "language" in ck and "python" in ck:
                in_python = True
                continue
            if in_python and (ck.startswith("adams.switchtocmd") or
                              ("language" in ck and ("cmd" in ck or "adams" in ck))):
                in_python = False
            continue  # non-control-flow statements are not relevant to E104

        # Skip control flow inside Python sections
        if in_python:
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

# Adams type compatibility: some schema types are super-types of others.
# Adams applies implicit type-widening in many places — e.g. a Part may be
# used wherever an Rframe (reference frame) is expected because Adams silently
# uses the part's center-of-mass marker.
# Keys are actual types (upper-cased); values are accepted super-types.
_TYPE_IS_A = {
    # Every object is an "Adams" object
    "PART":            {"BODY", "RFRAME", "ADAMS", "ALL"},
    "FE_PART":         {"BODY", "RFRAME", "ADAMS"},
    "FLEX_BODY":       {"BODY", "RFRAME", "ADAMS"},
    "GROUND":          {"BODY", "PART",   "RFRAME", "ADAMS"},
    "POINT_MASS":      {"BODY", "RFRAME", "ADAMS"},
    # Markers satisfy any positional/orientational role
    "MARKER":          {"RFRAME", "TRIAD", "POSITION", "ADAMS"},
    "FMARKER":         {"RFRAME", "TRIAD", "MARKER", "POSITION", "ADAMS"},
    # Mechanism subtypes
    "RUN":             {"MECHANISM"},
    "MECHANISM":       {"RFRAME", "ADAMS"},
    # Force subtypes
    "SFORCE":          {"FORCE", "ADAMS"},
    "VFORCE":          {"FORCE", "ADAMS"},
    "VTORQUE":         {"FORCE", "ADAMS"},
    "BUSHING":         {"FORCE", "ADAMS"},
    "GENFORCE":        {"FORCE", "ADAMS"},
    "SPRING":          {"FORCE", "ADAMS"},
    "BEAM":            {"FORCE", "ADAMS"},
    "FIELD":           {"FORCE", "ADAMS"},
    "CCURVE":          {"CONSTR", "FORCE", "ADAMS"},
    # Measure subtypes
    "MEA_OBJECT":      {"MEASURE"},
    "MEA_SOLVCOMP":    {"MEASURE"},
    "MEA_ANGLE":       {"MEASURE"},
    "MEA_VIEWCOMP":    {"MEASURE"},
    "MEA_PT2PT":       {"MEASURE"},
    # Graph/geometry subtypes
    "CYLINDER":        {"GRAPH"},
    "ELLIPSOID":       {"GRAPH"},
    "CSG":             {"GRAPH"},
    "BOX":             {"GRAPH"},
    "SPHERE":          {"GRAPH"},
    "TORUS":           {"GRAPH"},
    "FRUSTUM":         {"GRAPH"},
    "GLINK":           {"GRAPH", "CONTACT_SOLID"},
    "OUTLINE":         {"GRAPH", "GWIRE"},
    # Additional geometry subtypes missing from earlier batch
    "EXTRUSION":       {"GRAPH"},
    "ARC":             {"GRAPH"},
    "REVOLUTION":      {"GRAPH"},
    "GCURVE":          {"GRAPH", "GWIRE"},
    "GSPDP":           {"GRAPH"},
    # Animation subtypes
    "ANIMATION":       {"ANIM_BASE"},
    # Joint / constraint subtypes
    "JOINT":           {"CONSTR", "ADAMS"},
    "JPRIM":           {"CONSTR", "ADAMS"},
    "PCURVE":          {"CONSTR", "ADAMS"},
    # Generic CONSTR (e.g. from constraint copy) accepted wherever a specific
    # constraint subtype is expected.  Adams trusts the user to copy the
    # right subtype.
    "CONSTR":          {"JPRIM", "CCURVE"},
    # 'All' wildcard — accepted anywhere Adams allows a wildcard selection
    "ALL":             {"VIEW", "GROUP", "PART", "BODY", "RFRAME", "ADAMS", "ENT"},
    # SelectList is the type of the SELECT_LIST built-in: accepted as Group
    "SELECTLIST":      {"GROUP"},
    # Design point is a positional reference
    "DESIGN_POINT":    {"POSITION", "RFRAME"},
    # GUI dialog box subtypes
    "GI_DBOX":         {"GI_GUI"},
    # External system can be used as a reference frame
    "EXTERNAL_SYSTEM": {"RFRAME"},
    # Equation subtypes
    "EQU":             {"PART", "TFSISO"},
    "LSE":             {"EQU", "PART"},
    "GSE":             {"EQU", "PART"},
    # Additional FORCE subtypes (spring-damper-preload, modal force, gravity, etc.)
    "SPDP":            {"FORCE", "ADAMS"},
    "MFORCE":          {"FORCE", "ADAMS"},
    "ACCGRAV":         {"FORCE", "ADAMS"},
    # Generic FORCE (e.g. from force copy) accepted wherever a specific
    # force subtype is expected.
    "FORCE":           {"MFORCE", "ACCGRAV", "BEAM", "BUSHING", "SPDP"},
    # Additional MEASURE subtypes
    "MEA_POINT":       {"MEASURE"},
    # GUI subtypes
    "GI_WINDOW":       {"GI_GUI"},
    "GI_CONTAINER":    {"GI_GUI"},
    # Graph/geometry subtypes (additional)
    "PLATE":           {"GRAPH"},
    "CIRCLE":          {"GRAPH"},
    # TFSISO (transfer function, ISO) as equation
    "TFSISO":          {"EQU", "PART"},
    # MACRO is a top-level object accepted anywhere ALL is
    "MACRO":           {"ALL", "ADAMS"},
    # User-defined elements
    "UDEINST":         {"ALL", "ADAMS"},
    "UDEDEF":          {"ALL", "ADAMS"},
    # Variable-like data elements — Adams accepts any of these where Var is expected
    "SPLINE":          {"VAR"},
    "SOLVAR":          {"VAR"},
    "ARRAY":           {"VAR"},
    "PINPUT":          {"VAR"},
    "POUTPUT":         {"VAR"},
    "VVAR":            {"VAR"},
    # Generic Var (e.g. from data_element copy) accepted where specific subtypes expected
    "VAR":             {"SOLVAR"},
    # Result set is a data element compatible with spline/var queries
    "RESSET":          {"SPLINE", "VAR"},
    # Motion is a top-level Adams object
    "MOTION":          {"ADAMS"},
    # GRAPH is also accepted wherever a specific geometry subtype is expected
    # (this arises from geometry copy commands which record the copy as the
    # base GRAPH type rather than the original subtype).
    "GRAPH":           {
        "CIRCLE", "BOX", "CYLINDER", "FRUSTUM", "ELLIPSOID", "GSPDP",
        "ARC", "EXTRUSION", "REVOLUTION", "GCURVE", "GWIRE",
        "TORUS", "SPHERE", "PLATE", "OUTLINE", "GLINK",
    },
}


def _types_compatible(actual_type, expected_type):
    """Return True if actual_type is the same as or a subtype of expected_type.

    Special cases:
    - expected_type == 'ALL': Adams wildcard, accepts any object.
    - actual_type == 'ALL': entity copy returns the generic ALL type; Adams
      trusts the user to copy the right subtype, so ALL is accepted anywhere.
    - Same type (case-insensitive): always compatible.
    - Otherwise: look up actual_type in _TYPE_IS_A and check if expected_type
      is one of its accepted supertypes.
    """
    a = actual_type.upper()
    e = expected_type.upper()
    if e == "ALL":
        return True
    if a == "ALL":
        return True
    if a == e:
        return True
    return e in _TYPE_IS_A.get(a, set())


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

            # Array-valued args (e.g. coupler joint_name = .m.rev1, .m.rev2)
            # hold a comma-separated list — skip reference checking, as
            # individual elements cannot be reliably extracted here.
            if arg_def.get("array"):
                continue

            # Skip runtime expressions
            val = arg.value
            if "$" in val or val.lower().startswith("(") or "eval(" in val.lower():
                continue

            # Strip surrounding quotes for symbol lookup (Adams allows both
            # "front" and front to refer to the same view object).
            lookup_val = val.strip('"\'')

            symbol = symbols.lookup(lookup_val)
            expected_type = arg_def.get("object_type", "")

            if symbol:
                if expected_type and not _types_compatible(symbol.object_type, expected_type):
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
                # Suppress I202 if the name plausibly comes from an eval
                # expression that creates objects with a matching prefix
                # (e.g. loop-generated names like .model.mass_1.cm).
                if symbols.has_dynamic_prefix_match(lookup_val):
                    continue
                # Suppress I202 for any path that contains 'ground' as a component
                # (e.g. .MODEL_1.ground, .MODEL_1.ground.cm) — ground is
                # pre-created by Adams in every model and never defined in .cmd
                # files.  A path like '.model.ground.mkr' refers to a marker
                # on the built-in ground part; '.model.ground' IS the ground part.
                path_components = [
                    c.strip('"\'').lower()
                    for c in lookup_val.rstrip('"\'').split('.')
                    if c.strip('"\'')
                ]
                if "ground" in path_components:
                    continue
                # Suppress I202 for .materials.* references — Adams ships a
                # global materials library that is never defined in .cmd files.
                if lookup_val.lower().startswith(".materials.") or lookup_val.lower() == ".materials":
                    continue
                # Suppress I202 for custom colour strings (COLOR_R...G...B...).
                # Adams accepts these as colour identifiers; they are not objects.
                if lookup_val.upper().startswith("COLOR_"):
                    continue
                # Suppress I202 for GUI panel paths (.gui.*) — these are UI
                # elements, not model objects, and are never defined in .cmd files.
                if lookup_val.lower().startswith(".gui."):
                    continue
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
