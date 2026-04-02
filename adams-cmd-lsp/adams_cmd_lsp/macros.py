"""User-defined macro discovery for Adams CMD files.

Provides:
  - MacroParameter   — one parameter in a macro signature
  - MacroDefinition  — command/parameters extracted from a macro file
  - MacroRegistry    — in-memory lookup table for discovered macros
  - parse_macro_file — parse a single file's !USER_ENTERED_COMMAND header
  - scan_macro_globs — resolve glob patterns against a root and return file paths
  - scan_macro_files — build a MacroRegistry from roots + glob patterns
  - scan_macro_paths — legacy wrapper (directory list) kept for compat
  - extract_macros_from_statements — collect macros defined inline via
                                     'macro create' / 'macro read'
  - DEFAULT_IGNORE_DIRS — public alias for _DEFAULT_IGNORE_DIRS (used by
                          reference indexer and other modules)
"""

import fnmatch
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class MacroParameter:
    """One parameter in a user-defined macro signature.

    All fields are optional — Adams allows `!$name` with no qualifiers,
    which defaults to a single string value with no default.
    """
    name: str
    type_str: Optional[str] = None      # raw T= qualifier, e.g. "integer", "part", "list(yes,no)"
    default: Optional[str] = None       # constant default value (D= qualifier)
    updated_default: Optional[str] = None  # updated default (UD= qualifier)
    # Numeric range constraints: keys are 'gt','ge','lt','le'
    constraints: Dict[str, str] = field(default_factory=dict)
    count: Optional[str] = None         # C= qualifier value


@dataclass
class MacroDefinition:
    """A user-defined macro discovered from a .mac file or inline statement."""
    command: str                                    # e.g. "cdm wear"
    parameters: Dict[str, MacroParameter]           # keyed by lower-case param name
    source_file: str = ""                           # absolute path to defining file
    line: int = 0                                   # 0-based line of !USER_ENTERED_COMMAND


def _compute_min_prefixes(names):
    """Return a dict mapping each name to its minimum unique prefix length.

    The shortest prefix that unambiguously identifies a name among its siblings
    is computed case-insensitively.  If a name is a prefix of another name the
    full-length is required.

    Args:
        names: iterable of sibling parameter names

    Returns:
        dict[str, int] — name → minimum unique prefix length
    """
    lower_names = [n.lower() for n in names]
    result = {}
    for i, name in enumerate(lower_names):
        for prefix_len in range(1, len(name) + 1):
            prefix = name[:prefix_len]
            conflicts = sum(
                1 for j, other in enumerate(lower_names)
                if j != i and other.startswith(prefix)
            )
            if conflicts == 0:
                result[names[i]] = prefix_len
                break
        else:
            result[names[i]] = len(name)
    return result


def resolve_macro_argument_name(macro_def: "MacroDefinition", arg_name: str) -> Optional[str]:
    """Resolve a (possibly abbreviated) argument name against a macro's parameters.

    Uses the same shortest-unique-prefix algorithm as Adams built-in commands:
    a prefix is accepted only when it is unambiguous among all sibling
    parameter names *and* at least as long as the minimum unique prefix for
    the matching parameter.

    Returns the canonical (lower-case) parameter name on success, or ``None``
    when the name is unknown, ambiguous, or shorter than the minimum prefix.
    """
    params = macro_def.parameters          # keyed by lower-case param name
    if not params:
        return None

    arg_lower = arg_name.lower()

    # Exact match takes priority
    if arg_lower in params:
        return arg_lower

    # Compute minimum prefix lengths on the fly from sibling names
    min_prefixes = _compute_min_prefixes(list(params.keys()))

    # Prefix match — must be unambiguous and at least min_prefix chars
    matches = []
    for name in params:
        min_prefix = min_prefixes.get(name, len(name))
        if len(arg_lower) >= min_prefix and name.startswith(arg_lower):
            matches.append(name)

    if len(matches) == 1:
        return matches[0]

    return None


# ---------------------------------------------------------------------------
# Parameter string parsing
# ---------------------------------------------------------------------------

# Matches $name  or  $'name'  or  $name:q1:q2...  or  $'name:q1:q2...'
# Group 1: name (possibly with qualifiers inside quotes)
# Group 2: qualifiers after bare name (outside quotes), may be None
_PARAM_BARE_RE = re.compile(
    r"\$'([^']+)'"          # $'name' or $'name:qualifiers'
    r"|"
    r"\$([A-Za-z][A-Za-z0-9_]*)"  # $name (bare)
    r"((?::[A-Za-z0-9_=.()*,\-+]+)*)",  # optional :q1:q2... after bare name
    re.IGNORECASE,
)

