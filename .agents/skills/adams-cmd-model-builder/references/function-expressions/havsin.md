# HAVSIN — Haversine Step

Returns a smooth haversine-based transition from one value to another. Produces slightly larger intermediate derivatives than `STEP` or `STEP5` but is otherwise very smooth.

## Format

```
HAVSIN(x, Begin At, End At, Initial Function Value, Final Function Value)
```

> **Argument order:** Note that `Begin At` and `End At` (the transition range) come **before** the initial and final values. This differs from `STEP` and `STEP5`.

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable (usually `TIME`) |
| `Begin At` | Required | Value of `x` at which the transition begins |
| `End At` | Required | Value of `x` at which the transition ends |
| `Initial Function Value` | Required | Value returned when `x ≤ Begin At` |
| `Final Function Value` | Required | Value returned when `x ≥ End At` |

**Behavior:**
- When `x ≤ Begin At`: returns `Initial Function Value`
- When `x ≥ End At`: returns `Final Function Value`
- In between: haversine (1 - cos) interpolation

## Examples

```adams_fn
! Haversine ramp from 0 to 500 over the first second
HAVSIN(TIME, 0.0, 1.0, 0.0, 500.0)

! Note argument order: (x, begin, end, initial, final)
! NOT: HAVSIN(TIME, 0.0, 500.0, 0.0, 1.0)  ← wrong
```

## Comparison with STEP/STEP5

| Property | STEP | STEP5 | HAVSIN |
|----------|------|-------|--------|
| Polynomial? | Cubic | Quintic | Trigonometric (haversine) |
| Zero slope at endpoints | ✅ | ✅ | ✅ |
| Zero curvature at endpoints | ❌ | ✅ | ❌ |
| Peak intermediate derivative | Moderate | Lowest | Slightly higher than STEP |

## See also

- [STEP](step.md) — cubic polynomial step
- [STEP5](step5.md) — quintic polynomial step (smoothest derivatives)
