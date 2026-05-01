"""UDE (User Defined Element) definition discovery for Adams CMD files.

Provides:
  - UdeParameter         -- one parameter in a UDE definition
  - UdeDefinition        -- parameters/inputs/outputs extracted from a definition
  - UdeRegistry          -- in-memory lookup table for discovered UDE definitions
  - parse_ude_definitions -- extract definitions from parsed statements
  - scan_ude_files        -- build a UdeRegistry by walking workspace files
"""

import fnmatch
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .macros import DEFAULT_IGNORE_DIRS


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class UdeParameter:
    """One parameter exposed by a UDE definition.

    Only the leaf name is tracked.  Type inference from preceding ``var set``
    commands is deferred to a future enhancement.
    """
    name: str                    # leaf name, lower-cased, e.g. "damprat"
    category: str = "parameter"  # "parameter", "input", or "output"


@dataclass
class UdeDefinition:
    """A UDE definition extracted from ``ude create definition``, ``ude copy``,
    or ``ude modify definition`` commands."""
    definition_name: str                              # full dot-path, e.g. ".lib.flex_comp"
    parameters: Dict[str, UdeParameter] = field(default_factory=dict)
    source_file: str = ""  # absolute path to the defining file
    line: int = 0          # 0-based line of the originating command


class UdeRegistry:
    """In-memory lookup table for UDE definitions.

    Definitions are stored keyed by both the normalised full name *and* the
    leaf name so that lookup by short name works.
    """

    def __init__(self):
        self._definitions: Dict[str, UdeDefinition] = {}  # full-name → UdeDefinition
        self._leaf_index: Dict[str, UdeDefinition] = {}   # leaf-name → UdeDefinition
        self._mtimes: Dict[str, float] = {}

    @staticmethod
    def _normalize(name):
        """Normalise a definition name to lower-case with a leading dot."""
        return name.lower() if name.startswith('.') else ('.' + name).lower()

    def register(self, ude_def):
        """Add *ude_def* to the registry.  Later registrations win."""
        key = self._normalize(ude_def.definition_name)
        self._definitions[key] = ude_def
        leaf = key.rsplit('.', 1)[-1]
        self._leaf_index[leaf] = ude_def

    def lookup(self, name):
        """Return the UdeDefinition for *name*, or None.

        Tries full-path match first, then falls back to leaf-name match.
        """
        key = self._normalize(name)
        result = self._definitions.get(key)
        if result:
            return result
        leaf = key.rsplit('.', 1)[-1]
        return self._leaf_index.get(leaf)

    def needs_refresh(self, path):
        """Return True if *path* has not been parsed or has changed since."""
        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            return True
        return self._mtimes.get(path) != mtime

    def _record_mtime(self, path):
        try:
            self._mtimes[path] = os.stat(path).st_mtime
        except OSError:
            pass

    def unregister_by_file(self, path):
        """Remove all definitions that were sourced from *path*."""
        norm = Path(path)
        to_remove = [
            key for key, defn in self._definitions.items()
            if Path(defn.source_file) == norm
        ]
        for key in to_remove:
            defn = self._definitions.pop(key)
            leaf = key.rsplit('.', 1)[-1]
            if self._leaf_index.get(leaf) is defn:
                del self._leaf_index[leaf]
        self._mtimes.pop(path, None)
        self._mtimes.pop(str(norm), None)

    def items(self):
        """Iterate over (definition_name, UdeDefinition) pairs."""
        return iter(self._definitions.items())

    def __len__(self):
        return len(self._definitions)


# ---------------------------------------------------------------------------
# Parameter extraction helpers
# ---------------------------------------------------------------------------


def _extract_leaf_name(ref):
    """Extract the leaf (last dot-component) from a parameter reference.

    Handles:
      - ``$model.damprat``      -> ``"damprat"``
      - ``.model.damprat``      -> ``"damprat"``
      - ``damprat``             -> ``"damprat"``
      - ``(eval(...))``         -> None  (skip runtime expressions)
      - empty / whitespace-only -> None
    """
    ref = ref.strip().strip('"\'')
    if not ref or ref.startswith('(') or 'eval(' in ref.lower():
        return None
    # Strip leading $ from macro-parameter paths before splitting
    ref = ref.lstrip('$')
    if '.' in ref:
        return ref.rsplit('.', 1)[-1].lower() or None
    return ref.lower() or None


