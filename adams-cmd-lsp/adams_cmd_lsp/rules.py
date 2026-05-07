"""Lint rules for Adams CMD files.

Each rule is a callable:
    rule(statements, schema, symbols) -> list[Diagnostic]

Rules are collected in ALL_RULES at the bottom of this module.
"""

from .diagnostics import Diagnostic, Severity
from .parser import Statement, _char_to_line_col
from .macros import MacroDefinition, resolve_macro_argument_name


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _canonical_key(stmt):
    """Return the resolved command key if available, otherwise raw key."""
    return stmt.resolved_command_key or stmt.command_key


def _stmt_start_col(stmt):
    """Return the 0-based column of the first token of the statement.

    Falls back to 0 if command_key_tokens is empty (e.g. blank/comment stmts).
    """
    return stmt.command_key_tokens[0][2] if stmt.command_key_tokens else 0


# ---------------------------------------------------------------------------
# Adams entity type names (used by type_filter / type= arguments, DB_ENT)
#
# These are the user-visible type names accepted by Adams for filtering
# entities.  Derived from the class_name_list in Adams source (root.c).
# Adams performs case-insensitive prefix matching on these names, so
# 'spring' matches 'Spring_damper', 'constraint' matches 'Constraint', etc.
# ---------------------------------------------------------------------------
_ADAMS_ENTITY_TYPE_NAMES = [
    # Simulation topology
    "marker", "part", "joint", "primitive_joint", "coupler", "motion",
    "constraint", "general_constraint", "user_constraint", "higher_pair_contact",
    "floating_marker",
    # Force elements
    "force", "spring_damper", "spring_damper_graphic", "beam", "bushing",
    "field", "single_component_force", "force_vector", "torque_vector",
    "gravity_field", "general_force", "flexible_body_modal_force",
    "point_to_point_force", "contact", "contact_force_graphic", "friction",
    "gear", "tire",
    # Geometry
    "geometry", "arc", "circle", "block", "cylinder", "sphere", "torus",
    "ellipsoid", "extrusion", "revolution", "shell", "solid", "bspline",
    "outline", "polyline", "plate", "frustum", "contact_solid", "contact_curve",
    "wire_geometry", "link", "plane_surf", "solid_geometry", "blendfeature",
    "holefeature", "thin_shell_feature", "feature", "section", "face", "edge",
    # Data elements
    "data_element", "variable", "variable_class", "differential_equation",
    "linear_state_equation", "general_state_equation", "spline",
    "adams_matrix", "adams_array", "adams_string", "adams_surface",
    "adams_curve", "equation",
    # Flexible bodies
    "flexible_body", "fe_part", "fe_load",
    # Output / analysis
    "request", "sensor", "measure", "analysis", "analysis_function",
    "multi_run_analysis", "result_set", "result_set_component", "plot_curve",
    "curve_curve", "plot", "plot3d", "subplot", "page", "page_template",
    "response_surface", "linear_results", "mck", "eigen", "scatter",
    "spec_line", "report", "simulation_script",
    # Groups & model structure
    "group", "library", "subsystem", "model", "plugin",
    # Miscellaneous
    "macro", "note", "material", "color", "animation", "view",
    "time_marker", "legend", "image", "point", "body", "triad",
    "reference_frame", "position", "construction_grid",
    "symmetry_relationship", "clearance",
    # Catch-all
    "all",
]


