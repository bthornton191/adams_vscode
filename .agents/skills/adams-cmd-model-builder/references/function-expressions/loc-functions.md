# LOC_ Functions — Location / Coordinate Computation

LOC_ functions return a 3-element array `{x, y, z}` representing a point expressed in the **global** coordinate system, unless stated otherwise. They are design-time functions evaluated during model construction, not during simulation.

## Quick reference

| Function | Signature | Returns |
|----------|-----------|---------|
| `LOC_ALONG_LINE` | `LOC_ALONG_LINE(start, point_on_line, distance)` | Point a distance along a line |
| `LOC_BY_FLEXBODY_NODEID` | `LOC_BY_FLEXBODY_NODEID(flex_body, node_id)` | Location of a flex-body node |
| `LOC_CYLINDRICAL` | `LOC_CYLINDRICAL(r, theta, z)` | Cylindrical → Cartesian |
| `LOC_FRAME_MIRROR` | `LOC_FRAME_MIRROR(location, frame, plane)` | Mirror across a marker plane |
| `LOC_GLOBAL` | `LOC_GLOBAL(location, frame)` | Local → global conversion |
| `LOC_INLINE` | `LOC_INLINE(location, in_frame, to_frame)` | Transform & normalise between frames |
| `LOC_LOCAL` | `LOC_LOCAL(location, frame)` | Global → local conversion |
| `LOC_LOC` | `LOC_LOC(location, in_frame, to_frame)` | Transform between two frames |
| `LOC_MIRROR` | `LOC_MIRROR(location, frame, plane)` | Mirror across a named plane |
| `LOC_ON_AXIS` | `LOC_ON_AXIS(frame, distance, axis)` | Point along a frame axis |
| `LOC_ON_LINE` | `LOC_ON_LINE(line_matrix, distance)` | Point along a 2-point line |
| `LOC_PERPENDICULAR` | `LOC_PERPENDICULAR(plane_matrix)` | Normal to a 3-point plane |
| `LOC_PLANE_MIRROR` | `LOC_PLANE_MIRROR(location, plane_matrix)` | Mirror across a 3-point plane |
| `LOC_RELATIVE_TO` | `LOC_RELATIVE_TO(location, frame)` | Transform relative to context |
| `LOC_SPHERICAL` | `LOC_SPHERICAL(rho, theta, phi)` | Spherical → Cartesian |
| `LOC_TO_FLEXBODY_NODEID` | `LOC_TO_FLEXBODY_NODEID(flex_body, location)` | Nearest flex-body node ID |
| `LOC_X_AXIS` | `LOC_X_AXIS(frame)` | Unit vector along frame X-axis |
| `LOC_Y_AXIS` | `LOC_Y_AXIS(frame)` | Unit vector along frame Y-axis |
| `LOC_Z_AXIS` | `LOC_Z_AXIS(frame)` | Unit vector along frame Z-axis |

---

## LOC_ALONG_LINE

Returns the global coordinates of a point that is a specified distance along the line connecting two coordinate-system objects.

```
LOC_ALONG_LINE(start_object, line_object, distance)
```

| Argument | Description |
|----------|-------------|
| `start_object` | Coordinate system object defining the starting point |
| `line_object` | Coordinate system object defining a second point on the line |
| `distance` | Distance to travel from the starting point along the line |

```adams_fn
LOC_ALONG_LINE(marker_2, marker_1, 5)
! returns {7.5, 9.5, 0}
```

---

## LOC_BY_FLEXBODY_NODEID

Returns the global location `{x, y, z}` of a node on a flexible body.

```
LOC_BY_FLEXBODY_NODEID(flex_body, node_id)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `node_id` | Integer node ID |

> If the node ID does not exist in the flexible body, the function returns `{0, 0, 0}` without a warning.

---

## LOC_CYLINDRICAL

Converts cylindrical coordinates `(r, θ, z)` to Cartesian `(x, y, z)`. Both coordinate systems share the same origin and z-axis (the global frame).

```
LOC_CYLINDRICAL(r, theta, z)
```

| Argument | Description |
|----------|-------------|
| `r` | Radius (distance from z-axis) |
| `theta` | Angle about z-axis from x-axis, in degrees (right-hand rule) |
| `z` | Distance along global z-axis |

```adams_fn
LOC_CYLINDRICAL(1, 30, 0)
! returns {0.866, 0.5, 0}
```

---

## LOC_FRAME_MIRROR

Returns the global coordinates of a location mirrored across a plane defined by a coordinate system object (marker).

```
LOC_FRAME_MIRROR(location, frame, plane_name)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in global coordinates |
| `frame` | Coordinate system object (marker) defining the plane |
| `plane_name` | Plane of reflection: `"xy"`, `"xz"`, or `"yz"` (case- and order-insensitive) |

```adams_fn
LOC_FRAME_MIRROR({7, 7, 0}, marker_1, "xy")
! returns {7, 5, 0}
```

---

## LOC_GLOBAL

Converts a location expressed in a local (marker) coordinate system to global coordinates.

```
LOC_GLOBAL(location, frame)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in the local frame |
| `frame` | Coordinate system object defining the local frame |

```adams_fn
LOC_GLOBAL({-5, -8, 0}, marker_1)
! returns {14, 12, 0}
```

---

## LOC_INLINE

Transforms a location from one coordinate system to another, and normalises the result.

```
LOC_INLINE(location, in_frame, to_frame)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in `in_frame` |
| `in_frame` | Original coordinate system object |
| `to_frame` | Target coordinate system object |

```adams_fn
LOC_INLINE({-8, -2, 0}, marker_1, marker_2)
! returns {0.8, 0.6, 0.0}
```

