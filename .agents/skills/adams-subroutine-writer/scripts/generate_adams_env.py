"""
Generate adams_env_init.bat from the installed AdamsSetup.bat.

AdamsSetup.bat sets up the Adams PATH and the C/Fortran compiler environment
(MSVC via vswhere, or Intel oneAPI), which is required before mdi.bat can
compile a user subroutine DLL.  It must be `call`-ed rather than run directly
because it ends with `cmd.exe /K` to spawn an interactive shell.

This script:
  1. Reads AdamsSetup.bat from the Adams installation.
  2. Replaces the two `%~dsp0%`-relative topdir lines with a hardcoded
     assignment so the bat works correctly when called from any directory.
  3. Comments out the `cmd.exe /K` line so it returns instead of hanging.
  4. Writes the result to %LOCALAPPDATA%\\adams_env_init.bat.

Usage:
    python generate_adams_env.py [--adams-dir "C:\\Program Files\\MSC.Software\\Adams\\2024_2"]

If --adams-dir is not provided, the script searches for Adams installations
under "C:\\Program Files\\MSC.Software\\Adams" and uses the latest version found.
"""

import argparse
import ctypes
import os
import re
import sys
from pathlib import Path

DEFAULT_ADAMS_PARENT = Path(r"C:\Program Files\MSC.Software\Adams")
OUTPUT_DIR = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")))
OUTPUT_NAME = "adams_env_init.bat"


def get_short_path(path: Path) -> str:
    """Return the Windows 8.3 short path so topdir is space-safe in batch PATH expansions."""
    try:
        buf = ctypes.create_unicode_buffer(512)
        if ctypes.windll.kernel32.GetShortPathNameW(str(path), buf, 512):
            return buf.value
    except Exception:
        pass
    return str(path)


def find_latest_adams(parent: Path) -> Path | None:
    """Find the latest Adams installation directory by version string."""
    if not parent.is_dir():
        return None
    candidates = [d for d in parent.iterdir() if d.is_dir() and (d / "common" / "AdamsSetup.bat").exists()]
    if not candidates:
        return None
    # Sort by directory name — Adams versions like 2023_4_1, 2024_2 sort correctly as strings
    candidates.sort(key=lambda d: d.name)
    return candidates[-1]


def generate(adams_dir: Path) -> Path:
    """Patch AdamsSetup.bat (fix topdir, remove interactive shell) and write to LOCALAPPDATA."""
    setup_bat = adams_dir / "common" / "AdamsSetup.bat"
    if not setup_bat.exists():
        print(f"Error: {setup_bat} not found", file=sys.stderr)
        sys.exit(1)

    content = setup_bat.read_text(encoding="utf-8", errors="replace")

    # AdamsSetup.bat uses %~dsp0% (short path of the script itself) then strips
    # the trailing "common\" (7 chars) to derive topdir.  When the bat is placed
    # in %LOCALAPPDATA%, %~dsp0% resolves to the wrong location.  Replace both
    # lines with a single hardcoded assignment using the 8.3 short path so the
    # result is space-safe in batch PATH expansions.
    short_topdir = get_short_path(adams_dir).rstrip("\\") + "\\"
    modified = re.sub(
        r"^(\s*set\s+topdir=%~dsp0%\s*)$",
        f"set topdir={short_topdir}",
        content,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    modified = re.sub(
        r"^(\s*set\s+topdir=%topdir:~0,-7%\s*)$",
        r"REM \1",
        modified,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    # Comment out the line that spawns an interactive cmd shell so the bat
    # returns normally after setting up the environment.
    modified = re.sub(
        r"^(\s*%windir%\\system32\\cmd\.exe\s+/K.*)$",
        r"REM \1",
        modified,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    if modified == content:
        print("Warning: could not find expected lines to patch — writing as-is", file=sys.stderr)

    output_path = OUTPUT_DIR / OUTPUT_NAME
    output_path.write_text(modified, encoding="utf-8")
    print(f"Wrote: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate adams_env_init.bat for automated builds")
    parser.add_argument(
        "--adams-dir",
        type=Path,
        default=None,
        help="Path to Adams installation root (e.g. C:\\Program Files\\MSC.Software\\Adams\\2024_2)",
    )
    args = parser.parse_args()

    if args.adams_dir:
        adams_dir = args.adams_dir
    else:
        adams_dir = find_latest_adams(DEFAULT_ADAMS_PARENT)
        if not adams_dir:
            print(
                f"Error: no Adams installation found under {DEFAULT_ADAMS_PARENT}. "
                "Use --adams-dir to specify the path.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Found Adams installation: {adams_dir}")

    output = generate(adams_dir)
    print("\nTo build a user subroutine DLL, run:")
    print(f'  call "{output}"')
    print("  mdi.bat cr-u n <source files> -n <output>.dll ex")


if __name__ == "__main__":
    main()
