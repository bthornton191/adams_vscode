# DELAY — Time-Delayed Expression

Evaluates an expression and returns its value at a time `t − Δt` (i.e., delayed by a fixed amount). Used to model transport delays, dead-time in control loops, or fluid-transmission lags.

## Format

```
DELAY(Delayed_Expression, Delay_Magnitude, Initial_Expression_Value, Delay_Logic_Array)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Delayed_Expression` | Required | The expression whose past value is returned |
| `Delay_Magnitude` | Required | Positive scalar: how far back in time to look (Δt) |
| `Initial_Expression_Value` | Optional | Value to return before `Delay_Magnitude` seconds have elapsed; defaults to 0 |
| `Delay_Logic_Array` | Optional | Adams array element used to manage the delay buffer; pass `0` if not needed |

`Delay_Magnitude` **must be positive**.

## Examples

```adams_fn
! Return velocity as it was 0.1 seconds ago
DELAY(VZ(.MODEL.BODY.CM, .MODEL.ground.base_mkr), 0.1, 0.0, 0)

! Dead-time control: feed delayed position error into a proportional controller
1000.0 * DELAY(DZ(.MODEL.BODY.CM) - 50.0, 0.05, 0.0, 0)
```

## Notes

- During the initial period (TIME < Delay_Magnitude) the `Initial_Expression_Value` is returned.
- The solver manages an internal ring buffer to store past values; `Delay_Logic_Array` can be left as `0` unless you need to share the buffer across multiple delay calls.
- Delay functions introduce a **transcendental term** (DDE) into the equations of motion, which can significantly increase solver cost. Use only where physically required.
- Delay is incompatible with certain stiff integrators; verify solver settings when using DELAY.

## See also

- [IF](if.md) — conditional branching
- [STEP](step.md) — smooth ramp (no delay)
