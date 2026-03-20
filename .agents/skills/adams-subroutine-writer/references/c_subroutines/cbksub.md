# CBKSUB — Adams Solver Simulation Lifecycle Callback

## Purpose

CBKSUB is the simulation lifecycle callback subroutine. Adams calls it at specific points during a simulation (events), letting your code react to solver state changes, cache computed values, or clean up resources. It is the correct place to cache expensive SYSARY/SYSFNC results so that other user subroutines (e.g., VFOSUB) can reuse them without triggering extra solver evaluations.

---

## Function Signatures

### C (mdi_cbksub.dll target)
```c
#include "slv_c_utils.h"      /* all structs, c_sysary, c_errmes, c_usrmes, etc. */
#include "slv_cbksub.h"       /* ev_*, am_*, cm_*, sn_* enums                     */
#include "slv_cbksub_util.h"  /* get_event_name() helper — optional              */

adams_c_Callback  Cbksub;    /* forward declaration for compiler type-checking */

void Cbksub( const struct sAdamsCbksub *cbk, double time, int event, int *data )
```

### C++ (must be extern "C")
```cpp
#include "slv_c_utils.h"
#include "slv_cbksub.h"
#include "slv_cbksub_util.h"

extern "C" void Cbksub( const struct sAdamsCbksub *cbk, double time, int event, int *data )
```

### Fortran
```fortran
SUBROUTINE CBKSUB ( time, event, data )
  include 'slv_cbksub.inc'
  include 'slv_cbksub_util.inc'   ! optional utility routines
  DOUBLE PRECISION time
  INTEGER event, data(3)
```

---

## `sAdamsCbksub` Struct (C/C++ only)

```c
struct sAdamsCbksub {
    int ID;            /* CBKSUB element ID from the Adams dataset file  */
    int NPAR;          /* number of USER() parameters                    */
    const double* PAR; /* array of USER() parameter values               */
    void *reserved;    /* internal — do not use                          */
};
```

In Fortran, these are available via common-block variables from `slv_cbksub.inc`: `CBKID`, `NPAR`, `PAR(MAXPAR)`.

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `cbk` | `const struct sAdamsCbksub *` | Element metadata; NULL on ev_INITIALIZE and ev_TERMINATE |
| `time` | `double` | Current simulation time (seconds). Undefined during ev_INITIALIZE. |
| `event` | `int` | Event identifier — use enum constants from `slv_cbksub.h` (never raw integers) |
| `data` | `int[3]` | Event-specific payload; see table below |

> **Critical:** Always use the symbolic constants (`ev_*`, `am_*`, `sn_*`, `cm_*`) from the include files — never raw integer literals. Numeric values can change between Adams releases.

---

## Complete Event Reference

### Group 1: Session lifecycle

| Event | Name | data[0] | data[1] | data[2] |
|-------|------|---------|---------|---------|
| 1 | `ev_INITIALIZE` | undefined | undefined | undefined |
| 2 | `ev_TERMINATE` | solver exit status | undefined | undefined |
| 33 | `ev_SAVE_BEG` | undefined | undefined | undefined |
| 34 | `ev_SAVE_END` | undefined | undefined | undefined |
| 35 | `ev_RELOAD_BEG` | undefined | undefined | undefined |
| 36 | `ev_RELOAD_END` | undefined | undefined | undefined |
| 37 | `ev_TRAN_SIM_BEG` | undefined | undefined | undefined |
| 38 | `ev_TRAN_SIM_END` | undefined | undefined | undefined |
| 13 | `ev_MODEL_INPUT_BEG` | undefined | undefined | undefined |
| 14 | `ev_MODEL_INPUT_END` | undefined | undefined | undefined |
| 40 | `ev_MODEL_CHANGE` | undefined | undefined | undefined |

### Group 2: Analysis phase lifecycle (data[0]=sim mode, data[1]=analysis mode)

| Event | Name | data[2] note |
|-------|------|-------------|
| 15 | `ev_DIS_IC_BEG` | ignored |
| 16 | `ev_DIS_IC_END` | ignored |
| 17 | `ev_VEL_IC_BEG` | ignored |
| 18 | `ev_VEL_IC_END` | ignored |
| 19 | `ev_ACC_IC_BEG` | ignored |
| 20 | `ev_ACC_IC_END` | ignored |
| 21 | `ev_STATICS_BEG` | ignored |
| 22 | `ev_STATICS_END` | 0=converged, 1=failed |
| 23 | `ev_STEADY_STATE_BEG` | ignored |
| 24 | `ev_STEADY_STATE_END` | ignored |
| 25 | `ev_KINEMATICS_BEG` | ignored |
| 26 | `ev_KINEMATICS_END` | ignored |
| 27 | `ev_DYNAMICS_BEG` | ignored |
| 28 | `ev_DYNAMICS_END` | ignored |
| 29 | `ev_LINEAR_BEG` | ignored |
| 30 | `ev_LINEAR_END` | ignored |
| 31 | `ev_QSTATICS_BEG` | ignored |
| 32 | `ev_QSTATICS_END` | ignored |

