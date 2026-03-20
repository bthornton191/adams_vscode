"""Run an Adams Python script in Adams View (batch mode) and check aview.log for errors.

Usage:
    python run_adams_python.py <py_file> [--timeout 120]

The script:
  1. Locates mdi.bat (VS Code setting → env var → common install path)
  2. Launches Adams View in batch mode: mdi.bat aview ru-s -b <py_file>
  3. Waits for aview.exe to finish by monitoring aview.log or the process
  4. Parses aview.log for ERROR: lines
  5. Prints results and exits 0 (no errors) or 1 (errors found)

Exit codes:
  0 — Python script ran without errors
  1 — One or more ERROR: lines found in aview.log (or Python exception traceback)
  2 — Could not locate mdi.bat, or .py file not found
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
# Adams View adds this to the log when a batch session ends
FINISH_MARKERS = [
    "! Command file is exhausted, batch run is finished.",
    "Batch run is finished.",
]
# Python tracebacks indicate a fatal error in the script
PYTHON_ERROR_PATTERNS = [
    r"Traceback \(most recent call last\)",
    r"^\s*File \".*\", line \d+",
    r"^[A-Z][a-zA-Z]+Error:",
]


def find_mdi_bat() -> Path | None:
    """Locate mdi.bat using multiple fallback strategies."""
    # 1. VS Code extension setting (msc-adams.adamsLaunchCommand)
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


def wait_for_aview(log_path: Path, proc: subprocess.Popen, timeout: int) -> bool:
    """
    Wait for Adams View to finish.

    Polls aview.log for a batch-finish marker AND watches for the spawned
    process to exit. Returns True on clean finish, False on timeout.
    """
    start = time.time()
    time.sleep(3)  # Brief delay to let Adams clear the log on startup

    while time.time() - start < timeout:
        # Check if the process has exited
        if proc.poll() is not None:
            time.sleep(1)  # Small settle time for final log flush
            return True

        # Also accept the log finish marker
        if log_path.is_file():
            try:
                content = log_path.read_text(encoding="utf-8", errors="replace")
                if any(m in content for m in FINISH_MARKERS):
                    return True
            except OSError:
                pass  # File may be momentarily locked

        time.sleep(2)

    return False


def check_log_errors(log_path: Path) -> list[str]:
    """Extract ERROR: lines and Python traceback indicators from aview.log."""
    if not log_path.is_file():
        return ["aview.log not found — Adams View may not have started"]

    content = log_path.read_text(encoding="utf-8", errors="replace")
    errors = []

    for line in content.splitlines():
        if re.search(r"\bERROR:\s", line):
            errors.append(line.strip())
        # Python exception — any of the traceback patterns
        for pat in PYTHON_ERROR_PATTERNS:
            if re.search(pat, line):
                errors.append(f"[Python] {line.strip()}")
                break

    # Deduplicate while preserving order
    seen = set()
    unique_errors = []
    for e in errors:
        if e not in seen:
            seen.add(e)
            unique_errors.append(e)

    return unique_errors


def main():
    parser = argparse.ArgumentParser(
        description="Run an Adams Python script in Adams View batch mode and check for errors"
    )
    parser.add_argument("py_file", help="Path to the .py file to run")
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="Seconds to wait for Adams View to finish (default: 120)"
    )
    parser.add_argument(
        "--log-output", default=None,
        help="Copy aview.log to this path after the run (for eval output capture)"
    )
    args = parser.parse_args()

    py_path = Path(args.py_file).resolve()
    if not py_path.is_file():
        print(f"Error: Python file not found: {py_path}", file=sys.stderr)
        sys.exit(2)

    # Adams View runs in the .py file's parent directory
    work_dir = py_path.parent
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
    print(f"Running: {py_path.name}")
    print(f"Working dir: {work_dir}")

    # Launch Adams View in batch mode with the Python script
    launch_cmd = [str(mdi), "aview", "ru-s", "-b", py_path.name]
    try:
        proc = subprocess.Popen(
            launch_cmd,
            cwd=str(work_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as e:
        print(f"Error: Failed to launch Adams View: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"Adams View launched (PID {proc.pid}), waiting up to {args.timeout}s for completion...")

    finished = wait_for_aview(log_path, proc, args.timeout)
    if not finished:
        proc.terminate()
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
