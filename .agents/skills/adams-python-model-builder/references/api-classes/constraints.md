# Constraints and Motions — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/adamspy/Constraint.pyi`

All constraints are created via `model.Constraints.createX(**kwargs)`.

---

## Common Parameters for All Joints

Most joint creation methods accept:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Short name |
| `i_marker` / `i_marker_name` | `Marker` / `str` | Action-body marker |
| `j_marker` / `j_marker_name` | `Marker` / `str` | Reaction-body marker |
| `i_part` / `j_part` | `Part` | Alternate form: specify parts + `location`/`orientation` |
| `location` | `List[float]` | Joint location (when not using pre-created markers) |
| `orientation` | `List[float]` | Joint orientation — z-axis is the joint axis |
| `along_axis_orientation` | `List[float]` | Point z-axis of joint toward this vector |
| `in_plane_orientation` | `List[float]` | Point x-axis within xy-plane |
| `relative_to` | `Object` | Reference for `location`/`orientation` |
| `comments` | `str` | Optional comment |

---

## Standard Joints

### Revolute (1 rotational DOF)
```python
rev = m.Constraints.createRevolute(name='REV_1',
                                   i_marker=link_pin, j_marker=ground_pin)
# Initial conditions:
rev.rotational_ic = 45.0      # initial angle (model angle units)
rev.angular_velocity_ic = 0.0
```

### Translational (1 translational DOF)
```python
tr = m.Constraints.createTranslational(name='TRANS_1',
                                       i_marker=slider_mkr, j_marker=rail_mkr)
tr.translational_ic = 0.0
tr.velocity_ic = 0.0
```

### Cylindrical (1 rotational + 1 translational DOF)
```python
cyl = m.Constraints.createCylindrical(name='CYL_1',
                                      i_marker=shaft_mkr, j_marker=housing_mkr)
```

### Spherical (3 translational DOF removed)
```python
sph = m.Constraints.createSpherical(name='SPH_1',
                                    i_marker=ball_mkr, j_marker=socket_mkr)
```

### Universal / Hooke (2 rotational DOF)
```python
uni = m.Constraints.createUniversal(name='UNI_1',
                                    i_marker=shaft_i, j_marker=shaft_j)
# Equivalent:
uni = m.Constraints.createHooke(name='HOOKE_1',
                                i_marker=shaft_i, j_marker=shaft_j)
```

### Planar (2 translational + 1 rotational DOF)
```python
pln = m.Constraints.createPlanar(name='PLN_1',
                                 i_marker=plate_mkr, j_marker=ground_ref)
```

### Fixed (all DOF removed)
```python
fix = m.Constraints.createFixed(name='FIX_1',
                                i_marker=part_mkr, j_marker=ground_ref)
```

### Constant Velocity (Convel)
```python
cv = m.Constraints.createConvel(name='CV_1',
                                i_marker=driveshaft_i, j_marker=driveshaft_j)
```

### Screw
```python
scr = m.Constraints.createScrew(name='SCR_1',
                                i_marker=bolt_mkr, j_marker=nut_mkr,
                                pitch=1.5)      # mm per revolution
```

### Rack and Pinion
```python
rack = m.Constraints.createRackpin(name='RACK_1',
                                   i_marker=pinion_mkr, j_marker=rack_mkr,
                                   diameter_of_pitch=50.0)
```

---

## Constraint Primitives (JPrims)

JPrims are lower-pair constraints that remove individual DOF:

| JPrim | Method | DOF removed | Description |
|-------|--------|-------------|-------------|
| AtPoint | `createAtPoint()` | 3 trans | Coincident points |
| InLine | `createInline()` / `createInLine()` | 2 trans | Point on a line |
| InPlane | `createInPlane()` | 1 trans | Point on a plane |
| Orientation | `createOrientation()` | 3 rot | Aligned orientations |
| Parallel | `createParallel()` | 2 rot | Parallel z-axes |
| Perpendicular | `createPerpendicular()` | 1 rot | Perpendicular z-axes |
| PointPoint | `createPointPoint()` | 1 trans | Point-to-point distance |

```python
ip = m.Constraints.createInPlane(name='INPLN_1',
                                 i_marker=slider_mkr, j_marker=guide_mkr)
```

---

## Couplers and Gears

### Coupler (ratio between joint motions)
```python
coupler = m.Constraints.createCoupler(
    name='CPL_1',
    joints=[joint1, joint2],
    scale_factor=2.0,
    type_of_freedom=['rotational', 'rotational']
)
```

### Gear
```python
gear = m.Constraints.createGear(
    name='GEAR_1',
    joint_1=rev_driver,
    joint_2=rev_driven,
    common_velocity_marker=planet_mkr
)
```

---

## Motions

### Joint Motion (drives an existing joint)
```python
mo = m.Constraints.createJointMotion(
    name='DRIVE',
    joint=rev_crank,
    type_of_freedom='rotational',          # 'rotational' or 'translational'
    time_derivative='displacement',        # 'displacement' (default) or 'velocity'
    function='360D * TIME'                 # FUNCTION= expression string
)
```

### Generic Motion (marker-to-marker)
```python
mo2 = m.Constraints.createMotion(
    name='SLIDE_DRV',
    i_marker=slider_mkr, j_marker=rail_mkr,
    type_of_freedom='translational',
    time_derivative='velocity',
    function='STEP(TIME, 0, 0, 0.5, 100)'
)
```

### Point Motion (drives a floating point in space)
```python
pm = m.Constraints.createPointMotion(name='PT_DRV', ...)
```

---

## Friction on Joints

```python
fric = m.Forces.createFriction(
    name='FRIC_1',
    joint=rev,
    mu_static=0.3,
    mu_dynamic=0.2,
    stiction_transition_velocity=0.1
)
```

---

## General and User-Defined Constraints

```python
gc = m.Constraints.createGeneral(
    name='GEN_1',
    i_marker=mkr,
    function='DZ(.model.PART.cm, .model.ground.ref) - 50.0'
)
```
