# VR — Radial (Line-of-Sight) Velocity

Returns the component of relative velocity that lies along the line connecting two markers (the "radial" or "separation" velocity). Positive when the markers are moving apart; negative when approaching.

## Format

```
VR(To Marker, From Marker, Reference Frame)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `To Marker` | Required | Marker whose velocity is measured |
| `From Marker` | Optional | Marker whose velocity is subtracted; defaults to global origin |
| `Reference Frame` | Optional | Frame in which time-derivatives are computed; defaults to ground |

**Equation:** VR = (velocity of To − velocity of From) ∙ (unit vector from From to To)

**Sign convention:**
- VR > 0 → markers moving **apart**
- VR < 0 → markers **approaching**

## Example

```adams_fn
! Separation velocity between two attachment points
VR(.MODEL.SPRING_END_A.M1, .MODEL.SPRING_END_B.M2)
```

## Notes

VR is equivalent to `VXYZ(i,j) * UV(DXYZ(i,j))` (the dot product of the relative velocity with the unit direction vector). It is the natural velocity variable to pair with `DM` for radial spring-damper expressions.

## See also

- [DM](dm.md) — scalar distance (displacement magnitude)
- [VM](vm.md) — total velocity magnitude (all directions)
- [VX / VY / VZ](vx-vy-vz.md) — component velocities