### Group 3: Step and iteration lifecycle (data[0]=sim mode, data[1]=analysis mode)

| Event | Name | data[2] note |
|-------|------|-------------|
| 4 | `ev_ITERATION_BEG` | 1=Jacobian/partial derivative requested, 0=no |
| 5 | `ev_ITERATION_END` | ignored |
| 6 | `ev_BODY_ROTATION` | ignored |
| 7 | `ev_OUTPUT_STEP_REQ` | ignored |
| 8 | `ev_OUTPUT_STEP_BEG` | ignored |
| 9 | `ev_OUTPUT_STEP_END` | ignored |
| 10 | `ev_TIME_STEP_BEG` | ignored |
| 11 | `ev_TIME_STEP_FAILED` | ignored |
| 12 | `ev_TIME_STEP_END` | ignored |
| 41 | `ev_FORCE_RECONC_BEG` | ignored |
| 42 | `ev_FORCE_RECONC_END` | ignored |

### Group 4: Special events

| Event | Name | data[0] | data[1] | data[2] |
|-------|------|---------|---------|---------|
| 3 | `ev_SENSOR` | sensor element ID | sensor action type (`sn_*`) | ignored |
| 39 | `ev_COMMAND` | command identifier (`cm_*`) | 1=issued from CONSUB, 0=other | undefined |

### Group 5: MUST IGNORE — internal solver events

| Event | Name | Action |
|-------|------|--------|
| 43 | `ev_PRIVATE_EVENT1` | **Always ignore — never read data[]** |
| 44 | `ev_PRIVATE_EVENT2` | **Always ignore — never read data[]** |

---

## Simulation Mode Constants (`am_*`)

Used in `data[0]` (sim mode) and `data[1]` (analysis mode) for most events.

| Value | Constant | Description |
|-------|----------|-------------|
| 0 | `am_NULL` | Mode not yet established |
| 1 | `am_KINEMATICS` | Kinematics analysis |
| 2 | `am_RESERVED` | Reserved (do not use) |
| 3 | `am_INITIAL_CONDITIONS` | Initial conditions computation |
| 4 | `am_DYNAMICS` | Transient dynamics |
| 5 | `am_STATICS` | Static equilibrium |
| 6 | `am_QUASI_STATICS` | Quasi-static |
| 7 | `am_LINEAR` | Linear/eigenvalue analysis |
| 8 | `am_STEADY_STATE` | Steady-state |
| 9 | `am_COMPLIANCE` | Compliance analysis |

---

## Sensor Type Constants (`sn_*`) — for `ev_SENSOR`

| Value | Constant | Description |
|-------|----------|-------------|
| 1 | `sn_CODGEN` | Code generation sensor |
| 2 | `sn_DT` | Step size change |
| 3 | `sn_HALT` | Halt simulation |
| 4 | `sn_PRINT` | Print output |
| 5 | `sn_RESTART` | Restart simulation |
| 6 | `sn_RETURN` | Return to calling program |
| 7 | `sn_STEPSIZE` | Adjust step size |
| 8 | `sn_YYDUMP` | State dump |
| 9 | `sn_EVALUATE` | User evaluate |

> A SENSOR element must have an action (e.g., HALT) assigned, otherwise no `ev_SENSOR` event is fired.

---

## Command Constants (`cm_*`) — key values for `ev_COMMAND`

| Value | Constant | Corresponding Adams command |
|-------|----------|----------------------------|
| 1 | `cm_ACCGRAV` | ACCGRAV |
| 29 | `cm_KINEMATICS` | KINEMATICS |
| 43 | `cm_SAVE` | SAVE |
| 47 | `cm_SIMULATE` | SIMULATE |
| 50 | `cm_STOP` | STOP |
| 56 | `cm_WSTIFF` | WSTIFF |

The full enumeration (cm_ACCGRAV=1 through cm_WSTIFF=56) is defined in `slv_cbksub.h` / `slv_cbksub.inc`.

---

## Constraints and Forbidden Calls

CBKSUB **cannot** call any of the following user subroutines (doing so causes undefined behavior or a crash):

```
CFFSUB, CNFSUB, CONSUB, COUSUB, COUXX, COUXX2, CURSUB, DIFSUB, DMPSUB,
FIESUB, GFOSUB, GSE_DERIV, GSE_UPDATE, GSE_OUTPUT, GSE_SAMP, MFSUB,
MOTSUB, RELSUB, REQSUB, SAVSUB, SENSUB, SEVSUB, SFOSUB, SPLINE_READ,
SURSUB, TIRSUB, VARSUB, VFOSUB, VTOSUB
```

CBKSUB **cannot** call these utility routines:

```
ADAMS_DECLARE_THREADSAFE, ANALYS, DATOUT, GTCMAT, MODIFY, PUT_SPLINE, UCOVAR
```

CBKSUB **can** call SYSARY, SYSFNC, ERRMES, RCNVRT — but note that dependency registration does **not** occur when called from CBKSUB (no Jacobian coupling). This is intentional for the caching use case.

---

## Caching Pattern (Primary CBKSUB Use Case)

