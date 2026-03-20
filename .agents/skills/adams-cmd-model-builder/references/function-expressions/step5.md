# STEP5 — Quintic Polynomial Step

Returns a smooth quintic polynomial transition from one value to another. Like `STEP`, but with a continuous 2nd derivative — the smoothest option for ramp-up inputs.

## Format

```
STEP5(x, x0, h0, x1, h1)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable (usually `TIME`) |
| `x0` | Required | Value of `x` at which the step begins |
| `h0` | Required | Value of the function at `x0` (initial value) |
| `x1` | Required | Value of `x` at which the step ends |
| `h1` | Required | Value of the function at `x1` (final value) |

**Behavior:**
- When `x ≤ x0`: returns `h0`
- When `x ≥ x1`: returns `h1`
- In between: quintic polynomial with zero slope **and** zero curvature at both endpoints

**Continuity:** The function is continuous with continuous **1st and 2nd derivatives** (both are zero at the endpoints). The **3rd derivative is discontinuous** at `x0` and `x1`.

> Choose `STEP5` over `STEP` when the input feeds into a force that will be differentiated (e.g., a stiffness-dependent force), or when simulation convergence is sensitive to high-order derivative continuity.

## Examples

```adams_fn
! Quintic ramp-up of a force
STEP5(TIME, 0.0, 0.0, 1.5, 1000.0)

! Same range and values as STEP but smoother profile
STEP5(TIME, 0.5, 0.0, 2.0, 250.0)
```

## Comparison: STEP vs STEP5

| Property | STEP | STEP5 |
|----------|------|-------|
| Polynomial degree | Cubic (3rd) | Quintic (5th) |
| 1st derivative continuous | ✅ Yes | ✅ Yes |
| 2nd derivative continuous | ❌ No | ✅ Yes |
| Typical use | Standard ramps | Smoother ramps, fewer convergence issues |

## See also

- [STEP](step.md) — simpler cubic version
- [HAVSIN](havsin.md) — haversine alternative (also very smooth)
