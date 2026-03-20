# Geometry — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/adamspy/Geometry.pyi`

**Solid geometry** is created on a **part**: `part.Geometries.createX()`  
**Model-level geometry** (spring-damper visual, force display): `model.Geometries.createX()`

---

## Block (Box)

```python
box = part.Geometries.createBlock(
    name='BOX_1',
    corner_marker=corner_mkr,   # one corner of the box
    x=100.0,                    # x-dimension
    y=60.0,
    z=40.0
)
```

The box extends in +X, +Y, +Z from `corner_marker`.

---

## Cylinder

```python
cyl = part.Geometries.createCylinder(
    name='CYL_1',
    center_marker=mkr,
    radius=25.0,
    length=200.0,
    angle_extent=360.0,          # degrees; 360 = full cylinder
    side_count_for_body=16,      # facets around circumference
    segment_count_for_ends=8
)
```

The cylinder extends along the z-axis of `center_marker`.

---

## Ellipsoid (Sphere when equal scale factors)

```python
sphere = part.Geometries.createEllipsoid(
    name='SPHERE_1',
    center_marker=cm_mkr,
    x_scale_factor=20.0,   # radius in X
    y_scale_factor=20.0,   # radius in Y (equal → sphere)
    z_scale_factor=20.0    # radius in Z
)
```

---

## Frustum (Cone or Truncated Cone)

```python
cone = part.Geometries.createFrustum(
    name='CONE_1',
    center_marker=base_mkr,
    bottom_radius=30.0,
    top_radius=0.0,          # 0 = pointed cone
    length=100.0,
    angle_extent=360.0,
    side_count_for_body=20,
    segment_count_for_ends=0  # 0 = no end caps
)
```

The frustum extends along the z-axis of `center_marker`. Negative `length` reverses direction.

---

## Torus

```python
tor = part.Geometries.createTorus(
    name='TORUS_1',
    center_marker=mkr,
    major_radius=100.0,    # radius to center of tube
    minor_radius=20.0,     # tube radius
    angle_extent=360.0,
    side_count_for_perimeter=20,
    segment_count=16
)
```

---

## Link (Rod between Two Markers)

```python
rod = part.Geometries.createLink(
    name='ROD_1',
    i_marker=pin_top,
    j_marker=pin_bot,
    depth=12.0,    # out-of-plane thickness
    width=12.0     # in-plane width
)
```

`i_marker` and `j_marker` must be on the **same part** as the geometry.

---

## Arc

```python
arc = part.Geometries.createArc(
    name='ARC_1',
    center_marker=center_mkr,
    radius=50.0,
    angle_extent=180.0,   # degrees; 360 = full circle
    segment_count=24
)
```

---

## Ellipse

```python
ell = part.Geometries.createEllipse(
    name='ELLIPSE_1',
    center_marker=mkr,
    major_radius=100.0,
    minor_radius=50.0,
    start_angle=0.0,
    end_angle=360.0
)
```

---

## Plane (infinite reference plane)

```python
pln = part.Geometries.createPlane(
    name='GROUND_PLANE',
    ref_marker=ref_mkr,
    x_minimum=-200.0,
    x_maximum=200.0,
    y_minimum=-200.0,
    y_maximum=200.0
)
```

---

## Outline (Wireframe through Markers)

```python
outline = part.Geometries.createOutline(
    name='WIRE_1',
    marker=[mkr1, mkr2, mkr3, mkr4]
)
```

---

## Extrusion

```python
ext = part.Geometries.createExtrusion(
    name='EXT_1',
    ref_marker_name='.model.part.mkr',
    points_for_profile=[[0,0], [10,0], [10,10], [0,10]],
    length=50.0
)
```

---

## Revolution

```python
rev_geom = part.Geometries.createRevolution(
    name='REV_BODY',
    ref_marker=axis_mkr,
    points_for_profile=[[10, 0], [10, 50], [20, 50]],
    angle_extent=360.0
)
```

---

## Shell (from file)

```python
shell = part.Geometries.createShell(
    name='CAD_SHELL',
    file_name='body.shl',
    ref_mkr=ref_mkr
)
```

---

## Spring-Damper Visual (model-level)

The spring-damper visual is not attached to a specific part — it goes on the model:

```python
vis = m.Geometries.createSpringDamper(
    name='SPR_VIS',
    i_marker_name='.model.link.mkr_i',
    j_marker_name='.model.ground.mkr_j',
    diameter_of_spring=20.0,
    coil_count=8
)
```

---

## Appearance

All geometry objects support appearance properties:

```python
geom.color = 'Red'            # named color string
geom.visibility = 'on'        # 'on' / 'off' / 'inherit'
geom.render_mode = 'shaded'   # 'shaded', 'wireframe', 'hidden'
```
