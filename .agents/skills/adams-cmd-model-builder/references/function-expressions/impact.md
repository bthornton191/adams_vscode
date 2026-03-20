# IMPACT — One-Sided Contact Force

Models a one-sided collision: generates a repulsive force when a displacement variable falls below a trigger value. Commonly used for floor contacts, end-stop buffers, and penetration prevention.

## Format

```
IMPACT(Displacement Var, Velocity Var, Trigger, K, Stiffness Exponent, C, Damping Ramp-up Distance)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Displacement Var` | Required | Expression for the gap/displacement being monitored |
| `Velocity Var` | Required | Expression for the rate-of-change of the displacement variable |
| `Trigger` | Required | Threshold value; contact force activates when `Displacement Var < Trigger` |
| `K` | Required | Contact stiffness (force/length^e) |
| `Stiffness Exponent` | Required | Nonlinear exponent `e` for stiffness term (typically 1.0–2.2, Hertz contact uses 1.5) |
| `C` | Required | Maximum damping coefficient |
| `Damping Ramp-up Distance` | Required | Penetration depth over which damping ramps from 0 to C (prevents instantaneous damping) |

**Force equation (when penetration `d = Trigger - Displacement Var > 0`):**

$$F = K \cdot d^e - C \cdot \text{STEP}(d, 0, 0, \delta, 1) \cdot V$$

where $\delta$ is the damping ramp-up distance, and $V$ is `Velocity Var`.

**Note:** The velocity variable must be the time derivative of the displacement variable in the **same reference frame**. For DZ displacement, use VZ with the same marker arguments.

## Example

```adams_fn
! Contact when z-gap between m1 and ground drops below 15 mm
! Stiffness: 100 N/mm^1.2, damping: 2.5 N·s/mm, ramp: 0.01 mm
IMPACT(DZ(.MODEL.BODY.M1, .MODEL.ground.M0, .MODEL.ground.M0),
       VZ(.MODEL.BODY.M1, .MODEL.ground.M0, .MODEL.ground.M0, .MODEL.ground.M0),
       15.0, 100.0, 1.2, 2.5, 0.01)
```

## In context (Adams CMD)

```cmd
force create body_force single_component_force &
    force_name = .MODEL.CONTACT_FLOOR &
    adams_id = 5 &
    i_marker_name = .MODEL.BODY.btm_mkr &
    j_floating_marker = .MODEL.ground.FLOOR_REF &
    action_only = on &
    function = "IMPACT(DZ(.MODEL.BODY.btm_mkr, .MODEL.ground.FLOOR_REF), &
                       VZ(.MODEL.BODY.btm_mkr, .MODEL.ground.FLOOR_REF, &
                          .MODEL.ground.FLOOR_REF, .MODEL.ground.FLOOR_REF), &
                       0.0, 1.0E5, 1.5, 50.0, 0.1)"
```

## See also

- [BISTOP](bistop.md) — two-sided version (high and low limits)
- [DZ](dx-dy-dz.md), [VZ](vx-vy-vz.md) — displacement and velocity functions
