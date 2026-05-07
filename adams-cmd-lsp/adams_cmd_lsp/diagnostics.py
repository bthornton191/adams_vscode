"""Diagnostic dataclass and severity enum for Adams CMD linting."""

from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Diagnostic:
    line: int        # 0-based line number
    column: int      # 0-based column
    end_line: int    # 0-based end line
    end_column: int  # 0-based end column
    code: str        # e.g. "E001", "W005"
    message: str     # human-readable message
    severity: Severity
