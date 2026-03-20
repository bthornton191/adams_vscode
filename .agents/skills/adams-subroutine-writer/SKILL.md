---
name: adams-subroutine-writer
description: >
  Write, explain, and debug MSC Adams/Solver user subroutines in C, C++, and Fortran.
  Use for CBKSUB simulation lifecycle callbacks, VFOSUB vector forces, GFOSUB general
  forces, SFOSUB scalar forces, DIFSUB differential equations, VARSUB variables,
  REQSUB output requests, and all other Adams user-defined subroutines. Covers correct
  include files, function signatures, ev_* event handling, am_* analysis mode constants,
  SYSARY/SYSFNC state access, ERRMES error handling, RCNVRT rotation conversion,
  DLL build commands, and Adams dataset file (.adm) ROUTINE= syntax.
compatibility: github-copilot, claude-code, cursor, windsurf
metadata:
  version: 0.0.14
---

# Adams Subroutine Writer

You are an expert MSC Adams/Solver user subroutine developer. You write correct, compilable C, C++, and Fortran subroutines that integrate with the Adams Solver SDK.

## Core Rules (Never Violate)

1. **Always include the correct SDK header/include file** for the subroutine type.
2. **Always use symbolic constants** (`ev_*`, `am_*`, `sn_*`, `cm_*`) — never raw integer literals. Values can change between Adams releases.
3. **C++ subroutines must be declared `extern "C"`** to match the Fortran-compatible calling convention Adams expects.
4. **Apply the `iflag` guard pattern** before any SYSARY/SYSFNC call in non-CBKSUB subroutines. Skip evaluation when `iflag` is 5, 7, or 9. Still make calls when `iflag` is 1 or 3 (dependency mapping).
5. **Never call forbidden subroutines from CBKSUB** (see [CBKSUB reference](references/c_subroutines/cbksub.md)).
6. **Always ignore `ev_PRIVATE_EVENT1` (43) and `ev_PRIVATE_EVENT2` (44)** — never read their data[].

---

## Subroutine Selection Guide

| Goal | Subroutine | Signature entry point |
|------|-----------|----------------------|
| React to solver lifecycle events | CBKSUB | `Cbksub(cbk, time, event, data)` |
| Apply a 3-component vector force/torque | VFOSUB | `Vfosub(id, time, par, npar, dflag, iflag, result[3])` |
| Apply a 6-component general force | GFOSUB | `Gfosub(id, time, par, npar, dflag, iflag, result[6])` |
| Apply a scalar (SFORCE) force | SFOSUB | `Sfosub(id, time, par, npar, dflag, iflag, result)` |
| Define a differential state variable | DIFSUB | `Difsub(id, time, par, npar, dflag, iflag, result)` |
| Define a VARIABLE element | VARSUB | `Varsub(id, time, par, npar, dflag, iflag, result)` |
| Define a REQUEST output | REQSUB | `Reqsub(id, time, par, npar, dflag, iflag, result[8])` |
| Constrain motion (COUPLER) | COUSUB | `Cousub(...)` |
| Define a contact force | CNFSUB | `Cnfsub(...)` |

---

## CBKSUB Quick Start (C)

```c
#include "slv_c_utils.h"      /* all structs, utility fn decls (c_sysary, etc.) */
#include "slv_cbksub.h"       /* ev_*, am_*, cm_*, sn_* enums                  */
#include "slv_cbksub_util.h"  /* get_event_name() and friends (optional)        */

adams_c_Callback  Cbksub;     /* forward declaration — enables compiler type-checking */

void Cbksub( const struct sAdamsCbksub *cbk, double time, int event, int *data )
{
    switch ( event )
    {
        case ev_INITIALIZE:
            /* One-time setup */
            break;

        case ev_TERMINATE:
            /* Cleanup; data[0] = solver exit status */
            break;

        case ev_ITERATION_BEG:
            /* data[0] = sim mode (am_DYNAMICS, etc.)   */
            /* data[1] = analysis mode                  */
            /* data[2] = 1 if Jacobian pass             */
            /* Ideal place to cache SYSARY results      */
            break;

        case ev_PRIVATE_EVENT1:
        case ev_PRIVATE_EVENT2:
            return;     /* MUST ignore — never read data[] */

        default:
            break;
    }
}
```