---

## LOC_LOCAL

Converts a global location to local coordinates relative to a marker.

```
LOC_LOCAL(location, frame)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in global coordinates |
| `frame` | Coordinate system object defining the local frame |

```adams_fn
LOC_LOCAL({-4, -7, 0}, marker_2)
! returns {-23, 11, 0}  (in marker_2 coordinate system)
```

---

## LOC_LOC

Transforms a location from one coordinate system into another.

```
LOC_LOC(location, in_frame, to_frame)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in `in_frame` |
| `in_frame` | Original coordinate system object |
| `to_frame` | Target coordinate system object (use `0` for global) |

```adams_fn
LOC_LOC({-6, 12, 0}, marker_1, marker_2)
! returns {-2, 8, 0}  (with respect to marker_2)
```

---

## LOC_MIRROR

Returns the global coordinates of a location mirrored across a named plane of a marker.

```
LOC_MIRROR(location, frame, plane_name)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in global coordinates |
| `frame` | Coordinate system object defining the plane of reflection |
| `plane_name` | `"xy"`, `"xz"`, or `"yz"` (case- and order-insensitive) |

```adams_fn
LOC_MIRROR({7, 7, 0}, marker_1, "xy")
! returns {7, 5, 0}
```

---

## LOC_ON_AXIS

Returns the global coordinates of a point obtained by translating a distance along a specified axis of a marker.

```
LOC_ON_AXIS(frame, distance, axis)
```

| Argument | Description |
|----------|-------------|
| `frame` | Coordinate system object whose axis is used |
| `distance` | Distance to translate along the axis |
| `axis` | `"x"`, `"y"`, or `"z"` (case-insensitive) |

```adams_fn
LOC_ON_AXIS(marker_2, 5, "x")
! returns {4, 11, 0}
```

---

## LOC_ON_LINE

Returns the global coordinates of a point at a given distance from the first of two points defining a line.

```
LOC_ON_LINE(line_matrix, distance)
```

| Argument | Description |
|----------|-------------|
| `line_matrix` | 3x2 matrix `{{x1,y1,z1},{x2,y2,z2}}` — two points on the line |
| `distance` | Distance measured from the first point |

```adams_fn
LOC_ON_LINE({{7,5,0},{15,11,0}}, 7)
! returns {12.6, 9.2, 0.0}
```

---

## LOC_PERPENDICULAR

Returns a location one unit from the first point in the direction normal to the plane defined by three non-collinear points.

```
LOC_PERPENDICULAR(plane_matrix)
```

| Argument | Description |
|----------|-------------|
| `plane_matrix` | 3x3 matrix `{{x1,y1,z1},{x2,y2,z2},{x3,y3,z3}}` — three non-collinear points |

```adams_fn
LOC_PERPENDICULAR({{10,12,0},{14,12,0},{12,10,0}})
! returns {10, 12, 1}
```

---

## LOC_PLANE_MIRROR

Returns the global coordinates of a location mirrored across a plane defined by three non-collinear points.

```
LOC_PLANE_MIRROR(location, plane_matrix)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in global coordinates |
| `plane_matrix` | 3x3 matrix providing three non-collinear points on the plane |

```adams_fn
LOC_PLANE_MIRROR({2, 4, 0}, {{10,12,0},{14,12,0},{12,10,0}})
! returns {2, 4, 0}
```

---

## LOC_RELATIVE_TO

Transforms a location from a specified coordinate system relative to the parent expression context. Prefer `LOC_LOC` in nested expressions to avoid unexpected results.

```
LOC_RELATIVE_TO(location, frame)
```

| Argument | Description |
|----------|-------------|
| `location` | `{x, y, z}` expressed in `frame` |
| `frame` | Coordinate system object |

> **Note**: The result is expressed relative to the parent expression context (e.g., the owning part for a marker expression). Use `LOC_LOC(location, frame, 0)` for more predictable behaviour in nested expressions.

```adams_fn
LOC_RELATIVE_TO({16, 8, 0}, marker_2)
! returns {-4, 22, 0}
```

---

## LOC_SPHERICAL

Converts spherical coordinates `(ρ, θ, φ)` to Cartesian `(x, y, z)`.

```
LOC_SPHERICAL(rho, theta, phi)
```

| Argument | Description |
|----------|-------------|
| `rho` | Radius of the sphere |
| `theta` | Counterclockwise rotation about y-axis (degrees) |
| `phi` | Counterclockwise rotation about z-axis (degrees) |

```adams_fn
LOC_SPHERICAL(10, 8D, 90D)
! returns {9.9, 1.39, 0}
```

---

## LOC_TO_FLEXBODY_NODEID

Returns the integer node ID of the node on a flexible body that is closest to a specified location.

```
LOC_TO_FLEXBODY_NODEID(flex_body, location)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `location` | `{x, y, z}` three-dimensional vector |

---

## LOC_X_AXIS / LOC_Y_AXIS / LOC_Z_AXIS

Return a unit vector (normalised) representing one axis of a marker's coordinate system, expressed in global coordinates.

```
LOC_X_AXIS(frame)
LOC_Y_AXIS(frame)
LOC_Z_AXIS(frame)
```

| Argument | Description |
|----------|-------------|
| `frame` | Coordinate system object |

```adams_fn
LOC_X_AXIS(marker_2)   ! returns {1, 0, 0}  (for an unrotated marker)
LOC_Y_AXIS(marker_2)   ! returns {0, 1, 0}
LOC_Z_AXIS(marker_2)   ! returns {0, 0, 1}
```

---

## See also

- [ORI_ functions](ori-functions.md) — orientation / rotation-matrix functions
