"""LSP server for Adams CMD language.

Uses pygls 2.x (from pygls.lsp.server import LanguageServer).
Start via:
    python -m adams_cmd_lsp          # stdio (default, for editors)
    adams-cmd-lsp                    # same, via entry point
    adams-cmd-lsp --tcp --port 2087  # TCP, for debugging
"""

import argparse
import fnmatch
import logging
import os
import re
from pathlib import Path
from urllib.parse import urlparse, unquote, quote

from pygls.lsp.server import LanguageServer
from lsprotocol import types

from .linter import lint_text
from .parser import parse as _parse_cmd, _find_comment_start
from .schema import Schema
from .diagnostics import Severity
from .symbols import SymbolTable, build_symbol_table, _extract_eval_object_names, _EVAL_OBJECT_NAME_RE
from .object_index import ObjectIndex, index_file_objects, _resolve_command_keys
from .macros import (
    scan_macro_files, parse_macro_file, MacroRegistry, MacroDefinition, MacroParameter,
    DEFAULT_MACRO_PATTERNS, DEFAULT_IGNORE_DIRS, extract_macros_from_statements,
    _USER_ENTERED_COMMAND_RE, _COMMENT_PARAM_RE, _END_OF_PARAMETERS,
    resolve_macro_argument_name, _extract_params_from_text,
)
from .references import MacroIndex, index_file_text
from .rules import _ADAMS_ENTITY_TYPE_NAMES
from .ude import UdeRegistry, scan_ude_files, DEFAULT_UDE_PATTERNS


server = LanguageServer("adams-cmd-lsp", "v0.1.0")

# ---------------------------------------------------------------------------
# Macro parameter definition completions — type and qualifier constants
# ---------------------------------------------------------------------------

# Valid values for the t= qualifier on !$param lines.
# Primitives listed first (most common), then all Adams entity types,
# then 'list' last (special snippet form).
_PARAM_PRIMITIVE_TYPES = ["string", "str", "real", "integer"]
_PARAM_ENTITY_TYPES = sorted(_ADAMS_ENTITY_TYPE_NAMES)  # alphabetical
_PARAM_TYPE_VALUES = _PARAM_PRIMITIVE_TYPES + _PARAM_ENTITY_TYPES  # 'list' added dynamically

# Qualifier keys for !$param definition lines.
# Each entry: (key, insert_text_with_equals, description)
_PARAM_QUALIFIER_KEYS = [
    ("t",  "t=",  "type"),
    ("d",  "d=",  "default value"),
    ("ud", "ud=", "updated default"),
    ("ge", "ge=", "numeric constraint: \u2265 value"),
    ("gt", "gt=", "numeric constraint: > value"),
    ("le", "le=", "numeric constraint: \u2264 value"),
    ("lt", "lt=", "numeric constraint: < value"),
    ("c",  "c=",  "count"),
]

# Regex: matches a macro parameter definition line like  !$name  or  !$'name'
_PARAM_DEF_LINE_RE = re.compile(r'^!\$', re.IGNORECASE)

# Semantic token legend — used for macro command/argument highlighting
_SEMANTIC_TOKEN_TYPES = ["keyword", "parameter"]
_SEMANTIC_TOKEN_MODIFIERS: list = []
_SEMANTIC_LEGEND = types.SemanticTokensLegend(
    token_types=_SEMANTIC_TOKEN_TYPES,
    token_modifiers=_SEMANTIC_TOKEN_MODIFIERS,
)
_TOKEN_TYPE_KEYWORD = _SEMANTIC_TOKEN_TYPES.index("keyword")
_TOKEN_TYPE_PARAMETER = _SEMANTIC_TOKEN_TYPES.index("parameter")

# Schema and macro registry are loaded once in main() and stored here
_schema = None
_macro_registry = None
_macro_index = MacroIndex()          # persistent cross-file macro invocation index
_object_index = ObjectIndex()        # persistent cross-file Adams object index
_doc_cache = {}                      # uri -> (statements, symbol_table)
_macro_patterns = DEFAULT_MACRO_PATTERNS
_macro_ignore_patterns: list = []
_scan_workspace_macros = False
_ude_registry = None
_ude_patterns = DEFAULT_UDE_PATTERNS
_ude_ignore_patterns: list = []
_macro_show_hint: bool = True
_workspace_roots: list = []
_index_cmd_extensions = {".cmd", ".mac"}

# ---------------------------------------------------------------------------
# $variable navigation helpers
# ---------------------------------------------------------------------------

# Matches an Adams $variable token including dot-separated path components.
# e.g. '$_self.model' or '$_self.model.object_value.name'
# Each dot must be followed by at least one word char — this prevents a
# trailing dot when the next char is '$' (e.g. '$model.$arm2_name').
_DOLLAR_VAR_RE = re.compile(r'\$[a-zA-Z_]\w*(?:\.\w+)*')


def _get_dollar_var_at_position(line_text: str, character: int):
    """Return (var_token, col_start, col_end) if cursor is within a $variable token.

    var_token includes the leading '$'.
    Returns None when no $variable token spans the cursor.
    """
    for m in _DOLLAR_VAR_RE.finditer(line_text):
        if m.start() <= character < m.end():
            return (m.group(0), m.start(), m.end())
    return None


def _get_dollar_var_segment_at_position(line_text: str, character: int):
    """Return the single dot-separated segment of a $variable token under the cursor.

    For a token like ``$model.arm2_len`` the segments are ``$model`` and
    ``arm2_len``.  The first segment retains the ``$`` prefix; subsequent
    segments are the bare names between the dots.

    Returns a 5-tuple::

        (full_token, seg_col, seg_end_col, tok_col, tok_end_col)

    where *full_token* is the entire matched token (e.g. ``$model.arm2_len``),
    *seg_col* / *seg_end_col* bound only the segment the cursor is on, and
    *tok_col* / *tok_end_col* bound the full token.

    Returns ``None`` when no $variable token spans the cursor position.
    """
    for m in _DOLLAR_VAR_RE.finditer(line_text):
        tok_col = m.start()
        tok_end_col = m.end()
        if not (tok_col <= character < tok_end_col):
            continue
        full_token = m.group(0)
        # Build (start, end) pairs for each dot-segment within the line
        seg_start = tok_col
        for raw_seg in full_token.split('.'):
            seg_end = seg_start + len(raw_seg)
            if seg_start <= character < seg_end:
                return (full_token, seg_start, seg_end, tok_col, tok_end_col)
            seg_start = seg_end + 1  # +1 for the dot separator
        # Cursor is on a trailing dot — fall back to full token
        return (full_token, tok_col, tok_end_col, tok_col, tok_end_col)
    return None


def _find_variable_def_at_position(statements, schema, line: int, character: int):
    """If cursor is on the variable_name arg of a variable set/create command, return it.

    Returns (var_name_including_dollar, v_line, v_col, v_end_col) or None.
    """
    _VAR_DEF_COMMANDS = {"variable set", "variable create"}
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not (stmt.line_start <= line <= stmt.line_end):
            continue
        cmd_key = stmt.resolved_command_key or stmt.command_key
        if cmd_key not in _VAR_DEF_COMMANDS:
            continue
        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            if canonical != "variable_name":
                continue
            val = arg.value
            if not val or not val.startswith("$"):
                continue
            if arg.value_line != line:
                continue
            val_start = arg.value_column
            val_end = arg.value_column + len(val)
            if val_start <= character < val_end:
                return (val, line, val_start, val_end)
    return None


def _find_variable_definition_in_statements(statements, schema, var_token: str):
    """Find the 'variable set/create variable_name=X' statement that defines *var_token*.

    Tries progressively shorter dot-separated prefixes of *var_token* so that
    clicking anywhere within '$_self.model.object_value.name' still resolves
    to the definition of '$_self.model'.

    Returns (matched_name, def_line, val_col, val_end_col) or None.
    """
    _VARIABLE_DEF_COMMANDS = {"variable set", "variable create"}
    parts = var_token.split('.')
    candidates = ['.'.join(parts[:i]) for i in range(len(parts), 0, -1)]
    for candidate in candidates:
        candidate_lower = candidate.lower()
        for stmt in statements:
            if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
                continue
            cmd_key = stmt.resolved_command_key or stmt.command_key
            if cmd_key not in _VARIABLE_DEF_COMMANDS:
                continue
            for arg in stmt.arguments:
                canonical = schema.resolve_argument_name(cmd_key, arg.name)
                if canonical != "variable_name":
                    continue
                if not arg.value:
                    continue
                if arg.value.lower() == candidate_lower:
                    return (candidate, stmt.line_start, arg.value_column, arg.value_column + len(arg.value))
    return None


def _find_variable_references_in_text(text: str, var_name: str):
    """Return all (line, col, end_col) occurrences of *var_name* in *text*.

    A match is the exact *var_name* string (case-insensitive), even when followed
    by attribute access like '.object_value.name'.  Greedy prefix matches that
    extend *var_name* (e.g. '$_self.model_name' when looking for '$_self.model')
    are excluded by requiring that the match is not immediately followed by an
    alphanumeric character or underscore.
    """
    escaped = re.escape(var_name)
    # Lookahead: next char must not continue an identifier part (letter/digit/underscore)
    pattern = re.compile(escaped + r'(?![a-zA-Z0-9_])', re.IGNORECASE)
    results = []
    for i, line_text in enumerate(text.splitlines()):
        for m in pattern.finditer(line_text):
            results.append((i, m.start(), m.start() + len(var_name)))
    return results


def _find_macro_param_defs_in_text(text: str):
    """Scan *text* for comment-style macro parameter definitions (``!$name``).

    Returns a dict mapping the parameter token (``$name``, lowercased, with
    leading ``$``) to ``(line, col_start, col_end)`` where *col_start* and
    *col_end* span the ``$name`` token in the source line (excluding the
    leading ``!`` and any ``:qualifier`` suffixes).

    Scanning stops at the first ``!END_OF_PARAMETERS`` line.
    ``$_self`` is excluded — it is the macro's own namespace variable,
    not a user-declared parameter.
    """
    params = {}
    for i, line_text in enumerate(text.splitlines()):
        stripped = line_text.strip()
        if _END_OF_PARAMETERS.match(stripped):
            break
        m = _COMMENT_PARAM_RE.match(stripped)
        if m is None:
            continue
        # Group 1: quoted form  $'name'  (may include :qualifiers inside quotes)
        # Group 2: bare form    $name    (qualifiers are in group 3)
        if m.group(1) is not None:
            raw_name = m.group(1).split(':')[0].strip()
        else:
            raw_name = m.group(2)
        if not raw_name:
            continue
        param_token = '$' + raw_name
        if param_token.lower() == '$_self':
            continue
        # Locate the '$' character in the original (non-stripped) line.
        dollar_idx = line_text.find('$')
        if dollar_idx == -1:
            continue
        col_start = dollar_idx
        # For quoted form $'name:...' the source has '$' + "'" + raw_name;
        # for bare form $name the source has '$' + raw_name.
        if m.group(1) is not None:  # quoted form
            col_end = dollar_idx + 2 + len(raw_name)  # span: $'name
        else:  # bare form
            col_end = dollar_idx + 1 + len(raw_name)  # span: $name
        params[param_token.lower()] = (i, col_start, col_end)
    return params