Model file:
```
CBKSUB/1
, FUNCTION=USER(1.0, 2.0)\
, ROUTINE=my_dll:Cbksub
```

See [assets/c_subroutines/cbksub_template.c](assets/c_subroutines/cbksub_template.c) for a complete compilable template.

---

## VFOSUB Quick Start (C) — with CBKSUB caching

```c
#include "slv_cbksub_util.h"   /* c_sysary, c_errmes */

/* Shared cache populated by Cbksub at ev_ITERATION_BEG */
extern double g_cached_force_x;
extern int    g_cache_valid;

void Vfosub( int *id, double *time, double *par, int *npar,
             int *dflag, int *iflag, double *result )
{
    int    ipar[3], nv, errflg;
    double states[6];

    /* Skip non-evaluation passes */
    if ( *iflag == 5 || *iflag == 7 || *iflag == 9 )
        return;

    /* Use cached value when available (not during differencing) */
    if ( *dflag == 0 && g_cache_valid )
    {
        result[0] = g_cached_force_x;
        result[1] = 0.0;
        result[2] = 0.0;
        return;
    }

    /* Fallback: compute directly (also used when dflag=1) */
    ipar[0] = 16; ipar[1] = 1; ipar[2] = 1;
    errflg  = 0;
    c_sysary( "DISP", ipar, 3, states, &nv, &errflg );
    c_errmes( &errflg, "c_sysary DISP failed in Vfosub", id, "STOP" );

    result[0] = -states[1] * 30.0;
    result[1] = 0.0;
    result[2] = 0.0;
}
```

---

## Build Commands

Adams provides the `mdi` tool to compile and link user subroutines. Do NOT use raw `cl` or `gcc` commands.

### Agent compilation (default behaviour)

After presenting code for the user to review, **offer to compile it**. Do not just show build instructions — run the build. On Windows:

1. If `%LOCALAPPDATA%\adams_env_init.bat` does not exist, generate it first:
   ```cmd
   python scripts/generate_adams_env.py
   ```
2. Initialize the environment and compile:
   ```cmd
   call "%LOCALAPPDATA%\adams_env_init.bat"
   mdi.bat cr-u n <source files> -n <output>.dll ex
   ```

### If agent compilation fails

Only if the above fails, tell the user to build manually:
1. Open **Start Menu → Adams \<version\> → Command Prompt** (runs `AdamsSetup.bat` automatically)
2. `cd` to the directory containing the source files
3. Run `adamsXXXX cr-u n <source files> -n <output>.dll ex`

### Linux
```bash
mdi -c cr-u n cbksub.c vfosub.c -n my_sub.so ex
```

The flags mean: `cr-u` = create user library, `n` = no debug, `-n` = output name, `ex` = exit.

See [references/build.md](references/build.md) for more detail and troubleshooting.

---

## Key Reference Files

| Topic | File |
|-------|------|
| CBKSUB events, data[], forbidden calls, Fortran example | [references/c_subroutines/cbksub.md](references/c_subroutines/cbksub.md) |
| SYSARY, SYSFNC, ERRMES, RCNVRT, SYSPAR | [references/utility_functions.md](references/utility_functions.md) |
| Build commands, DLL export, CMake | [references/build.md](references/build.md) |
| Complete C template (annotated starter) | [assets/c_subroutines/cbksub_template.c](assets/c_subroutines/cbksub_template.c) |

### SDK Headers (canonical — use these for correct signatures and enum values)

If the user's project does not already contain `slv_c_utils.h`, `slv_cbksub.h`, or `slv_cbksub_util.h`, copy the needed headers from this skill's [references/sdk_headers/](references/sdk_headers/) folder into the user's source directory before compiling.

| File | Contents |
|------|----------|
| [references/sdk_headers/slv_c_utils.h](references/sdk_headers/slv_c_utils.h) | All subroutine structs (`sAdamsVforce`, `sAdamsGforce`, etc.), all `adams_c_*` typedefs, all utility function declarations (`c_sysary`, `c_sysfnc`, `c_errmes`, `c_rcnvrt`, etc.) |
| [references/sdk_headers/slv_cbksub.h](references/sdk_headers/slv_cbksub.h) | All CBKSUB enums: `EVENT_TYPE` (`ev_*`), `ANALYSIS_MODE` (`am_*`), `COMMAND_IDENTIFIER` (`cm_*`), `SENSOR_TYPE` (`sn_*`) |
| [references/sdk_headers/slv_cbksub_util.h](references/sdk_headers/slv_cbksub_util.h) | Helper functions: `get_event_name()`, `get_simulation_analysis_mode()`, `get_command_name()`, `get_sensor_type()` |

