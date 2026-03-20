# Utility Functions Reference

Core utility functions callable from Adams user subroutines. All are available in C, C++, and Fortran. Function names shown are Fortran/C mixed-case names; C wrappers are prefixed with `c_` (e.g., `c_sysary`, `c_sysfnc`, `c_errmes`).

---

## SYSARY — Retrieve Array of Solver State Variables

Returns multiple state values in a single call. Preferred over SYSFNC when you need several related components (e.g., all 6 displacement components).

### Fortran
```fortran
CALL SYSARY ( fncnam, ipar, nsize, states, nstates, errflg )
```

### C
```c
#include "slv_cbksub_util.h"   /* or the subroutine-specific util header */

c_sysary( fncnam, ipar, nsize, states, nstates, &errflg );
```

### Parameters

| Parameter | Fortran type | C type | Description |
|-----------|-------------|--------|-------------|
| `fncnam` | `CHARACTER*(*) IN` | `const char *` | State type string (see table below) |
| `ipar` | `INTEGER IN` | `const int *` | Parameter array (marker IDs, etc.) |
| `nsize` | `INTEGER IN` | `int` | Number of elements in `ipar` |
| `states` | `DOUBLE PRECISION OUT` | `double *` | Output array of state values |
| `nstates` | `INTEGER OUT` | `int *` | Number of values returned |
| `errflg` | `LOGICAL OUT` | `int *` (0=ok, 1=error) | Error flag |

### `fncnam` Values

| Name | `ipar` contents | `nstates` | Description |
|------|-----------------|-----------|-------------|
| `'DISP'` | [marker_i, marker_j, marker_k] | 6 | Displacement (tx,ty,tz,rx,ry,rz) |
| `'TDISP'` | [marker_i, marker_j, marker_k] | 3 | Translational displacement only |
| `'RDISP'` | [marker_i, marker_j] | 3 | Rotational displacement (Euler angles) |
| `'Q'` | [body_id] | NMODES | Flexible body modal coordinates |
| `'UVX'` | [marker_i, marker_j] | 3 | X-axis unit vector of marker_i in marker_j frame |
| `'UVY'` | [marker_i, marker_j] | 3 | Y-axis unit vector |
| `'UVZ'` | [marker_i, marker_j] | 3 | Z-axis unit vector |
| `'DC'` | [marker_i, marker_j] | 9 | Direction cosine matrix (3×3, row order) |
| `'VEL'` | [marker_i, marker_j, marker_k, marker_l] | 6 | Velocity (vx,vy,vz,wx,wy,wz) |
| `'TVEL'` | [marker_i, marker_j, marker_k, marker_l] | 3 | Translational velocity only |
| `'RVEL'` | [marker_i, marker_j, marker_k] | 3 | Rotational velocity only |
| `'QDOT'` | [body_id] | NMODES | Flexible body modal velocities |
| `'ACC'` | [marker_i, marker_j, marker_k, marker_l] | 6 | Acceleration (ax,ay,az,αx,αy,αz) |
| `'TACC'` | [marker_i, marker_j, marker_k, marker_l] | 3 | Translational acceleration |
| `'RACC'` | [marker_i, marker_j, marker_k] | 3 | Rotational acceleration |
| `'QDDOT'` | [body_id] | NMODES | Flexible body modal accelerations |
| `'FORCE'` | [element_id, marker_j, marker_k] | 6 | Force/torque (fx,fy,fz,tx,ty,tz) |
| `'TFORCE'` | [element_id, marker_j, marker_k] | 3 | Force only |
| `'RFORCE'` | [element_id, marker_j, marker_k] | 3 | Torque only |
| `'PINPUT'` | [plant_input_id] | n | Plant input values |
| `'POUTPUT'` | [plant_output_id] | n | Plant output values |
| `'ARRAY'` | [array_id] | n | ARRAY element values |
| `'FXTDISP'` | [marker_i, marker_j, marker_k] | 3 | Flexible body translational displacement |
| `'FXDC'` | [marker_i, marker_j] | 9 | Flexible body direction cosines |
| `'FXTVEL'` | [marker_i, marker_j, marker_k] | 3 | Flexible body translational velocity |
| `'FXRVEL'` | [marker_i, marker_j, marker_k] | 3 | Flexible body rotational velocity |

### `iflag` / Evaluation Mode Guard Pattern

> **Critical for Jacobian correctness:** You must make the **same** SYSARY calls during dependency-mapping passes (iflag=1 or iflag=3) as during normal evaluation. The solver uses these calls to build the Jacobian sparsity pattern. If you skip them, derivatives will be wrong.

| `iflag` | Meaning | Call SYSARY? |
|---------|---------|-------------|
| 0 | Normal force/state evaluation | Yes |
| 1 | Expression construction (C++ only) | Yes — same calls as normal |
| 3 | Dependency mapping (Jacobian sparsity) | Yes — same calls as normal |
| 5 | Expression destruction (C++ only) | **No** |
| 7 | Serialization | **No** |
| 9 | Unserialization | **No** |

```c
/* Correct guard pattern (C): */
if ( iflag == 5 || iflag == 7 || iflag == 9 )
    return;

/* Now it is safe to call c_sysary / c_sysfnc */
```

