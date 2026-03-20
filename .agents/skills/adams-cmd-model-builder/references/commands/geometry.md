# Geometry — CMD Reference

Geometry in Adams is purely visual — it does not affect the dynamics. All geometry is attached to a marker on a part and follows that part's motion in the animation.

## Important Notes (Adams 2023.2)

- **Do NOT use `part_name`** in geometry commands — the part is inferred from the geometry object path (e.g., `.model.link.cyl_body` belongs to `.model.link`).
- **Do NOT use `adams_id`** in geometry commands.
- **`sphere` and `box` are not valid shape keywords** in Adams 2023.2. Use `ellipsoid` for spheres, `frustum` for box-like shapes, or `cylinder` for rods.
- **`side_count_for_perimeter` is not a valid parameter** for `cylinder`.
- **`i_marker_name` / `j_marker_name` are not valid for `link`** — use `i_marker` / `j_marker` instead.

---

## Cylinder

```cmd
geometry create shape cylinder &
    cylinder_name = .model.link.cyl_body &
    center_marker = .model.link.base_mkr &
    angle_extent  = 360.0D &
    length        = 200.0 &
    radius        = 8.0
```

- `center_marker` is at one **end** of the cylinder; the cylinder extends along the marker's z-axis.
- `angle_extent = 360D` = full cylinder.

---

## Ellipsoid (use instead of sphere)

Use equal x/y/z scale factors for a sphere-like shape.

```cmd
geometry create shape ellipsoid &
    ellipsoid_name = .model.part.ellips_tip &
    center_marker  = .model.part.tip_mkr &
    x_scale_factor = 10.0 &
    y_scale_factor = 10.0 &
    z_scale_factor = 10.0
```

---

## Torus

```cmd
geometry create shape torus &
    torus_name    = .model.wheel.torus_rim &
    center_marker = .model.wheel.hub_mkr &
    outer_radius  = 150.0 &
    inner_radius  = 120.0
```

- Torus axis = z-axis of `center_marker`.

---

## Frustum (Cone / Truncated Cone)

```cmd
geometry create shape frustum &
    frustum_name  = .model.piston.frus_tip &
    center_marker = .model.piston.base_mkr &
    length        = 50.0 &
    bottom_radius = 15.0 &
    top_radius    = 5.0 &
    angle_extent  = 360.0D
```

- For a full cone set `top_radius = 0.0`.

---

## Link (Bar / Rod Shape)

A `link` geometry draws a bar between two markers, with optional width and depth.
Use `i_marker` and `j_marker` (not `i_marker_name` / `j_marker_name`).

```cmd
geometry create shape link &
    link_name = .model.link.shape_link &
    i_marker  = .model.link.end_a_mkr &
    j_marker  = .model.link.end_b_mkr &
    width     = 10.0 &
    depth     = 5.0
```

---

## Modifying Geometry Color

```cmd
geometry modify shape cylinder &
    cylinder_name = .model.link.cyl_body &
    color         = red
```

---

## See also

- [Model, Parts, and Markers](model-parts-markers.md)