# Matches a comment-style parameter definition line: !$name  or  !$name:qualifiers
# Leading whitespace is stripped before matching.
_COMMENT_PARAM_RE = re.compile(
    r"^!\s*\$'([^']+)'"     # !$'name:qualifiers'
    r"|"
    r"^!\s*\$([A-Za-z][A-Za-z0-9_]*)"  # !$name
    r"((?::[A-Za-z0-9_=.()*,\-+]+)*)",  # optional :q1:q2...
    re.IGNORECASE,
)

_END_OF_PARAMETERS = re.compile(r"^\s*!?\s*END_OF_PARAMETERS\b", re.IGNORECASE)
_USER_ENTERED_COMMAND_RE = re.compile(
    r"^\s*!\s*USER_ENTERED_COMMAND\s+(.+?)\s*$", re.IGNORECASE
)


def _parse_qualifiers(qualifier_str: str) -> MacroParameter:
    """Parse a colon-separated qualifier string into a MacroParameter (name='').

    qualifier_str is everything after the first colon, e.g.
      "t=real:ge=1:d=0"
    All keys are case-insensitive.
    """
    p = MacroParameter(name="")
    if not qualifier_str:
        return p
    # Strip a leading colon if present
    parts = qualifier_str.lstrip(":").split(":")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            continue
        key, _, val = part.partition("=")
        key = key.strip().lower()
        val = val.strip()
        if key == "t":
            p.type_str = val.lower()
        elif key == "d":
            p.default = val
        elif key == "ud":
            p.updated_default = val
        elif key in ("gt", "ge", "lt", "le"):
            p.constraints[key] = val
        elif key == "c":
            p.count = val
    return p


def _extract_params_from_text(text: str) -> Dict[str, MacroParameter]:
    """Scan *text* for all parameter occurrences and return {name: MacroParameter}.

    Rules (per Adams docs):
    - The FIRST occurrence of a parameter defines it.
    - Qualifiers can only appear on the first occurrence.
    - `!$name` in a comment is the canonical way to define parameters.
    - `$name` in command text (first occurrence) also works if no comment
      definition precedes it.
    - Stops at !END_OF_PARAMETERS if present.
    """
    params: Dict[str, MacroParameter] = {}

    for line in text.splitlines():
        stripped = line.strip()

        # Stop at !END_OF_PARAMETERS
        if _END_OF_PARAMETERS.match(stripped):
            break

        # Try comment-style definition first: !$name or !$name:qualifiers
        m = _COMMENT_PARAM_RE.match(stripped)
        if m:
            if m.group(1):
                # Quoted form: !$'name:qualifiers' or !$'name'
                inner = m.group(1)
                colon_idx = inner.find(":")
                if colon_idx >= 0:
                    pname = inner[:colon_idx].strip().lower()
                    qual_str = inner[colon_idx:]
                else:
                    pname = inner.strip().lower()
                    qual_str = ""
            else:
                # Bare form: !$name  or  !$name:qualifiers
                pname = m.group(2).lower()
                qual_str = m.group(3) or ""

            if pname and pname not in params:
                p = _parse_qualifiers(qual_str)
                p.name = pname
                params[pname] = p
            continue

        # Scan the whole line for $param occurrences (including inside commands)
        for m in _PARAM_BARE_RE.finditer(line):
            if m.group(1):
                # Quoted: $'name:...' or $'name'
                inner = m.group(1)
                colon_idx = inner.find(":")
                if colon_idx >= 0:
                    pname = inner[:colon_idx].strip().lower()
                    qual_str = inner[colon_idx:]
                else:
                    pname = inner.strip().lower()
                    qual_str = ""
            else:
                pname = m.group(2).lower()
                qual_str = m.group(3) or ""

            # Skip $_self — this is the macro's own database path, not a parameter
            if pname == "_self":
                continue
            if pname and pname not in params:
                p = _parse_qualifiers(qual_str)
                p.name = pname
                params[pname] = p

    return params


# ---------------------------------------------------------------------------
# Public parsing API
# ---------------------------------------------------------------------------