```fortran
! Fortran equivalent:
IF ( iflag .EQ. 5 .OR. iflag .EQ. 7 .OR. iflag .EQ. 9 ) RETURN
```

### Callable From

DIFSUB, GFOSUB, REQSUB, SFOSUB, VARSUB, VFOSUB, VTOSUB — and CBKSUB (no Jacobian dependency registered from CBKSUB).

---

## SYSFNC — Retrieve Single Solver State Variable

Same semantics as SYSARY but returns a single scalar value. Use SYSARY when you need several components; use SYSFNC for a single value to avoid allocating an output array.

### Fortran
```fortran
CALL SYSFNC ( fncnam, ipar, nsize, state, errflg )
```

### C
```c
c_sysfnc( fncnam, ipar, nsize, &state, &errflg );
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `fncnam` | Same name set as SYSARY |
| `ipar` | Same parameter array as SYSARY |
| `nsize` | Number of elements in `ipar` |
| `state` | Single `double` output |
| `errflg` | Error flag (same semantics as SYSARY) |

> Same `iflag` guard pattern applies as for SYSARY. The NFORCE name is only available from REQSUB/SENSUB in the Fortran solver; use FX/FY/FZ in C++.

### Callable From

CFFSUB, CNFSUB, CONSUB, DIFSUB, GFOSUB, REQSUB, SENSUB, SFOSUB, VARSUB, VFOSUB, VTOSUB — and CBKSUB.

---

## ERRMES / c_errmes — Report Errors

### Fortran
```fortran
CALL ERRMES ( errflg, mesage, id, endflg )
```

### C
```c
c_errmes( &errflg, mesage, &id, endflg );
```

### Parameters

| Parameter | Fortran type | Description |
|-----------|-------------|-------------|
| `errflg` | `LOGICAL IN` | If `.TRUE.`, write message. If `.FALSE.`, do nothing. |
| `mesage` | `CHARACTER*(*) IN` | Error text (up to 1024 chars) |
| `id` | `INTEGER IN` | Element ID for context in message |
| `endflg` | `CHARACTER*(*) IN` | `'STOP'` halts the simulation; any other value continues |

```fortran
! Typical usage:
CALL SYSARY( 'DISP', IPAR, 3, DATINF, NV, errflg )
CALL ERRMES( errflg, 'SYSARY DISP call failed in VFOSUB', id, 'STOP' )
```

```c
/* C equivalent: */
c_sysary( "DISP", ipar, 3, states, &nv, &errflg );
c_errmes( &errflg, "SYSARY DISP failed in Vfosub", &id, "STOP" );
```

### Callable From

Any user subroutine.

---

## RCNVRT — Rotation Coordinate Conversion

Converts a rotation representation from one form to another. All angle values are in **radians**.

### Fortran
```fortran
CALL RCNVRT ( sys1, coord1, sys2, coord2, istat )
```

### C
```c
c_rcnvrt( sys1, coord1, sys2, coord2, &istat );
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `sys1` | Input coordinate system name string |
| `coord1` | Input coordinate array |
| `sys2` | Output coordinate system name string |
| `coord2` | Output coordinate array |
| `istat` | Status: 0=success, non-zero=error |

### Coordinate System Names and Array Sizes

| Name | Array size | Description |
|------|-----------|-------------|
| `'EULPAR'` | 4 | Euler parameters: [P0, P1, P2, P3] where P0=cos(θ/2), [P1,P2,P3]=sin(θ/2)×axis |
| `'COSINES'` | 9 | 3×3 direction cosine matrix stored in row order |
| `'EULER'` | 3 | Body-3 (3-1-3) Euler angles in radians |
| `'BRYAN'` | 3 | Body-3 (1-2-3) Bryant angles in radians |
| `'SPACE'` | 3 | Space-fixed rotation angles in radians |
| `'RODRIGUES'` | 3 | Rodrigues parameters: R=P/P0 (undefined when P0=0, i.e., 180° rotation) |

```c
/* Convert Euler parameters to direction cosines */
double ep[4]  = { 0.7071, 0.7071, 0.0, 0.0 };  /* 90° rotation about X */
double dc[9];
int    istat;
c_rcnvrt( "EULPAR", ep, "COSINES", dc, &istat );
```

### Callable From

Any user subroutine.

---

## SYSPAR — Analytical Partial Derivatives (Advanced/Optional)

Provides analytical partial derivatives to the solver for improved Jacobian accuracy. Only needed when you want to avoid finite-differencing for your force contributions.

### Fortran
```fortran
! First check whether partials are actually needed:
CALL ADAMS_NEEDS_PARTIALS ( parflg )
IF ( parflg ) THEN
  CALL SYSPAR ( fncname, iparam, nparam, partl, npartl, errflg )
END IF
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `fncname` | Same name set as SYSARY |
| `iparam` | Same parameter array as SYSARY |
| `nparam` | Number of elements in `iparam` |
| `partl` | Output array of partial derivative values |
| `npartl` | Number of partial derivatives returned |
| `errflg` | Error flag |

> SYSPAR is optional. If not called, the solver uses finite differencing to determine Jacobian contributions from your subroutine. Only implement SYSPAR if you have verified that finite differencing is causing convergence or performance issues.
