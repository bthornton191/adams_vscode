# WX / WY / WZ — Angular Velocity Components

Return a single component (x, y, or z) of the relative angular velocity vector between two markers.

> **Note:** The third argument is called **"About Marker"** (not "Along Marker" as with DX/DY/DZ). WX/WY/WZ take **3 arguments** — unlike VX/VY/VZ which take 4.

## Formats

```
WX(To Marker, From Marker, About Marker)
WY(To Marker, From Marker, About Marker)
WZ(To Marker, From Marker, About Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose angular velocity is measured |
| `From Marker` | Optional | Marker whose angular velocity is subtracted; defaults to global |
| `About Marker` | Optional | Marker whose x/y/z axis defines the measurement axis; defaults to global x/y/z |

## Examples

```adams_fn
! Angular velocity of SHAFT about its own z-axis
WZ(.MODEL.SHAFT.ref_mkr, .MODEL.ground.BASE, .MODEL.SHAFT.ref_mkr)

! Relative angular velocity between two rotating parts, about global z
WZ(.MODEL.ARM.tip_mkr, .MODEL.BASE.pivot_mkr)
```

## Key difference from VX/VY/VZ

| Function family | 3rd argument name | 4th argument |
|-----------------|-------------------|--------------|
| DX/DY/DZ | `Along Marker` | (none — 3 args total) |
| VX/VY/VZ | `Along Marker` | `Reference Frame` (4 args total) |
| WX/WY/WZ | `About Marker` | (none — 3 args total) |

## See also

- [WM](wm.md) — angular velocity magnitude
- [AX / AY / AZ](ax-ay-az.md) — rotational displacement (not velocity)