def parse_macro_file(text: str, source_file: str = "") -> Optional[MacroDefinition]:
    """Parse *text* for a !USER_ENTERED_COMMAND header and extract parameters.

    Returns a MacroDefinition if a USER_ENTERED_COMMAND is found, else None.

    Scanning behaviour:
    - Stops collecting parameters at !END_OF_PARAMETERS when present.
    - If !END_OF_PARAMETERS is absent, scans the entire file.
    - First occurrence of each parameter wins (qualifiers on later occurrences
      are ignored, per Adams docs).
    """
    command = None
    command_line = 0

    for i, line in enumerate(text.splitlines()):
        m = _USER_ENTERED_COMMAND_RE.match(line)
        if m:
            command = m.group(1).strip().lower()
            command_line = i
            break

    if command is None:
        return None

    parameters = _extract_params_from_text(text)

    return MacroDefinition(
        command=command,
        parameters=parameters,
        source_file=source_file,
        line=command_line,
    )


# ---------------------------------------------------------------------------
# Macro Registry
# ---------------------------------------------------------------------------

class MacroRegistry:
    """In-memory lookup table for user-defined macro commands.

    Commands are stored lower-cased. Lookup uses exact matching only —
    callers should normalise the command key before lookup.
    """

    def __init__(self):
        self._commands: Dict[str, MacroDefinition] = {}
        # Maps absolute path → mtime at last parse, for incremental updates
        self._mtimes: Dict[str, float] = {}

    def register(self, macro_def: MacroDefinition) -> None:
        """Add *macro_def* to the registry.  Later registrations win."""
        self._commands[macro_def.command.lower()] = macro_def

    def lookup_command(self, command_key: str) -> Optional[MacroDefinition]:
        """Return the MacroDefinition for *command_key*, or None.

        Matching is exact (after lower-casing).  The caller is responsible
        for passing the full normalised command key (e.g. "cdm wear").
        """
        return self._commands.get(command_key.lower())

    def has_command(self, command_key: str) -> bool:
        return command_key.lower() in self._commands

    def get_parameters(self, command_key: str) -> Optional[Dict[str, MacroParameter]]:
        macro = self.lookup_command(command_key)
        return macro.parameters if macro else None

    def items(self) -> Iterator[Tuple[str, MacroDefinition]]:
        """Iterate over (command_key, MacroDefinition) pairs."""
        return iter(self._commands.items())

    def needs_refresh(self, path: str) -> bool:
        """Return True if *path* is new or has been modified since last parse."""
        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            return True
        return self._mtimes.get(path) != mtime

    def _record_mtime(self, path: str) -> None:
        """Record the current mtime for *path* after a successful parse."""
        try:
            self._mtimes[path] = os.stat(path).st_mtime
        except OSError:
            pass

    def unregister_by_file(self, path: str) -> None:
        """Remove all registry entries whose source_file matches *path*.

        Uses Path-based comparison so that equivalent paths with different
        separator styles (forward vs backslash on Windows) are treated as equal.
        Also removes the cached mtime so the file will be re-parsed next time
        the workspace scanner encounters it.
        """
        norm = Path(path)
        to_remove = [
            key for key, defn in self._commands.items()
            if Path(defn.source_file) == norm
        ]
        for key in to_remove:
            del self._commands[key]
        # Remove mtime entry under both the original and normalised form
        self._mtimes.pop(path, None)
        self._mtimes.pop(str(norm), None)

    def __len__(self) -> int:
        return len(self._commands)


# ---------------------------------------------------------------------------
# Workspace scanner
# ---------------------------------------------------------------------------

# Directories that are never interesting for macro scanning.
# Also exported as DEFAULT_IGNORE_DIRS for use by other modules (e.g. the
# reference indexer) that need the same skip-list without importing a private name.
_DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".tox", "build", "dist", ".hg", ".svn",
}
DEFAULT_IGNORE_DIRS = _DEFAULT_IGNORE_DIRS  # public alias

# Default glob patterns for macro file discovery (relative to a workspace root)
DEFAULT_MACRO_PATTERNS = ["**/*.mac"]


def scan_macro_globs(
    root: str,
    patterns: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
) -> List[Path]:
    """Resolve *patterns* against *root* and return matching file paths.

    Args:
        root:            Root directory against which patterns are resolved.
        patterns:        Glob patterns (default: [``**/*.mac``]).  Each pattern
                         is passed to ``Path.glob()``.  Non-recursive patterns
                         like ``macros/*`` avoid a full tree walk.
        ignore_patterns: User-supplied glob patterns (matched against relative
                         paths) to exclude beyond the built-in ignored dirs.
    """
    if patterns is None:
        patterns = DEFAULT_MACRO_PATTERNS
    ignore_patterns = list(ignore_patterns or [])
    root_path = Path(root)
    if not root_path.is_dir():
        return []

    seen: set = set()
    results: List[Path] = []

    for pattern in patterns:
        for abs_path in root_path.glob(pattern):
            if not abs_path.is_file():
                continue
            if abs_path in seen:
                continue

            # Compute relative path for ignore matching
            try:
                rel = abs_path.relative_to(root_path).as_posix()
            except ValueError:
                rel = abs_path.as_posix()

            # Skip default ignored directories (any path component check)
            if any(part in _DEFAULT_IGNORE_DIRS for part in Path(rel).parts[:-1]):
                continue

            # Apply user-supplied ignore patterns
            if any(fnmatch.fnmatch(rel, pat) for pat in ignore_patterns):
                continue

            seen.add(abs_path)
            results.append(abs_path)

    return results


