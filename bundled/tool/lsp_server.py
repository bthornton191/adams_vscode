"""Wrapper that starts the adams-cmd-lsp server using bundled dependencies.

This script is launched by the VS Code extension. It prepends the bundled
libs directory to sys.path so that pygls, lsprotocol, and adams_cmd_lsp are
found without requiring the user to pip-install anything.
"""
import os
import sys

# bundled/libs sits one level above this file (bundled/tool/)
_BUNDLED_LIBS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "libs"
)
if _BUNDLED_LIBS not in sys.path:
    sys.path.insert(0, _BUNDLED_LIBS)

from adams_cmd_lsp.server import main  # noqa: E402

if __name__ == "__main__":
    main()
