"""Wrapper that starts the adams-cmd-mcp server using bundled dependencies.

This script is launched by the VS Code extension. It prepends the bundled
libs directory to sys.path so that adams_cmd_lsp is found without requiring
the user to pip-install it.  No external packages (mcp, pydantic, etc.) are
required — the server uses only the Python standard library plus the bundled
adams_cmd_lsp package.
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
    sys.stderr.write(
        f"adams-cmd-mcp: bundled libs missing or incomplete — "
        f"run the 'Bundle LSP Dependencies' task. ({exc})\n"
    )
    sys.exit(1)

if __name__ == "__main__":
    main()
