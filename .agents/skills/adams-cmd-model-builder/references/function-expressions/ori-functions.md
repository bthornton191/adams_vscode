# ORI_ Functions — Orientation / Rotation Computation

ORI_ functions return a **body-fixed 3-1-3 Euler angle sequence** `{psi, theta, phi}` (degrees) describing the orientation of a coordinate system. They are design-time functions evaluated during model construction.

## Usage in CMD commands

When an `ORI_` function is used as a parameter value in a CMD command, it **must** be enclosed in outer parentheses `(...)`. Without them Adams treats the text as a literal string rather than an expression. See **Core Rule 17** in the skill for the parametric vs immediate (`eval()`) distinction.

```adams_cmd
! WRONG — no outer parentheses
marker create marker_name = .model.part.mkr &
    orientation = ori_in_plane(.model.ground.m1, .model.ground.m2, .model.ground.m3, "z_zy")

! Parametric — Adams stores and re-evaluates the expression on model update
marker create marker_name = .model.part.mkr &
    orientation = (ori_in_plane(.model.ground.m1, .model.ground.m2, .model.ground.m3, "z_zy"))

! Immediate — Adams evaluates now and stores fixed angles (use in loops)
marker create marker_name = .model.part.mkr &
    orientation = (eval(ori_in_plane(.model.ground.m1, .model.ground.m2, .model.ground.m3, "z_zy")))
```

## Quick reference

| Function | Signature | Returns |
|----------|-----------|---------|
| `ORI_ALIGN_AXIS` | `ORI_ALIGN_AXIS(frame, axis_spec)` | Orientation aligning one axis to a frame axis |
| `ORI_ALIGN_AXIS_EUL` | `ORI_ALIGN_AXIS_EUL(orientation, axis_spec)` | Align one axis from an Euler orientation |
| `ORI_ALL_AXES` | `ORI_ALL_AXES(plane_matrix, axes_names)` | Orientation with two axes defined by a plane |
| `ORI_ALONG_AXIS` | `ORI_ALONG_AXIS(from_frame, to_frame, axis)` | Align an axis from one frame to another |
| `ORI_FRAME_MIRROR` | `ORI_FRAME_MIRROR(angles, frame, plane, axes)` | Mirror orientation across a frame plane |
| `ORI_GLOBAL` | `ORI_GLOBAL(orientation, frame)` | Local Euler angles → global frame |
| `ORI_IN_PLANE` | `ORI_IN_PLANE(frame1, frame2, frame3, axes_spec)` | Orientation from a 3-point plane |
| `ORI_LOCAL` | `ORI_LOCAL(orientation, frame)` | Global Euler angles → local frame |
| `ORI_MIRROR` | `ORI_MIRROR(angles, frame, plane, axes)` | Mirror orientation across a plane |
| `ORI_ONE_AXIS` | `ORI_ONE_AXIS(line_matrix, axis)` | Orientation aligning one axis with a line |
| `ORI_ORI` | `ORI_ORI(orientation, from_frame, to_frame)` | Transform orientation between two frames |
| `ORI_PLANE_MIRROR` | `ORI_PLANE_MIRROR(angles, plane_matrix, axes)` | Mirror orientation across a 3-point plane |
| `ORI_RELATIVE_TO` | `ORI_RELATIVE_TO(angles, frame)` | Transform orientation relative to context |

---

## ORI_ALIGN_AXIS

Returns an orientation that aligns one axis of the result with an axis of a specified coordinate system object. The other axes are left in unspecified orientations.

```
ORI_ALIGN_AXIS(frame, axis_spec)
```

| Argument | Description |
|----------|-------------|
| `frame` | Coordinate system object defining the alignment reference |
| `axis_spec` | String specifying which axis to align, e.g. `"xy"` (x-axis of result → y-axis of frame), `"z-z"` (z-axis of result → opposite z-axis of frame). Valid: `xx xy xz yx yy yz zx zy zz` and with `+`/`-` middle character |

```adams_fn
ORI_ALIGN_AXIS(marker_1, "z-z")
! returns {90, 180, 0}
```

---

