# POLY — Standard Polynomial

Evaluates a polynomial with up to 31 coefficients at a shifted value of the independent variable.

## Format

```
POLY(x, Shift, c0, c1, c2, ..., cN)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable (e.g., `TIME`) |
| `Shift` | Required | Horizontal shift applied before evaluation: polynomial is evaluated at `(x - Shift)` |
| `c0, c1, ..., cN` | Required | Coefficients: `c0 + c1*(x-Shift) + c2*(x-Shift)^2 + ...` (up to 31 terms, so N ≤ 30) |

**Equation:**

$$\text{POLY} = c_0 + c_1(x - s) + c_2(x - s)^2 + \cdots + c_N(x - s)^N$$

where $s$ is the shift value.

## Examples

```adams_fn
! x^2:  POLY(TIME, 0, 0, 0, 1)
! = 0 + 0*TIME + 1*TIME^2
POLY(TIME, 0, 0, 0, 1)

! 10*(TIME - 5):  shift = 5, linear coefficient = 10
POLY(TIME, 5, 0, 10)

! Cubic: 3 + 2*(DZ-10) - 0.5*(DZ-10)^3
POLY(DZ(.MODEL.BODY.CM, .MODEL.ground.REF), 10.0, 3.0, 2.0, 0.0, -0.5)
```

## In context (Adams CMD)

```cmd
force create body_force single_component_force &
    force_name = .MODEL.POLY_SPRING &
    adams_id = 20 &
    i_marker_name = .MODEL.BODY.CM &
    j_floating_marker = .MODEL.BODY.CM &
    action_only = on &
    function = "POLY(DZ(.MODEL.BODY.CM, .MODEL.ground.REF), 0, 0, 500, 0, -0.1)"
```

## See also

- [CHEBY](cheby.md) — same interface but uses Chebyshev polynomial basis (better numerical conditioning for curve fitting)
