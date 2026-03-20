# ACCX / ACCY / ACCZ — Translational Acceleration Components

Return a single Cartesian component (x, y, or z) of the relative translational acceleration between two markers.

> These take **4 arguments** — the same signature as [VX/VY/VZ](vx-vy-vz.md).

## Formats

```
ACCX(To Marker, From Marker, Along Marker, Reference Frame)
ACCY(To Marker, From Marker, Along Marker, Reference Frame)
ACCZ(To Marker, From Marker, Along Marker, Reference Frame)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker being measured |
| `From Marker` | Optional | Marker subtracted from; defaults to global origin |
| `Along Marker` | Optional | Whose x/y/z axis defines the component direction; defaults to global x/y/z |
| `Reference Frame` | Optional | Non-rotating frame for measuring the derivative; defaults to global |

## Example

```adams_fn
! Vertical acceleration of a body's CM in global frame (mm/s² or m/s²)
ACCZ(.MODEL.BODY.CM, .MODEL.ground.ORIGIN)

! Acceleration along a part's local x-axis, measured in global frame
ACCX(.MODEL.BODY.CM, .MODEL.ground.ORIGIN, .MODEL.BODY.ref_mkr, .MODEL.ground.ORIGIN)
```

## Notes

- Returns acceleration in length/time² units matching the model.
- All four arguments parallel [VX/VY/VZ](vx-vy-vz.md) exactly; the only difference is the quantity measured (acceleration vs velocity).

## See also

- [VX / VY / VZ](vx-vy-vz.md) — velocity components (same 4-arg signature)
- [DX / DY / DZ](dx-dy-dz.md) — displacement components (3 args)
- [VM](vm.md) — velocity magnitude