def _find_macro_param_def_at_position(text: str, line: int, character: int):
    """Return param info if cursor is on the ``$name`` part of a ``!$name`` definition.

    Returns ``(param_token, line, col_start, col_end)`` where *param_token*
    includes the leading ``$``, or ``None`` if the cursor is not on a macro
    parameter definition.
    """
    lines_text = text.splitlines()
    if not (0 <= line < len(lines_text)):
        return None
    line_text = lines_text[line]
    stripped = line_text.strip()
    if _END_OF_PARAMETERS.match(stripped):
        return None
    m = _COMMENT_PARAM_RE.match(stripped)
    if m is None:
        return None
    if m.group(1) is not None:
        raw_name = m.group(1).split(':')[0].strip()
    else:
        raw_name = m.group(2)
    if not raw_name:
        return None
    param_token = '$' + raw_name
    if param_token.lower() == '$_self':
        return None
    dollar_idx = line_text.find('$')
    if dollar_idx == -1:
        return None
    col_start = dollar_idx
    # For quoted form $'name:...' the source has '$' + "'" + raw_name;
    # for bare form $name the source has '$' + raw_name.
    if m.group(1) is not None:  # quoted form
        col_end = dollar_idx + 2 + len(raw_name)  # span: $'name
    else:  # bare form
        col_end = dollar_idx + 1 + len(raw_name)  # span: $name
    if col_start <= character < col_end:
        return (param_token, line, col_start, col_end)
    return None


# ---------------------------------------------------------------------------
# SymbolKind mapping for Adams object types
# ---------------------------------------------------------------------------


_ADAMS_SYMBOL_KIND = {
    "Part": types.SymbolKind.Class,
    "Body": types.SymbolKind.Class,
    "Flex_Body": types.SymbolKind.Class,
    "FlexBody": types.SymbolKind.Class,
    "Mechanism": types.SymbolKind.Module,
    "MECHANISM": types.SymbolKind.Module,
    "MODEL": types.SymbolKind.Module,
    "Marker": types.SymbolKind.Field,
    "Joint": types.SymbolKind.Interface,
    "Constraint": types.SymbolKind.Interface,
    "Coupler": types.SymbolKind.Interface,
    "Fixed": types.SymbolKind.Interface,
    "ComplexJoint": types.SymbolKind.Interface,
    "Force": types.SymbolKind.Function,
    "Spring": types.SymbolKind.Function,
    "SpringDamper": types.SymbolKind.Function,
    "Bushing": types.SymbolKind.Function,
    "Beam": types.SymbolKind.Function,
    "VForce": types.SymbolKind.Function,
    "VTorque": types.SymbolKind.Function,
    "SForce": types.SymbolKind.Function,
    "GenForce": types.SymbolKind.Function,
    "Contact": types.SymbolKind.Function,
    "Variable": types.SymbolKind.Variable,
    "StateVariable": types.SymbolKind.Variable,
    "Array": types.SymbolKind.Array,
    "Spline": types.SymbolKind.Array,
    "Curve": types.SymbolKind.Array,
    "StringFixed": types.SymbolKind.String,
    "Geometry": types.SymbolKind.Object,
    "Cylinder": types.SymbolKind.Object,
    "Sphere": types.SymbolKind.Object,
    "Box": types.SymbolKind.Object,
    "BodyPath": types.SymbolKind.Object,
    "Shell": types.SymbolKind.Object,
    "Torus": types.SymbolKind.Object,
    "Run": types.SymbolKind.Namespace,
    "Analysis": types.SymbolKind.Namespace,
    "Ude": types.SymbolKind.Object,
    "UserElement": types.SymbolKind.Object,
    "Macro": types.SymbolKind.Module,
}

_SEVERITY_MAP = {
    Severity.ERROR: types.DiagnosticSeverity.Error,
    Severity.WARNING: types.DiagnosticSeverity.Warning,
    Severity.INFO: types.DiagnosticSeverity.Information,
}


# ---------------------------------------------------------------------------
# Document cache helpers
# ---------------------------------------------------------------------------

def _update_doc_cache(uri: str, text: str) -> None:
    """Parse and resolve command keys for *uri*, caching the result.

    The cache stores (statements, symbol_table) so that handlers that need
    symbol information (goto_definition, find_references, document_symbol)
    don't have to re-parse on every invocation.  The cache is invalidated
    on every did_change / did_open event.
    """
    if _schema is None:
        return
    try:
        statements = _parse_cmd(text)
        # Pre-resolve command keys so build_symbol_table sees canonical names
        _resolve_command_keys(statements, _schema)
        symbols = build_symbol_table(statements, _schema)
    except Exception:  # noqa: BLE001
        return
    _doc_cache[uri] = (statements, symbols)


def _get_doc_cache(uri: str, text: str = None):
    """Return (statements, symbols) from cache, building on demand if *text* supplied.

    Returns (None, None) when unavailable.
    """
    cached = _doc_cache.get(uri)
    if cached:
        return cached
    if text is not None:
        _update_doc_cache(uri, text)
        return _doc_cache.get(uri, (None, None))
    return None, None


# ---------------------------------------------------------------------------
# Adams object navigation helpers
# ---------------------------------------------------------------------------

def _get_eval_object_at_position(statements, line: int, character: int):
    """Find an Adams object name inside an eval() expression at the cursor.

    Complements :func:`_get_object_at_position` by scanning *all* argument
    types — Adams variables are frequently referenced inside ``(eval(...))``
    on ``real``, ``integer``, or ``function`` arguments where the schema type
    alone provides no hint that an object name is embedded.

    Returns:
        ``("reference", name, v_line, v_col, v_end_col)`` on success.
        ``None`` if no object name spans the cursor position.
    """
    if statements is None:
        return None
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not (stmt.line_start <= line <= stmt.line_end):
            continue
        for arg in stmt.arguments:
            val = arg.value
            if not val or "eval(" not in val.lower():
                continue
            # eval expressions are always single-line after continuation joining
            if arg.value_line != line:
                continue
            for e_name, e_line, e_col, e_end_col in _extract_eval_object_names(
                val, arg.value_line, arg.value_column
            ):
                if e_col <= character <= e_end_col:
                    return ("reference", e_name, e_line, e_col, e_end_col)
    return None


def _get_paren_object_at_position(statements, symbols, line: int, character: int):
    """Find an Adams object name inside a parenthesized (non-eval) expression at the cursor.

    Handles values like ``(.model.part.marker.location_global)`` on location,
    orientation, or other argument types that are not ``new_object``/
    ``existing_object`` in the schema.  The expression is not an ``eval()``,
    so :func:`_get_eval_object_at_position` does not pick it up.

    Strategy:
    1. Scan all argument values that start with ``(`` but do not contain ``eval(``.
    2. Extract Adams dot-path names using :data:`~symbols._EVAL_OBJECT_NAME_RE`.
    3. For each candidate name under the cursor, progressively strip the
       trailing path segment until a registered symbol is found — this handles
       property accessors like ``.location_global`` that are not objects.

    Returns:
        ``("reference", name, v_line, v_col, v_end_col)`` on success.
        ``None`` if no resolvable object name spans the cursor position.
    """
    if statements is None:
        return None
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not (stmt.line_start <= line <= stmt.line_end):
            continue
        for arg in stmt.arguments:
            val = arg.value
            if not val:
                continue
            if not val.startswith("("):
                continue
            if "eval(" in val.lower():
                continue
            if "$" in val:
                continue
            if arg.value_line != line:
                continue
            # Extract all dot-path names from the parenthesized expression
            for m in _EVAL_OBJECT_NAME_RE.finditer(val):
                e_col = arg.value_column + m.start()
                e_end_col = arg.value_column + m.end()
                if not (e_col <= character <= e_end_col):
                    continue
                full_name = m.group(0)
                # Progressively strip trailing segments until we find a known object.
                # This handles property accessors like .location_global that are not
                # registered in the symbol table.
                parts = full_name.split('.')
                # parts[0] is always '' because full_name starts with '.'
                for tail_count in range(0, len(parts) - 1):
                    candidate = '.'.join(parts[:len(parts) - tail_count])
                    if not candidate or candidate == '.':
                        break
                    if symbols is not None and (
                        symbols.lookup(candidate) is not None
                        or symbols.lookup_by_leaf_name(candidate.rsplit('.', 1)[-1])
                    ):
                        return ("reference", candidate, line, e_col, e_end_col)
                # No registered symbol found — return the full name anyway so
                # the cross-file index still has a chance to resolve it.
                return ("reference", full_name, line, e_col, e_end_col)
    return None


def _resolve_segment_at_cursor(name: str, val_start: int, character: int):
    """Given an Adams dot-path *name* and the cursor position, return the partial
    path corresponding to the dot-segment under the cursor.

    For example, with name='.model_1.part_1.marker_2' and the cursor sitting on
    'part_1', returns ('.model_1.part_1', seg_col_start, seg_col_end) where the
    column offsets are relative to the start of the argument value (val_start).

    The cursor column *character* is an absolute document column.

    Returns:
        (partial_path, seg_doc_col_start, seg_doc_col_end) on success.
        (name, val_start, val_start + len(name)) when the cursor is not within
        a recognisable segment (fall-back to the full name).
    """
    # Normalise so the path always starts with a '.' for uniform processing.
    norm = name if name.startswith('.') else '.' + name
    # Collect the start positions of each segment within the normalised string.
    # A segment boundary is every '.'; the root '.' at index 0 is also a boundary.
    segment_ends = []   # (seg_start_in_norm, seg_end_in_norm)
    i = 0
    while i < len(norm):
        if norm[i] == '.':
            seg_start = i  # include the dot as part of the path up to this point
            j = i + 1
            while j < len(norm) and norm[j] != '.':
                j += 1
            segment_ends.append((i, j))  # [i:j] is ".segment_name"
        i += 1

    # Map each segment to its absolute document column range.
    # norm_offset is the offset of norm[0] in the document.
    norm_offset = val_start - (0 if name.startswith('.') else 0)
    # name starts at val_start; if name had a leading '.', norm == name.
    # if name did not have a leading '.', norm has one extra char at front.
    extra = 0 if name.startswith('.') else 1

    for seg_idx, (seg_start, seg_end) in enumerate(segment_ends):
        # Document column of the first character of this segment's text (after the dot)
        seg_doc_col = val_start + max(0, seg_start - extra)
        seg_doc_end = val_start + (seg_end - extra)
        # Cursor hit test: is the character within the textual span of this segment?
        char_in_dot = seg_doc_col
        char_in_end = seg_doc_end
        # The dot itself (seg_doc_col) is not a clickable character for this
        # segment — require the cursor to be on the segment text, not the dot.
        if char_in_dot + 1 <= character < char_in_end:
            # Build the partial path up to and including this segment.
            partial = norm[:seg_end]
            if not name.startswith('.'):
                # The caller passed a non-dotted name; strip the leading dot we added.
                partial = partial.lstrip('.')
            return (partial, seg_doc_col, seg_doc_end)

    # Fallback: return the full name
    return (name, val_start, val_start + len(name))