def _split_comma_values(raw):
    """Split a comma-separated argument value, respecting parentheses and quotes.

    Adams continuation lines join multi-line values into a single string with
    commas.  We must not split inside parens or quotes.
    """
    if not raw:
        return []

    parts = []
    depth = 0
    in_dq = False
    in_sq = False
    current = []

    for ch in raw:
        if ch == '"' and not in_sq:
            in_dq = not in_dq
            current.append(ch)
        elif ch == "'" and not in_dq:
            in_sq = not in_sq
            current.append(ch)
        elif ch == '(' and not in_dq and not in_sq:
            depth += 1
            current.append(ch)
        elif ch == ')' and not in_dq and not in_sq:
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == ',' and depth == 0 and not in_dq and not in_sq:
            token = ''.join(current).strip()
            if token:
                parts.append(token)
            current = []
        else:
            current.append(ch)

    tail = ''.join(current).strip()
    if tail:
        parts.append(tail)

    return parts


# ---------------------------------------------------------------------------
# Statement-level parsing
# ---------------------------------------------------------------------------


def parse_ude_definitions(statements, schema):
    """Extract UDE definitions from a list of parsed statements.

    Handles three command types in a single pass:
      - ``ude create definition``  — creates a new UdeDefinition
      - ``ude copy``               — clones parameters from a source definition
      - ``ude modify definition``  — renames and/or replaces parameter categories

    Args:
        statements: list of Statement objects from parser.py
        schema:     Schema object used for argument name resolution

    Returns:
        list of UdeDefinition objects (the final state after all modifications)
    """
    # First pass: resolve command keys for all statements we care about
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow or stmt.is_property_assignment:
            continue
        if stmt.resolved_command_key or not stmt.command_key:
            continue
        if schema.has_command(stmt.command_key):
            stmt.resolved_command_key = stmt.command_key
        else:
            tokens = stmt.command_key.split()
            resolved_key, _ = schema.resolve_command_key(tokens)
            if resolved_key:
                stmt.resolved_command_key = resolved_key

    # Single-pass collection
    definitions_ordered: List[UdeDefinition] = []  # insertion order
    defs_by_name: Dict[str, UdeDefinition] = {}    # normalised key → def (mutable)

    for stmt in statements:
        cmd_key = stmt.resolved_command_key or stmt.command_key
        if not cmd_key:
            continue

        if cmd_key == "ude create definition":
            ude_def = _parse_ude_create_definition(stmt, schema)
            if ude_def:
                definitions_ordered.append(ude_def)
                defs_by_name[_norm_key(ude_def.definition_name)] = ude_def

        elif cmd_key == "ude copy":
            ude_def = _parse_ude_copy(stmt, schema, defs_by_name)
            if ude_def:
                definitions_ordered.append(ude_def)
                defs_by_name[_norm_key(ude_def.definition_name)] = ude_def

        elif cmd_key == "ude modify definition":
            _parse_ude_modify_definition(stmt, schema, defs_by_name)
            # Mutates in place; no new entry added to definitions_ordered

    return definitions_ordered


def _norm_key(name):
    """Normalise a definition name for use as a dict key."""
    return name.lower() if name.startswith('.') else ('.' + name).lower()


def _resolve_arg(stmt, schema, cmd_key, target_name):
    """Find the first argument whose resolved name equals *target_name*."""
    for arg in stmt.arguments:
        canonical = schema.resolve_argument_name(cmd_key, arg.name)
        if (canonical or arg.name.lower()) == target_name:
            return arg.value
    return None


def _extract_params(raw, category):
    """Parse a comma-separated parameter argument value into UdeParameter objects."""
    params = {}
    if not raw:
        return params
    for ref in _split_comma_values(raw):
        leaf = _extract_leaf_name(ref)
        if leaf:
            params[leaf] = UdeParameter(name=leaf, category=category)
    return params


def _parse_ude_create_definition(stmt, schema):
    cmd_key = "ude create definition"
    def_name = _resolve_arg(stmt, schema, cmd_key, "definition_name")
    if not def_name:
        return None
    def_name = def_name.strip().strip('"\'')

    ude_def = UdeDefinition(definition_name=def_name, line=stmt.line_start)

    for arg_name, category in [
        ("parameters",        "parameter"),
        ("input_parameters",  "input"),
        ("output_parameters", "output"),
    ]:
        raw = _resolve_arg(stmt, schema, cmd_key, arg_name)
        ude_def.parameters.update(_extract_params(raw, category))

    return ude_def


def _parse_ude_copy(stmt, schema, defs_by_name):
    cmd_key = "ude copy"
    new_name = _resolve_arg(stmt, schema, cmd_key, "new_definition_name")
    if not new_name:
        return None
    new_name = new_name.strip().strip('"\'')

    ude_def = UdeDefinition(definition_name=new_name, line=stmt.line_start)

    src_raw = _resolve_arg(stmt, schema, cmd_key, "definition_name")
    if src_raw:
        src_key = _norm_key(src_raw.strip().strip('"\''))
        src_def = defs_by_name.get(src_key)
        if src_def:
            for key, param in src_def.parameters.items():
                ude_def.parameters[key] = UdeParameter(name=param.name, category=param.category)

    return ude_def