The most common use of CBKSUB is to cache solver state at `ev_ITERATION_BEG` so that other user subroutines (VFOSUB, GFOSUB, etc.) can reuse the cached value without making redundant SYSARY calls.

### C caching pattern

```c
#include "slv_cbksub.h"
#include "slv_cbksub_util.h"

/* Shared state — use a file-scope struct or global */
static struct {
    double force_x;
    int    valid;
} g_cache;

void Cbksub( const struct sAdamsCbksub *cbk, double time, int event, int *data )
{
    int    ipar[3], nv;
    double states[6];
    int    errflg = 0;

    g_cache.valid = 0;

    if ( event == ev_ITERATION_BEG )
    {
        ipar[0] = 16;   /* marker ID */
        ipar[1] = 1;    /* reference marker ID */
        ipar[2] = 1;    /* result marker ID */

        c_sysary( "DISP", ipar, 3, states, &nv, &errflg );
        if ( errflg ) return;

        g_cache.force_x = -states[1] * 30.0;
        g_cache.valid   = 1;
    }
}
```

Then in VFOSUB (or any other subroutine):
```c
/* Access g_cache.force_x if g_cache.valid, else compute directly */
```

### Fortran caching pattern (complete example from Adams docs)

This example shows the full pattern: a `VFOSUB` that falls back to a direct SYSARY call when not differencing, and a `CBKSUB` that caches the result at `ev_ITERATION_BEG`.

```fortran
! ---------------------------------------------------------------
! File-level: must appear before any SUBROUTINE keyword
include 'slv_cbksub_util.inc'

! ---------------------------------------------------------------
! VFOSUB — vector force subroutine that uses cached value
SUBROUTINE VFOSUB ( id, time, par, npar, dflag, iflag, result )
  IMPLICIT NONE
  INTEGER          id
  DOUBLE PRECISION time
  DOUBLE PRECISION par(*)
  INTEGER          npar
  LOGICAL          dflag
  INTEGER          iflag
  DOUBLE PRECISION result(3)

  LOGICAL          errflg
  INTEGER          IPAR(3), NV
  DOUBLE PRECISION DATINF(6)
  INTEGER          FLAG
  DOUBLE PRECISION VALUE
  COMMON / FORCES / VALUE, FLAG

  ! When differencing or cache is stale, compute directly
  IF ( dflag .EQ. .TRUE. .OR. FLAG .EQ. 0 ) THEN
    errflg    = .FALSE.
    IPAR(1)   = 16
    IPAR(2)   = 1
    IPAR(3)   = 1
    CALL SYSARY( 'DISP', IPAR, 3, DATINF, NV, errflg )
    IF ( errflg ) CALL STOPERR( 101, 'Error in SYSARY' )
    result(1) = -DATINF(2) * 30
    result(2) = 0.0D0
    result(3) = 0.0D0
    RETURN
  END IF

  result(1) = VALUE
  result(2) = 0.0D0
  result(3) = 0.0D0
  RETURN
END

! ---------------------------------------------------------------
! CBKSUB — caches SYSARY result at ev_ITERATION_BEG
SUBROUTINE CBKSUB ( time, event, data )
  include 'slv_cbksub.inc'
  DOUBLE PRECISION time
  INTEGER          event, data(3)

  INTEGER          FLAG
  DOUBLE PRECISION VALUE
  COMMON / FORCES / VALUE, FLAG

  FLAG = 0

  IF ( event .EQ. ev_ITERATION_BEG ) THEN
    FLAG      = 1
    IPAR(1)   = 16
    IPAR(2)   = 1
    IPAR(3)   = 1
    CALL SYSARY( 'DISP', IPAR, 3, DATINF, NV, ERRFLG )
    VALUE = -DATINF(2) * 30
  END IF

  RETURN
END
```

---

## Adams Dataset File (`.adm`) Syntax

```
CBKSUB/1
, FUNCTION=USER(param1, param2)\
, ROUTINE=user_sub:Cbksub
```

- `ROUTINE=` points to `<dll_name>:<function_name>`
- `USER()` parameters populate `cbk->PAR[0]`, `cbk->PAR[1]`, ... (0-indexed in C)

---

## Include Files

| Language | Required | Optional utility |
|----------|----------|-----------------|
| C | `slv_c_utils.h` + `slv_cbksub.h` | `slv_cbksub_util.h` |
| C++ | `slv_c_utils.h` + `slv_cbksub.h` | `slv_cbksub_util.h` |
| Fortran | `slv_cbksub.inc` | `slv_cbksub_util.inc` |

> **Note:** `slv_c_utils.h` includes `slv_cbksub.h` implicitly via the `sAdamsCbksub` struct definition, but include both explicitly for clarity. `slv_c_utils.h` also declares all utility functions (`c_sysary`, `c_errmes`, `c_usrmes`, `c_rcnvrt`, etc.) and defines the `adams_c_Callback` typedef used for the forward declaration.

Location: `%ADAMS_INSTALL%\solver\c_usersubs\` (bundled in Adams install) or `%ADAMS_SDK%\sdk\include\` (SDK distribution)