def _get_object_at_position(statements, schema, symbols, line: int, character: int):
    """Find the Adams object name at cursor position (line, character).

    Scans parsed statement arguments for an existing_object or new_object arg
    whose value span (value_line, value_column … value_column+len(value))
    contains the cursor.

    Returns:
        (kind, name, v_line, v_col, v_end_col)  on success
        None                                      if no Adams object at cursor

    kind is "definition" for new_object args, "reference" for existing_object.
    """
    if schema is None or statements is None:
        return None

    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not (stmt.line_start <= line <= stmt.line_end):
            continue

        cmd_key = stmt.resolved_command_key or stmt.command_key
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue

        for arg in stmt.arguments:
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_def = cmd["args"].get(canonical or arg.name)
            if not arg_def:
                continue

            arg_type = arg_def.get("type")
            if arg_type not in ("new_object", "existing_object"):
                continue
            if arg_def.get("array"):
                continue

            val = arg.value
            if not val or "$" in val or val.lower().startswith("(") or "eval(" in val.lower():
                continue

            # Single-line span check — object names never wrap across lines
            if arg.value_line != line:
                continue

            val_start = arg.value_column
            val_end = arg.value_column + len(val)

            if val_start <= character <= val_end:
                lookup_val = val.strip("\"'")
                if not lookup_val:
                    continue
                kind = "definition" if arg_type == "new_object" else "reference"
                return (kind, lookup_val, line, val_start, val_end)

    return None


def _to_lsp_diagnostic(d):
    """Convert a Diagnostic dataclass to an LSP Diagnostic protocol object."""
    return types.Diagnostic(
        range=types.Range(
            start=types.Position(line=d.line, character=d.column),
            end=types.Position(line=d.end_line, character=d.end_column),
        ),
        message=d.message,
        source="adams-cmd-lint",
        code=d.code,
        severity=_SEVERITY_MAP.get(d.severity, types.DiagnosticSeverity.Information),
    )


def _validate_document(uri, text):
    """Lint the document text and publish diagnostics to the client."""
    try:
        diagnostics = lint_text(
            text,
            schema=_schema,
            macro_registry=_macro_registry if _scan_workspace_macros else None,
            show_macro_hint=_macro_show_hint,
            ude_registry=_ude_registry if _scan_workspace_macros else None,
        )
    except Exception as exc:  # noqa: BLE001
        # Never let a lint crash kill the server
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Error,
                message=f"adams-cmd-lint error: {exc}",
            )
        )
        diagnostics = []
    lsp_diags = [_to_lsp_diagnostic(d) for d in diagnostics]
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=uri, diagnostics=lsp_diags)
    )


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    doc = params.text_document
    _validate_document(doc.uri, doc.text)
    _index_document(doc.uri, doc.text)
    _update_doc_cache(doc.uri, doc.text)
    _refresh_object_index_for_file(doc.uri, doc.text)
    # If this is a macro file, register it in the registry immediately
    # (same as did_save) so callers in other open files get def-navigation
    # and E001 suppression without having to save the file first.
    changed = _refresh_macro_file(doc.uri, doc.text)
    changed_ude = _refresh_ude_file(doc.uri, doc.text)
    if (changed or changed_ude) and server.workspace:
        for open_uri, open_doc in list(server.workspace.text_documents.items()):
            if open_uri != doc.uri:
                _validate_document(open_uri, open_doc.source)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: types.DidChangeTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)
    _index_document(params.text_document.uri, doc.source)
    _update_doc_cache(params.text_document.uri, doc.source)
    # Cross-file object index is refreshed on open/save only — per-keystroke
    # re-indexing of the whole workspace would be too expensive.


@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(params: types.DidCloseTextDocumentParams):
    server.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri=params.text_document.uri, diagnostics=[])
    )
    _doc_cache.pop(params.text_document.uri, None)


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_save(params: types.DidSaveTextDocumentParams):
    doc = server.workspace.get_text_document(params.text_document.uri)
    _validate_document(params.text_document.uri, doc.source)
    _index_document(params.text_document.uri, doc.source)
    # If the saved file is a macro file, refresh that entry in the registry
    # and re-lint other open documents so E001 clears immediately.
    changed = _refresh_macro_file(params.text_document.uri, doc.source)
    changed_ude = _refresh_ude_file(params.text_document.uri, doc.source)
    if (changed or changed_ude) and server.workspace:
        for open_uri, open_doc in list(server.workspace.text_documents.items()):
            if open_uri != params.text_document.uri:
                _validate_document(open_uri, open_doc.source)
    # Update the workspace object index for cross-file navigation (save-based)
    _refresh_object_index_for_file(params.text_document.uri, doc.source)


def _uri_to_path(uri: str) -> str:
    """Convert a file:// URI to a local filesystem path."""
    parsed = urlparse(uri)
    path = unquote(parsed.path)
    # On Windows the path starts with /C:/... — strip the leading slash
    if os.name == "nt" and path.startswith("/") and len(path) > 2 and path[2] == ":":
        path = path[1:]
    return path


def _path_to_uri(path: str) -> str:
    """Convert a local filesystem path to a file:// URI."""
    p = Path(path)
    # Use as_posix() so we get forward slashes then url-encode
    posix = p.as_posix()
    # Encode special chars but keep slashes and colons (drive letter) intact
    encoded = quote(posix, safe="/:")
    if os.name == "nt" and not encoded.startswith("/"):
        # Windows: "C:/path" -> "file:///C:/path"
        return "file:///" + encoded
    return "file://" + encoded


def _collect_cmd_files(roots):
    """Walk *roots* and return all .cmd / .mac file paths.

    Skips directories in DEFAULT_IGNORE_DIRS (same set used by the macro
    scanner) so version-control folders, build artefacts, etc. are excluded.
    """
    results = []
    for root in roots:
        root_path = Path(root)
        if not root_path.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Prune ignored directories in-place so os.walk doesn't recurse
            dirnames[:] = [
                d for d in dirnames if d not in DEFAULT_IGNORE_DIRS
            ]
            for fname in filenames:
                if Path(fname).suffix.lower() in _index_cmd_extensions:
                    results.append(Path(dirpath) / fname)
    return results


def _index_document(uri: str, text: str) -> None:
    """Re-index a single document's macro invocations in _macro_index."""
    if _schema is None:
        return
    path = _uri_to_path(uri)
    if not path:
        return
    try:
        refs = index_file_text(text, _schema, source_file=path)
        _macro_index.update_file(path, refs)
        _macro_index.record_mtime(path)
    except Exception:  # noqa: BLE001
        pass


def _get_command_key_at_position(text: str, line: int, uri: str):
    """Return (origin, command_key, macro_def_or_None, origin_range) for the command at *line*.

    *origin* is one of:
    - ``"registry"``        — command matched a workspace macro in _macro_registry
    - ``"inline"``          — command matched an inline macro create/read in the file
    - ``"definition_site"`` — cursor is on a !USER_ENTERED_COMMAND line
    - ``None``              — not a macro invocation (built-in or unrecognised)

    *origin_range* is a (line, col_start, col_end) tuple marking the command key
    span in the source document.

    Returns None when no match is found.
    """
    if _schema is None:
        return None

    # Check if the cursor is on a !USER_ENTERED_COMMAND comment line in a .mac
    lines = text.splitlines()
    if 0 <= line < len(lines):
        m = _USER_ENTERED_COMMAND_RE.match(lines[line])
        if m:
            command_key = m.group(1).strip().lower()
            col_start = m.start(1)
            col_end = col_start + len(m.group(1).strip())
            macro_def = _macro_registry.lookup_command(command_key) if _macro_registry else None
            return ("definition_site", command_key, macro_def, (line, col_start, col_end))

    # Parse and find the statement at the cursor line
    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return None

    stmt = None
    for s in statements:
        if s.is_comment or s.is_blank:
            continue
        if s.line_start <= line <= s.line_end:
            stmt = s
            break
    if stmt is None:
        return None

    tokens = stmt.command_key.split() if stmt.command_key else []
    if not tokens:
        return None

    # If the command resolves as a built-in, it's not a macro
    resolved_key, _ = _schema.resolve_command_key(tokens)
    if resolved_key is not None:
        return None

    command_key = stmt.command_key.lower()
    first_line = lines[stmt.line_start] if 0 <= stmt.line_start < len(lines) else ""
    leading = len(first_line) - len(first_line.lstrip())
    origin_range = (stmt.line_start, leading, leading + len(stmt.command_key))

    # Check registry (workspace .mac files)
    if _macro_registry is not None:
        macro_def = _macro_registry.lookup_command(command_key)
        if macro_def is not None:
            return ("registry", command_key, macro_def, origin_range)

    # Check inline macros defined earlier in the same file
    path = _uri_to_path(uri)
    preceding = [s for s in statements if s.line_end < stmt.line_start]
    inline_macros = extract_macros_from_statements(preceding, _schema, source_file=path)
    for idef in inline_macros:
        if idef.command == command_key:
            return ("inline", command_key, idef, origin_range)

    return None


def _refresh_macro_file(uri: str, text: str) -> bool:
    """Re-parse *uri* and update _macro_registry if it matches a macro pattern.

    Returns True if the file matched a macro pattern and was processed without
    error (regardless of whether the registry content actually changed), so
    callers can decide whether to re-lint open documents.
    """
    global _macro_registry  # noqa: PLW0603
    if _macro_registry is None:
        return False
    path = _uri_to_path(uri)
    if not path:
        return False

    # Check whether this file matches any configured macro pattern.
    # Strategy: compute the path relative to each known workspace root and test
    # against the full glob pattern (e.g. "macros/*" must NOT match a file
    # outside the macros/ directory). Fall back to filename-only matching for
    # patterns whose last component is not the bare wildcard "*".
    matched = False
    for root in _workspace_roots:
        try:
            rel = Path(path).relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, pat) for pat in _macro_patterns):
                matched = True
                break
        except (ValueError, Exception):  # noqa: BLE001
            continue
    if not matched and not _workspace_roots:
        # No workspace roots yet (e.g. first save before INITIALIZED) — fall
        # back to filename matching, but only for patterns whose last segment
        # is not the bare "*" (which would match every file).
        filename = Path(path).name
        for pat in _macro_patterns:
            last = Path(pat).name
            if last != "*" and fnmatch.fnmatch(filename, last):
                matched = True
                break
    if not matched:
        return False
    # Always remove any stale entry first so the registry stays consistent
    # even if the parse step raises.
    _macro_registry.unregister_by_file(path)
    try:
        macro_def = parse_macro_file(text, source_file=path)
        if macro_def is not None:
            _macro_registry.register(macro_def)
    except Exception:  # noqa: BLE001
        return True
    return True