## ORI_ALIGN_AXIS_EUL

Returns an orientation that aligns one axis based on an input Euler orientation. Functionally similar to `ORI_ALIGN_AXIS` but takes an explicit orientation array instead of a frame.

```
ORI_ALIGN_AXIS_EUL(orientation, axis_spec)
```

| Argument | Description |
|----------|-------------|
| `orientation` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles (degrees) |
| `axis_spec` | Axis alignment string (see `ORI_ALIGN_AXIS`) |

```adams_fn
ORI_ALIGN_AXIS_EUL({8, 10, 0}, "z-z")
! returns {188, 170, 90}
```

---

## ORI_ALL_AXES

Returns a body-fixed 3-1-3 Euler sequence that orients two axes using three non-collinear plane points. The first axis is parallel to and co-directed with the line from the first to the second point; the second axis lies in the plane.

```
ORI_ALL_AXES(plane_matrix, axes_names)
```

| Argument | Description |
|----------|-------------|
| `plane_matrix` | 3x3 matrix `{{x1,y1,z1},{x2,y2,z2},{x3,y3,z3}}` — three non-collinear points |
| `axes_names` | Which two axes to orient: `"xy"`, `"xz"`, `"yx"`, `"yz"`, `"zx"`, or `"zy"` (case-insensitive; `"xy"` ≠ `"yx"`) |

```adams_fn
ORI_ALL_AXES({{14,18,0},{10,14,0},{16,14,0}}, "xz")
! returns {45, 90, 180}
```

---

## ORI_ALONG_AXIS

Returns an orientation that aligns a specified axis of one coordinate system with the same-named axis of a second coordinate system.

```
ORI_ALONG_AXIS(from_frame, to_frame, axis)
```

| Argument | Description |
|----------|-------------|
| `from_frame` | Source coordinate system object |
| `to_frame` | Target coordinate system object |
| `axis` | `"x"`, `"y"`, or `"z"` (case-insensitive) |

```adams_fn
ORI_ALONG_AXIS(marker_1, marker_2, "y")
! returns {315, 0, 0}
```

---

## ORI_FRAME_MIRROR

Returns an orientation produced by mirroring specified axes across a plane within a coordinate system object.

```
ORI_FRAME_MIRROR(angles, frame, plane_name, axes_names)
```

| Argument | Description |
|----------|-------------|
| `angles` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles |
| `frame` | Coordinate system object defining the plane of reflection |
| `plane_name` | Plane to reflect across: `"xy"`, `"xz"`, or `"yz"` |
| `axes_names` | Which axes to mirror: `"xy"`, `"xz"`, or `"yz"` |

```adams_fn
ORI_FRAME_MIRROR({6, 14, 0}, marker_1, "xz", "xz")
! returns {174, 14, 180}
```

---

## ORI_GLOBAL

Converts a body-fixed 3-1-3 Euler orientation from a local coordinate system to the global coordinate system. Shorthand for `ORI_ORI`.

```
ORI_GLOBAL(orientation, frame)
```

| Argument | Description |
|----------|-------------|
| `orientation` | `{psi, theta, phi}` expressed in `frame` |
| `frame` | Source coordinate system object |

```adams_fn
ORI_GLOBAL({marker_2.orientation}, marker_1)
! returns {270, 0, 0}
```

---

## ORI_IN_PLANE

Returns an orientation by directing one axis and constraining a second axis to lie in a plane defined by three marker positions.

```
ORI_IN_PLANE(frame1, frame2, frame3, axes_spec)
```

| Argument | Description |
|----------|-------------|
| `frame1` | Marker for the first point (origin of the directed axis) |
| `frame2` | Marker for the second point (direction of the first axis) |
| `frame3` | Marker for the third point (defines the plane) |
| `axes_spec` | String of the form `"<axis1>_<axis2><plane>"`, e.g. `"z_zy"` means z-axis directed from frame1→frame2, y-axis in the zy-plane |

```adams_fn
ORI_IN_PLANE(marker_1, marker_2, marker_3, "z_zy")
! returns {135, 90, 90}
```

---

## ORI_LOCAL

