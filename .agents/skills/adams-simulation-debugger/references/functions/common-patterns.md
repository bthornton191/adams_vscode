# Functions: Common Patterns and Gotchas

> Quick reference table of frequently used expression patterns.

## Force & Spring Expressions

| Intent | Expression |
|--------|-----------|
| Spring force from distance | `-K*(DM(i,j) - L0)` |
| Spring-damper (radial) | `-K*(DM(i,j)-L0) - C*VR(i,j)` |
| Spring along Z-axis | `-K*(DZ(i,j,j) - L0) - C*VZ(i,j,j,j)` |
| One-sided contact impact | `IMPACT(DZ(i,j,j), VZ(i,j,j,j), gap, 1e5, 2.2, 100, 0.1)` |
| Two-sided stop | `BISTOP(DX(i,j,j), VX(i,j,j,j), x_lo, x_hi, 1e5, 2.2, 100, 0.1)` |

## Motion & Velocity Expressions

| Intent | Expression |
|--------|-----------|
| Smooth velocity ramp | `STEP(TIME, t0, 0, t1, v_final)` |
| Smooth displacement ramp | `STEP5(TIME, t0, 0, t1, d_final)` |
| Constant angular velocity (rad/s) | `omega * TIME` |
| Look up angle from spline | `AKISPL(TIME, 0, spline_id)` |

## Angle and Orientation

| Intent | Expression |
|--------|-----------|
| Single-axis angle (no wrapping) | `AZ(i, j)` |
| Unwrap to (−π, π] | `MOD(AZ(i,j)+PI, 2*PI)-PI` |
| Convert output to degrees | `AZ(i,j)*RTOD` |
| Convert degrees constant | `45*DTOR` |

## System Queries

| Intent | Expression |
|--------|-----------|
| Read VARIABLE/5 | `VARVAL(5)` |
| Read ARRAY/3 element 2 | `ARYVAL(3, 2)` |
| Read DIFF/10 state | `DIF(10)` |
| Apply force in dynamics only | `IF(MODE-4 : 0, 0, force_expr)` |
| Power integral | `DIFF/1, FUNCTION=SFORCE(id,0,1,0)*VR(i,j)` → `DIF(1)` |

## Measurement

| Intent | Expression |
|--------|-----------|
| Distance between two points | `DM(mkr_i, mkr_j)` |
| Relative velocity (radial) | `VR(mkr_i, mkr_j)` |
| Revolute joint reaction force | `JOINT(jnt_id, 0, 1, ref_mkr)` |
| Spring-damper force output | `SPDP(sd_id, 0, 1, 0)` |
| Contact normal force | `CONTACT(ct_id, 0, 1, 0)` |

---

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `IF(...)` causes HMIN | Discontinuous branch transition | Replace with `STEP` or `STEP5` |
| Large DM spike at t=0 | Markers on overlapping parts | Check initial geometry; use IMPACT not CONTACT |
| AKISPL extrapolation error | Data range too narrow | Extend spline data ±10% beyond simulation range |
| AZ wraps at ±π | Full rotation crosses ±180° | Use `MOD(AZ(i,j)+PI,2*PI)-PI` to unwrap |
| VR positive when compressing | VR = d/dt(distance) — positive = separating | Use `-C*VR(i,j)` for damping (restoring force = negative) |
| FRICTION function unavailable | Accessible only from REQUEST/SENSOR | Check expression location |
| NFORCE inaccessible in subroutine | C++ NFORCE not in SYSFNC | Use REQUEST wrapper to capture NFORCE value |
