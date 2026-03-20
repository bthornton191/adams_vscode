# YAW / PITCH / ROLL — Body-321 Euler Angles

Return the three **Body-321** (Z-Y-X, body-fixed) Euler angles describing the orientation of the `To Marker` frame relative to the `From Marker` frame. Commonly used for vehicle dynamics and aerospace applications.

## Formats

```
YAW(To Marker, From Marker)
PITCH(To Marker, From Marker)
ROLL(To Marker, From Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose orientation is measured |
| `From Marker` | Optional | Reference marker; defaults to global frame |

Each function takes exactly **2 arguments**.

## Rotation Sequence (Body-321 / Z-Y-X)

| Function | Rotation Number | Axis (body-fixed) | Typical Application |
|----------|-----------------|-------------------|--------------------|
| `YAW`   | 1st | Z-axis | Heading / steering angle |
| `PITCH` | 2nd | Y-axis | Fore-aft inclination |
| `ROLL`  | 3rd | X-axis | Side-to-side lean |

Results are in **radians**, right-hand rule.

## Examples

```adams_fn
! Roll angle of a vehicle body relative to ground
ROLL(.MODEL.BODY.cm_mkr, .MODEL.ground.base_mkr)

! Pitch-angle-dependent stiffness boost
STEP(ABS(PITCH(.MODEL.CHASSIS.CM)) - 0.1745, 0.0, 0.0, 0.05, 500.0)
```

## Notes

- **Body-321** matches the aerospace / vehicle convention: yaw → pitch → roll.
- **Gimbal lock occurs at PITCH = ±90°** — YAW and ROLL become singular. Avoid this configuration or use quaternion-based markers instead.
- For spin-stabilized systems (gyroscopes), prefer [PSI/THETA/PHI](psi-theta-phi.md).

## See also

- [PSI / THETA / PHI](psi-theta-phi.md) — Body-313 Euler angles
- [AX / AY / AZ](ax-ay-az.md) — single-axis rotational displacement
