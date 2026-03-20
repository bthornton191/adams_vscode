# VX / VY / VZ — Translational Velocity Components

Return a single component (x, y, or z) of the relative velocity vector between two markers.

> **Note:** VX/VY/VZ take **4 arguments**, not 3. The extra `Reference Frame` argument distinguishes them from DX/DY/DZ.

## Formats

```
VX(To Marker, From Marker, Along Marker, Reference Frame)
VY(To Marker, From Marker, Along Marker, Reference Frame)
VZ(To Marker, From Marker, Along Marker, Reference Frame)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose velocity is measured |
| `From Marker` | Optional | Marker whose velocity is subtracted; defaults to the global origin |
| `Along Marker` | Optional | Marker whose x/y/z axis defines the measurement direction; defaults to global x/y/z |
| `Reference Frame` | Optional | Marker defining the frame in which time-derivatives are computed; defaults to the ground frame |

## Examples

```adams_fn
! z-velocity of BODY.CM in the global frame
VZ(.MODEL.BODY.CM)

! Relative z-velocity between two markers, in ground frame
VZ(.MODEL.PISTON.M1, .MODEL.ground.BASE, .MODEL.ground.BASE, .MODEL.ground.BASE)

! Velocity measured along and in a moving frame
VX(.MODEL.BODY.CM, .MODEL.CAR.CHASSIS_CM, .MODEL.CAR.CHASSIS_CM, .MODEL.CAR.CHASSIS_CM)
```

## Correct pairing with DZ for IMPACT

When providing the velocity argument to `IMPACT`, always match the marker arguments:

```adams_fn
IMPACT(
    DZ(.MODEL.BODY.M1, .MODEL.ground.FLOOR),
    VZ(.MODEL.BODY.M1, .MODEL.ground.FLOOR, .MODEL.ground.FLOOR, .MODEL.ground.FLOOR),
    0.0, 1.0E5, 1.5, 50.0, 0.1
)
```

## See also

- [DX / DY / DZ](dx-dy-dz.md) — 3-argument displacement functions
- [VM](vm.md) — velocity magnitude (scalar)
- [VR](vr.md) — radial (line-of-sight) velocity
