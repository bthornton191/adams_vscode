# IF — Conditional Expression

Returns one of three values depending on whether an expression is negative, zero, or positive.

> **Warning:** Using `IF` introduces hard discontinuities in function derivatives. The integrator must reduce the time step at the discontinuity, which can slow or fail the simulation. **Prefer `STEP` or `STEP5`** wherever a smooth transition is acceptable.

## Format

```
IF(Expression1: Expression2, Expression3, Expression4)
```

Note the colon `:` separating Expression1 from the result expressions.

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Expression1` | Required | The condition expression to evaluate |
| `Expression2` | Required | Returned when `Expression1 < 0` |
| `Expression3` | Required | Returned when `Expression1 = 0` |
| `Expression4` | Required | Returned when `Expression1 > 0` |

## Example

```adams_fn
! Returns 0 if time < 2.5, 0.5 if time = 2.5, 1 if time > 2.5
IF(TIME - 2.5 : 0, 0.5, 1)

! Switch force direction based on displacement
IF(DZ(.MODEL.PISTON.CM, .MODEL.ground.REF) - 50 : -F_MAX, 0, F_MAX)
```

## Better alternative with STEP

```adams_fn
! Instead of IF, use STEP for a smooth version of a switch:
! Force is 0 below t=2.4, transitions to 1 between t=2.4 and t=2.6
STEP(TIME, 2.4, 0, 2.6, 1)
```

## See also

- [STEP](step.md) — preferred smooth alternative
- [STEP5](step5.md) — even smoother alternative