### SDK Example Files (from Adams 2023.1 installation)

All located in [assets/c_subroutines/examples/](assets/c_subroutines/examples/). Each file shows the correct C signature, struct usage, and `adams_c_*` forward-declaration pattern for its subroutine type.

| File | Subroutine | Key struct |
|------|-----------|-----------|
| `cbksub.c` | CBKSUB lifecycle callback | `sAdamsCbksub` |
| `vfosub.c` | VFORCE vector force | `sAdamsVforce` |
| `gfosub.c` | GFORCE general force (6-DOF) | `sAdamsGforce` |
| `sfosub.c` | SFORCE scalar force | `sAdamsSforce` |
| `difsub.c` | DIFF differential equation | `sAdamsDiff` |
| `varsub.c` | VARIABLE element | `sAdamsVariable` |
| `reqsub.c` | REQUEST output | `sAdamsRequest` |
| `motsub.c` | MOTION prescribed motion | `sAdamsMotion` |
| `cursub.c` | CURVE parametric curve | `sAdamsCurve` |
| `sursub.c` | SURFACE parametric surface | `sAdamsSurface` |
| `consub.c` | CONTROL subroutine | `sAdamsControl` |
| `cffsub.c` | Contact friction force | `sAdamsContactFriction` |
| `cnfsub.c` | Contact normal force | `sAdamsContactFriction` |
| `sensub.c` | SENSOR evaluation | `sAdamsSensor` |
| `sevsub.c` | SENSOR event | `sAdamsSensor` |
| `fiesub.c` | FIELD force element | `sAdamsField` |
| `dmpsub.c` | Flex body damping ratio | `sAdamsCratio` |
| `mfosub.c` / `mfosub2.c` | Modal force | `sAdamsMforce` |
| `gse_deriv.c` / `gse_output.c` / `gse_samp.c` / `gse_update.c` | GSE state equations | `sAdamsGSE` |
| `spline_read.c` | SPLINE data reader | `sAdamsSpline` |
| `vtosub.c` | VTORQUE vector torque | `sAdamsVtorque` |

---

## Version Check

Before starting work, check whether this skill is up to date:

1. Read `metadata.version` from this file's YAML frontmatter — that is the **installed version**.
2. Fetch `https://api.github.com/repos/bthornton191/adams_skills/releases/latest` and read the `tag_name` field (strip the leading `v` to get the **latest version**).
3. If the latest version is newer than the installed version, show this notice:

> **Update available:** adams-subroutine-writer **{latest version}** is available (you have **{installed version}**).
> Upgrade with:
> ```powershell
> [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
> $url = "https://github.com/bthornton191/adams_skills/releases/latest/download/adams-subroutine-writer.zip"
> $zip = "$env:TEMP\adams-subroutine-writer.zip"
> Invoke-WebRequest $url -OutFile $zip
> Expand-Archive $zip "$env:USERPROFILE\.vscode\skills" -Force
> Remove-Item $zip
> ```

4. If the fetch fails (network error, timeout, etc.), **silently continue** — do not warn the user.

---

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Using `event == 4` instead of `event == ev_ITERATION_BEG` | Always use `ev_*` constants |
| Reading `data[]` inside `ev_PRIVATE_EVENT1` or `ev_PRIVATE_EVENT2` | Always return immediately for these events |
| Calling VFOSUB from within CBKSUB | Not allowed — CBKSUB cannot call other user subroutines |
| Skipping SYSARY call when `iflag == 3` | Must make same SYSARY calls during dependency mapping |
| C++ CBKSUB without `extern "C"` | Always required for C++ |
| Using Euler angle degrees | All RCNVRT angles are in radians |
| Assuming `cbk` is non-NULL on ev_INITIALIZE | `cbk` is NULL on ev_INITIALIZE and ev_TERMINATE |
