"""Persistent macro invocation index for Adams CMD workspaces.

Provides a fast, incrementally-maintained in-memory index of all macro
invocations (unresolved commands) across a workspace, enabling O(1)
"find all references" queries without re-parsing on every request.

Public API
----------
MacroReference  — one occurrence of a macro invocation in a file
MacroIndex      — persistent bimap: file_path <-> List[MacroReference]
index_file_text — pure function: parse text -> List[MacroReference]
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .parser import parse


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class MacroReference:
    """One macro invocation occurrence in a source file.

    All positions are 0-based and refer to the physical line where the
    command token starts (i.e. ``statement.line_start``).
    """
    command_key: str   # normalized (lower-cased) command key as written
    line: int          # 0-based line number of the first token
    column: int        # 0-based column of the first character of the command
    end_column: int    # 0-based column one past the last character


class MacroIndex:
    """Persistent in-memory index of macro invocations across the workspace.

    Design
    ------
    Every statement that the command schema *cannot* resolve is stored as a
    MacroReference.  This includes genuine macro calls, misspelled commands,
    and any other unrecognised input.  Storing everything means the index
    never needs to be rebuilt when new macros are discovered — the references
    handler simply filters by the requested command_key.

    Two complementary dicts are maintained in sync:
    - ``_refs_by_file``    — file_path -> [MacroReference, ...]  (forward)
    - ``_files_by_command`` — command_key -> {file_path, ...}   (reverse)

    Mtime tracking (same pattern as MacroRegistry) lets the startup scan skip
    files that have not changed since last indexed.
    """

    def __init__(self):
        self._refs_by_file: Dict[str, List[MacroReference]] = {}
        self._files_by_command: Dict[str, Set[str]] = {}
        self._mtimes: Dict[str, float] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def update_file(self, file_path: str, references: List[MacroReference]) -> None:
        """Replace all refs for *file_path* and rebuild the reverse index.

        Safe to call repeatedly — removes stale entries from the previous
        version before adding the new ones.
        """
        self.remove_file(file_path)
        self._refs_by_file[file_path] = list(references)
        for ref in references:
            self._files_by_command.setdefault(ref.command_key, set()).add(file_path)

    def remove_file(self, file_path: str) -> None:
        """Remove all references contributed by *file_path*."""
        old_refs = self._refs_by_file.pop(file_path, [])
        for ref in old_refs:
            files = self._files_by_command.get(ref.command_key)
            if files is not None:
                files.discard(file_path)
                if not files:
                    del self._files_by_command[ref.command_key]

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_references(self, command_key: str) -> List[Tuple[str, MacroReference]]:
        """Return all (file_path, MacroReference) pairs for *command_key*.

        Matching is exact (after lower-casing the query).
        """
        key = command_key.lower()
        file_paths = self._files_by_command.get(key, set())
        result = []
        for path in file_paths:
            for ref in self._refs_by_file.get(path, []):
                if ref.command_key == key:
                    result.append((path, ref))
        return result

    def get_file_refs(self, file_path: str) -> List[MacroReference]:
        """Return all MacroReferences for *file_path* (may be empty)."""
        return list(self._refs_by_file.get(file_path, []))

    def all_files(self) -> List[str]:
        """Return all indexed file paths."""
        return list(self._refs_by_file.keys())

    def command_count(self) -> int:
        """Return the number of distinct command keys in the index."""
        return len(self._files_by_command)

    def total_references(self) -> int:
        """Return the total number of MacroReference entries across all files."""
        return sum(len(refs) for refs in self._refs_by_file.values())

    # ------------------------------------------------------------------
    # Mtime helpers (startup incremental scan)
    # ------------------------------------------------------------------

    def needs_refresh(self, path: str) -> bool:
        """Return True if *path* is new or has been modified since last index."""
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


# ---------------------------------------------------------------------------
# Indexing function
# ---------------------------------------------------------------------------

def index_file_text(
    text: str,
    schema,
    source_file: Optional[str] = None,
) -> List[MacroReference]:
    """Parse *text* and return a MacroReference for every unresolved command.

    A command is "unresolved" when ``schema.resolve_command_key()`` fails for its
    token list.  This deliberately includes all unrecognised input — genuine
    macro calls, misspellings, etc. — so the index stays complete regardless of
    which macros are currently registered.

    Comments, blank lines, and control-flow keywords (if/else/end/for/while)
    are skipped.

    Args:
        text:        Raw .cmd / .mac file text.
        schema:      Schema object used to test command resolution.
        source_file: Optional path hint (unused for results, available for
                     future diagnostics).

    Returns:
        List of MacroReference objects, one per unresolved command statement.
    """
    references: List[MacroReference] = []
    statements = parse(text)

    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        if not stmt.command_key:
            continue

        tokens = stmt.command_key.split()
        resolved_key, _err = schema.resolve_command_key(tokens)
        if resolved_key is not None:
            # Known built-in command — not a macro reference
            continue

        # Unresolved command: record it as a potential macro invocation.
        # Column is always 0 because Adams CMD commands start at column 0.
        # end_column spans the length of the full command_key text.
        references.append(MacroReference(
            command_key=stmt.command_key.lower(),
            line=stmt.line_start,
            column=0,
            end_column=len(stmt.command_key),
        ))

    return references
