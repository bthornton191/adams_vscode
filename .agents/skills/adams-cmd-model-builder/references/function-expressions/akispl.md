# AKISPL — Akima Spline Interpolation

Evaluates an Akima spline defined by a `data_element create spline` entity. Akima splines use local fitting (each segment uses only nearby data points), giving better local smoothness and less oscillation than global cubic splines when data has irregularities.

## Format

```
AKISPL(First Ind Var, Second Ind Var, Spline Name, Derivative Order)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `First Ind Var` | Required | Value of the first (x) independent variable for lookup |
| `Second Ind Var` | Required | Value of the second (z) independent variable; use `0` for a 1D spline |
| `Spline Name` | Required | Object name of an existing `data_element spline` entity |
| `Derivative Order` | Required | `0` = function value, `1` = first derivative, `2` = second derivative |

## Spline data element

The spline must be defined before use:

```cmd
data_element create spline &
    spline_name = .MODEL.MY_SPLINE &
    adams_id = 1 &
    x = 0.0, 10.0, 20.0, 30.0, 40.0 &
    y = 0.0, 5.2, 9.8, 12.1, 11.5
```

## Examples

```adams_fn
! Look up function value at current DX displacement
AKISPL(DX(.MODEL.BODY.CM, .MODEL.ground.REF), 0, .MODEL.FORCE_SPL, 0)

! First derivative at current time
AKISPL(TIME, 0, .MODEL.INPUT_SPL, 1)

! 2D spline: x = displacement, z = temperature variable
AKISPL(DX(.MODEL.PART.M1, .MODEL.ground.BASE), VARVAL(.MODEL.TEMP), .MODEL.MAP_SPL, 0)
```

## In context (Adams CMD)

```cmd
! Define the spline
data_element create spline &
    spline_name = .MODEL.FORCE_CURVE &
    adams_id = 10 &
    x = 0.0, 5.0, 10.0, 20.0, 30.0 &
    y = 0.0, 100.0, 350.0, 600.0, 500.0

! Use it in a force
force create body_force single_component_force &
    force_name = .MODEL.CAM_FORCE &
    adams_id = 11 &
    i_marker_name = .MODEL.FOLLOWER.CM &
    j_floating_marker = .MODEL.FOLLOWER.CM &
    action_only = on &
    function = "AKISPL(DZ(.MODEL.FOLLOWER.CM, .MODEL.ground.CAM_REF), &
                       0, .MODEL.FORCE_CURVE, 0)"
```

## See also

- [CUBSPL](cubspl.md) — global cubic spline (smoother overall, but can oscillate with irregular data)
