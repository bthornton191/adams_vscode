# DM — Distance Magnitude

Returns the scalar magnitude of the displacement vector between two markers. Always ≥ 0.

## Format

```
DM(To Marker, From Marker)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose position is measured |
| `From Marker` | Optional | Origin marker; defaults to the global origin if omitted |

**Equation:** `DM = |position_of_To − position_of_From|`

## Examples

```adams_fn
! Distance from BODY.CM to global origin
DM(.MODEL.BODY.CM)

! Separation between two parts
DM(.MODEL.LINK_A.end_mkr, .MODEL.LINK_B.start_mkr)
```

## Notes

- `DM` is always non-negative, so it cannot indicate direction. Use `DX`, `DY`, or `DZ` when sign matters.
- `UV(DXYZ(i, j))` gives the unit direction vector along the same line.

## See also

- [DX / DY / DZ](dx-dy-dz.md) — signed displacement components
- [VR](vr.md) — signed radial (line-of-sight) velocity along the same distance vector
