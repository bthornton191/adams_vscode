# Forces — Python API Reference

> **Authoritative stub**: `references/adamspy-stubs/Force.pyi`

All forces are created via `model.Forces.createX(**kwargs)`.

---

## Gravity

```python
grav = m.Forces.createGravity(name='GRAVITY')
grav.xyz_component_gravity = [0.0, -9806.65, 0.0]   # mm-kg-s units
```

- One gravity field per model.
- Use −9806.65 for mm-kg-s; −9.80665 for m-kg-s.

---

## Translational Spring-Damper

```python
spr = m.Forces.createTranslationalSpringDamper(
    name='SPRING_1',
    i_marker=link_mkr,
    j_marker=ground_mkr,
    stiffness=5000.0,               # N/mm
    damping=100.0,                  # N·s/mm
    displacement_at_preload=250.0,  # free (natural) length in model length units
    force_preload=0.0               # preload force at natural length
)
```

**Properties**: `stiffness`, `damping`, `displacement_at_preload`, `force_preload`, `i_marker`, `j_marker`.

---

## Rotational Spring-Damper

```python
rspr = m.Forces.createRotationalSpringDamper(
    name='TORSION_1',
    i_marker=shaft_mkr,
    j_marker=housing_mkr,
    r_stiff=1000.0,       # N·mm/deg
    r_damp=10.0,
    displacement_at_preload=0.0,
    torque_preload=0.0
)
```

---

## Bushing (6-DOF)

```python
bush = m.Forces.createBushing(
    name='BUSH_1',
    i_marker=subframe_mkr,
    j_marker=chassis_mkr,
    stiffness=[Kx, Ky, Kz, Kaa, Kbb, Kcc],   # translational then rotational
    damping  =[Cx, Cy, Cz, Caa, Cbb, Ccc],
    force_preload=[0, 0, 0, 0, 0, 0],
    torque_preload=[0, 0, 0, 0, 0, 0]
)
```

`tstiffness` and `tdamping` are aliases for the rotational stiffness/damping terms.

---

## Beam (Euler-Bernoulli / Timoshenko)

```python
beam = m.Forces.createBeam(
    name='BEAM_1',
    i_marker=node_i,
    j_marker=node_j,
    length=500.0,                   # undeformed length
    youngs_modulus=2.07e5,          # MPa (for mm-tonne-s)
    shear_modulus=8.0e4,
    area_of_cross_section=400.0,    # mm²
    ixx=5000.0,                     # torsional second moment
    iyy=2000.0,                     # bending second moment (y)
    izz=2000.0,                     # bending second moment (z)
    damping_ratio=0.01,
    y_shear_area_ratio=0.9,
    z_shear_area_ratio=0.9,
    formulation='timoshenko'        # or 'euler_bernoulli'
)
```

---

## Field (Full 6×6 Stiffness Matrix)

```python
fld = m.Forces.createField(
    name='FIELD_1',
    i_marker=mkr_i,
    j_marker=mkr_j,
    stiffness_matrix=[...],   # 36-element list (row-major)
    damping_ratio=0.02
)
```

---

## Single Component Force (SFORCE)

Scalar force or torque along one direction, driven by a `FUNCTION=` expression.

```python
sf = m.Forces.createSingleComponentForce(
    name='SFORCE_1',
    i_marker=body_mkr,
    j_marker=ground_mkr,
    type_of_freedom='translational',   # 'translational' (default) or 'rotational'
    function='STEP(TIME, 0, 0, 1, 500)',
    action_only=False                   # True = force on i-body only, no reaction
)
```

**Properties**: `function`, `type_of_freedom`, `action_only`, `user_function`, `routine`.

---

## Force Vector (VFORCE — 3-component translational)

```python
vf = m.Forces.createForceVector(
    name='VFORCE_1',
    i_marker_name='.model.body.mkr',
    j_floating_marker_name='.model.body.fmkr',
    ref_marker_name='.model.ground.ref',
    x_force_function='0',
    y_force_function='-9.81 * .model.body.mass',
    z_force_function='0'
)
```

The `j_floating_marker` is a `FloatingMarker` — it follows the i-body but belongs to the j-body for reaction purposes.

---

## Torque Vector (VTORQUE — 3-component)

```python
vt = m.Forces.createTorqueVector(
    name='VTORQUE_1',
    i_marker=mkr_i,
    j_floating_marker=fmkr_j,
    ref_marker=ground_ref,
    x_torque_function='0',
    y_torque_function='500 * sin(2 * pi * TIME)',
    z_torque_function='0'
)
```

---

## General Force (GFORCE — 6-component)

```python
gf = m.Forces.createGeneralForce(
    name='GFORCE_1',
    i_marker=mkr_i,
    j_floating_marker=fmkr_j,
    ref_marker=ref_mkr,
    x_force_function='Fx_expr',
    y_force_function='Fy_expr',
    z_force_function='Fz_expr',
    xyz_force_function='...'    # alternative: single expression returning 3 values
)
```

---

## Modal Force (on FlexBody)

```python
mf = m.Forces.createModalForce(
    name='MODAL_1',
    flexible_body=flex_part,
    scale_function='STEP(TIME, 0, 0, 1, 1)',
    force_function='...'
)
```

---

## Applied Force / Torque (action-only)

```python
af = m.Forces.createAppliedForce(name='APPLIED_1', i_marker=mkr, ...)
at = m.Forces.createAppliedTorque(name='TORQUE_1', i_marker=mkr, ...)
```

---

## Friction

Add friction to an existing joint:

```python
fric = m.Forces.createFriction(
    name='FRIC_1',
    joint=revolute_joint,
    mu_static=0.3,
    mu_dynamic=0.25,
    stiction_transition_velocity=0.1,
    max_stiction_deformation=0.01,
    transition_velocity_coefficient=0.1
)
```