def _refresh_ude_file(uri: str, text: str) -> bool:
    """Re-parse *uri* and update _ude_registry if it matches a UDE pattern.

    Returns True if the file matched a UDE pattern and was processed.
    """
    if _ude_registry is None or _schema is None or not _scan_workspace_macros:
        return False
    path = _uri_to_path(uri)
    if not path:
        return False

    matched = False
    for root in _workspace_roots:
        try:
            rel = Path(path).relative_to(root).as_posix()
            if any(fnmatch.fnmatch(rel, pat) for pat in _ude_patterns):
                matched = True
                break
        except (ValueError, Exception):  # noqa: BLE001
            continue
    if not matched and not _workspace_roots:
        filename = Path(path).name
        for pat in _ude_patterns:
            last = Path(pat).name
            if last != "*" and fnmatch.fnmatch(filename, last):
                matched = True
                break
    if not matched:
        return False

    from .ude import parse_ude_file as _parse_ude_file
    path = str(Path(path).resolve())
    _ude_registry.unregister_by_file(path)
    try:
        defs = _parse_ude_file(text, _schema, source_file=path)
        for d in defs:
            _ude_registry.register(d)
    except Exception:  # noqa: BLE001
        return True
    return True


def _refresh_object_index_for_file(uri: str, text: str) -> None:
    """Re-index *uri*'s Adams object definitions and references in _object_index.

    Called on did_open and did_save so the cross-file navigation index stays current.
    """
    if _schema is None:
        return
    path = _uri_to_path(uri)
    if not path:
        return
    try:
        defs, refs = index_file_objects(text, _schema, source_file=path)
        _object_index.update_file(path, defs, refs)
        _object_index.record_mtime(path)
    except Exception:  # noqa: BLE001
        pass


def main():
    """Entry point for the adams-cmd-lsp LSP server."""
    global _schema, _macro_registry, _macro_patterns, _macro_ignore_patterns, _scan_workspace_macros, _macro_show_hint, _workspace_roots, _macro_index, _object_index, _doc_cache, _ude_registry, _ude_patterns, _ude_ignore_patterns  # noqa: PLW0603

    parser = argparse.ArgumentParser(
        prog="adams-cmd-lsp",
        description="Adams CMD Language Server",
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Use TCP transport instead of stdio (useful for debugging)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="TCP port (only with --tcp, default: 2087)",
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
        help="Glob patterns for macro file discovery (resolved relative to workspace roots)",
    )
    parser.add_argument(
        "--macro-ignore-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns to exclude from macro scanning",
    )
    parser.add_argument(
        "--scan-workspace-macros",
        action="store_true",
        default=False,
        help="Scan workspace folders for macro files on startup",
    )
    parser.add_argument(
        "--show-macro-hint",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Include a hint in E001 messages suggesting 'scanWorkspaceMacros' "
            "when no macro registry is active (default: on)"
        ),
    )
    # vscode-languageclient passes --stdio automatically; accept and ignore it.
    parser.add_argument(
        "--ude-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns for UDE definition file discovery (resolved relative to workspace roots)",
    )
    parser.add_argument(
        "--ude-ignore-paths",
        nargs="+",
        metavar="GLOB",
        default=[],
        help="Glob patterns to exclude from UDE scanning",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Use stdio transport (default, passed automatically by VS Code)",
    )
    args = parser.parse_args()

    _schema = Schema.load(args.schema) if args.schema else Schema.load()
    _macro_patterns = args.macro_paths if args.macro_paths else DEFAULT_MACRO_PATTERNS
    _macro_ignore_patterns = args.macro_ignore_paths or []
    _scan_workspace_macros = args.scan_workspace_macros
    _macro_show_hint = args.show_macro_hint
    _ude_patterns = args.ude_paths if args.ude_paths else DEFAULT_UDE_PATTERNS
    _ude_ignore_patterns = args.ude_ignore_paths or []

    # Build initial registry and index — always created so did_save can
    # refresh them later. Workspace folders are merged after client connects.
    _macro_registry = MacroRegistry()
    _ude_registry = UdeRegistry()
    _macro_index = MacroIndex()    # reset in case main() is called more than once
    _object_index = ObjectIndex()  # reset cross-file object navigation index
    _doc_cache.clear()             # reset per-document parse cache

    # Suppress the harmless "Cancel notification for unknown message id" warning
    # that pygls logs when VS Code sends $/cancelRequest after the hover response
    # has already been sent (race condition that is normal per the LSP spec).
    class _SuppressCancelWarning(logging.Filter):
        def filter(self, record):
            return "Cancel notification for unknown message id" not in record.getMessage()

    logging.getLogger("pygls.protocol.json_rpc").addFilter(_SuppressCancelWarning())

    if args.tcp:
        server.start_tcp("localhost", args.port)
    else:
        server.start_io()


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def goto_definition(params: types.DefinitionParams):
    """Jump to the definition of the macro or Adams object at the cursor.

    Tries in order:
    1. Macro definition (multi-word command → .mac file)
    2. Adams object definition (same-file symbol table lookup)
    3. Adams object definition (cross-file object index)

    Returns a LocationLink so VS Code underlines the full reference span on
    Ctrl+hover.
    """
    uri = params.text_document.uri
    line = params.position.line
    character = params.position.character
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return None

    # --- 1. Macro definition (existing behaviour) ---
    result = _get_command_key_at_position(text, line, uri)
    if result is not None:
        origin, _command_key, macro_def, origin_range = result
        src_line, src_col_start, src_col_end = origin_range
        origin_selection = types.Range(
            start=types.Position(line=src_line, character=src_col_start),
            end=types.Position(line=src_line, character=src_col_end),
        )
        if origin == "definition_site":
            # Cursor is on the !USER_ENTERED_COMMAND definition line — show references
            # (inverse navigation: same behaviour as Shift+F12 from the def site).
            refs = _macro_index.get_references(_command_key)
            locations = [
                types.LocationLink(
                    target_uri=_path_to_uri(file_path),
                    target_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    target_selection_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    origin_selection_range=origin_selection,
                )
                for file_path, ref in refs
            ]
            return locations if locations else None
        if macro_def is not None:
            def_uri = _path_to_uri(macro_def.source_file) if macro_def.source_file else uri
            target_range = types.Range(
                start=types.Position(line=macro_def.line, character=0),
                end=types.Position(line=macro_def.line, character=0),
            )
            return [types.LocationLink(
                target_uri=def_uri,
                target_range=target_range,
                target_selection_range=target_range,
                origin_selection_range=origin_selection,
            )]

    # --- 2 & 3. Adams object navigation ---
    if _schema is None:
        return None

    statements, symbols = _get_doc_cache(uri, text)
    if statements is None or symbols is None:
        return None

    obj = _get_object_at_position(statements, _schema, symbols, line, character)
    if obj is None:
        # Fallback: names inside (eval(...)) on any arg type (real, integer, etc.)
        obj = _get_eval_object_at_position(statements, line, character)
    if obj is None:
        # Fallback: names inside parenthesized non-eval expressions, e.g.
        # location=(.model.part.marker.location_global)
        obj = _get_paren_object_at_position(statements, symbols, line, character)
    if obj is not None:
        kind, name, v_line, v_col, v_end_col = obj

        # --- Per-segment resolution ---
        # When the cursor is on one segment of a multi-segment path (e.g. 'part_1'
        # in '.model_1.part_1.marker_2'), resolve only the partial path up to that
        # segment rather than the full path, and highlight just that segment.
        seg_name, seg_col, seg_end_col = _resolve_segment_at_cursor(
            name, v_col, character
        )
        if seg_name != name:
            # Cursor is on an intermediate segment — navigate to that partial path.
            name = seg_name
            v_col = seg_col
            v_end_col = seg_end_col

        origin_selection = types.Range(
            start=types.Position(line=v_line, character=v_col),
            end=types.Position(line=v_line, character=v_end_col),
        )

        if kind == "definition":
            # Cursor is on the definition site — show references (inverse navigation).
            # Same behaviour as Shift+F12 but triggered via Ctrl+Click.
            same_file_refs = symbols.get_references_by_name(name)
            locations = [
                types.LocationLink(
                    target_uri=uri,
                    target_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    target_selection_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    origin_selection_range=origin_selection,
                )
                for ref in same_file_refs
            ]
            current_path = os.path.normcase(os.path.normpath(_uri_to_path(uri)))
            for ref in _object_index.get_references(name):
                if os.path.normcase(os.path.normpath(ref.source_file)) == current_path:
                    continue
                ref_uri = _path_to_uri(ref.source_file) if ref.source_file else uri
                locations.append(types.LocationLink(
                    target_uri=ref_uri,
                    target_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    target_selection_range=types.Range(
                        start=types.Position(line=ref.line, character=ref.column),
                        end=types.Position(line=ref.line, character=ref.end_column),
                    ),
                    origin_selection_range=origin_selection,
                ))
            return locations if locations else None

        # Same-file lookup: full path first, then leaf name
        sym = symbols.lookup(name)
        if sym is None:
            leaf = SymbolTable._normalize(name).lower().rsplit('.', 1)[-1]
            candidates = symbols.lookup_by_leaf_name(leaf)
            if candidates:
                sym = candidates[0]

        if sym is not None:
            target_pos = types.Position(line=sym.line, character=0)
            target_range = types.Range(start=target_pos, end=target_pos)
            return [types.LocationLink(
                target_uri=uri,
                target_range=target_range,
                target_selection_range=target_range,
                origin_selection_range=origin_selection,
            )]

        # Cross-file lookup via object index
        current_path = os.path.normcase(os.path.normpath(_uri_to_path(uri)))
        cross_defs = _object_index.get_definitions(name)
        locations = []
        for d in cross_defs:
            if os.path.normcase(os.path.normpath(d.source_file)) == current_path:
                continue  # already checked same-file above
            def_uri = _path_to_uri(d.source_file) if d.source_file else uri
            target_pos = types.Position(line=d.line, character=0)
            target_range = types.Range(start=target_pos, end=target_pos)
            locations.append(types.LocationLink(
                target_uri=def_uri,
                target_range=target_range,
                target_selection_range=target_range,
                origin_selection_range=origin_selection,
            ))
        return locations if locations else None

    # --- 4. $variable navigation ---
    lines_text = text.splitlines()
    if 0 <= line < len(lines_text):
        # Is the cursor on a !$param_name definition in a macro header?
        # Return None so VS Code does not show "Click to show N definitions" in the
        # hover tooltip.  Use Shift+F12 (textDocument/references) to find usages.
        mac_param_def = _find_macro_param_def_at_position(text, line, character)
        if mac_param_def is not None:
            return None

        # Is the cursor on the variable_name arg of 'variable set'? → definition site
        var_def = _find_variable_def_at_position(statements, _schema, line, character)
        if var_def is not None:
            var_name, v_line, v_col, v_end_col = var_def
            origin_selection = types.Range(
                start=types.Position(line=v_line, character=v_col),
                end=types.Position(line=v_line, character=v_end_col),
            )
            ref_locs = _find_variable_references_in_text(text, var_name)
            locations = [
                types.LocationLink(
                    target_uri=uri,
                    target_range=types.Range(
                        start=types.Position(line=rl, character=rc),
                        end=types.Position(line=rl, character=re_),
                    ),
                    target_selection_range=types.Range(
                        start=types.Position(line=rl, character=rc),
                        end=types.Position(line=rl, character=re_),
                    ),
                    origin_selection_range=origin_selection,
                )
                for rl, rc, re_ in ref_locs
                if not (rl == v_line and rc == v_col)  # exclude the definition itself
            ]
            return locations if locations else None

        # Is the cursor on a $variable reference? → navigate to definition
        var_seg = _get_dollar_var_segment_at_position(lines_text[line], character)
        if var_seg is not None:
            full_token, seg_col, seg_end_col, tok_col, tok_end_col = var_seg
            # Resolve only the prefix up to the cursor's segment so that
            # e.g. cursor on '$model' in '$model.arm2_len' resolves '$model'
            # (the macro param) rather than the longer variable definition.
            cursor_prefix = full_token[:seg_end_col - tok_col]
            # Only attempt $variable resolution if the cursor prefix starts
            # with '$'.  Literal suffixes like 'pivot_I' in '$arm1_name.pivot_I'
            # are object name parts, not variable references.
            if cursor_prefix.startswith('$'):
                def_r = _find_variable_definition_in_statements(statements, _schema, cursor_prefix)
                if def_r is not None:
                    matched_name, def_line, def_col, def_end_col = def_r
                    # Only navigate if the match covers the cursor's segment
                    if matched_name.lower() == cursor_prefix.lower():
                        origin_selection = types.Range(
                            start=types.Position(line=line, character=seg_col),
                            end=types.Position(line=line, character=seg_end_col),
                        )
                        target_range = types.Range(
                            start=types.Position(line=def_line, character=def_col),
                            end=types.Position(line=def_line, character=def_end_col),
                        )
                        return [types.LocationLink(
                            target_uri=uri,
                            target_range=target_range,
                            target_selection_range=target_range,
                            origin_selection_range=origin_selection,
                        )]

                # Fallback: check macro parameter definitions (exact prefix only)
                mac_param_defs = _find_macro_param_defs_in_text(text)
                if cursor_prefix.lower() in mac_param_defs:
                    p_line, p_col, p_end_col = mac_param_defs[cursor_prefix.lower()]
                    origin_selection = types.Range(
                        start=types.Position(line=line, character=seg_col),
                        end=types.Position(line=line, character=seg_end_col),
                    )
                    target_range = types.Range(
                        start=types.Position(line=p_line, character=p_col),
                        end=types.Position(line=p_line, character=p_end_col),
                    )
                    return [types.LocationLink(
                        target_uri=uri,
                        target_range=target_range,
                        target_selection_range=target_range,
                        origin_selection_range=origin_selection,
                    )]

    return None


