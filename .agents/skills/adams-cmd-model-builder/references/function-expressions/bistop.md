# BISTOP — Two-Sided Contact Force

Models a two-sided contact (end-stop): generates repulsive forces when a displacement falls below a lower limit or above an upper limit. Used for bumpers, travel limiters, and two-sided gap closures.

## Format

```
BISTOP(Displacement Var, Velocity Var, Low Trigger, High Trigger, K, Stiffness Exponent, C, Damping Ramp-up Distance)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Displacement Var` | Required | Expression for the monitored displacement or angle |
| `Velocity Var` | Required | Time derivative of the displacement variable (same reference frame) |
| `Low Trigger` | Required | Lower threshold; contact activates when `Displacement Var < Low Trigger` |
| `High Trigger` | Required | Upper threshold; contact activates when `Displacement Var > High Trigger` |
| `K` | Required | Contact stiffness (force/length^e) |
| `Stiffness Exponent` | Required | Nonlinear exponent `e` (typically 1.0–2.2) |
| `C` | Required | Maximum damping coefficient |
| `Damping Ramp-up Distance` | Required | Penetration depth over which damping ramps from 0 to C |

**Behavior:**
- No force when `Low Trigger ≤ Displacement Var ≤ High Trigger`
- Repulsive force (positive) when `Displacement Var < Low Trigger`
- Repulsive force (negative) when `Displacement Var > High Trigger`

## Example

```adams_fn
! Two-sided stop on DZ: keep DZ between -50 and +50 mm
BISTOP(DZ(.MODEL.SLIDER.M1, .MODEL.ground.REF),
       VZ(.MODEL.SLIDER.M1, .MODEL.ground.REF, .MODEL.ground.REF, .MODEL.ground.REF),
       -50.0, 50.0, 1.0E4, 1.5, 20.0, 0.1)
```

## In context (Adams CMD)

```cmd
force create body_force single_component_force &
    force_name = .MODEL.ENDSTOP &
    adams_id = 7 &
    i_marker_name = .MODEL.SLIDER.CM &
    j_floating_marker = .MODEL.SLIDER.CM &
    action_only = on &
    function = "BISTOP(DZ(.MODEL.SLIDER.CM, .MODEL.ground.STOP_REF), &
                       VZ(.MODEL.SLIDER.CM, .MODEL.ground.STOP_REF, &
                          .MODEL.ground.STOP_REF, .MODEL.ground.STOP_REF), &
                       -50.0, 50.0, 1.0E4, 1.5, 20.0, 0.1)"
```

## See also

- [IMPACT](impact.md) — one-sided version
