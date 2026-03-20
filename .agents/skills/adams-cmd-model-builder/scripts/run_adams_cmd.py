"""
Run an Adams CMD script in Adams View (batch mode) and check aview.log for errors.

Usage:
    python run_adams_cmd.py <cmd_file> [--timeout 120]

The script:
  1. Locates mdi.bat (VS Code setting → env var → common install path)
  2. Launches Adams View in batch mode: mdi.bat aview ru-s -b <cmd_file>
  3. Waits for the aview.exe process to finish (watches for the spawned process
     whose working directory matches)
  4. Parses aview.log for ERROR: lines
  5. Prints results and exits 0 (no errors) or 1 (errors found)

Exit codes:
  0 — CMD script ran without errors
  1 — One or more ERROR: lines found in aview.log
  2 — Could not locate mdi.bat
  3 — Adams View failed to start or timed out
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

LOG_NAME = "aview.log"
FINISH_MARKER = "! Command file is exhausted, batch run is finished."


def find_mdi_bat() -> Path | None:
    """Locate mdi.bat using multiple fallback strategies."""
    # 1. VS Code extension setting (msc-adams.adamsLaunchCommand)
    #    Read from workspace .vscode/settings.json or user settings
    for settings_path in [
        Path.cwd() / ".vscode" / "settings.json",
        Path(os.environ.get("APPDATA", "")) / "Code" / "User" / "settings.json",
    ]:
        if settings_path.is_file():
            try:
                data = json.loads(settings_path.read_text(encoding="utf-8"))
                launch_cmd = data.get("msc-adams.adamsLaunchCommand")
                if launch_cmd:
                    p = Path(launch_cmd)
                    if p.is_file():
                        return p
            except (json.JSONDecodeError, OSError):
                pass

    # 2. ADAMS_LAUNCH_COMMAND env var → direct path to mdi.bat
    env_launch = os.environ.get("ADAMS_LAUNCH_COMMAND")
    if env_launch:
        p = Path(env_launch)
        if p.is_file():
            return p

    # 3. ADAMS_INSTALL_DIR env var → find latest version
    env_install = os.environ.get("ADAMS_INSTALL_DIR")
    if env_install:
        install_dir = Path(env_install)
        if install_dir.is_dir():
            candidates = sorted(
                (d for d in install_dir.iterdir()
                 if d.is_dir() and (d / "common" / "mdi.bat").exists()),
                key=lambda d: d.name,
            )
            if candidates:
                return candidates[-1] / "common" / "mdi.bat"

    # 4. Default install location
    default_parent = Path(r"C:\Program Files\MSC.Software\Adams")
    if default_parent.is_dir():
        candidates = sorted(
            (d for d in default_parent.iterdir()
             if d.is_dir() and (d / "common" / "mdi.bat").exists()),
            key=lambda d: d.name,
        )
        if candidates:
            return candidates[-1] / "common" / "mdi.bat"

    return None


def wait_for_aview(log_path: Path, timeout: int) -> bool:
    """
    Wait for Adams View to finish by watching aview.log for the completion marker.

    Returns True if the process completed, False if timed out.
    """
    start = time.time()

    # Brief initial delay — Adams View clears the log file on startup,
    # but there's a window where a stale log from a previous run could
    # already contain the finish marker.
    time.sleep(3)

    while time.time() - start < timeout:
        if log_path.is_file():
            try:
                content = log_path.read_text(encoding="utf-8", errors="replace")
                if FINISH_MARKER in content:
                    return True
            except OSError:
                pass  # File may be locked by aview.exe
        time.sleep(2)

    return False


def check_log_errors(log_path: Path) -> list[str]:
    """Extract ERROR: lines from aview.log."""
    if not log_path.is_file():
        return ["aview.log not found — Adams View may not have started"]

    content = log_path.read_text(encoding="utf-8", errors="replace")
    errors = []
    for line in content.splitlines():
        if re.search(r"\bERROR:\s", line):
            errors.append(line.strip())
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Run an Adams CMD script and check for errors"
    )
    parser.add_argument("cmd_file", help="Path to the .cmd file to run")
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="Seconds to wait for Adams View to finish (default: 120)"
    )
    parser.add_argument(
        "--log-output", default=None,
        help="Copy aview.log to this path after the run (for eval output capture)"
    )
    args = parser.parse_args()

    cmd_path = Path(args.cmd_file).resolve()
    if not cmd_path.is_file():
        print(f"Error: CMD file not found: {cmd_path}", file=sys.stderr)
        sys.exit(2)

    # Adams View runs in the CMD file's parent directory
    work_dir = cmd_path.parent
    log_path = work_dir / LOG_NAME

    # Find mdi.bat
    mdi = find_mdi_bat()
    if mdi is None:
        print(
            "Error: Could not locate mdi.bat. Set ADAMS_LAUNCH_COMMAND or "
            "ADAMS_INSTALL_DIR environment variable, or configure "
            "msc-adams.adamsLaunchCommand in VS Code settings.",
            file=sys.stderr,
        )
        sys.exit(2)

    print(f"Using mdi.bat: {mdi}")
    print(f"Running: {cmd_path.name}")
    print(f"Working dir: {work_dir}")

    # Launch Adams View in batch mode
    launch_cmd = [str(mdi), "aview", "ru-s", "-b", cmd_path.name]
    try:
        subprocess.Popen(
            launch_cmd,
            cwd=str(work_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as e:
        print(f"Error: Failed to launch Adams View: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"Adams View launched, waiting up to {args.timeout}s for completion...")

    # Wait for completion
    finished = wait_for_aview(log_path, args.timeout)
    if not finished:
        print(f"Error: Adams View did not finish within {args.timeout}s", file=sys.stderr)
        sys.exit(3)

    print("Adams View finished.")

    # Copy log if requested
    if args.log_output:
        out_path = Path(args.log_output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(log_path, out_path)
        print(f"Log copied to: {out_path}")

    # Check for errors
    errors = check_log_errors(log_path)
    if errors:
        print(f"\nFOUND {len(errors)} ERROR(S) in aview.log:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("\nNo errors found in aview.log.")
        sys.exit(0)


if __name__ == "__main__":
    main()