def _format_param_line(param) -> str:
    """Return a single Markdown list item for a MacroParameter."""
    parts = [f"- `{param.name}`"]
    if param.type_str:
        parts.append(f" *({param.type_str})*")
    if param.default is not None:
        parts.append(f" (default: `{param.default}`)")
    if param.docstring:
        parts.append(f" — {param.docstring}")
    return "".join(parts)


def _build_param_hover_md(param) -> str:
    """Return standalone Markdown for a single parameter (invocation-site hover)."""
    heading = f"**`{param.name}`**"
    if param.type_str:
        heading += f" *({param.type_str})*"
    if param.default is not None:
        heading += f" (default: `{param.default}`)"
    lines = [heading]
    if param.docstring:
        lines.append("")
        lines.append(param.docstring)
    return "\n".join(lines)


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(params: types.HoverParams):
    """Show hover documentation for macro command invocations.

    Returns Markdown with the macro name, help string, and parameter list
    for ``"registry"`` and ``"inline"`` origins.  When the cursor is on an
    argument name at an invocation site, returns info for that parameter only.
    Returns ``None`` for built-in commands (handled by the JS hover provider)
    and for the ``!USER_ENTERED_COMMAND`` definition site.
    """
    uri = params.text_document.uri
    line = params.position.line
    character = params.position.character
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return None

    result = _get_command_key_at_position(text, line, uri)
    if result is None:
        return None

    origin, command_key, macro_def, origin_range = result
    if origin not in ("registry", "inline"):
        return None

    src_line, src_col_start, src_col_end = origin_range

    # --- Invocation-site argument hover ---
    # Check whether the cursor sits on an argument name in the statement.
    if macro_def is not None and macro_def.parameters:
        try:
            statements = _parse_cmd(text)
        except Exception:  # noqa: BLE001
            statements = []

        stmt = next(
            (s for s in statements
             if not s.is_comment and not s.is_blank
             and s.line_start <= line <= s.line_end),
            None,
        )
        if stmt is not None:
            for arg in stmt.arguments:
                if arg.name_line != line:
                    continue
                arg_end_col = arg.name_column + len(arg.name)
                if arg.name_column <= character < arg_end_col:
                    canonical = resolve_macro_argument_name(macro_def, arg.name)
                    if canonical is not None:
                        param = macro_def.parameters[canonical]
                        arg_range = types.Range(
                            start=types.Position(line=arg.name_line, character=arg.name_column),
                            end=types.Position(line=arg.name_line, character=arg_end_col),
                        )
                        return types.Hover(
                            contents=types.MarkupContent(
                                kind=types.MarkupKind.Markdown,
                                value=_build_param_hover_md(param),
                            ),
                            range=arg_range,
                        )

    # --- Command-level hover ---
    hover_range = types.Range(
        start=types.Position(line=src_line, character=src_col_start),
        end=types.Position(line=src_line, character=src_col_end),
    )

    description = macro_def.description if macro_def is not None else None
    if description:
        # Replace newlines with double-newlines so each line renders as a
        # separate paragraph in Markdown (single \n is treated as a space).
        formatted_desc = description.replace("\n", "\n\n")
        md = f"# {command_key}\n\n{formatted_desc}"
    else:
        md = f"# {command_key}"

    if macro_def is not None and macro_def.parameters:
        param_lines = [_format_param_line(p) for p in macro_def.parameters.values()]
        md += "\n\n**Parameters:**\n" + "\n".join(param_lines)

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value=md,
        ),
        range=hover_range,
    )


# ---------------------------------------------------------------------------
# Completion helpers
# ---------------------------------------------------------------------------

# Matches "list(val1, val2, ...)" in a MacroParameter.type_str
_LIST_TYPE_RE = re.compile(r'^list\(([^)]+)\)$', re.IGNORECASE)


def _parse_list_type_values(type_str: str) -> list:
    """Extract completable values from a MacroParameter.type_str.

    - ``"list(yes,no)"``  → ``["yes", "no"]``
    - Anything else       → ``[]``
    """
    if not type_str:
        return []
    m = _LIST_TYPE_RE.match(type_str.strip())
    if m:
        return [v.strip() for v in m.group(1).split(',') if v.strip()]
    return []


def _lookup_macro_for_cmd(command_key: str, statements: list, stmt_line_start: int, uri: str):
    """Return the MacroDefinition for *command_key*, or None.

    Checks the workspace macro registry first, then falls back to macros
    defined inline (via ``macro create`` / ``macro read``) earlier in the file.
    """
    key = command_key.lower().strip()

    if _macro_registry is not None:
        macro_def = _macro_registry.lookup_command(key)
        if macro_def is not None:
            return macro_def

    if _schema is not None:
        path = _uri_to_path(uri)
        preceding = [s for s in statements if s.line_end < stmt_line_start]
        inline_macros = extract_macros_from_statements(preceding, _schema, source_file=path or "")
        for idef in inline_macros:
            if idef.command == key:
                return idef

    return None


