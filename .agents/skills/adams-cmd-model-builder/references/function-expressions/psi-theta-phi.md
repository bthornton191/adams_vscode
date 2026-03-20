# PSI / THETA / PHI — Body-313 Euler Angles

Return the three **Body-313** (Z-X-Z, body-fixed) Euler angles describing the orientation of the `To Marker` frame relative to the `From Marker` frame.

## Formats

```
PSI(To Marker, From Marker)
THETA(To Marker, From Marker)
PHI(To Marker, From Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose orientation is measured |
| `From Marker` | Optional | Reference marker; defaults to global frame |

Each function takes exactly **2 arguments**.

## Rotation Sequence (Body-313 / Z-X-Z)

| Function | Rotation Number | Axis (body-fixed) |
|----------|-----------------|-------------------|
| `PSI`   | 1st | Z-axis (precession) |
| `THETA` | 2nd | X-axis (nutation) |
| `PHI`   | 3rd | Z-axis (spin) |

Results are in **radians**, right-hand rule.

## Examples

```adams_fn
! Nutation angle (2nd Body-313 rotation) of GYRO relative to GROUND
THETA(.MODEL.GYRO.cm_mkr, .MODEL.ground.base_mkr)

! PSI angle converted to a torque input
STEP(PSI(.MODEL.ARM.ref_mkr, .MODEL.ground.base_mkr) - 0.5236, 0.0, 0.0, 0.1, 100.0)
```

## Notes

- Use Body-313 for systems with a natural spin axis (gyroscopes, tops, turbines).
- **Avoid THETA = 0 or π** — these are gimbal-lock configurations where PSI and PHI are undefined.
- For vehicle-type orientation (yaw-pitch-roll), prefer [YAW/PITCH/ROLL](yaw-pitch-roll.md).

## See also

- [YAW / PITCH / ROLL](yaw-pitch-roll.md) — Body-321 Euler angles
- [AX / AY / AZ](ax-ay-az.md) — single-axis rotational displacement
