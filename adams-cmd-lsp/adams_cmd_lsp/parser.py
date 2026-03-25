"""Parser for Adams CMD language.

Tokenizes raw .cmd text into Statement objects.
Ported from src/cmd_completion_provider.ts.js with extensions for
full-file parsing (line/column tracking, argument extraction, etc.).
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Argument:
    name: str         # e.g. "marker_name"
    value: str        # raw text value, not interpreted
    name_line: int    # 0-based line of the argument name token
    name_column: int  # 0-based column of the argument name token
    value_line: int   # 0-based line of the value start
    value_column: int # 0-based column of the value start


@dataclass
class Statement:
    command_key: str                          # as written by user, normalised lowercase
    resolved_command_key: Optional[str]       # canonical form after abbreviation resolution, or None
    arguments: List[Argument] = field(default_factory=list)
    line_start: int = 0                       # 0-based first line
    line_end: int = 0                         # 0-based last line (inclusive)
    raw_text: str = ""                        # full raw text including continuations (no comments)
    is_comment: bool = False
    is_blank: bool = False
    is_control_flow: bool = False
    control_flow_keyword: Optional[str] = None


# Control-flow keywords (first word only triggers control-flow detection)
_CONTROL_FLOW_KEYWORDS = frozenset(
    ["if", "else", "elseif", "end", "for", "while"]
)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _find_comment_start(line: str) -> int:
    """Return the index of the first unquoted '!' comment character, or len(line).

    In Adams CMD, '!' is a comment delimiter only when it appears OUTSIDE
    parentheses.  Inside parentheses it is the logical NOT operator (e.g.
    ``!DB_EXISTS(...)``) or the first character of the inequality operator
    ``!=``.  This function tracks paren depth so that '!' inside any level
    of parentheses is never mistaken for a comment start.

    Also correctly ignores '!' inside double-quoted or single-quoted strings,
    including strings that contain backslash-escaped quote characters (\\" or \\').
    """
    in_double = False
    in_single = False
    paren_depth = 0
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == '\\' and i + 1 < n:
            next_ch = line[i + 1]
            if in_double and next_ch == '"':
                i += 2  # skip escaped double-quote inside double-quoted string
                continue
            if in_single and next_ch == "'":
                i += 2  # skip escaped single-quote inside single-quoted string
                continue
        if ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "'" and not in_double:
            in_single = not in_single
        elif not in_double and not in_single:
            if ch == '(':
                paren_depth += 1
            elif ch == ')' and paren_depth > 0:
                paren_depth -= 1
            elif ch == '!' and paren_depth == 0:
                return i
        i += 1
    return n


def _strip_comment(line: str) -> str:
    """Return line with trailing comment removed."""
    return line[:_find_comment_start(line)]


def _is_continuation(line: str) -> bool:
    """Return True if the stripped-of-comment line ends with '&'."""
    stripped = _strip_comment(line).rstrip()
    return stripped.endswith('&')


def _strip_continuation(line: str) -> str:
    """Remove the trailing '&' (and any whitespace after stripping comment)."""
    stripped = _strip_comment(line).rstrip()
    if stripped.endswith('&'):
        return stripped[:-1]
    return stripped


# ---------------------------------------------------------------------------
# Continuation-line grouping
# ---------------------------------------------------------------------------

def _is_comment_only(line: str) -> bool:
    """Return True if the line is a comment-only line (first non-whitespace is '!')."""
    return line.lstrip().startswith('!')


def _group_continuation_lines(
    lines: List[str],
) -> List[Tuple[int, int, str, List[Tuple[int, int, int]]]]:
    """Group physical lines connected by '&' into logical statements.

    Returns a list of tuples:
        (line_start, line_end, joined_text, line_offsets)

    line_offsets is a list of (char_pos, phys_line, col) triples --
    for every character position in joined_text, which physical line
    and column it came from.  This enables precise diagnostic positions.

    Comment-only lines inside a continuation group are absorbed silently.
    Lines that are blank (empty or whitespace-only without '&') terminate
    the group.  Lines containing only '&' (spacer lines) are absorbed --
    they do not break the group.
    Note: a '&' appearing after '!' in a comment line is NOT a
    continuation marker -- it is part of the comment.
    """
    groups = []
    i = 0
    n = len(lines)

    while i < n:
        start = i
        parts = []          # text segments (comment stripped, & stripped)
        offsets = []        # (char_pos_in_joined, phys_line, col)
        char_pos = 0
        in_continuation = False  # True after the first real continuation line

        while i < n:
            raw = lines[i]

            # Inside a continuation group:
            # - Comment-only lines are absorbed silently.
            # - Lines containing only '&' (optionally preceded by whitespace)
            #   are absorbed as placeholder spacer lines -- a common pattern
            #   in generated Adams CMD files.
            # - Blank lines (empty or whitespace-only, with NO '&') terminate
            #   the continuation group.
            if in_continuation:
                if _is_comment_only(raw):
                    i += 1
                    continue
                if not raw.strip():
                    # Empty or whitespace-only without '&' — break the group
                    i += 1
                    break

            is_cont = _is_continuation(raw)
            text_part = _strip_continuation(raw) if is_cont else _strip_comment(raw)

            # Build per-character offset mapping for this segment
            for col, ch in enumerate(text_part):
                offsets.append((char_pos, i, col))
                char_pos += 1

            # Add a space separator between joined lines (unless last segment)
            # We record the space as belonging to the start of the *next* line
            # so any error on the space points somewhere sensible.
            if is_cont:
                # Record separator space as belonging to the continuation line
                offsets.append((char_pos, i, len(text_part)))
                char_pos += 1
                parts.append(text_part)
                in_continuation = True
                i += 1
            else:
                parts.append(text_part)
                i += 1
                break

        joined = " ".join(parts)
        groups.append((start, i - 1, joined, offsets))

    return groups


def _char_to_line_col(
    char_pos: int,
    offsets: List[Tuple[int, int, int]],
) -> Tuple[int, int]:
    """Map a character position in joined_text back to (phys_line, col).

    Uses the offsets list from _group_continuation_lines.
    Falls back to the last entry if char_pos is out of range.
    """
    if not offsets:
        return (0, 0)

    # Binary-search would be faster but linear is fine for typical statement lengths
    best = offsets[0]
    for entry in offsets:
        if entry[0] <= char_pos:
            best = entry
        else:
            break
    return (best[1], best[2] + (char_pos - best[0]))


# ---------------------------------------------------------------------------
# Value consumption (ported from cmd_completion_provider.ts.js)
# ---------------------------------------------------------------------------

def _consume_argument_value(text: str, start: int) -> int:
    """Consume a single argument value starting at position start.

    Handles:
    - Quoted strings: "..."
    - Parenthesised expressions: (...) with nesting
    - Bare words: sequences of non-whitespace chars (stops at whitespace)

    Returns the position immediately after the consumed value.
    """
    if start >= len(text):
        return start

    ch = text[start]

    # Quoted string (double-quoted)
    # Handles backslash-escaped quotes (\") inside the string.
    if ch == '"':
        i = start + 1
        while i < len(text):
            c = text[i]
            if c == '\\' and i + 1 < len(text) and text[i + 1] == '"':
                i += 2  # skip escaped quote
                continue
            if c == '"':
                break
            i += 1
        return i + 1 if i < len(text) else i

    # Quoted string (single-quoted)
    # Handles backslash-escaped quotes (\') inside the string.
    if ch == "'":
        i = start + 1
        while i < len(text):
            c = text[i]
            if c == '\\' and i + 1 < len(text) and text[i + 1] == "'":
                i += 2  # skip escaped quote
                continue
            if c == "'":
                break
            i += 1
        return i + 1 if i < len(text) else i

    # Parenthesised expression (with nesting, ignores quoted contents)
    if ch == '(':
        depth = 0
        in_double = False
        in_single = False
        i = start
        while i < len(text):
            c = text[i]
            if c == '"' and not in_single:
                in_double = not in_double
            elif c == "'" and not in_double:
                in_single = not in_single
            elif not in_double and not in_single:
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        return i + 1
            i += 1
        return i  # unclosed paren

    # Bare word (may contain embedded quoted segments, e.g. .MODEL."Part 1")
    i = start
    while i < len(text) and not text[i].isspace():
        ch = text[i]
        if ch in ('"', "'"):
            # Consume through the matching closing quote so that spaces inside
            # quoted segments (e.g. "Part 1") do not terminate the bare word.
            quote = ch
            i += 1
            while i < len(text) and text[i] != quote:
                i += 1
            if i < len(text):
                i += 1  # consume the closing quote
        else:
            i += 1
    return i


def _consume_comma_separated_tail(text: str, i: int, value_start: int) -> int:
    """After consuming a value, continue consuming comma-separated values.

    Handles: stiffness=1e6, 1e6, 1e6
    Also handles whitespace before a leading comma, e.g.:
        points_for_profile = 30.0, 0.0, 60.0         , 60.0, 0.0, 80.0
    which arises when comma-prefixed continuation lines are joined.
    Stops when a new word= pattern or end of text is reached.
    """
    while True:
        # Trailing comma already consumed into the value (e.g. bare-word "1e6,")
        has_trailing_comma = (i > value_start and i <= len(text)
                              and i > 0 and text[i - 1] == ',')
        has_following_comma = (i < len(text) and text[i] == ',')

        # Also look past whitespace for a leading comma, e.g. "val   , next_val".
        # This pattern arises when Adams CMD continuation lines start with ", val"
        # (polyline coordinates, macro commands= arrays, etc.) and are joined.
        ws_comma_pos = -1
        if not has_trailing_comma and not has_following_comma:
            j = i
            while j < len(text) and text[j].isspace():
                j += 1
            if j < len(text) and text[j] == ',':
                ws_comma_pos = j

        if has_trailing_comma or has_following_comma or ws_comma_pos >= 0:
            if ws_comma_pos >= 0:
                next_pos = ws_comma_pos + 1
            else:
                next_pos = i
                if has_following_comma:
                    next_pos += 1
            while next_pos < len(text) and text[next_pos].isspace():
                next_pos += 1

            if next_pos >= len(text):
                break

            # Stop if the next token looks like a new arg=value pair
            if re.match(r'^\w+\s*=', text[next_pos:]):
                break

            i = _consume_argument_value(text, next_pos)
        else:
            break

    return i


# ---------------------------------------------------------------------------
# Command key extraction (ported from strip_argument_pairs in JS)
# ---------------------------------------------------------------------------

def _extract_command_key(text: str) -> str:
    """Strip all arg=value pairs from text to isolate the command key.

    Port of strip_argument_pairs() from cmd_completion_provider.ts.js.

    Example:
        "part create rigid_body name_and_position part_name=.model.P1 loc=0,0,0"
        → "part create rigid_body name_and_position"
    """
    result = []
    i = 0
    n = len(text)

    while i < n:
        if text[i].isspace():
            ws_start = i
            while i < n and text[i].isspace():
                i += 1
            # Look ahead: is the next token an arg= pattern?
            m = re.match(r'(\w+\s*=\s*)', text[i:])
            if m:
                # Consume the arg=value pair without adding to result
                value_start = i + len(m.group(0))
                end = _consume_argument_value(text, value_start)
                end = _consume_comma_separated_tail(text, end, value_start)
                i = end
            else:
                # It's whitespace between command keywords — keep it
                result.append(text[ws_start:i])
        else:
            result.append(text[i])
            i += 1

    return "".join(result).strip()


# ---------------------------------------------------------------------------
# Argument extraction
# ---------------------------------------------------------------------------

def _extract_arguments(
    text: str,
    offsets: List[Tuple[int, int, int]],
) -> List[Argument]:
    """Extract all arg=value pairs from a statement's joined text.

    Returns a list of Argument objects with physical line/column positions.
    """
    arguments = []
    i = 0
    n = len(text)

    while i < n:
        # Must be at a word boundary (start or preceded by whitespace)
        if i > 0 and not text[i - 1].isspace():
            i += 1
            continue

        # Match word= pattern
        m = re.match(r'(\w+)\s*=\s*', text[i:])
        if not m:
            i += 1
            continue

        name = m.group(1)
        name_pos = i
        value_start = i + len(m.group(0))

        value_end = _consume_argument_value(text, value_start)
        value_end = _consume_comma_separated_tail(text, value_end, value_start)
        value = text[value_start:value_end].strip()

        name_line, name_col = _char_to_line_col(name_pos, offsets)
        val_line, val_col = _char_to_line_col(value_start, offsets)

        arguments.append(Argument(
            name=name.lower(),
            value=value,
            name_line=name_line,
            name_column=name_col,
            value_line=val_line,
            value_column=val_col,
        ))
        i = value_end if value_end > i else i + 1

    return arguments


# ---------------------------------------------------------------------------
# Top-level parse function
# ---------------------------------------------------------------------------

def parse(text: str) -> List[Statement]:
    """Parse raw .cmd text into a list of Statement objects.

    Args:
        text: raw .cmd file content (any line endings)

    Returns:
        list of Statement objects, one per logical line / continuation group
    """
    lines = text.splitlines()
    groups = _group_continuation_lines(lines)
    statements = []

    for line_start, line_end, joined, offsets in groups:
        stripped = joined.strip()

        # Detect if the original first physical line of this group is comment-only.
        # We must check the original line because _group_continuation_lines strips
        # comment text from the joined output, turning comment lines into empty strings.
        first_raw_line = lines[line_start] if lines else ""
        is_first_line_comment = _is_comment_only(first_raw_line)

        # Comment-only line (check raw first, before the stripped blank check)
        if is_first_line_comment:
            statements.append(Statement(
                command_key="",
                resolved_command_key=None,
                line_start=line_start,
                line_end=line_end,
                raw_text=first_raw_line,
                is_comment=True,
            ))
            continue

        # Blank line (may also appear when a comment line was stripped to nothing)
        if not stripped:
            statements.append(Statement(
                command_key="",
                resolved_command_key=None,
                line_start=line_start,
                line_end=line_end,
                raw_text=joined,
                is_blank=True,
            ))
            continue

        # Extract the command key (strip arg=value pairs)
        cmd_key_raw = _extract_command_key(stripped)
        cmd_key = cmd_key_raw.lower()

        # Detect control flow keywords (only first word matters)
        first_word = cmd_key.split()[0] if cmd_key.split() else ""
        if first_word in _CONTROL_FLOW_KEYWORDS:
            statements.append(Statement(
                command_key=cmd_key,
                resolved_command_key=None,
                line_start=line_start,
                line_end=line_end,
                raw_text=joined,
                is_control_flow=True,
                control_flow_keyword=first_word,
            ))
            continue

        # Normal command statement — extract arguments
        args = _extract_arguments(joined, offsets)

        statements.append(Statement(
            command_key=cmd_key,
            resolved_command_key=None,  # filled in by rules.py rule_unknown_command
            arguments=args,
            line_start=line_start,
            line_end=line_end,
            raw_text=joined,
        ))

    return statements
