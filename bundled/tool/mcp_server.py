"""Wrapper that starts the adams-cmd-mcp server using bundled dependencies.

This script is launched by the VS Code extension. It prepends the bundled
libs directory to sys.path so that adams_cmd_lsp is found without requiring
the user to pip-install it.

The ``mcp`` package (and its transitive dependencies pydantic / pydantic_core)
must be installed in the Python environment selected by the user.  These are
not bundled because pydantic_core contains a compiled C extension that is
platform- and Python-version-specific.
"""
import os
import sys

# bundled/libs sits one level above this file (bundled/tool/)
_BUNDLED_LIBS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "libs"
)
if _BUNDLED_LIBS not in sys.path:
    sys.path.insert(0, _BUNDLED_LIBS)

try:
    from adams_cmd_lsp.mcp_server import main  # noqa: E402
except ImportError as exc:
    print(
        f"Adams CMD MCP server failed to start: {exc}\n"
        "Ensure the 'mcp' package is installed in your Python environment:\n"
        "    pip install 'mcp[cli]>=1.0'",
        file=sys.stderr,
    )
    sys.exit(1)

if __name__ == "__main__":
    main()
