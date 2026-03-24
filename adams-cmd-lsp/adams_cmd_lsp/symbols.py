"""Single-file symbol table for semantic analysis of Adams CMD files."""

from dataclasses import dataclass


@dataclass
class Symbol:
    name: str         # full object path, e.g. ".model.PART_1"
    object_type: str  # e.g. "Marker", "Part", "MECHANISM"
    line: int         # 0-based line where created


class SymbolTable:
    def __init__(self):
        self.symbols = {}  # lower-cased name → Symbol

    def register(self, name, object_type, line):
        """Register a newly created object."""
        self.symbols[name.lower()] = Symbol(name, object_type, line)

    def lookup(self, name):
        """Return the Symbol for name, or None if not registered."""
        return self.symbols.get(name.lower())

    def has(self, name):
        """Return True if name has been registered."""
        return name.lower() in self.symbols


def build_symbol_table(statements, schema):
    """Walk parsed statements top-to-bottom and collect created objects.

    Args:
        statements: list of Statement objects from parser.py
        schema: Schema object

    Returns:
        SymbolTable populated with all objects created in the file
    """
    table = SymbolTable()
    for stmt in statements:
        if stmt.is_comment or stmt.is_blank or stmt.is_control_flow:
            continue
        cmd_key = stmt.resolved_command_key or stmt.command_key
        cmd = schema.get_command(cmd_key)
        if not cmd:
            continue
        for arg in stmt.arguments:
            # Resolve abbreviated argument names
            canonical = schema.resolve_argument_name(cmd_key, arg.name)
            arg_def = cmd["args"].get(canonical or arg.name)
            if arg_def and arg_def.get("type") == "new_object":
                table.register(
                    arg.value,
                    arg_def.get("object_type", "unknown"),
                    arg.name_line,
                )
    return table
