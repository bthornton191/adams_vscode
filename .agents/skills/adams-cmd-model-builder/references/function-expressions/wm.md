# WM — Angular Velocity Magnitude

Returns the magnitude of the angular velocity vector between two markers. Always returns a non-negative value.

## Format

```
WM(To Marker, From Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose angular velocity is measured |
| `From Marker` | Optional | Marker whose angular velocity is subtracted; defaults to global frame |

## Example

```adams_fn
! Spin speed of a shaft (rad/s)
WM(.MODEL.SHAFT.end_mkr, .MODEL.ground.BASE)
```

## Notes

- Returns speed in **rad/s** (or rad/time_unit matching model units).
- Always ≥ 0 — cannot detect direction; use [WX/WY/WZ](wx-wy-wz.md) for signed components.

## See also

- [WX / WY / WZ](wx-wy-wz.md) — signed angular velocity components
- [VM](vm.md) — translational velocity magnitude
- [AX / AY / AZ](ax-ay-az.md) — rotational displacement