def scan_macro_files(
    roots: List[str],
    patterns: Optional[List[str]] = None,
    ignore_patterns: Optional[List[str]] = None,
    registry: Optional[MacroRegistry] = None,
) -> MacroRegistry:
    """Scan each root in *roots* using *patterns* and return a MacroRegistry.

    If *registry* is supplied, it is updated in-place (incremental scan).
    Files whose mtime has not changed since the last parse are skipped.

    Args:
        roots:           List of root directories to scan.
        patterns:        Glob patterns (default: [``**/*.mac``]).
        ignore_patterns: Glob patterns to exclude.
        registry:        Existing registry for incremental updates (optional).
    """
    if registry is None:
        registry = MacroRegistry()

    for root in roots:
        for abs_path in scan_macro_globs(root, patterns=patterns, ignore_patterns=ignore_patterns):
            path_str = str(abs_path)
            if not registry.needs_refresh(path_str):
                continue
            try:
                text = abs_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            macro_def = parse_macro_file(text, source_file=path_str)
            if macro_def is not None:
                registry.register(macro_def)
            # Record mtime even for files with no USER_ENTERED_COMMAND so we
            # don't re-read them on subsequent incremental scans.
            registry._record_mtime(path_str)

    return registry


# ---------------------------------------------------------------------------
# Legacy alias — kept for backward compatibility with existing callers
# ---------------------------------------------------------------------------

def scan_macro_paths(
    paths: List[str],
    ignore_patterns: Optional[List[str]] = None,
    extensions: Optional[List[str]] = None,  # retained for compat, ignored
) -> MacroRegistry:
    """Backward-compatible wrapper around scan_macro_files.

    *extensions* is accepted but ignored — use glob patterns instead.
    """
    return scan_macro_files(paths, patterns=DEFAULT_MACRO_PATTERNS, ignore_patterns=ignore_patterns)


# ---------------------------------------------------------------------------
# In-file macro extraction (from 'macro create' / 'macro read' statements)
# ---------------------------------------------------------------------------

def extract_macros_from_statements(
    statements,
    schema,
    source_file: str = "",
) -> List[MacroDefinition]:
    """Walk *statements* and collect MacroDefinitions from macro create/read.

    Handles two cases:
    1. ``macro create macro_name=foo user_entered_command="my cmd" ...``
    2. ``macro read   macro_name=bar user_entered_command="other cmd" ...``

    If ``user_entered_command`` is absent, the macro_name itself becomes the
    callable command (single-token, no spaces).

    Args:
        statements:  Parsed statements from parser.parse().
        schema:      Schema object used to resolve abbreviated argument names.
        source_file: Absolute path of the file being parsed.  When provided,
                     MacroDefinition.source_file is populated so that
                     go-to-definition can return a proper file URI.
    """
    results: List[MacroDefinition] = []
    _MACRO_CMDS = {"macro create", "macro read"}

    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue

        cmd_key = (stmt.resolved_command_key or stmt.command_key or "").lower()
        if cmd_key not in _MACRO_CMDS:
            continue

        arg_map = {a.name.lower(): a.value for a in stmt.arguments}

        # Resolve abbreviated argument names using schema if available
        if schema:
            resolved_map = {}
            for aname, aval in arg_map.items():
                canonical = schema.resolve_argument_name(cmd_key, aname)
                resolved_map[canonical or aname] = aval
            arg_map = resolved_map

        macro_name = arg_map.get("macro_name", "").strip().strip('"').strip("'")
        user_cmd = arg_map.get("user_entered_command", "").strip().strip('"').strip("'")

        command = user_cmd if user_cmd else macro_name
        if not command:
            continue

        results.append(MacroDefinition(
            command=command.lower(),
            parameters={},          # inline macro create doesn't expose parameters
            source_file=source_file,
            line=stmt.line_start,
        ))

    return results
