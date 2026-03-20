# UV — Unit Vector

Returns a **unit vector** in the direction of the supplied vector expression. Used to normalize a vector so that only its direction, not its magnitude, drives a calculation.

## Format

```
UV(vector_expression)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `vector_expression` | Required | Any Adams vector-valued expression (e.g., `DXYZ`, `VXYZ`, a combination) |

Takes **1 argument** — the vector to normalize.

## Examples

```adams_fn
! Unit vector of the displacement from BODY to TARGET
UV(DXYZ(.MODEL.TARGET.ref_mkr, .MODEL.BODY.ref_mkr))

! Radial velocity = velocity component along the line of sight
! (equivalent to VR)
VXYZ(.MODEL.BODY.i_mkr, .MODEL.ground.j_mkr) * UV(DXYZ(.MODEL.BODY.i_mkr, .MODEL.ground.j_mkr))
```

## Zero-vector handling

When the input vector has zero magnitude (the two markers coincide), `UV` reuses the **last valid direction** rather than returning a singularity. This prevents solver crashes at coincident-marker configurations, but be aware the direction at that instant is frozen to the previous direction.

## Notes

- `UV` is most useful when you want to project a force along the current line connecting two moving markers without manually computing the direction cosines.
- Combine with `DM` for a full spring-along-line-of-sight model: magnitude from `DM`, direction from `UV(DXYZ(...))`.

## See also

- [DM](dm.md) — displacement magnitude (scalar)
- [VR](vr.md) — radial (line-of-sight) velocity component
- [DX / DY / DZ](dx-dy-dz.md) — displacement components