# ---------------------------------------------------------------------------
# Adams design function names (used by rule_unwrapped_design_function / E105)
#
# Any identifier in this set, when used as a bare argument value followed
# immediately by '(', is a design-function call that REQUIRES outer
# parentheses: '(func(...))' or '(eval(func(...)))'.
# Sourced from resources/adams_design_functions/ filenames (one per function).
# ---------------------------------------------------------------------------
_ADAMS_DESIGN_FUNCTIONS = frozenset({
    # Math / trig
    "abs", "acos", "aint", "anint", "asin", "atan", "atan2",
    "ceil", "clip", "cos", "cosh", "dtor", "exp", "floor", "int",
    "log", "log10", "mod", "nint", "rtod", "rtoi", "sign", "sin",
    "sinh", "sqrt", "tan", "tanh",
    # Vector / matrix math
    "allm", "anym", "cols", "compress", "cond", "cross", "det",
    "diff", "differentiate", "dim", "dm", "dmat", "dot", "element",
    "exclude", "first", "first_n", "integr", "integrate", "inverse",
    "last", "last_n", "mag", "maxi", "mean", "meshgrid", "mini",
    "mode", "norm", "norm2", "normalize", "prod", "reshape", "reverse",
    "roll", "rows", "series", "series2", "shape", "sort", "sort_by",
    "sort_index", "ssq", "stack", "sum", "transpose", "unique", "unwrap",
    # Interpolation / spline
    "akima_spline", "akima_spline2", "cspline", "cubic_spline",
    "griddata", "hermite_spline", "interp1", "interp2", "interpft",
    "linear_spline", "notaknot_spline", "polyfit", "polyval",
    "resample", "spline",
    # Signal processing
    "bartlett", "bartlett_window", "blackman", "blackman_window",
    "butter_denominator", "butter_filter", "butter_numerator",
    "buttord_frequency", "buttord_order", "detrend", "fftmag",
    "fftphase", "filter", "filtfilt", "frequency", "hamming",
    "hamming_window", "hanning", "hanning_window", "hot_spots",
    "parzen", "parzen_window", "psd", "pwelch", "rectangular",
    "rectangular_window", "rms", "triangular", "triangular_window",
    "welch", "welch_window",
    # Bode / control
    "bodeabcd", "bodelse", "bodelsm", "bodeseq", "bodetfcoef", "bodetfs",
    # Adams location functions
    "loc_along_line", "loc_by_flexbody_nodeid", "loc_cylindrical",
    "loc_frame_mirror", "loc_global", "loc_inline", "loc_loc", "loc_local",
    "loc_mirror", "loc_on_axis", "loc_on_line", "loc_perpendicular",
    "loc_plane_mirror", "loc_relative_to", "loc_spherical",
    "loc_to_flexbody_nodeid", "loc_x_axis", "loc_y_axis", "loc_z_axis",
    # Adams orientation functions
    "ori_align_axis", "ori_align_axis_eul", "ori_all_axes", "ori_along_axis",
    "ori_frame_mirror", "ori_global", "ori_in_plane", "ori_local",
    "ori_mirror", "ori_one_axis", "ori_ori", "ori_plane_mirror",
    "ori_relative_to",
    # Adams result / runtime functions
    "ax", "ay", "az", "dx", "dy", "dz", "measure", "phi", "pitch",
    "psi", "theta", "yaw",
    # Database / object query
    "aggregate_mass", "align", "balance", "center",
    "db_active", "db_ancestor", "db_changed", "db_children", "db_count",
    "db_default", "db_default_name", "db_default_name_for_type",
    "db_delete_dependents", "db_del_param_dependents",
    "db_del_unparam_dependents", "db_dependents",
    "db_dependents_exhaustive", "db_descendants", "db_exists",
    "db_field_filter", "db_field_type", "db_filter_name", "db_filter_type",
    "db_full_name_from_short", "db_full_type_fields",
    "db_immediate_children", "db_object_count", "db_obj_exists",
    "db_obj_exists_exhaustive", "db_obj_from_name_type", "db_of_class",
    "db_of_type_exists", "db_oldest_ancestor", "db_referents",
    "db_referents_exhaustive", "db_short_name", "db_two_way", "db_type",
    "db_type_fields", "find_macro_from_command", "max", "min",
    # String functions
    "append", "expr_exists", "expr_reference", "expr_references",
    "expr_string", "on_off", "param_string", "parse_status", "refs_string",
    "status_print", "stoi", "stoo", "stor", "str_case", "str_chr",
    "str_compare", "str_date", "str_delete", "str_find", "str_find_count",
    "str_find_in_strings", "str_find_n", "str_insert", "str_is_real",
    "str_is_space", "str_length", "str_match", "str_merge_strings",
    "str_print", "str_remove_whitespace", "str_replace_all", "str_split",
    "str_sprintf", "str_substr", "str_timestamp", "str_xlate", "user_string",
    # File / system
    "aview_edit_file", "backup_file", "chdir", "copy_files",
    "execute_view_command", "file_alert", "file_directory_name",
    "file_exists", "file_minus_ext", "file_temp_name", "getcwd", "getenv",
    "guicleanup", "local_file_name", "mkdir", "putenv", "rand",
    "remove_file", "rename_file", "rmdir", "security_check", "sys_info",
    "term_status",
    # Unique name utilities
    "unique_file_name", "unique_full_name", "unique_id", "unique_local_name",
    "unique_name", "unique_name_in_hierarchy", "unique_partial_name",
    # Time / simulation
    "pi", "sim_status", "sim_time", "step", "time", "timer_cpu",
    "timer_elapsed",
    # Matrix transformations
    "convert_angles", "tmat", "tmat3",
    # FE / flex body
    "dura_hot_spots", "dura_life", "dura_max_stress", "dura_top_spots",
    "node_ids_closest_to", "node_ids_in_volume", "node_ids_within_radius",
    "node_id_closest", "node_id_is_interface", "node_node_closest",
    "top_spots",
    # GUI / interactive
    "alert", "alert2", "alert3", "pick_object", "select_directory",
    "select_field", "select_file", "select_multi_text", "select_object",
    "select_objects", "select_request_ids", "select_text", "select_type",
    # Conditional (IF() function — not the control-flow keyword)
    "if",
    # Eigenvalue
    "eigenvalues_i", "eigenvalues_r", "eig_di", "eig_dr", "eig_vi", "eig_vr",
    # Table
    "otable_changed_cells", "table_column_selected_cells", "table_get_cells",
    "table_get_dimension", "table_get_reals", "table_get_selected_cols",
    "table_get_selected_rows",
    # DOE
    "doe_matrix", "doe_num_terms",
    # Read / write (T/O format)
    "read_t_o_attribute_exists", "read_t_o_block_exists",
    "read_t_o_check_header", "read_t_o_close_file", "read_t_o_find_block",
    "read_t_o_find_subblock", "read_t_o_integer", "read_t_o_next_attribute",
    "read_t_o_next_block", "read_t_o_open_file", "read_t_o_read_table_line",
    "read_t_o_real", "read_t_o_real_array",
    "read_t_o_start_subblock_table_read", "read_t_o_start_table_read",
    "read_t_o_string", "read_t_o_subblock_integer", "read_t_o_subblock_real",
    "read_t_o_subblock_real_array", "read_t_o_subblock_string",
    "read_t_o_subblock_table_column", "read_t_o_table_column",
    "read_t_o_units",
    "write_i_n_table_reals", "write_t_o_close_file", "write_t_o_comment",
    "write_t_o_data_block", "write_t_o_integer", "write_t_o_open_file",
    "write_t_o_pop_precision", "write_t_o_push_precision", "write_t_o_real",
    "write_t_o_real_array", "write_t_o_string", "write_t_o_subblock",
    "write_t_o_table_header", "write_t_o_table_line", "write_t_o_table_reals",
    "write_t_o_table_string", "write_t_o_units",
    # Misc
    "angles", "tilde", "units_conversion_factor", "units_string",
    "units_type", "units_value", "val", "valat", "vali", "user",
})


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
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow or stmt.is_property_assignment:
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

        # Suppress E001 if the full command key matches a workspace-discovered
        # macro from the MacroRegistry.  Stash the MacroDefinition on the
        # statement so rule_macro_invalid_argument can validate arguments.
        if symbols.macro_registry is not None:
            macro_def = symbols.macro_registry.lookup_command(stmt.command_key)
            if macro_def is not None:
                stmt._macro_def = macro_def
                continue

        # Report the problematic token position
        col = sum(len(t) + 1 for t in tokens[:error_index]) if error_index else 0
        bad_token = tokens[error_index] if error_index is not None and error_index < len(tokens) else stmt.command_key
        message = f"Unknown command: '{stmt.command_key}'"
        if symbols.macro_registry is None and symbols.show_macro_hint:
            message += (
                " If this is a user-defined macro, enable "
                "'msc-adams.linter.scanWorkspaceMacros' to scan the workspace for macro definitions."
            )
        start_col = _stmt_start_col(stmt)
        diagnostics.append(Diagnostic(
            line=stmt.line_start,
            column=start_col + col,
            end_line=stmt.line_start,
            end_column=start_col + col + len(bad_token),
            code="E001",
            message=message,
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
            start_col = _stmt_start_col(stmt)
            return Diagnostic(
                line=stmt.line_start,
                column=start_col,
                end_line=stmt.line_start,
                end_column=start_col + len(stmt.command_key),
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

            start_col = _stmt_start_col(stmt)
            diagnostics.append(Diagnostic(
                line=stmt.line_start,
                column=start_col,
                end_line=stmt.line_start,
                end_column=start_col + len(stmt.command_key),
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
    stack = []  # list of (keyword, line, col)
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

        start_col = _stmt_start_col(stmt)
        if kw in ("if", "for", "while"):
            stack.append((kw, stmt.line_start, start_col))
        elif kw == "elseif":
            if not stack or stack[-1][0] not in ("if",):
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=start_col,
                    end_line=stmt.line_start,
                    end_column=start_col + len(kw),
                    code="E104",
                    message="'elseif' without matching 'if'",
                    severity=Severity.ERROR,
                ))
        elif kw == "else":
            if not stack or stack[-1][0] != "if":
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=start_col,
                    end_line=stmt.line_start,
                    end_column=start_col + len(kw),
                    code="E104",
                    message="'else' without matching 'if'",
                    severity=Severity.ERROR,
                ))
        elif kw == "end":
            if not stack:
                diagnostics.append(Diagnostic(
                    line=stmt.line_start,
                    column=start_col,
                    end_line=stmt.line_start,
                    end_column=start_col + len(kw),
                    code="E104",
                    message="'end' without matching 'if', 'for', or 'while'",
                    severity=Severity.ERROR,
                ))
            else:
                stack.pop()

    # Any unclosed blocks remaining in the stack
    for kw, line, col in stack:
        diagnostics.append(Diagnostic(
            line=line,
            column=col,
            end_line=line,
            end_column=col + len(kw),
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

            # DB_ENT arguments (type_filter, type=) take an Adams entity-type
            # name string, not an object reference.  Validate against the
            # known list of entity type names using prefix matching (the same
            # way Adams resolves them) and never emit I202.
            if arg_def.get("db_type") == "DB_ENT":
                val_lower = lookup_val.lower()
                if not any(name.startswith(val_lower)
                           for name in _ADAMS_ENTITY_TYPE_NAMES):
                    diagnostics.append(Diagnostic(
                        line=arg.value_line,
                        column=arg.value_column,
                        end_line=arg.value_line,
                        end_column=arg.value_column + len(val),
                        code="E004",
                        message=(
                            f"Unknown entity type name: '{val}'. "
                            "Expected a valid Adams entity type "
                            "(e.g. 'part', 'marker', 'constraint', "
                            "'force', 'spring', 'geometry')."
                        ),
                        severity=Severity.ERROR,
                    ))
                continue

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
# User macro argument validation
# ---------------------------------------------------------------------------

def rule_macro_invalid_argument(statements, schema, symbols):
    """E002 (macro) — Argument not in the user-defined macro's parameter list.

    Fires only when the statement was matched to a MacroDefinition from the
    MacroRegistry (i.e. stmt._macro_def was set by rule_unknown_command).
    Skips validation when the macro has no declared parameters — either
    because the macro file could not be scanned or because the macro truly
    accepts anything.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue

        macro_def = getattr(stmt, "_macro_def", None)
        if not isinstance(macro_def, MacroDefinition):
            continue
        if not macro_def.parameters:
            # No declared parameters — skip validation to avoid false positives
            continue

        for arg in stmt.arguments:
            if resolve_macro_argument_name(macro_def, arg.name) is None:
                diagnostics.append(Diagnostic(
                    line=arg.name_line,
                    column=arg.name_column,
                    end_line=arg.name_line,
                    end_column=arg.name_column + len(arg.name),
                    code="E002",
                    message=(
                        f"Invalid argument '{arg.name}' for macro '{macro_def.command}'"
                    ),
                    severity=Severity.ERROR,
                ))

    return diagnostics


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

def rule_unwrapped_design_function(statements, schema, symbols):
    """E105 — Design function call used as argument value without outer parentheses.

    Adams CMD requires that any design-function call used as an argument value
    be wrapped in outer parentheses so the parser recognises it as an
    expression rather than a bare word.  Both forms are valid:

        location = (loc_relative_to(...))          ! parametric
        location = (eval(loc_relative_to(...)))    ! immediate evaluation

    The bare form is NOT valid and Adams will treat it as a literal string:

        location = loc_relative_to(...)            ! ERROR — missing outer ()

    Detection: if an argument value starts with an identifier that is a known
    Adams design function, immediately followed by '(', flag it as E105.
    Values already starting with '(' (including '(eval(...))'), '"', "'",
    or '$' are skipped.
    """
    diagnostics = []
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        for arg in stmt.arguments:
            val = arg.value.strip()
            if not val:
                continue
            # Already wrapped in parens, quoted, or a macro parameter — OK
            if val[0] in ('(', '"', "'", '$'):
                continue
            # Must start with a valid identifier character
            if not (val[0].isalpha() or val[0] == '_'):
                continue
            # Extract the leading identifier
            i = 0
            while i < len(val) and (val[i].isalnum() or val[i] == '_'):
                i += 1
            if i == 0:
                continue
            # Must be immediately followed by '(' to be a function call
            if i >= len(val) or val[i] != '(':
                continue
            name = val[:i].lower()
            if name not in _ADAMS_DESIGN_FUNCTIONS:
                continue
            diagnostics.append(Diagnostic(
                line=arg.value_line,
                column=arg.value_column,
                end_line=arg.value_line,
                end_column=arg.value_column + i,
                code="E105",
                message=(
                    f"Design function '{name}' used without outer parentheses. "
                    f"Use '({name}(...))' or '(eval({name}(...)))'."
                ),
                severity=Severity.ERROR,
            ))
    return diagnostics


ALL_RULES = [
    rule_unknown_command,           # E001 — sets resolved_command_key as side-effect
    rule_invalid_argument,          # E002
    rule_duplicate_argument,        # E003
    rule_invalid_enum_value,        # E004
    rule_missing_required,          # E005 / W005
    rule_manual_adams_id,           # I006
    rule_exclusive_conflict,        # E006
    rule_unbalanced_parens,         # E101
    rule_unclosed_quote,            # E102
    rule_control_flow_balance,      # E104
    rule_unwrapped_design_function,  # E105
    rule_type_mismatch,             # W201 / I202
    rule_macro_invalid_argument,    # E002 (macro) — must run after rule_unknown_command
]
