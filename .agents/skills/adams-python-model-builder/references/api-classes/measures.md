# Measures — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/adamspy/Measure.pyi`

All measures are created via `model.Measures.createX(**kwargs)`.

See also [simulation-analysis.md](simulation-analysis.md) for post-processing usage patterns.

---

## Object Measure

Measures a named characteristic of a specific Adams object (part, joint, force, etc.):

```python
meas = m.Measures.createObject(
    name='MY_MEAS',
    object=link_body,                    # Adams object to measure
    characteristic='cm_velocity',        # what to measure (see below)
    component='x_component',             # which component
    coordinate_rframe=ref_mkr,           # optional: express in this frame
    from_first=False,                    # True = from i-marker, False = from j-marker
    legend='Link CM Velocity X',         # plot legend
    create_measure_display=True          # show display window in GUI
)
```

**Characteristic options** (subset — see Measure.pyi for full list):

| Characteristic | Applies to |
|---------------|------------|
| `cm_position` | Part |
| `cm_velocity` | Part |
| `cm_acceleration` | Part |
| `cm_angular_velocity` | Part |
| `cm_angular_acceleration` | Part |
| `euler_angles` | Part |
| `ax_ay_az_projection_angles` | Part |
| `translational_velocity` | Part |
| `translational_acceleration` | Part |
| `angular_velocity` | Part |
| `kinetic_energy` | Part |
| `potential_energy_delta` | Part |
| `element_force` | Joint, Force |
| `element_torque` | Joint, Force |
| `power_consumption` | Force |
| `pressure_angle` | Constraint |

**Component options**: `x_component`, `y_component`, `z_component`, `mag_component`, `r_component`, `rho_component`, `theta_component`, `phi_component`

---

## Point-to-Point Measure

```python
d = m.Measures.createPt2pt(
    name='DIST_AB',
    from_point=mkr_a,
    to_point=mkr_b,
    characteristic='translational_displacement',
    component='mag_component',
    coordinate_rframe=None
)
```

---

## Angle Measure (3-point)

```python
ang = m.Measures.createAngle(
    name='CRANK_ANGLE',
    first_point=mkr_a,
    middle_point=mkr_pivot,
    last_point=mkr_b
)
```

---

## Orientation Measure

```python
ori = m.Measures.createOrient(
    name='EULER_PSI',
    to_frame=body_mkr,
    from_frame=ground_mkr,
    characteristic='euler_angles',
    component='phi_component'
)
```

---

## Function Measure

Arbitrary FUNCTION= expression evaluated during the simulation:

```python
fm = m.Measures.createFunction(
    name='SPRING_DEFL',
    function='DM(.model.LINK.pin_i, .model.GROUND.pin_j) - 250.0',
    units='length',               # unit type for axis label
    legend='Spring Deflection',
    create_measure_display=True,
    routine='',
    user_function=''
)
```

---

## Range Measure

Computes min/max/rms of another measure over time:

```python
rng = m.Measures.createRange(
    name='FORCE_MAX',
    range_measure_type='maximum',   # 'minimum', 'maximum', 'rms', 'average'
    of_measure_name='.model.MEAS_1'
)
```

---

## Point Measure

```python
pt = m.Measures.createPoint(
    name='POINT_POS',
    point=mkr,
    characteristic='cm_position',
    component='z_component'
)
```
