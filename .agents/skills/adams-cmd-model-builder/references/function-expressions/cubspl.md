# CUBSPL — Cubic Spline Interpolation

Evaluates a cubic spline defined by a `data_element create spline` entity. The cubic spline is fitted globally (all data points influence the fit), giving smooth results but potentially oscillating when data contains irregularities or sparse regions.

## Format

```
CUBSPL(First Ind Var, Second Ind Var, Spline Name, Derivative Order)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `First Ind Var` | Required | Value of the first (x) independent variable for lookup |
| `Second Ind Var` | Required | Value of the second (z) independent variable; use `0` for a 1D spline |
| `Spline Name` | Required | Object name of an existing `data_element spline` entity |
| `Derivative Order` | Required | `0` = function value, `1` = first derivative, `2` = second derivative |

## Spline data element

```cmd
data_element create spline &
    spline_name = .MODEL.MY_SPLINE &
    adams_id = 1 &
    x = 0.0, 10.0, 20.0, 30.0 &
    y = 0.0, 8.0, 15.0, 10.0
```

## Examples

```adams_fn
! Evaluate spline at current time
CUBSPL(TIME, 0, .MODEL.INPUT_SPL, 0)

! First derivative of the spline
CUBSPL(TIME, 0, .MODEL.INPUT_SPL, 1)
```

## AKISPL vs CUBSPL

| Property | AKISPL | CUBSPL |
|----------|--------|--------|
| Fitting method | Local (nearby points) | Global (all points) |
| Oscillation with irregular data | Less | More |
| Smoothness | Very good | Excellent (globally 2nd-order continuous) |
| Best for | Experimental/measured data | Smooth analytical curves |

## See also

- [AKISPL](akispl.md) — Akima spline, better for non-uniform data spacing
