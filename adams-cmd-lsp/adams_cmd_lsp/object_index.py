"""Workspace-level index of Adams object definitions and references.

Provides fast cross-file Go to Definition and Find All References for
Adams View objects in .cmd / .mac files.

Design mirrors MacroIndex in references.py:
- Two complementary forward/reverse dicts for O(1) lookups
- Mtime-based incremental refresh (skip unchanged files)
- Full-path match first, leaf-name fallback for partial names

Public API
----------
IndexedDefinition  — one object definition (create command) found in a file
IndexedReference   — one object reference (existing_object arg) found in a file
ObjectIndex        — persistent bimap: file_path <-> definitions/references
index_file_objects — pure function: parse text -> (definitions, references)
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from .parser import parse as _parse_cmd
from .schema import Schema
from .symbols import SymbolTable, build_symbol_table


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class IndexedDefinition:
    """One Adams object definition (from a new_object argument) in a workspace file."""
    name: str           # normalized path, e.g. ".model.PART_1.MAR_1"
    object_type: str    # e.g. "Marker", "Part"
    line: int           # 0-based line number of the create command
    source_file: str    # absolute file path


@dataclass
class IndexedReference:
    """One Adams object reference (from an existing_object argument) in a workspace file."""
    name: str           # object path as written
    object_type: str    # expected type per schema
    line: int           # 0-based line number
    column: int         # 0-based column of value start
    end_column: int     # 0-based column one past the last char
    source_file: str    # absolute file path


# ---------------------------------------------------------------------------
# ObjectIndex
# ---------------------------------------------------------------------------

class ObjectIndex:
    """Persistent in-memory workspace index of Adams object definitions and references.

    Maintains two bimap pairs:
        _defs_by_file / _files_by_def_name  — forward/reverse for definitions
        _refs_by_file / _files_by_ref_name  — forward/reverse for references

    The reverse dicts are keyed by lower-cased normalized name.  A second set
    of entries keyed ``"__leaf__" + leaf_name`` enables leaf-name lookups
    (matching on the last dot-separated component of the path).
    """

    def __init__(self):
        self._defs_by_file: Dict[str, List[IndexedDefinition]] = {}
        self._refs_by_file: Dict[str, List[IndexedReference]] = {}
        self._files_by_def_name: Dict[str, Set[str]] = {}
        self._files_by_ref_name: Dict[str, Set[str]] = {}
        self._mtimes: Dict[str, float] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(name: str) -> str:
        """Normalize an Adams path to always start with a leading dot."""
        return name if name.startswith('.') else '.' + name

    @staticmethod
    def _index_keys(name: str):
        """Yield the lookup keys for *name*: full path and, if multi-level, a leaf key."""
        normalized = ObjectIndex._normalize(name).lower()
        yield normalized
        leaf = normalized.rsplit('.', 1)[-1]
        if leaf != normalized.lstrip('.'):
            yield '__leaf__' + leaf

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def update_file(
        self,
        file_path: str,
        definitions: List[IndexedDefinition],
        references: List[IndexedReference],
    ) -> None:
        """Replace all entries for *file_path* in the index."""
        self.remove_file(file_path)
        self._defs_by_file[file_path] = list(definitions)
        self._refs_by_file[file_path] = list(references)
        for d in definitions:
            for key in self._index_keys(d.name):
                self._files_by_def_name.setdefault(key, set()).add(file_path)
        for r in references:
            for key in self._index_keys(r.name):
                self._files_by_ref_name.setdefault(key, set()).add(file_path)

    def remove_file(self, file_path: str) -> None:
        """Remove all index entries contributed by *file_path*."""
        old_defs = self._defs_by_file.pop(file_path, [])
        old_refs = self._refs_by_file.pop(file_path, [])
        for d in old_defs:
            for key in self._index_keys(d.name):
                files = self._files_by_def_name.get(key)
                if files is not None:
                    files.discard(file_path)
                    if not files:
                        del self._files_by_def_name[key]
        for r in old_refs:
            for key in self._index_keys(r.name):
                files = self._files_by_ref_name.get(key)
                if files is not None:
                    files.discard(file_path)
                    if not files:
                        del self._files_by_ref_name[key]

    # ------------------------------------------------------------------
    # Query — definitions
    # ------------------------------------------------------------------

    def get_definitions(self, name: str) -> List[IndexedDefinition]:
        """Return all IndexedDefinitions for *name*.

        Tries full-path match first; falls back to leaf-name match.
        """
        normalized = self._normalize(name).lower()
        file_paths = self._files_by_def_name.get(normalized, set())
        results = [
            d for path in file_paths
            for d in self._defs_by_file.get(path, [])
            if self._normalize(d.name).lower() == normalized
        ]
        if results:
            return results
        # Leaf fallback: find definitions whose last path component equals the query leaf.
        #
        # If the QUERY is a full path (has dots), only match stored definitions that are
        # themselves leaf-only names.  This prevents '.demo_model.GROUND.MAR_1' from
        # matching '.model_1.ground.MAR_1' just because both share the leaf 'MAR_1'.
        #
        # If the QUERY is already a leaf-only name (no dots), match any stored definition
        # with the same leaf regardless of how it was written.
        leaf = normalized.rsplit('.', 1)[-1]
        query_is_leaf_only = '.' not in normalized.lstrip('.')
        leaf_key = '__leaf__' + leaf
        file_paths = self._files_by_def_name.get(leaf_key, set())
        return [
            d for path in file_paths
            for d in self._defs_by_file.get(path, [])
            if self._normalize(d.name).lower().rsplit('.', 1)[-1] == leaf
            and (query_is_leaf_only or '.' not in self._normalize(d.name).lower().lstrip('.'))
        ]

    # ------------------------------------------------------------------
    # Query — references
    # ------------------------------------------------------------------

    def get_references(self, name: str) -> List[IndexedReference]:
        """Return all IndexedReferences for *name*.

        Tries full-path match first; falls back to leaf-name match.
        """
        normalized = self._normalize(name).lower()
        file_paths = self._files_by_ref_name.get(normalized, set())
        results = [
            r for path in file_paths
            for r in self._refs_by_file.get(path, [])
            if self._normalize(r.name).lower() == normalized
        ]
        if results:
            return results
        # Leaf fallback: find references whose last path component equals the query leaf.
        #
        # If the QUERY is a full path (has dots), only match stored references that are
        # themselves leaf-only names.  This prevents '.demo_model.GROUND.MAR_1' from
        # matching '.model_1.ground.MAR_1' just because both share the leaf 'MAR_1'.
        #
        # If the QUERY is already a leaf-only name (no dots), match any stored reference
        # with the same leaf regardless of how it was written.
        leaf = normalized.rsplit('.', 1)[-1]
        query_is_leaf_only = '.' not in normalized.lstrip('.')
        leaf_key = '__leaf__' + leaf
        file_paths = self._files_by_ref_name.get(leaf_key, set())
        return [
            r for path in file_paths
            for r in self._refs_by_file.get(path, [])
            if self._normalize(r.name).lower().rsplit('.', 1)[-1] == leaf
            and (query_is_leaf_only or '.' not in self._normalize(r.name).lower().lstrip('.'))
        ]

    # ------------------------------------------------------------------
    # Mtime helpers
    # ------------------------------------------------------------------

    def needs_refresh(self, path: str) -> bool:
        """Return True if *path* is new or modified since last index."""
        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            return True
        return self._mtimes.get(path) != mtime

    def record_mtime(self, path: str) -> None:
        """Record the current mtime for *path* after a successful index."""
        try:
            self._mtimes[path] = os.stat(path).st_mtime
        except OSError:
            pass

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def total_definitions(self) -> int:
        return sum(len(v) for v in self._defs_by_file.values())

    def total_references(self) -> int:
        return sum(len(v) for v in self._refs_by_file.values())


# ---------------------------------------------------------------------------
# Indexing function
# ---------------------------------------------------------------------------

def _resolve_command_keys(statements, schema) -> None:
    """Pre-resolve abbreviated command keys in-place via the schema command tree.

    Mirrors the side-effect performed by rule_unknown_command() in rules.py,
    but operates standalone so that callers that don't run the full linter
    pipeline can still benefit from abbreviation resolution.
    """
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if stmt.resolved_command_key:
            continue
        if schema.has_command(stmt.command_key):
            stmt.resolved_command_key = stmt.command_key
            continue
        tokens = stmt.command_key.split()
        resolved, _ = schema.resolve_command_key(tokens)
        if resolved:
            stmt.resolved_command_key = resolved


def index_file_objects(
    text: str,
    schema: Schema,
    source_file: Optional[str] = None,
) -> Tuple[List[IndexedDefinition], List[IndexedReference]]:
    """Parse *text* and return all object definitions and references it contains.

    Args:
        text:        Raw .cmd / .mac file text.
        schema:      Schema object for command resolution.
        source_file: Absolute path of the file (stored on results; may be None).

    Returns:
        A 2-tuple (definitions, references).
        - definitions: one IndexedDefinition per new_object argument.
        - references:  one IndexedReference per existing_object argument.
        Builtins (line == -1 in the SymbolTable) are excluded from definitions.
    """
    sf = source_file or ""
    try:
        statements = _parse_cmd(text)
    except Exception:  # noqa: BLE001
        return [], []

    _resolve_command_keys(statements, schema)

    try:
        table = build_symbol_table(statements, schema)
    except Exception:  # noqa: BLE001
        return [], []

    definitions = [
        IndexedDefinition(
            name=sym.name,
            object_type=sym.object_type,
            line=sym.line,
            source_file=sf,
        )
        for sym in table.symbols.values()
        if sym.line >= 0  # exclude builtins (line == -1)
    ]

    references = [
        IndexedReference(
            name=ref.name,
            object_type=ref.object_type,
            line=ref.line,
            column=ref.column,
            end_column=ref.end_column,
            source_file=sf,
        )
        for ref in table.references
    ]

    return definitions, references
