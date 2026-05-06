"""Run an Adams Python script in Adams View (batch mode) and check the log for errors.

Usage:
    python run_adams_python.py <py_file> [--cwd <dir>] [--timeout 120]

The script:
  1. Locates mdi.bat (VS Code setting → env var → common install path)
  2. Injects ``Adams.execute_cmd('file log_file file_name = "..."')`` at the top of a
     temporary copy of the Python file so that multiple agents can run Adams in
     parallel without their logs clashing.
  3. Launches Adams View in batch mode: mdi.bat aview ru-s b <modified_py>
     The working directory can be overridden with --cwd (e.g. ./working_directory
     for qualification runs that rely on aview.cmd / aviewBS.cmd being present).
  4. Waits for Adams to finish by watching the unique log file for the batch
     completion marker AND polling the process for exit.
  5. Parses the log for ERROR: lines and Python traceback indicators.
  6. Prints results and exits 0 (no errors) or 1 (errors found)

Exit codes:
  0 — Python script ran without errors
  1 — One or more ERROR: lines found in the log (or Python exception traceback)
  2 — Could not locate mdi.bat, or .py file not found
  3 — Adams View failed to start or timed out
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

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


def _strip_json_comments(text: str) -> str:
    """Strip // line comments and /* */ block comments from a JSONC string."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def _cleanup_old_logs() -> None:
    """Delete aview_*.log files in the temp directory that are older than 24 hours."""
    cutoff = time.time() - 86400
    for log_file in Path(tempfile.gettempdir()).glob("aview_*.log"):
        try:
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
        except OSError:
            pass  # File may be locked by a concurrent run


def find_mdi_bat() -> Path | None:
    """Locate mdi.bat using multiple fallback strategies."""
    # 1. VS Code extension setting (msc-adams.adamsLaunchCommand)
    for settings_path in [
        Path.cwd() / ".vscode" / "settings.json",
        Path(os.environ.get("APPDATA", "")) / "Code" / "User" / "settings.json",
    ]:
        if settings_path.is_file():
            try:
                data = json.loads(_strip_json_comments(settings_path.read_text(encoding="utf-8")))
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

    Polls *log_path* for a batch-finish marker AND watches for the spawned
    process to exit. Returns True on clean finish, False on timeout.
    """
    start = time.time()
    time.sleep(3)  # Brief delay — Adams may not create the log file immediately after launch.

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
    """Extract ERROR: lines and Python traceback indicators from *log_path*."""
    if not log_path.is_file():
        return [f"Log file not found ({log_path}) — Adams View may not have started"]

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
        "--cwd", default=None,
        help=(
            "Working directory for Adams View (default: directory of the Python file). "
            "Override to e.g. ./working_directory so that aview.cmd / aviewBS.cmd are "
            "picked up automatically (required for qualification runs)."
        ),
    )
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="Seconds to wait for Adams View to finish (default: 120)"
    )
    parser.add_argument(
        "--log-output", default=None,
        help="Copy the unique log file to this path after the run"
    )
    args = parser.parse_args()

    py_path = Path(args.py_file).resolve()
    if not py_path.is_file():
        print(f"Error: Python file not found: {py_path}", file=sys.stderr)
        sys.exit(2)

    work_dir = Path(args.cwd).resolve() if args.cwd else py_path.parent
    if not work_dir.is_dir():
        print(f"Error: Working directory not found: {work_dir}", file=sys.stderr)
        sys.exit(2)

    # Locate mdi.bat before creating any temp files so we fail fast and cleanly.
    mdi = find_mdi_bat()
    if mdi is None:
        print(
            "Error: Could not locate mdi.bat. Set ADAMS_LAUNCH_COMMAND or "
            "ADAMS_INSTALL_DIR environment variable, or configure "
            "msc-adams.adamsLaunchCommand in VS Code settings.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Clean up stale logs from previous runs before creating the new one.
    _cleanup_old_logs()

    # Build a unique log path in the OS temp directory so that concurrent Adams
    # sessions never write to the same log file.
    unique_log = Path(tempfile.gettempdir()) / f"aview_{uuid.uuid4().hex}.log"

    # Inject the log-file redirect at the very top of a temporary copy of the
    # Python script using Adams.execute_cmd() so it runs before the rest of
    # the script.
    log_redirect_line = (
        f"import Adams; "
        f"Adams.execute_cmd('file log_file file_name = \"{unique_log.as_posix()}\" "
        f"messages_include = on commands_include = on')"
    )
    original_content = py_path.read_text(encoding="utf-8")
    modified_content = log_redirect_line + "\n" + original_content

    modified_py = Path(tempfile.gettempdir()) / f"_run_adams_{uuid.uuid4().hex}.py"
    modified_py.write_text(modified_content, encoding="utf-8")

    print(f"Using mdi.bat: {mdi}")
    print(f"Running: {py_path.name}")
    print(f"Working dir: {work_dir}")
    print(f"Log file: {unique_log}")

    # Launch Adams View in batch mode.  The modified script uses an absolute
    # path so Adams can find it regardless of the working directory.
    launch_cmd = [str(mdi), "aview", "ru-s", "b", str(modified_py)]
    try:
        try:
            # Clear PYTHONSTARTUP so VS Code's injected pythonrc.py does not
            # cause a SyntaxError inside Adams View's Python interpreter.
            launch_env = {**os.environ, "PYTHONSTARTUP": ""}
            proc = subprocess.Popen(
                launch_cmd,
                cwd=str(work_dir),
                env=launch_env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as e:
            print(f"Error: Failed to launch Adams View: {e}", file=sys.stderr)
            sys.exit(3)

        print(f"Adams View launched (PID {proc.pid}), waiting up to {args.timeout}s for completion...")

        # Wait for completion — watch the unique log AND poll the process.
        finished = wait_for_aview(unique_log, proc, args.timeout)
        if not finished:
            proc.terminate()
            print(f"Error: Adams View did not finish within {args.timeout}s", file=sys.stderr)
            sys.exit(3)

        print("Adams View finished.")

        # Copy log if requested — retry a few times because aview.exe may still
        # hold the file briefly after writing the finish marker.
        if args.log_output:
            out_path = Path(args.log_output).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path == unique_log.resolve():
                print(f"Log already at: {out_path}")
            else:
                for attempt in range(10):
                    try:
                        shutil.copy2(unique_log, out_path)
                        print(f"Log copied to: {out_path}")
                        break
                    except PermissionError:
                        if attempt < 9:
                            time.sleep(2)
                        else:
                            out_path.write_text(
                                unique_log.read_text(encoding="utf-8", errors="replace"),
                                encoding="utf-8",
                            )
                            print(f"Log written to: {out_path} (fallback copy)")

        # Check for errors in the unique log
        errors = check_log_errors(unique_log)
        if errors:
            print(f"\nFOUND {len(errors)} ERROR(S) in log:")
            for err in errors:
                print(f"  {err}")
            sys.exit(1)
        else:
            print("\nNo errors found in log.")
            sys.exit(0)
    finally:
        # Clean up the temporary modified script — the unique log is left in place
        # so that callers can still read it after this script exits.
        modified_py.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
