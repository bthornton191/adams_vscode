# DX / DY / DZ — Translational Displacement Components

Return a single component (x, y, or z) of the displacement vector from one marker to another, measured along a specified axis.

## Formats

```
DX(To Marker, From Marker, Along Marker)
DY(To Marker, From Marker, Along Marker)
DZ(To Marker, From Marker, Along Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose position is measured |
| `From Marker` | Optional | Marker that serves as the origin; defaults to the global origin if omitted |
| `Along Marker` | Optional | Marker whose x/y/z axis defines the measurement direction; defaults to the global x/y/z axis if omitted |

**Result:** `DX` returns the x-component of `(To − From)` projected onto the x-axis of `Along Marker`. `DY` and `DZ` project onto the y- and z-axes respectively.

## Examples

```adams_fn
! Horizontal distance of BODY.CM from the global origin (x-axis)
DX(.MODEL.BODY.CM)

! Displacement of PISTON.M1 from GROUND.BASE along z, in global frame
DZ(.MODEL.PISTON.M1, .MODEL.ground.BASE)

! Same but measured along the z-axis of a local reference marker
DZ(.MODEL.PISTON.M1, .MODEL.ground.BASE, .MODEL.ground.LOCAL_REF)
```

## Common usage: IMPACT with matching DZ / VZ

When using `IMPACT` or `BISTOP`, the displacement and velocity must be in the same reference frame:

```adams_fn
! DZ and VZ with identical marker arguments (except VZ adds RefFrame)
IMPACT(DZ(.MODEL.BODY.M1, .MODEL.ground.FLOOR),
       VZ(.MODEL.BODY.M1, .MODEL.ground.FLOOR, .MODEL.ground.FLOOR, .MODEL.ground.FLOOR),
       0.0, 1.0E5, 1.5, 50.0, 0.1)
```

## See also

- [DM](dm.md) — scalar distance magnitude (always ≥ 0)
- [VX / VY / VZ](vx-vy-vz.md) — velocity components (note: 4 arguments vs DX/DY/DZ's 3)
