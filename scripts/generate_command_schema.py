#!/usr/bin/env python3
"""Generate command_schema.json from Adams source files.

Usage:
    python scripts/generate_command_schema.py \
        --input "../hexagon/Adams/source/aview/src/cmd_language/commands.exp" \
        --language-src "../hexagon/Adams/source/aview/src/cmd_language/language.src" \
        --arg-options "resources/adams_view_commands/argument_options.json" \
        --output "adams-cmd-lsp/adams_cmd_lsp/data/command_schema.json" \
        --validate "resources/adams_view_commands/structured.json" \
        --patches "scripts/schema_patches.json"

The --patches file (scripts/schema_patches.json) is committed to the repo and
contains manual corrections that override incorrect or missing data from the
Adams source files. It is applied as the final step before writing output, so
re-running the generator always produces the correct result.

IMPORTANT: Review command_schema.json before committing.
Do not commit proprietary data from commands.exp or language.src.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Type classification
# ---------------------------------------------------------------------------

_REAL_UNIT_TYPES = {
    "REAL", "LENGTH", "MASS", "TIME", "FORCE", "VELOCITY",
    "ACCELERATION", "ANGULAR_VEL", "ANGULAR_ACCEL", "STIFFNESS",
    "DAMPING", "TORQUE", "PRESSURE", "INERTIA", "DENSITY", "AREA",
    "VOLUME", "ANGLE",
}

_BOOLEAN_TYPES = {"BOOLEAN", "ON_OFF", "ON_OFF_WITH_TOGGLE", "TRUE_ONLY"}


def _classify_type(type_token):
    """Classify a raw type token into a schema type dict."""
    t = type_token.upper()

    if t.startswith("NDBWD_"):
        obj = t[len("NDBWD_"):]
        return {"type": "new_object", "object_type": obj.capitalize(), "db_type": t}
    if t.startswith("NDB_"):
        obj = t[len("NDB_"):]
        return {"type": "new_object", "object_type": obj.capitalize(), "db_type": t}
    if t.startswith("DB_"):
        obj = t[3:]
        return {"type": "existing_object", "object_type": obj.capitalize(), "db_type": t}
    if t == "INT":
        return {"type": "integer"}
    if t in _REAL_UNIT_TYPES:
        unit = t.lower()
        return {"type": "real", "unit": unit}
    if t == "LOCATION":
        return {"type": "location"}
    if t == "ORIENTATION":
        return {"type": "orientation"}
    if t in _BOOLEAN_TYPES:
        return {"type": "boolean"}
    if t in ("STRING", "FILE"):
        return {"type": "string"}
    if t == "FUNCTION":
        return {"type": "function"}
    if t == "ADAMS_ID":
        return {"type": "adams_id", "db_type": "ADAMS_ID"}

    return {"type": "unknown", "raw_type": t}


# ---------------------------------------------------------------------------
# Parse a single argument line from commands.exp
# ---------------------------------------------------------------------------

# Matches TYPE(…) modifier — array spec or range constraint
_ARRAY_RE = re.compile(r'^(\d+),(\d+)$')
_RANGE_BOUND_RE = re.compile(r'^(GT|GE|LT|LE|UNLIMITED)$')


def _parse_type_modifiers(modifier_content):
    """Parse the content inside TYPE(…) parentheses.

    Returns (array_spec, range_spec):
      array_spec: {"min": int, "max": int|None} or None
      range_spec: {"lower_type": str, "lower": float, "upper_type": str, "upper": float} or None
    """
    parts = [p.strip() for p in modifier_content.split(',')]

    # Check if it looks like a range spec (first part is a bound keyword or number)
    if parts and _RANGE_BOUND_RE.match(parts[0].upper()):
        # range constraint: GT,lo,LT,hi  (4 parts)
        if len(parts) == 4:
            def _bound_val(s):
                if s.upper() == "UNLIMITED":
                    return None
                try:
                    return float(s)
                except ValueError:
                    return None

            return None, {
                "lower_type": parts[0].upper(),
                "lower": _bound_val(parts[1]),
                "upper_type": parts[2].upper(),
                "upper": _bound_val(parts[3]),
            }

    # Array spec: (0) → unbounded, (n,m) → n..m, (n) → exactly n
    if len(parts) == 1:
        try:
            n = int(parts[0])
            if n == 0:
                return {"min": 0, "max": None}, None
            return {"min": n, "max": n}, None
        except ValueError:
            pass
    if len(parts) == 2:
        try:
            lo, hi = int(parts[0]), int(parts[1])
            return {"min": lo, "max": hi}, None
        except ValueError:
            pass

    return None, None


def _parse_argument_line(text):
    """Parse a single argument definition line from commands.exp.

    Input examples:
        marker_name=NDBWD_MARKER*
        comments=STRING(0)
        fit_to_view=BOOLEAN=yes
        transparency=INT(GT,-1,LT,101)
        view_name=DB_VIEW(0)=DYN_DB

    Returns (name, spec_dict) or (None, None) on parse failure.
    """
    text = text.strip()
    if not text or '=' not in text:
        return None, None

    # Split on first '=' to get name and remainder
    eq_pos = text.index('=')
    name = text[:eq_pos].strip()

    # Strip ?suffix from name (should be clean in .exp but be safe)
    if '?' in name:
        name = name[:name.index('?')]

    if not name:
        return None, None

    remainder = text[eq_pos + 1:]

    # Check for required marker (trailing '*' in the type portion)
    required = False
    # The * comes right after the type token (before any =default)
    # We need to detect it before we split on =default
    # Strategy: find the type token boundary first

    # The remainder is: TYPE[modifier][*][=default]
    # TYPE is alphanumeric + underscore (no spaces)
    # modifier is (...)
    # Then optional * and =default

    # Extract TYPE token (up to '(' or '=' or '*' or end)
    type_match = re.match(r'^([A-Za-z_]\w*)', remainder)
    if not type_match:
        return None, None

    type_token = type_match.group(1)
    pos = len(type_token)

    # Optional modifier (...)
    array_spec = None
    range_spec = None
    if pos < len(remainder) and remainder[pos] == '(':
        # Find matching close paren
        depth = 0
        end = pos
        for i in range(pos, len(remainder)):
            if remainder[i] == '(':
                depth += 1
            elif remainder[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        modifier_content = remainder[pos + 1:end]
        array_spec, range_spec = _parse_type_modifiers(modifier_content)
        pos = end + 1

    # Optional required marker *
    if pos < len(remainder) and remainder[pos] == '*':
        required = True
        pos += 1

    # Optional =default
    default = None
    if pos < len(remainder) and remainder[pos] == '=':
        default = remainder[pos + 1:].strip()

    spec = _classify_type(type_token)
    spec["required"] = required

    if array_spec is not None:
        spec["array"] = True
        if array_spec.get("min") is not None:
            spec["min_values"] = array_spec["min"]
        if array_spec.get("max") is not None:
            spec["max_values"] = array_spec["max"]

    if range_spec:
        spec["range"] = range_spec

    if default is not None:
        spec["default"] = default

    return name.lower(), spec


# ---------------------------------------------------------------------------
# Parse commands.exp
# ---------------------------------------------------------------------------

def parse_commands_exp(text):
    """Parse commands.exp into {command_key: {"args": {name: spec}}}."""
    commands = {}
    current_cmd = None

    for line in text.splitlines():
        if not line:
            continue

        # Command key line: starts with exactly 1 leading space (not 2+)
        if (line.startswith(' ')
                and not line.startswith('  ')
                and line.strip()):
            current_cmd = line.strip().lower()
            commands[current_cmd] = {"args": {}}
            continue

        # Argument line: indented 3+ spaces with '=' in it
        if current_cmd and line.startswith('   ') and '=' in line:
            name, spec = _parse_argument_line(line.strip())
            if name:
                commands[current_cmd]["args"][name] = spec

    return commands


# ---------------------------------------------------------------------------
# Extract exclusive groups from language.src
# ---------------------------------------------------------------------------

def _find_macro_bodies(text):
    """Extract {macro_name: body_text} from language.src.

    Macros start with '#name' and end with ';' at the same nesting level.
    """
    macros = {}
    i = 0
    n = len(text)

    while i < n:
        # Skip whitespace and comments
        if text[i].isspace():
            i += 1
            continue

        # Macro definition: #name
        if text[i] == '#':
            # Read macro name
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] == '_'):
                j += 1
            macro_name = text[i + 1:j].lower()
            i = j

            # Find the body up to the terminating ';' at depth 0
            body_start = i
            depth = 0
            while i < n:
                if text[i] in '[({':
                    depth += 1
                elif text[i] in '])}':
                    depth -= 1
                elif text[i] == ';' and depth == 0:
                    macros[macro_name] = text[body_start:i]
                    i += 1
                    break
                i += 1
            continue

        i += 1

    return macros


def _parse_exclusion_blocks(body):
    """Extract mutual exclusion groups from a macro body.

    Returns list of {"group": N, "members": [arg_name, ...]}
    """
    groups = []
    group_num = [0]

    def _extract_group_members(content):
        """Extract argument names (lines with '=') from a block content."""
        members = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('!'):
                continue
            if '=' in line:
                # Extract arg name (before first '='), strip ?suffix
                name = line[:line.index('=')].strip()
                if '?' in name:
                    name = name[:name.index('?')]
                name = name.lower()
                # Skip ALL-CAPS labels (menu labels, not arguments)
                if name and not name.isupper():
                    members.append(name)
        return members

    def _scan_blocks(text, start=0):
        """Recursively scan for { } blocks."""
        i = start
        n = len(text)
        while i < n:
            if text[i] == '{':
                # Find matching close brace (tracking nesting)
                depth = 0
                j = i
                while j < n:
                    if text[j] == '{':
                        depth += 1
                    elif text[j] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                content = text[i + 1:j]
                # Check for nested blocks inside this one
                if '{' in content:
                    # Recurse into sub-groups
                    _scan_blocks(content)
                else:
                    members = _extract_group_members(content)
                    if len(members) > 1:
                        group_num[0] += 1
                        groups.append({"group": group_num[0], "members": members})
                i = j + 1
            else:
                i += 1

    _scan_blocks(body)
    return groups


def _macro_name_to_command_key(macro_name, command_keys):
    """Map a language.src macro name to a flattened command key.

    Heuristic: underscores in macro name → spaces in command key.
    E.g. "marker_create" → "marker create".
    Tries progressively shorter tails as fallback.
    """
    # Replace underscores with spaces
    candidate = macro_name.replace('_', ' ')
    if candidate in command_keys:
        return candidate

    # Try all splits of the underscore-name into space-separated tokens
    # by treating each underscore as either a word separator or part of a word
    parts = macro_name.split('_')
    # Try joining first N parts as first token, rest as second, etc.
    for split in range(1, len(parts)):
        a = '_'.join(parts[:split])
        b = '_'.join(parts[split:])
        candidate = f"{a} {b}"
        if candidate in command_keys:
            return candidate
        candidate = f"{a.replace('_', ' ')} {b.replace('_', ' ')}"
        if candidate in command_keys:
            return candidate

    return None


def extract_exclusive_groups(language_src_text, command_keys):
    """Extract {command_key: [groups]} from language.src.

    Returns dict of command_key → list of {"group": N, "members": [...]}
    """
    command_key_set = set(command_keys)
    macros = _find_macro_bodies(language_src_text)

    groups_by_cmd = {}
    for macro_name, body in macros.items():
        cmd_key = _macro_name_to_command_key(macro_name, command_key_set)
        if not cmd_key:
            continue
        groups = _parse_exclusion_blocks(body)
        if groups:
            groups_by_cmd[cmd_key] = groups

    return groups_by_cmd


# ---------------------------------------------------------------------------
# Abbreviation prefix computation
# ---------------------------------------------------------------------------

def compute_min_prefixes(names):
    """Compute the minimum unique prefix length for each name among its siblings.

    Args:
        names: list of sibling names (comparison is case-insensitive)

    Returns:
        dict of name → min_prefix_length (integer)
    """
    lower_names = [n.lower() for n in names]
    result = {}

    for i, name in enumerate(lower_names):
        for prefix_len in range(1, len(name) + 1):
            prefix = name[:prefix_len]
            # Count siblings that share this prefix
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


# ---------------------------------------------------------------------------
# Command tree
# ---------------------------------------------------------------------------

def build_command_tree(command_keys):
    """Build a hierarchical prefix-annotated tree from flat command keys.

    Returns a dict suitable for JSON serialisation:
    {
      "children": {
        "model": {
          "min_prefix": 3,
          "children": {
            "create": {"min_prefix": 1, "is_leaf": True, "children": {}},
            ...
          }
        }
      }
    }
    """
    tree = {"children": {}}

    for key in command_keys:
        tokens = key.split()
        node = tree
        for token in tokens:
            if token not in node["children"]:
                node["children"][token] = {"children": {}}
            node = node["children"][token]
        node["is_leaf"] = True

    def _annotate(node):
        children = node.get("children", {})
        if children:
            prefixes = compute_min_prefixes(list(children.keys()))
            for name, min_len in prefixes.items():
                children[name]["min_prefix"] = min_len
            for child in children.values():
                _annotate(child)

    _annotate(tree)
    return tree


# ---------------------------------------------------------------------------
# Validation against structured.json
# ---------------------------------------------------------------------------

def validate_against_structured(schema_commands, structured_path, verbose=True):
    """Cross-check the generated schema against structured.json.

    Prints warnings for mismatches but does not abort.
    Returns (missing_commands_count, missing_args_count).
    """
    with open(structured_path, encoding="utf-8") as f:
        structured = json.load(f)

    missing_cmds = 0
    missing_args = 0

    # Commands in structured.json but not in schema
    for cmd_key in structured:
        if cmd_key not in schema_commands:
            if verbose:
                print(f"  WARNING: '{cmd_key}' in structured.json but not in generated schema")
            missing_cmds += 1
        else:
            for arg in structured[cmd_key]:
                if arg not in schema_commands[cmd_key]["args"]:
                    if verbose:
                        print(f"  WARNING: '{cmd_key}'.'{arg}' in structured.json but not in schema")
                    missing_args += 1

    if verbose:
        # Commands in schema but not in structured.json
        extra = [k for k in schema_commands if k not in structured]
        if extra:
            print(f"  INFO: {len(extra)} commands in schema but not in structured.json "
                  f"(may be debug/menu-only). Examples: {extra[:5]}")

    return missing_cmds, missing_args


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate command_schema.json from commands.exp (and optionally language.src).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPORTANT: Review command_schema.json before committing.
Do not commit proprietary data from commands.exp or language.src.
""",
    )
    parser.add_argument(
        "--input", required=True, metavar="PATH",
        help="Path to commands.exp (primary input)",
    )
    parser.add_argument(
        "--language-src", metavar="PATH",
        help="Path to language.src (optional; for exclusive groups only)",
    )
    parser.add_argument(
        "--arg-options", metavar="PATH",
        help="Path to argument_options.json (optional; for enum values)",
    )
    parser.add_argument(
        "--output", required=True, metavar="PATH",
        help="Output path for command_schema.json",
    )
    parser.add_argument(
        "--validate", metavar="PATH",
        help="Path to structured.json for cross-validation",
    )
    parser.add_argument(
        "--patches", metavar="PATH",
        help=(
            "Path to a JSON patches file (e.g. scripts/schema_patches.json). "
            "Applied as the final step before writing output. "
            "Each entry under 'commands' REPLACES the corresponding key(s) "
            "in the generated command entry without touching other keys."
        ),
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress validation warnings",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Step 1: Parse commands.exp
    # ------------------------------------------------------------------
    print(f"Parsing {args.input} ...")
    exp_text = Path(args.input).read_text(encoding="utf-8", errors="replace")
    commands = parse_commands_exp(exp_text)
    print(f"  Found {len(commands)} command keys.")

    # ------------------------------------------------------------------
    # Step 2: Extract exclusive groups from language.src
    # ------------------------------------------------------------------
    exclusive_groups = {}
    if args.language_src:
        print(f"Extracting exclusive groups from {args.language_src} ...")
        src_text = Path(args.language_src).read_text(encoding="utf-8", errors="replace")
        exclusive_groups = extract_exclusive_groups(src_text, list(commands.keys()))
        total_groups = sum(len(v) for v in exclusive_groups.values())
        print(f"  Found {total_groups} exclusive groups across {len(exclusive_groups)} commands.")

    # Attach exclusive_groups to each command
    for cmd_key in commands:
        commands[cmd_key]["exclusive_groups"] = exclusive_groups.get(cmd_key, [])

    # ------------------------------------------------------------------
    # Step 3: Merge enum values from argument_options.json
    # ------------------------------------------------------------------
    if args.arg_options:
        print(f"Merging enum values from {args.arg_options} ...")
        arg_opts = json.loads(Path(args.arg_options).read_text(encoding="utf-8"))
        merged = 0
        for cmd_key, arg_opts_for_cmd in arg_opts.items():
            if cmd_key in commands:
                for arg_name, values in arg_opts_for_cmd.items():
                    if arg_name in commands[cmd_key]["args"]:
                        commands[cmd_key]["args"][arg_name]["enum_values"] = values
                        merged += 1
        print(f"  Merged {merged} enum value lists.")

    # ------------------------------------------------------------------
    # Step 4: Compute argument abbreviation prefixes
    # ------------------------------------------------------------------
    print("Computing argument abbreviation prefixes ...")
    for cmd_data in commands.values():
        arg_names = list(cmd_data["args"].keys())
        if arg_names:
            prefixes = compute_min_prefixes(arg_names)
            for arg_name, min_len in prefixes.items():
                cmd_data["args"][arg_name]["min_prefix"] = min_len

    # ------------------------------------------------------------------
    # Step 5: Build command tree with abbreviation prefixes
    # ------------------------------------------------------------------
    print("Building command tree ...")
    command_tree = build_command_tree(list(commands.keys()))

    # ------------------------------------------------------------------
    # Step 6: Validate against structured.json
    # ------------------------------------------------------------------
    if args.validate:
        print(f"Validating against {args.validate} ...")
        verbose = not args.quiet
        missing_cmds, missing_args = validate_against_structured(
            commands, args.validate, verbose=verbose
        )
        print(f"  Validation: {missing_cmds} missing commands, {missing_args} missing args.")

    # ------------------------------------------------------------------
    # Step 7: Apply manual patches (schema_patches.json)
    # ------------------------------------------------------------------
    if args.patches:
        print(f"Applying patches from {args.patches} ...")
        patches = json.loads(Path(args.patches).read_text(encoding="utf-8"))
        patched = 0
        for cmd_key, overrides in patches.get("commands", {}).items():
            if cmd_key in commands:
                for field, value in overrides.items():
                    commands[cmd_key][field] = value
                patched += 1
            else:
                print(f"  WARNING: patch target '{cmd_key}' not found in generated schema")
        print(f"  Applied patches to {patched} commands.")

    # ------------------------------------------------------------------
    # Step 8: Write output
    # ------------------------------------------------------------------
    schema = {
        "commands": commands,
        "command_tree": command_tree,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWrote {out_path} ({out_path.stat().st_size // 1024} KB).")
    print()
    print("=" * 70)
    print("REMINDER: Review command_schema.json before committing.")
    print("Do NOT commit proprietary data from commands.exp or language.src.")
    print("=" * 70)


if __name__ == "__main__":
    main()
