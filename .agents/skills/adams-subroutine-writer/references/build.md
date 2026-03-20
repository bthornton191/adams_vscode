# Build Reference — Adams User Subroutine DLLs

## Building with the `mdi` Tool

Adams provides the `mdi` (Model Development Interface) tool to compile and link user subroutines into a shared library (DLL on Windows, `.so` on Linux). This is the standard and correct way to build — it handles SDK paths, compiler flags, and linking automatically.

On Windows the command is `mdi.bat`; on Linux it is `mdi` (with `-c` flag).

### Prerequisite: Set Up the Compiler Environment (Windows)

Before calling `mdi.bat`, the Adams build environment must be initialized (PATH, Visual Studio, Intel Fortran).

#### Agent workflow (default)

After presenting generated code for the user to review, **the agent should offer to compile it** — not merely show build instructions. Adams ships `AdamsSetup.bat` for environment setup, but it spawns an interactive `cmd.exe /K` shell, making it unusable from automated workflows. Use the bundled script to generate a `call`-able version:

```cmd
python scripts/generate_adams_env.py
```

This finds the latest Adams installation, patches `AdamsSetup.bat` to hardcode the install path and remove the interactive shell, and writes the result to `%LOCALAPPDATA%\adams_env_init.bat`. You can also specify the Adams path explicitly:

```cmd
python scripts/generate_adams_env.py --adams-dir "C:\Program Files\MSC.Software\Adams\2024_2"
```

If `%LOCALAPPDATA%\adams_env_init.bat` already exists, skip the `python` step. Then initialize the environment and build:

```cmd
call "%LOCALAPPDATA%\adams_env_init.bat"
mdi.bat cr-u n <source files> -n <output>.dll ex
```

#### Fallback: manual user build (only if agent compilation fails)

If the agent compilation step fails, tell the user to build manually:
1. Open **Start Menu → Adams \<version\> → Command Prompt** (runs `AdamsSetup.bat` automatically)
2. `cd` to the directory containing the source files
3. Run `mdi.bat cr-u n <source files> -n <output>.dll ex`

On Linux, source the Adams environment script before calling `mdi`.

### Basic Usage

```
mdi[.bat] cr-u <options> <source files> -n <output library> ex
```

Arguments for `cr-u` (create user library):

| Argument | Meaning |
|----------|--------|
| `y` or `n` | Yes/no option to link in debug mode |
| `.c`, `.cxx`, `.f` | Source files to compile |
| `.o` | Pre-compiled object files |
| `.lst` | List file containing source/object file paths |
| `-n` | Marks end of source list; followed by output library name |
| `ex` | Exit the mdi tool |

### Windows

```cmd
mdi.bat cr-u n cbksub.c vfosub.c -n my_sub.dll ex
```

### Linux

```bash
mdi -c cr-u n cbksub.c vfosub.c -n my_sub.so ex
```

### With debug symbols

```cmd
mdi.bat cr-u y cbksub.c vfosub.c -n my_sub.dll ex
```

Use `y` instead of `n` to enable debug mode.

### Fortran source files

```cmd
mdi.bat cr-u n cbksub.f vfosub.f -n my_sub.dll ex
```

The `mdi` tool handles Fortran source files (`.f`) identically — just pass them instead of `.c` files.

---

## Referencing the Library in the Adams Dataset File (`.adm`)

```
CBKSUB/1
, FUNCTION=USER(1.0, 2.0)\
, ROUTINE=my_subroutines:Cbksub
```

- `my_subroutines` is the DLL name (without `.dll` / `.so`)
- `Cbksub` is the exported function name (case-sensitive on Linux)
- `USER(...)` parameters are accessible via `cbk->PAR[]` (0-indexed in C) or `PAR(*)` in Fortran

The DLL must be on the `PATH` (Windows) or `LD_LIBRARY_PATH` (Linux), or placed in the same directory as the Adams dataset file (`.adm`).

---

## Verifying Exports

After building with `mdi`, verify the exported symbols:

```cmd
dumpbin /exports my_sub.dll
```

Confirm the exported name matches exactly what the `ROUTINE=` line in the Adams dataset file (`.adm`) specifies (case-sensitive on Linux).

---

## Common Build Errors

| Error | Likely Cause |
|-------|-------------|
| `mdi.bat` not found / not recognized | Adams environment not initialized — run `scripts/generate_adams_env.py` then `call "%LOCALAPPDATA%\adams_env_init.bat"` |
| Adams reports "cannot find routine Cbksub" | DLL not on PATH, or function name case mismatch |
| Crash at startup | C++ CBKSUB not declared `extern "C"` |
| Linker errors for `c_sysary` etc. | Unusual — `mdi` handles linking automatically; check source file paths |
