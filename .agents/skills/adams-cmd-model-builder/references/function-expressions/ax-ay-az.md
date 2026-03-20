# AX / AY / AZ — Rotational Displacement

Return the rotational displacement (angle, in radians) that describes the orientation of the `To Marker` relative to the `From Marker` about the x, y, or z axis.

> **These return angles, not angular velocities.** For angular velocity use [WX/WY/WZ](wx-wy-wz.md).

## Formats

```
AX(To Marker, From Marker)
AY(To Marker, From Marker)
AZ(To Marker, From Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose orientation is measured |
| `From Marker` | Optional | Reference marker; defaults to global frame |

These functions take only **2 arguments** — there is no "Along Marker" or "Reference Frame" argument.

## Examples

```adams_fn
! Rotation angle of ARM about the Z-axis of the PIVOT marker (radians)
AZ(.MODEL.ARM.tip_mkr, .MODEL.BASE.pivot_mkr)

! Check if angle exceeds 45 degrees
IF(AZ(.MODEL.BODY.CM) - 45D : 0, 0, STEP(AZ(.MODEL.BODY.CM), 45D, 0, 90D, 1))
```

## Notes

- Result is in **radians** by default. Append `D` when interpreting literalangles elsewhere in the expression (e.g., comparing to `90D`).
- AX/AY/AZ report a **fixed-axis** rotation angle, not Euler angles. For full orientation description use [PSI/THETA/PHI](psi-theta-phi.md) or [YAW/PITCH/ROLL](yaw-pitch-roll.md).

## See also

- [WX / WY / WZ](wx-wy-wz.md) — angular velocity components
- [PSI / THETA / PHI](psi-theta-phi.md) — Body-313 Euler angles
- [YAW / PITCH / ROLL](yaw-pitch-roll.md) — Body-321 Euler angles