def _get_completion_context(text: str, line: int, character: int, uri: str):
    """Determine the completion context at the cursor position.

    Returns one of:

    - ``("command", prefix)``
        Suggest macro command names starting with *prefix*.
    - ``("argument", macro_def, used_arg_names, prefix)``
        Suggest unused argument names for *macro_def*.
    - ``("value", param, prefix)``
        Suggest enum values for the *MacroParameter*.
    - ``None``
        Built-in command or no useful context — JS provider handles it.
    """
    if _schema is None:
        return None

    lines = text.splitlines()
    if not (0 <= line < len(lines)):
        return None

    line_text = lines[line]

    # Never complete inside plain comment lines
    if line_text.lstrip().startswith('!'):
        return None

    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return None

    # Find the statement that spans the cursor line
    stmt = None
    for s in statements:
        if s.is_comment or s.is_blank:
            continue
        if s.line_start <= line <= s.line_end:
            stmt = s
            break

    text_to_cursor = line_text[:character]

    # --- 1. Value completion: line ends with  argname=  or  argname=partial ---
    value_m = re.search(r'(\w+)\s*=\s*(\w*)$', text_to_cursor)
    if value_m and stmt is not None and not stmt.is_control_flow:
        cmd_tokens = stmt.command_key.split() if stmt.command_key else []
        resolved_cmd, _ = _schema.resolve_command_key(cmd_tokens)
        if resolved_cmd is None and stmt.command_key:
            macro_def = _lookup_macro_for_cmd(stmt.command_key, statements, stmt.line_start, uri)
            if macro_def is not None and isinstance(macro_def, MacroDefinition):
                canonical = resolve_macro_argument_name(macro_def, value_m.group(1))
                if canonical is not None:
                    param = macro_def.parameters.get(canonical)
                    if param is not None:
                        return ("value", param, value_m.group(2))

    # --- 2. No statement found: try raw command prefix ---
    if stmt is None or stmt.is_control_flow:
        raw_prefix = text_to_cursor.lstrip()
        if '=' not in raw_prefix:
            return ("command", raw_prefix)
        return None

    cmd_tokens = stmt.command_key.split() if stmt.command_key else []
    resolved_cmd, _ = _schema.resolve_command_key(cmd_tokens)

    # Built-in command: JS provider handles it
    if resolved_cmd is not None:
        return None

    # --- 3. Determine if cursor is in the command-key region ---
    # command_key_tokens: [(token_text, phys_line, phys_col), ...]
    cursor_past_cmd = True
    if stmt.command_key_tokens:
        last_tok, last_tok_line, last_tok_col = stmt.command_key_tokens[-1]
        cmd_end_col = last_tok_col + len(last_tok)
        cursor_past_cmd = line > last_tok_line or (line == last_tok_line and character > cmd_end_col)
    else:
        first_line = lines[stmt.line_start] if 0 <= stmt.line_start < len(lines) else ""
        leading = len(first_line) - len(first_line.lstrip())
        cursor_past_cmd = character > leading + len(stmt.command_key)

    if not cursor_past_cmd:
        # Cursor is within the command key region.
        # The parser may have absorbed a partial arg-name-without-equals into
        # the command_key (e.g. 'custom command part_' → key='custom command part_').
        # Check if a known macro matches a *prefix* of the parsed command_key;
        # if so, the trailing token is a partial argument name.
        full_key = stmt.command_key.lower()
        matched_macro = None
        arg_prefix_from_key = ""
        if _macro_registry is not None:
            for cmd_key, mdef in _macro_registry.items():
                if full_key == cmd_key:
                    matched_macro = mdef
                    break
                if full_key.startswith(cmd_key + " "):
                    arg_prefix_from_key = full_key[len(cmd_key) + 1:].strip()
                    matched_macro = _lookup_macro_for_cmd(cmd_key, statements, stmt.line_start, uri)
                    break
        if matched_macro is not None and arg_prefix_from_key:
            used_args = {a.name.lower() for a in stmt.arguments}
            used_args.discard(arg_prefix_from_key.lower())
            return ("argument", matched_macro, used_args, arg_prefix_from_key)
        # No macro match: fall through to command prefix suggestion
        cmd_prefix = text_to_cursor.lstrip()
        if '=' not in cmd_prefix:
            return ("command", cmd_prefix)
        return None

    # --- 4. Cursor is after command key: argument name completion ---
    macro_def = _lookup_macro_for_cmd(stmt.command_key, statements, stmt.line_start, uri)
    if macro_def is None:
        # Unknown command — might be a multi-word command prefix; suggest names
        return ("command", stmt.command_key)

    # Collect already-used argument names from the parsed statement
    used_args = {a.name.lower() for a in stmt.arguments}

    # Check if there's a partial argument name being typed before the cursor
    arg_prefix = ""
    partial_m = re.search(r'\b(\w+)$', text_to_cursor)
    if partial_m:
        # Only treat as a partial arg name if there's no '=' after it
        rest = line_text[partial_m.end():]
        comment_start = _find_comment_start(rest)
        if '=' not in rest[:comment_start]:
            arg_prefix = partial_m.group(1)
            used_args.discard(arg_prefix.lower())

    return ("argument", macro_def, used_args, arg_prefix)


@server.feature(
    types.TEXT_DOCUMENT_COMPLETION,
    types.CompletionOptions(trigger_characters=["=", "$", ":"]),
)
def completion(params: types.CompletionParams):
    """Provide completions for macro command names, arguments, and values.

    Also provides macro parameter reference completions ($param) when the
    cursor is immediately after a '$' anywhere on the line — including after
    '=' and inside expressions like eval(...).

    Built-in Adams commands are handled by the JS completion provider; this
    handler returns results only for macro commands that are not in the schema,
    EXCEPT for $param completions which work in all command contexts.
    """
    if _schema is None:
        return None

    uri = params.text_document.uri
    line = params.position.line
    character = params.position.character

    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return None

    # --- $param reference completions ---
    # Fires on '$' trigger or whenever the cursor follows a '$' anywhere on the
    # line (after '=', mid-expression, etc.).  Works for ALL commands — both
    # built-in and macro.  Guard: skip if the cursor is on a comment line.
    lines_for_param = text.splitlines()
    line_text_for_param = lines_for_param[line] if 0 <= line < len(lines_for_param) else ""
    if not line_text_for_param.lstrip().startswith('!'):
        text_to_cursor_for_param = line_text_for_param[:character]
        param_m = re.search(r'\$(\w*)$', text_to_cursor_for_param)
        if param_m:
            partial = param_m.group(1).lower()
            # Replace range: from the '$' to the cursor
            dollar_col = character - len(param_m.group(0))
            replace_range = types.Range(
                start=types.Position(line=line, character=dollar_col),
                end=types.Position(line=line, character=character),
            )
            # Extract macro parameters from the current file using the canonical parser
            file_params = _extract_params_from_text(text)
            param_items = []
            for pname, param in file_params.items():
                if partial and not pname.startswith(partial):
                    continue
                doc_content = None
                if isinstance(param, MacroParameter) and param.docstring:
                    doc_content = types.MarkupContent(
                        kind=types.MarkupKind.PlainText,
                        value=param.docstring,
                    )
                param_items.append(types.CompletionItem(
                    label="$" + pname,
                    kind=types.CompletionItemKind.Variable,
                    detail=param.type_str if isinstance(param, MacroParameter) else None,
                    documentation=doc_content,
                    sort_text="a" + pname,
                    text_edit=types.TextEdit(range=replace_range, new_text="$" + pname),
                    filter_text="$" + pname,
                ))
            # Always include $_self (sorts last)
            if not partial or "_self".startswith(partial):
                param_items.append(types.CompletionItem(
                    label="$_self",
                    kind=types.CompletionItemKind.Variable,
                    detail="macro",
                    sort_text="z_self",
                    text_edit=types.TextEdit(range=replace_range, new_text="$_self"),
                    filter_text="$_self",
                ))
            if param_items:
                return types.CompletionList(items=param_items, is_incomplete=False)

    # --- Macro parameter definition completions ---
    # Fires on !$param_name:... lines.  Provides:
    #   * type values after  t=<partial>
    #   * qualifier keys after  :<partial>  (excluding keys already on the line)
    lines_for_def = text.splitlines()
    line_text_for_def = lines_for_def[line] if 0 <= line < len(lines_for_def) else ""
    if _PARAM_DEF_LINE_RE.match(line_text_for_def.lstrip()):
        text_to_cursor_def = line_text_for_def[:character]

        # ---- t= type value completions ----
        type_m = re.search(r'(?:^|:)t=(\w*)$', text_to_cursor_def, re.IGNORECASE)
        if type_m:
            partial = type_m.group(1).lower()
            items = []
            # Sort index: primitives get "0_", entity types get "1_", list gets "2_"
            for i, tval in enumerate(_PARAM_PRIMITIVE_TYPES):
                if tval.startswith(partial):
                    items.append(types.CompletionItem(
                        label=tval,
                        kind=types.CompletionItemKind.EnumMember,
                        detail="primitive type",
                        sort_text=f"0_{i:02d}_{tval}",
                    ))
            for tval in _PARAM_ENTITY_TYPES:
                if tval.startswith(partial):
                    items.append(types.CompletionItem(
                        label=tval,
                        kind=types.CompletionItemKind.EnumMember,
                        detail="Adams object type",
                        sort_text=f"1_{tval}",
                    ))
            if "list".startswith(partial):
                items.append(types.CompletionItem(
                    label="list",
                    kind=types.CompletionItemKind.EnumMember,
                    detail="enumerated choices: list(val1,val2,...)",
                    sort_text="2_list",
                    insert_text="list($1)",
                    insert_text_format=types.InsertTextFormat.Snippet,
                ))
            if items:
                return types.CompletionList(items=items, is_incomplete=False)

        # ---- qualifier key completions ----
        # Trigger: cursor is at  :  or  :partial  (no = in the trailing segment)
        qual_key_m = re.search(r':(\w*)$', text_to_cursor_def)
        if qual_key_m:
            partial = qual_key_m.group(1).lower()
            # Collect qualifier keys already present on the line (before the cursor)
            used_keys = {m.group(1).lower() for m in re.finditer(r':(\w+)=', text_to_cursor_def)}
            items = []
            for key, insert, description in _PARAM_QUALIFIER_KEYS:
                if key in used_keys:
                    continue
                if not partial or key.startswith(partial):
                    items.append(types.CompletionItem(
                        label=key,
                        kind=types.CompletionItemKind.Property,
                        detail=description,
                        insert_text=insert,
                    ))
            if items:
                return types.CompletionList(items=items, is_incomplete=False)

        return None

    ctx = _get_completion_context(text, line, character, uri)
    if ctx is None:
        return None

    lines = text.splitlines()
    line_text = lines[line] if 0 <= line < len(lines) else ""
    leading_ws = len(line_text) - len(line_text.lstrip())

    kind = ctx[0]
    items = []

    if kind == "command":
        prefix = ctx[1].lower()

        # Replace range: from start of typed text on this line to cursor
        replace_range = types.Range(
            start=types.Position(line=line, character=leading_ws),
            end=types.Position(line=line, character=character),
        )

        seen: set = set()

        # Workspace registry macros
        if _macro_registry is not None:
            for cmd_key, macro_def in _macro_registry.items():
                if cmd_key.startswith(prefix) and cmd_key not in seen:
                    seen.add(cmd_key)
                    doc_content = None
                    if macro_def.description:
                        doc_content = types.MarkupContent(
                            kind=types.MarkupKind.Markdown,
                            value=macro_def.description,
                        )
                    items.append(types.CompletionItem(
                        label=cmd_key,
                        kind=types.CompletionItemKind.Function,
                        detail=os.path.basename(macro_def.source_file) if macro_def.source_file else None,
                        documentation=doc_content,
                        text_edit=types.TextEdit(range=replace_range, new_text=cmd_key),
                        filter_text=cmd_key,
                    ))

        # Inline macros defined earlier in the file
        if _schema is not None:
            try:
                stmts_for_inline = _parse_cmd(text)
            except Exception:  # noqa: BLE001
                stmts_for_inline = []
            preceding = [s for s in stmts_for_inline if s.line_start < line]
            path = _uri_to_path(uri)
            inline_macros = extract_macros_from_statements(preceding, _schema, source_file=path or "")
            for idef in inline_macros:
                if idef.command.startswith(prefix) and idef.command not in seen:
                    seen.add(idef.command)
                    items.append(types.CompletionItem(
                        label=idef.command,
                        kind=types.CompletionItemKind.Function,
                        detail="inline macro",
                        text_edit=types.TextEdit(range=replace_range, new_text=idef.command),
                        filter_text=idef.command,
                    ))

    elif kind == "argument":
        _, macro_def, used_args, prefix = ctx

        # Replace range: from start of the partial arg name to cursor
        replace_start = character - len(prefix)
        replace_range = types.Range(
            start=types.Position(line=line, character=replace_start),
            end=types.Position(line=line, character=character),
        )

        params_dict = macro_def.parameters if macro_def is not None else {}
        for param_name, param in params_dict.items():
            if param_name in used_args:
                continue
            if prefix and not param_name.startswith(prefix.lower()):
                continue
            doc_content = None
            detail = None
            if isinstance(param, MacroParameter):
                detail = param.type_str or None
                if param.docstring:
                    doc_content = types.MarkupContent(
                        kind=types.MarkupKind.PlainText,
                        value=param.docstring,
                    )
            new_text = param_name + "="
            items.append(types.CompletionItem(
                label=param_name,
                kind=types.CompletionItemKind.Property,
                detail=detail,
                documentation=doc_content,
                text_edit=types.TextEdit(range=replace_range, new_text=new_text),
                filter_text=param_name,
            ))

    elif kind == "value":
        _, param, prefix = ctx

        # Replace range: from start of partial value to cursor
        replace_start = character - len(prefix)
        replace_range = types.Range(
            start=types.Position(line=line, character=replace_start),
            end=types.Position(line=line, character=character),
        )

        if param is not None and isinstance(param, MacroParameter):
            values = _parse_list_type_values(param.type_str or "")
            default_val = param.default.strip('"\'') if param.default else None
            for val in values:
                if not val.lower().startswith(prefix.lower()):
                    continue
                items.append(types.CompletionItem(
                    label=val,
                    kind=types.CompletionItemKind.EnumMember,
                    text_edit=types.TextEdit(range=replace_range, new_text=val),
                ))
            # Suggest default value if not already in the list
            if default_val and default_val.lower().startswith(prefix.lower()):
                if not any(v.lower() == default_val.lower() for v in values):
                    items.append(types.CompletionItem(
                        label=default_val,
                        kind=types.CompletionItemKind.Value,
                        detail="default",
                        text_edit=types.TextEdit(range=replace_range, new_text=default_val),
                    ))

    if not items:
        return None

    return types.CompletionList(is_incomplete=False, items=items)