def _parse_ude_modify_definition(stmt, schema, defs_by_name):
    """Mutate an existing UdeDefinition in-place based on a ``ude modify definition`` command.

    Handles:
      - Rename via ``new_definition_name``
      - Per-category parameter replacement (only replaces categories explicitly listed)
    """
    cmd_key = "ude modify definition"
    src_raw = _resolve_arg(stmt, schema, cmd_key, "definition_name")
    if not src_raw:
        return
    src_key = _norm_key(src_raw.strip().strip('"\''))
    ude_def = defs_by_name.get(src_key)
    if ude_def is None:
        return  # can't modify a definition not seen in this file

    # Handle rename
    new_name_raw = _resolve_arg(stmt, schema, cmd_key, "new_definition_name")
    if new_name_raw:
        new_name = new_name_raw.strip().strip('"\'')
        del defs_by_name[src_key]
        ude_def.definition_name = new_name
        new_key = _norm_key(new_name)
        defs_by_name[new_key] = ude_def

    # Replace parameter categories that are explicitly present in the modify command
    for arg_name, category in [
        ("parameters",        "parameter"),
        ("input_parameters",  "input"),
        ("output_parameters", "output"),
    ]:
        raw = _resolve_arg(stmt, schema, cmd_key, arg_name)
        if raw is None:
            continue  # arg not present — leave this category untouched
        # Replace: remove all params of this category, then add the new ones
        ude_def.parameters = {
            k: v for k, v in ude_def.parameters.items()
            if v.category != category
        }
        ude_def.parameters.update(_extract_params(raw, category))


# ---------------------------------------------------------------------------
# File-level parsing
# ---------------------------------------------------------------------------


def parse_ude_file(text, schema, source_file=""):
    """Parse a .cmd/.mac file and extract all UDE definitions.

    Args:
        text:        raw file content
        schema:      Schema object
        source_file: absolute path (for provenance tracking)

    Returns:
        list of UdeDefinition objects with source_file set
    """
    from .parser import parse as _parse
    statements = _parse(text)
    defs = parse_ude_definitions(statements, schema)
    for d in defs:
        d.source_file = source_file
    return defs


# ---------------------------------------------------------------------------
# Workspace scanner
# ---------------------------------------------------------------------------

DEFAULT_UDE_PATTERNS = ["**/*.cmd"]


def scan_ude_globs(root, patterns=None, ignore_patterns=None):
    """Resolve *patterns* against *root* and return matching file Paths."""
    if patterns is None:
        patterns = DEFAULT_UDE_PATTERNS
    ignore_patterns = list(ignore_patterns or [])
    root_path = Path(root)

    files = []
    seen = set()
    for pattern in patterns:
        for p in root_path.glob(pattern):
            if not p.is_file():
                continue
            abs_str = str(p.resolve())
            if abs_str in seen:
                continue
            seen.add(abs_str)
            if any(d in DEFAULT_IGNORE_DIRS for d in p.parts):
                continue
            rel = str(p.relative_to(root_path))
            if any(_fnmatch_path(rel, ipat) for ipat in ignore_patterns):
                continue
            files.append(p)
    return files


def _fnmatch_path(rel_path, pattern):
    rel_fwd = rel_path.replace("\\", "/")
    pat_fwd = pattern.replace("\\", "/")
    return fnmatch.fnmatch(rel_fwd, pat_fwd)


def scan_ude_files(roots, schema, patterns=None, ignore_patterns=None, registry=None):
    """Scan workspace *roots* for UDE definitions and populate a registry.

    Args:
        roots:           list of workspace root directories
        schema:          Schema object
        patterns:        glob patterns for file discovery (default: ``['**/*.cmd']``)
        ignore_patterns: glob patterns to exclude
        registry:        existing UdeRegistry to update (creates a new one if None)

    Returns:
        populated UdeRegistry
    """
    if registry is None:
        registry = UdeRegistry()

    for root in roots:
        for path in scan_ude_globs(root, patterns, ignore_patterns):
            abs_path = str(path.resolve())
            if not registry.needs_refresh(abs_path):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            defs = parse_ude_file(text, schema, source_file=abs_path)
            registry.unregister_by_file(abs_path)
            for d in defs:
                registry.register(d)
            registry._record_mtime(abs_path)

    return registry
