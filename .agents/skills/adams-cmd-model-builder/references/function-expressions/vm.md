# VM — Velocity Magnitude

Returns the scalar magnitude of the relative velocity vector between two markers.

## Format

```
VM(To Marker, From Marker, Reference Frame)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose velocity is measured |
| `From Marker` | Optional | Marker whose velocity is subtracted; defaults to global origin |
| `Reference Frame` | Optional | Frame in which time-derivatives are computed; defaults to ground |

**Result:** Always ≥ 0.

## Examples

```adams_fn
! Speed of BODY.CM with respect to ground
VM(.MODEL.BODY.CM)

! Relative speed between two markers
VM(.MODEL.LINK_A.end_mkr, .MODEL.LINK_B.start_mkr)

! Speed relative to a moving reference frame
VM(.MODEL.WHEEL.HUB, .MODEL.CAR.CHASSIS_CM, .MODEL.CAR.CHASSIS_CM)
```

## See also

- [VX / VY / VZ](vx-vy-vz.md) — signed velocity components
- [VR](vr.md) — signed radial velocity (line-of-sight)