@server.feature(types.TEXT_DOCUMENT_REFERENCES)
def find_references(params: types.ReferenceParams):
    """Return all invocations of the macro or Adams object at the cursor.

    Tries in order:
    1. Macro references (command key → all workspace invocations)
    2. Adams object references (same-file + cross-file object index)
    """
    uri = params.text_document.uri
    line = params.position.line
    character = params.position.character
    include_declaration = (
        params.context.include_declaration
        if params.context is not None else False
    )
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return []

    # --- 1. Macro references (existing behaviour) ---
    result = _get_command_key_at_position(text, line, uri)
    if result is not None:
        origin, command_key, macro_def, _origin_range = result
        refs = _macro_index.get_references(command_key)
        locations = [
            types.Location(
                uri=_path_to_uri(file_path),
                range=types.Range(
                    start=types.Position(line=ref.line, character=ref.column),
                    end=types.Position(line=ref.line, character=ref.end_column),
                ),
            )
            for file_path, ref in refs
        ]
        if include_declaration and macro_def is not None and macro_def.source_file:
            locations.append(types.Location(
                uri=_path_to_uri(macro_def.source_file),
                range=types.Range(
                    start=types.Position(line=macro_def.line, character=0),
                    end=types.Position(line=macro_def.line, character=0),
                ),
            ))
        return locations

    # --- 2. Adams object references ---
    if _schema is None:
        return []

    statements, symbols = _get_doc_cache(uri, text)
    if statements is None or symbols is None:
        return []

    obj = _get_object_at_position(statements, _schema, symbols, line, character)
    if obj is None:
        # Fallback: names inside (eval(...)) on any arg type (real, integer, etc.)
        obj = _get_eval_object_at_position(statements, line, character)
    if obj is None:
        # Fallback: names inside parenthesized non-eval expressions
        obj = _get_paren_object_at_position(statements, symbols, line, character)
    if obj is not None:
        kind, name, v_line, v_col, v_end_col = obj

        # Per-segment: resolve only the partial path under the cursor
        seg_name, _seg_col, _seg_end_col = _resolve_segment_at_cursor(
            name, v_col, character
        )
        if seg_name != name:
            name = seg_name

        # Collect same-file references from the live symbol table
        same_file_refs = symbols.get_references_by_name(name)
        locations = [
            types.Location(
                uri=uri,
                range=types.Range(
                    start=types.Position(line=ref.line, character=ref.column),
                    end=types.Position(line=ref.line, character=ref.end_column),
                ),
            )
            for ref in same_file_refs
        ]

        # Include the definition if requested
        if include_declaration:
            sym = symbols.lookup(name)
            if sym is None:
                leaf = SymbolTable._normalize(name).lower().rsplit('.', 1)[-1]
                candidates = symbols.lookup_by_leaf_name(leaf)
                if candidates:
                    sym = candidates[0]
            if sym is not None and sym.line >= 0:
                locations.append(types.Location(
                    uri=uri,
                    range=types.Range(
                        start=types.Position(line=sym.line, character=0),
                        end=types.Position(line=sym.line, character=0),
                    ),
                ))

        # Cross-file references from the workspace object index
        current_path = os.path.normcase(os.path.normpath(_uri_to_path(uri)))
        for ref in _object_index.get_references(name):
            if os.path.normcase(os.path.normpath(ref.source_file)) == current_path:
                continue  # already covered by same-file pass
            locations.append(types.Location(
                uri=_path_to_uri(ref.source_file) if ref.source_file else uri,
                range=types.Range(
                    start=types.Position(line=ref.line, character=ref.column),
                    end=types.Position(line=ref.line, character=ref.end_column),
                ),
            ))

        return locations

    # --- 3. $variable references ---
    lines_text = text.splitlines()
    if 0 <= line < len(lines_text):
        # Is the cursor on a !$param_name definition in a macro header? → return all references
        mac_param_def = _find_macro_param_def_at_position(text, line, character)
        if mac_param_def is not None:
            param_token, p_line, p_col, p_end_col = mac_param_def
            ref_locs = _find_variable_references_in_text(text, param_token)
            return [
                types.Location(
                    uri=uri,
                    range=types.Range(
                        start=types.Position(line=rl, character=rc),
                        end=types.Position(line=rl, character=re_),
                    ),
                )
                for rl, rc, re_ in ref_locs
                if include_declaration or not (rl == p_line and rc == p_col)
            ]

        # Detect whether cursor is on the variable_name arg of 'variable set'
        var_def = _find_variable_def_at_position(statements, _schema, line, character)
        if var_def is None:
            # Check if cursor is on a general $variable token
            var_seg = _get_dollar_var_segment_at_position(lines_text[line], character)
            if var_seg is not None:
                full_token, seg_col, seg_end_col, tok_col, tok_end_col = var_seg
                cursor_prefix = full_token[:seg_end_col - tok_col]
                # Only attempt $variable resolution if the prefix starts with '$'.
                # Literal suffixes like 'pivot_I' are not variable references.
                if cursor_prefix.startswith('$'):
                    def_r = _find_variable_definition_in_statements(statements, _schema, cursor_prefix)
                    if def_r is not None:
                        matched_name, def_line, def_col, def_end_col = def_r
                        if matched_name.lower() == cursor_prefix.lower():
                            ref_locs = _find_variable_references_in_text(text, matched_name)
                            locations = [
                                types.Location(
                                    uri=uri,
                                    range=types.Range(
                                        start=types.Position(line=rl, character=rc),
                                        end=types.Position(line=rl, character=re_),
                                    ),
                                )
                                for rl, rc, re_ in ref_locs
                                if include_declaration or not (rl == def_line and rc == def_col)
                            ]
                            return locations

                    # Fallback: check macro parameter definitions (exact prefix only)
                    mac_param_defs = _find_macro_param_defs_in_text(text)
                    if cursor_prefix.lower() in mac_param_defs:
                        p_line, p_col, p_end_col = mac_param_defs[cursor_prefix.lower()]
                        ref_locs = _find_variable_references_in_text(text, cursor_prefix)
                        return [
                            types.Location(
                                uri=uri,
                                range=types.Range(
                                    start=types.Position(line=rl, character=rc),
                                    end=types.Position(line=rl, character=re_),
                                ),
                            )
                            for rl, rc, re_ in ref_locs
                            if include_declaration or not (rl == p_line and rc == p_col)
                        ]
        else:
            # Cursor is on the definition site — return all references
            var_name, v_line, v_col, v_end_col = var_def
            ref_locs = _find_variable_references_in_text(text, var_name)
            locations = [
                types.Location(
                    uri=uri,
                    range=types.Range(
                        start=types.Position(line=rl, character=rc),
                        end=types.Position(line=rl, character=re_),
                    ),
                )
                for rl, rc, re_ in ref_locs
                if include_declaration or not (rl == v_line and rc == v_col)
            ]
            return locations

    return []


