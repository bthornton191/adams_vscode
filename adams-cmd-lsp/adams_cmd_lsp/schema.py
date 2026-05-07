"""Load and query command_schema.json for Adams CMD linting."""

import json
from pathlib import Path

_DEFAULT_SCHEMA_PATH = Path(__file__).parent / "data" / "command_schema.json"


class Schema:
    def __init__(self, data):
        self._commands = data.get("commands", {})
        self._tree = data.get("command_tree", {})

    @classmethod
    def load(cls, path=None):
        """Load schema from path (or the bundled default if path is None)."""
        path = Path(path) if path else _DEFAULT_SCHEMA_PATH
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    # ------------------------------------------------------------------
    # Command lookups
    # ------------------------------------------------------------------

    def has_command(self, key):
        """Return True if key (exact, lowercase) is a known command."""
        return key in self._commands

    def get_command(self, key):
        """Return the full command definition dict, or None."""
        return self._commands.get(key)

    def get_args(self, key):
        """Return the args dict for a command, or None."""
        cmd = self._commands.get(key)
        return cmd["args"] if cmd else None

    def get_arg(self, cmd_key, arg_name):
        """Return a single argument definition dict, or None."""
        cmd = self._commands.get(cmd_key)
        if cmd:
            return cmd["args"].get(arg_name)
        return None

    def commands(self):
        """Return an iterable of all canonical command keys."""
        return self._commands.keys()

    def get_exclusive_groups(self, cmd_key):
        """Return the exclusive_groups list for a command (empty list if none)."""
        cmd = self._commands.get(cmd_key)
        return cmd.get("exclusive_groups", []) if cmd else []

    # ------------------------------------------------------------------
    # Abbreviation resolution
    # ------------------------------------------------------------------

    def resolve_command_key(self, tokens):
        """Resolve a list of (possibly abbreviated) command tokens to a canonical key.

        Uses the command_tree to match abbreviated prefixes against siblings.

        Returns:
            (canonical_key, error_token_index)
            - canonical_key is None on failure
            - error_token_index is None on success, or the index of the first
              unresolvable token on failure

        Matching rules (per Adams runtime behaviour):
        - Case-insensitive
        - Exact match takes priority over prefix match
        - Prefix must be at least min_prefix chars long
        - Prefix must be unambiguous (match exactly one sibling)
        """
        node = self._tree
        resolved = []

        for i, token in enumerate(tokens):
            children = node.get("children", {})
            if not children:
                return None, i

            match = self._match_token(token, children)
            if match is None:
                return None, i

            resolved.append(match)
            node = children[match]

        key = " ".join(resolved)
        if key in self._commands:
            return key, None
        # Partial command — intermediate node, not a leaf
        return None, len(tokens) - 1

    def _match_token(self, token, children):
        """Match a single token against sibling children.

        Returns the canonical name on match, None on no-match or ambiguity.
        """
        token_lower = token.lower()

        # Exact match takes priority
        for name in children:
            if name.lower() == token_lower:
                return name

        # Prefix match — must be unambiguous and long enough
        matches = []
        for name, node_data in children.items():
            min_prefix = node_data.get("min_prefix", len(name))
            if len(token_lower) >= min_prefix and name.lower().startswith(token_lower):
                matches.append(name)

        if len(matches) == 1:
            return matches[0]

        return None  # 0 matches or ambiguous

    def resolve_argument_name(self, cmd_key, arg_name):
        """Resolve a (possibly abbreviated) argument name to its canonical form.

        Returns canonical name on match, None on no-match or ambiguity.
        """
        cmd = self._commands.get(cmd_key)
        if not cmd:
            return None

        args = cmd["args"]
        arg_lower = arg_name.lower()

        # Exact match first
        for name in args:
            if name.lower() == arg_lower:
                return name

        # Prefix match
        matches = []
        for name, arg_def in args.items():
            min_prefix = arg_def.get("min_prefix", len(name))
            if len(arg_lower) >= min_prefix and name.lower().startswith(arg_lower):
                matches.append(name)

        if len(matches) == 1:
            return matches[0]

        return None
