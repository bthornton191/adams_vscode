# STEP — Cubic Polynomial Step

Returns a smooth cubic polynomial transition from one value to another over a specified range of an independent variable.

## Format

```
STEP(x, x0, h0, x1, h1)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable (usually `TIME` or a displacement expression) |
| `x0` | Required | Value of `x` at which the step begins |
| `h0` | Required | Value of the function at `x0` (initial value) |
| `x1` | Required | Value of `x` at which the step ends |
| `h1` | Required | Value of the function at `x1` (final value) |

**Behavior:**
- When `x ≤ x0`: returns `h0`
- When `x ≥ x1`: returns `h1`
- In between: cubic polynomial that satisfies the boundary values

**Continuity:** The function is continuous with a continuous **1st derivative** (slope is zero at both endpoints). The **2nd derivative is discontinuous** at `x0` and `x1`.

> If continuity of the 2nd derivative is required, use `STEP5` instead.

## Examples

```adams_fn
! Ramp force from 0 to 500 N over the first second of simulation
STEP(TIME, 0.0, 0.0, 1.0, 500.0)

! Ramp with non-zero start value: goes from 100 to 800 between t=0.5 and t=2.0
STEP(TIME, 0.5, 100.0, 2.0, 800.0)

! Use a displacement as the independent variable:
! spring preload kicks in as DZ goes from 5 to 0 mm
STEP(DZ(.MODEL.PISTON.CM, .MODEL.ground.REF), 5.0, 0.0, 0.0, 1000.0)
```

## In context (Adams CMD)

```cmd
force create body_force single_component_force &
    force_name = .MODEL.RAMP_FORCE &
    adams_id = 1 &
    i_marker_name = .MODEL.BODY.CM &
    j_floating_marker = .MODEL.BODY.CM &
    action_only = on &
    function = "STEP(TIME, 0.0, 0.0, 1.0, 500.0)"
```

## See also

- [STEP5](step5.md) — smoother (quintic) version with continuous 2nd derivative
- [HAVSIN](havsin.md) — haversine-based alternative
- [IF](if.md) — avoid; causes hard derivative discontinuities