@server.feature(types.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbol(params: types.DocumentSymbolParams):
    """Return all Adams objects defined in the document as outline symbols.

    Each created object (from a new_object argument, e.g. marker create) is
    returned as a SymbolInformation with an appropriate SymbolKind based on
    the Adams object type.  Builtins (ground, colors, views) are excluded.
    """
    uri = params.text_document.uri
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return []

    _, symbols = _get_doc_cache(uri, text)
    if symbols is None:
        return []

    result = []
    for sym in symbols.symbols.values():
        if sym.line < 0:  # skip builtins (registered with line == -1)
            continue
        kind = _ADAMS_SYMBOL_KIND.get(sym.object_type, types.SymbolKind.Variable)
        sym_range = types.Range(
            start=types.Position(line=sym.line, character=0),
            end=types.Position(line=sym.line, character=0),
        )
        result.append(types.SymbolInformation(
            name=sym.name,
            kind=kind,
            location=types.Location(uri=uri, range=sym_range),
        ))
    return result


@server.feature(
    types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    _SEMANTIC_LEGEND,
)
def semantic_tokens_full(params: types.SemanticTokensParams):
    """Provide semantic tokens for macro command invocations and their arguments."""
    uri = params.text_document.uri
    try:
        doc = server.workspace.get_text_document(uri)
        text = doc.source
    except Exception:  # noqa: BLE001
        return types.SemanticTokens(data=[])

    try:
        data = _compute_semantic_tokens(text, uri)
    except Exception:  # noqa: BLE001
        data = []
    return types.SemanticTokens(data=data)


def _compute_semantic_tokens(text, uri):
    """Build the integer-encoded semantic token data for all recognised commands.

    Emits ``keyword`` tokens for command key words of built-in and macro
    commands, and ``parameter`` tokens for recognised argument names.
    Unresolved commands produce no tokens (TextMate fallback applies).

    Returns a flat list of integers in groups of 5:
        [deltaLine, deltaStart, length, tokenType, tokenModifiers]
    sorted by position.
    """
    if _schema is None:
        return []

    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return []

    # Resolve built-in command abbreviations so that
    # extract_macros_from_statements can recognise "mac cre" → "macro create"
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key or stmt.resolved_command_key:
            continue
        toks = stmt.command_key.split()
        resolved, _ = _schema.resolve_command_key(toks)
        if resolved:
            stmt.resolved_command_key = resolved

    # Pre-compute inline macros from the whole file for same-file matching
    inline_macros = None

    # Collect raw tokens as (line, col, length, type_index)
    raw_tokens = []

    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow or stmt.is_property_assignment:
            continue
        if not stmt.command_key:
            continue

        # Skip dot-path property assignments (same as rule_unknown_command)
        if stmt.command_key.startswith('.'):
            continue

        if stmt.resolved_command_key is not None:
            # Built-in command — emit keyword tokens for each command key word
            # and parameter tokens only for schema-resolved argument names.
            for token_text, token_line, token_col in stmt.command_key_tokens:
                raw_tokens.append((token_line, token_col, len(token_text), _TOKEN_TYPE_KEYWORD))

            for arg in stmt.arguments:
                canonical = _schema.resolve_argument_name(stmt.resolved_command_key, arg.name)
                if canonical is not None:
                    raw_tokens.append((arg.name_line, arg.name_column, len(arg.name), _TOKEN_TYPE_PARAMETER))
            continue

        # Normalise multi-space command keys (from continuation-line joining)
        # to single spaces for registry lookup.
        normalised_key = " ".join(stmt.command_key.split())

        # Check workspace macro registry.
        macro_def = None
        if _macro_registry is not None:
            macro_def = _macro_registry.lookup_command(normalised_key)

        # Check inline macros (lazily computed).
        # Unlike _get_command_key_at_position (which uses only preceding stmts
        # for accuracy), we use ALL statements so the entire file highlights
        # consistently — a macro defined on line 50 colours invocations above.
        if macro_def is None:
            if inline_macros is None:
                path = _uri_to_path(uri)
                inline_macros = extract_macros_from_statements(
                    statements, _schema, source_file=path,
                )
            for idef in inline_macros:
                if idef.command == normalised_key:
                    macro_def = idef
                    break

        if macro_def is None:
            continue

        # Macro invocation — emit keyword tokens for each command key word
        # and parameter tokens for all argument names (no schema validation).
        for token_text, token_line, token_col in stmt.command_key_tokens:
            raw_tokens.append((token_line, token_col, len(token_text), _TOKEN_TYPE_KEYWORD))

        for arg in stmt.arguments:
            raw_tokens.append((arg.name_line, arg.name_column, len(arg.name), _TOKEN_TYPE_PARAMETER))

    if not raw_tokens:
        return []

    # Sort by (line, col) and encode as delta format
    raw_tokens.sort(key=lambda t: (t[0], t[1]))
    data = []
    prev_line = 0
    prev_col = 0
    for line, col, length, token_type in raw_tokens:
        delta_line = line - prev_line
        delta_col = col - prev_col if delta_line == 0 else col
        data.extend([delta_line, delta_col, length, token_type, 0])
        prev_line = line
        prev_col = col

    return data


@server.feature(types.WORKSPACE_DID_CHANGE_CONFIGURATION)
def did_change_configuration(params: types.DidChangeConfigurationParams):
    """Update server globals when VS Code settings change.

    The vscode-languageclient library sends changes as:
        {"msc-adams": {"linter": {"scanWorkspaceMacros": true, ...}}}
    All keys are optional — guard against missing keys throughout.
    """
    global _scan_workspace_macros, _macro_patterns, _macro_ignore_patterns, _macro_show_hint  # noqa: PLW0603

    raw = params.settings or {}
    linter_cfg = {}
    if isinstance(raw, dict):
        adams_cfg = raw.get("msc-adams") or {}
        if isinstance(adams_cfg, dict):
            linter_cfg = adams_cfg.get("linter") or {}

    # Capture values before update so we can detect changes
    old_scan = _scan_workspace_macros
    old_patterns = list(_macro_patterns)
    old_ignore = list(_macro_ignore_patterns)

    if "scanWorkspaceMacros" in linter_cfg:
        _scan_workspace_macros = bool(linter_cfg["scanWorkspaceMacros"])
    if "macroPaths" in linter_cfg:
        paths = linter_cfg["macroPaths"]
        if isinstance(paths, list):
            _macro_patterns = paths if paths else DEFAULT_MACRO_PATTERNS
    if "macroIgnorePaths" in linter_cfg:
        ignore = linter_cfg["macroIgnorePaths"]
        if isinstance(ignore, list):
            _macro_ignore_patterns = ignore
    if "showMacroHint" in linter_cfg:
        _macro_show_hint = bool(linter_cfg["showMacroHint"])

    # Re-scan workspace macros if scanning was enabled or patterns changed
    scan_changed = _scan_workspace_macros and (
        not old_scan
        or _macro_patterns != old_patterns
        or _macro_ignore_patterns != old_ignore
    )
    if scan_changed and _macro_registry is not None and _workspace_roots:
        try:
            scan_macro_files(
                _workspace_roots,
                patterns=_macro_patterns,
                ignore_patterns=_macro_ignore_patterns or None,
                registry=_macro_registry,
            )
        except Exception:  # noqa: BLE001
            pass

    # Re-lint all open documents so diagnostics reflect the updated settings
    if server.workspace:
        for uri, doc in list(server.workspace.text_documents.items()):
            _validate_document(uri, doc.source)


@server.feature(types.WORKSPACE_DID_CHANGE_WATCHED_FILES)
def did_change_watched_files(params: types.DidChangeWatchedFilesParams):
    """Update the macro registry and object index when watched files change."""
    if _macro_registry is None:
        return

    changed = False
    for event in params.changes:
        path = _uri_to_path(event.uri)
        if not path:
            continue
        if event.type == types.FileChangeType.Deleted:
            _macro_registry.unregister_by_file(path)
            _object_index.remove_file(path)
            changed = True
        else:
            # Created or Changed — remove any stale entry then re-parse.
            _macro_registry.unregister_by_file(path)
            _object_index.remove_file(path)
            changed = True
            try:
                text = Path(path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            macro_def = parse_macro_file(text, source_file=path)
            if macro_def is not None:
                _macro_registry.register(macro_def)
                _macro_registry._record_mtime(path)
            # Also refresh the object index for this file
            if _schema is not None:
                try:
                    defs, refs = index_file_objects(text, _schema, source_file=path)
                    _object_index.update_file(path, defs, refs)
                    _object_index.record_mtime(path)
                except Exception:  # noqa: BLE001
                    pass

    # Re-lint open documents so diagnostics reflect registry changes
    if changed and server.workspace:
        for uri, doc in list(server.workspace.text_documents.items()):
            _validate_document(uri, doc.source)


@server.feature(types.INITIALIZED)
def on_initialized(params: types.InitializedParams):
    """Scan workspace folders for macro files and build the reference index."""
    global _macro_registry, _ude_registry, _workspace_roots  # noqa: PLW0603
    workspace = server.workspace
    if not workspace:
        return
    workspace_paths = []
    try:
        for folder in (workspace.folders or {}).values():
            path = _uri_to_path(folder.uri)
            if os.path.isdir(path):
                workspace_paths.append(path)
    except Exception:  # noqa: BLE001
        return
    # Always record workspace roots so _refresh_macro_file can do accurate
    # relative-path pattern matching even when scanning is disabled.
    _workspace_roots = list(workspace_paths)
    if not workspace_paths:
        return
    # Always build the reference index — it is needed for find-references even
    # when macro scanning is disabled for linting purposes.
    _build_index_for_workspace(workspace_paths)
    if not _scan_workspace_macros:
        return
    if _macro_registry is None:
        return
    # Merge workspace-discovered macros into the existing registry (incremental)
    try:
        scan_macro_files(
            workspace_paths,
            patterns=_macro_patterns,
            ignore_patterns=_macro_ignore_patterns or None,
            registry=_macro_registry,
        )
    except Exception as exc:  # noqa: BLE001
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Warning,
                message=f"Adams macro scan failed: {exc}",
            )
        )
        return
    # Scan for UDE definitions in parallel with macro scanning
    if _ude_registry is not None and _schema is not None:
        try:
            scan_ude_files(
                workspace_paths,
                _schema,
                patterns=_ude_patterns,
                ignore_patterns=_ude_ignore_patterns or None,
                registry=_ude_registry,
            )
        except Exception as exc:  # noqa: BLE001
            server.window_log_message(
                types.LogMessageParams(
                    type=types.MessageType.Warning,
                    message=f"Adams UDE scan failed: {exc}",
                )
            )
    # Log all discovered macros to the VS Code output panel
    count = len(_macro_registry)
    if count == 0:
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message="Adams macro scan complete: no macro files found.",
            )
        )
    else:
        lines = [f"Adams macro scan complete: {count} macro(s) discovered."]
        for cmd_key, macro_def in sorted(_macro_registry.items()):
            src = macro_def.source_file or "<unknown>"
            lines.append(f"  {cmd_key}  ({src})")
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message="\n".join(lines),
            )
        )
    # Log discovered UDE definitions
    if _ude_registry is not None:
        ude_count = len(_ude_registry)
        if ude_count == 0:
            server.window_log_message(
                types.LogMessageParams(
                    type=types.MessageType.Info,
                    message="Adams UDE scan complete: no UDE definitions found.",
                )
            )
        else:
            ude_lines = [f"Adams UDE scan complete: {ude_count} UDE definition(s) discovered."]
            for def_name, ude_def in sorted(_ude_registry._definitions.items()):
                src = ude_def.source_file or "<unknown>"
                ude_lines.append(f"  {def_name}  ({src})")
            server.window_log_message(
                types.LogMessageParams(
                    type=types.MessageType.Info,
                    message="\n".join(ude_lines),
                )
            )


def _build_index_for_workspace(workspace_paths):
    """Walk *workspace_paths* and index all .cmd/.mac files.

    Populates both _macro_index (macro invocations for Find References) and
    _object_index (Adams object definitions/references for Go to Definition
    and Find All References on Adams objects).
    """
    if _schema is None:
        return
    if not workspace_paths:
        return
    all_files = _collect_cmd_files(workspace_paths)
    indexed = 0
    for abs_path in all_files:
        path_str = str(abs_path)
        needs_macro = _macro_index.needs_refresh(path_str)
        needs_obj = _object_index.needs_refresh(path_str)
        if not needs_macro and not needs_obj:
            continue
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if needs_macro:
            try:
                refs = index_file_text(text, _schema, source_file=path_str)
                _macro_index.update_file(path_str, refs)
                _macro_index.record_mtime(path_str)
            except Exception:  # noqa: BLE001
                pass
        if needs_obj:
            try:
                defs, obj_refs = index_file_objects(text, _schema, source_file=path_str)
                _object_index.update_file(path_str, defs, obj_refs)
                _object_index.record_mtime(path_str)
            except Exception:  # noqa: BLE001
                pass
        indexed += 1
    if indexed:
        server.window_log_message(
            types.LogMessageParams(
                type=types.MessageType.Info,
                message=(
                    f"Adams reference index built: {indexed} file(s) indexed, "
                    f"{_macro_index.total_references()} macro invocation(s) found, "
                    f"{_object_index.total_definitions()} object definition(s) indexed."
                ),
            )
        )