Converts a body-fixed 3-1-3 Euler orientation from the global coordinate system to a local coordinate system. Shorthand for `ORI_ORI`.

```
ORI_LOCAL(orientation, frame)
```

| Argument | Description |
|----------|-------------|
| `orientation` | `{psi, theta, phi}` expressed in global coordinates |
| `frame` | Target coordinate system object |

```adams_fn
ORI_LOCAL({marker_1.orientation}, marker_2)
! returns {90, 0, 0}
```

---

## ORI_MIRROR

Returns an orientation produced by mirroring specified axes across a plane of a coordinate system object.

```
ORI_MIRROR(angles, frame, plane_name, axes_names)
```

| Argument | Description |
|----------|-------------|
| `angles` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles expressed in `frame` |
| `frame` | Coordinate system object defining the plane of reflection |
| `plane_name` | `"xy"`, `"xz"`, or `"yz"` (case-insensitive) |
| `axes_names` | Which axes to mirror: `"xy"`, `"xz"`, or `"yz"` |

```adams_fn
ORI_MIRROR({{10,8,0}}, marker_1, "xy", "xy")
! returns {190, 8, 180}
```

---

## ORI_ONE_AXIS

Returns a body-fixed 3-1-3 Euler rotation sequence that aligns a specified axis with a line defined by two points. Rotation about the directed axis is arbitrary.

```
ORI_ONE_AXIS(line_matrix, axis)
```

| Argument | Description |
|----------|-------------|
| `line_matrix` | 3x2 matrix `{{x1,y1,z1},{x2,y2,z2}}` — two points on the line |
| `axis` | `"x"`, `"y"`, or `"z"` (case-insensitive) |

```adams_fn
ORI_ONE_AXIS({{10,16,0},{8,16,0}}, "x")
! returns {180, 180, 0}
```

---

## ORI_ORI

Transforms a body-fixed 3-1-3 Euler orientation expressed in one coordinate system to the equivalent orientation as expressed in another.

```
ORI_ORI(orientation, from_frame, to_frame)
```

| Argument | Description |
|----------|-------------|
| `orientation` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles |
| `from_frame` | Coordinate system object in which `orientation` is expressed |
| `to_frame` | Target coordinate system object |

```adams_fn
ORI_ORI({marker_1.orientation}, marker_1, marker_2)
! returns {180, 90, 90}
```

---

## ORI_PLANE_MIRROR

Returns a body-fixed 3-1-3 Euler sequence produced by mirroring specified axes across a plane defined by three non-collinear points.

```
ORI_PLANE_MIRROR(angles, plane_matrix, axes_names)
```

| Argument | Description |
|----------|-------------|
| `angles` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles expressed in global coordinates |
| `plane_matrix` | 3x3 matrix providing three non-collinear points on the plane |
| `axes_names` | Which axes to mirror: `"xy"`, `"xz"`, or `"yz"` |

```adams_fn
ORI_PLANE_MIRROR({marker_1.orientation}, {{18,6,0},{18,12,0},{21,6,0}}, "xy")
! returns {0, 0, 0}
```

---

## ORI_RELATIVE_TO

Returns an orientation by transforming body-fixed 3-1-3 Euler angles expressed in a coordinate system to the context of the parent expression. Shorthand for `ORI_ORI(angles, frame, parent_frame)`.

```
ORI_RELATIVE_TO(angles, frame)
```

| Argument | Description |
|----------|-------------|
| `angles` | `{psi, theta, phi}` body-fixed 3-1-3 Euler angles expressed in `frame` |
| `frame` | Source coordinate system object |

```adams_fn
ORI_RELATIVE_TO({marker_1.orientation}, marker_2)
! returns {180, 90, 180}
```

---

## Euler convention note

All ORI_ functions use the **body-fixed 3-1-3 sequence** (also called the ZXZ sequence):
1. Rotate about Z by **psi** (ψ)
2. Rotate about new X by **theta** (θ)
3. Rotate about new Z by **phi** (φ)

Angles are in **degrees**.

---

## See also

- [LOC_ functions](loc-functions.md) — location / coordinate conversion functions
