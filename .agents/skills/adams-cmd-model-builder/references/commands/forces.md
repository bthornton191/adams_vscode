# Forces — CMD Reference

## Force Selection Guide

| Use this | When … |
|----------|--------|
| `spring_damper` | 1-DOF translational spring + damper along the line of sight between two markers |
| `rotational_spring_damper` | 1-DOF torsional spring + damper about parallel z-axes of two markers |
| `bushing` | 6-DOF compliant connection with independent diagonal stiffness/damping per DOF |
| `field` | 6-DOF force with a full 6×6 stiffness (and damping) matrix; captures cross-coupling between DOF |
| `beam` | Structural flexible member where cross-section geometry drives stiffness |
| `friction` | Friction force on an existing revolute, translational, or cylindrical joint |
| `single_component_force` | Custom scalar force or torque defined by a FUNCTION= expression |
| `vector_force` | Three-component force vector via FUNCTION= (no accompanying torque) |
| `general_force` | Six-component force + torque all from a single FUNCTION= expression |
| `single_component_torque` | Pure torque along one axis via FUNCTION= |
| `motion_generator` | Prescribe kinematics rather than apply a force load |
| `gravitational` | Constant body-force acceleration applied to all parts |

---

## Gravity

```cmd
force create body gravitational &
    gravity_field_name  = .model.gravity &
    x_component_gravity = 0.0 &
    y_component_gravity = -9806.65 &
    z_component_gravity = 0.0
```

- Values in length/time² units. Use −9806.65 for mm-kg-s; −9.80665 for MKS.
- There can only be one gravity field per model.

---

## Spring-Damper

```cmd
force create element_like translational_spring_damper &
    spring_damper_name     = .model.spring_main &
    i_marker_name          = .model.body.spring_i_mkr &
    j_marker_name          = .model.ground.spring_j_mkr &
    stiffness              = 5000.0 &
    damping                = 100.0 &
    preload                = 0.0 &
    displacement_at_preload = 250.0
```

- `displacement_at_preload` = free (natural) length (the distance at which preload = 0).
- Force = −K × (deformation) − C × (rate of deformation). Positive = compression.

---

## Bushing (6-DOF Spring-Damper)

```cmd
force create element_like bushing &
    bushing_name  = .model.bush_mount &
    i_marker_name = .model.subframe.bush_i_mkr &
    j_marker_name = .model.chassis.bush_j_mkr &
    stiffness     = 8000.0, 8000.0, 12000.0, 200.0, 200.0, 500.0 &
    damping       = 80.0,   80.0,   120.0,   2.0,   2.0,   5.0
```

- Six stiffness values: Tx, Ty, Tz, Rx, Ry, Rz (force/length, force/length, force/length, torque/angle, …).
- Six damping values in the same order.

---

## Rotational Spring-Damper

```cmd
force create element_like rotational_spring_damper &
    spring_damper_name      = .model.torsion_spring &
    i_marker_name           = .model.arm.pivot_i_mkr &
    j_marker_name           = .model.base.pivot_j_mkr &
    stiffness               = 200.0 &
    damping                 = 2.0 &
    displacement_at_preload = 0.0D
```

- The **z-axes of the I and J markers must be parallel and point in the same direction**. Misaligned z-axes produce unpredictable results.
- `stiffness` in torque/angle units (N·mm/deg when using mm-kg-s units).
- `displacement_at_preload` is the free (neutral) angle; set `0.0D` for zero-preload.
- Torque on I marker: `torque = -C * dα/dt - K * (α - displacement_at_preload)`

---

## Beam (Euler-Bernoulli)

```cmd
force create element_like beam &
    beam_name     = .model.beam_1 &
    i_marker_name = .model.link.end_i_mkr &
    j_marker_name = .model.base.end_j_mkr &
    area          = 78.54 &
    ixx           = 490.9 &
    iyy           = 490.9 &
    length        = 300.0 &
    youngs_modulus = 2.1e5 &
    shear_modulus  = 8.1e4
```

- `area` in length², moment of inertia in length⁴.
- Both I and J markers must be at the **beam ends**; beam axis = line between them.

---

## Field (6×6 Stiffness+Damping Matrix)

A `field` applies a 6-DOF action-reaction force+torque between two markers using a full 6×6 stiffness matrix and 6×6 damping matrix. Unlike `bushing` (which uses independent per-DOF values), a `field` can capture **cross-coupling** between translational and rotational DOF.

```cmd
force create element_like field &
    field_name       = .model.chassis_mount &
    i_marker_name    = .model.subframe.mount_i_mkr &
    j_marker_name    = .model.chassis.mount_j_mkr &
    stiffness_matrix = 1.0e4, 0, 0, 0, 0, 0, &
                       0, 1.0e4, 0, 0, 0, 0, &
                       0, 0, 1.2e4, 0, 0, 0, &
                       0, 0, 0, 500, 0, 0, &
                       0, 0, 0, 0, 500, 0, &
                       0, 0, 0, 0, 0, 800 &
    damping_ratio    = 0.05
```

- `stiffness_matrix` — 36 values entered **column-major** (column 1 top-to-bottom, then column 2, …). The first 6 values are the first column `[K11,K21,K31,K41,K51,K61]`.
- The matrix order is: [Fx, Fy, Fz, Tx, Ty, Tz] vs [x, y, z, α, β, γ] of the I marker relative to J marker.
- `damping_ratio` — scalar multiplier applied to `stiffness_matrix` to derive damping: `C = damping_ratio × K`.
- Alternative: use `matrix_of_damping_terms` (another 36 values) to specify the damping matrix directly instead of `damping_ratio`.
- Optional `translation_at_preload` and `rotation_at_preload` (3 values each) set the reference displacement at which preload forces apply.
- For nonlinear behaviour, use `user_function` to pass constants to an Adams FIESUB user subroutine instead of specifying matrix parameters.

---

## Friction

Adds Coulomb friction to an existing revolute, translational, or cylindrical joint.

```cmd
force create element_like friction &
    friction_name  = .model.rev_pin_friction &
    joint_name     = .model.rev_pin &
    mu_static      = 0.12 &
    mu_dynamic     = 0.10 &
    reaction_arm   = 10.0 &
    effect         = all
```

- `joint_name` — the existing joint this friction acts on. Works with `revolute`, `translational`, and `cylindrical` joints.
- `mu_static` / `mu_dynamic` — static and kinetic friction coefficients.
- `reaction_arm` — effective moment arm (in length units) used to compute the friction torque from the joint reaction force.
- `effect = all` captures both stiction and sliding; use `stiction` or `sliding` to isolate phases.
- Optional `bending_moment = on` and `torsional_moment = on` include the contributions of bending and torsional moments for revolute joints.
- Optional `formulation = lugre` switches to the LuGre dynamic friction model (requires additional bristle stiffness / damping parameters).

---

## Single Component Force (SFORCE)

A custom scalar force or torque defined by a FUNCTION= expression. Most flexible 1-DOF load.

### Action-reaction force

```cmd
force create direct single_component_force &
    single_component_force_name = .model.scf_aero &
    i_marker_name               = .model.wing.aero_mkr &
    j_marker_name               = .model.body.ref_mkr &
    action_only                 = off &
    function                    = "STEP(TIME, 0, 0, 2, 500) * COS(AZ(.model.wing.aero_mkr))"
```

### Action-only force

```cmd
force create direct single_component_force &
    single_component_force_name = .model.scf_driver &
    i_marker_name               = .model.part.load_mkr &
    action_only                 = on &
    function                    = "STEP(TIME, 0.5, 0, 1.5, 2000)"
```

- `action_only = on` means no equal-and-opposite reaction.
- When `action_only = off` (default), the reaction is applied at the J marker.
- Force direction = **along the line of sight from the I marker to the J marker** (not the z-axis of the I marker).
- The name parameter is `single_component_force_name`, not `force_name`.

---

## Single Component Torque

```cmd
force create direct single_component_force &
    type_of_freedom              = rotational &
    single_component_force_name  = .model.torq_motor &
    i_marker_name                = .model.rotor.axis_mkr &
    j_marker_name                = .model.stator.axis_mkr &
    action_only                  = off &
    function                     = "500 * SIN(2 * PI * 10 * TIME)"
```

---

## Vector Force (VFORCE — 3-component force, no torque)

Use a vector force when the direction of the force changes during simulation (e.g., aero loads, contact normals). Use `j_part_name` instead of `j_floating_marker` — Adams creates the required floating marker automatically.

```cmd
force create direct force_vector &
    force_vector_name = .model.vf_wind &
    i_marker_name     = .model.vehicle.aero_mkr &
    j_part_name       = .model.ground &
    ref_marker_name   = .model.vehicle.aero_mkr &
    function_x        = "0.5 * 1.225e-9 * 2.2 * STEP(TIME,0,0,1,30)**2" &
    function_y        = "0" &
    function_z        = "0"
```

- `j_part_name` specifies the part that receives the reaction force; Adams auto-creates the floating marker.

---

## General Force (GFORCE — 3 forces + 3 torques)

```cmd
force create direct general_force &
    general_force_name = .model.gf_aero &
    i_marker_name      = .model.body.cm_mkr &
    j_part_name        = .model.ground &
    ref_marker_name    = .model.ground.global_mkr &
    x_force_function   = "FX_EXPR" &
    y_force_function   = "FY_EXPR" &
    z_force_function   = "FZ_EXPR" &
    x_torque_function  = "TX_EXPR" &
    y_torque_function  = "TY_EXPR" &
    z_torque_function  = "TZ_EXPR"
```

- Each force and torque component has its own parameter.
- Use `j_part_name` — Adams auto-creates the floating marker.

---

## Data Elements: Spline (for non-linear force maps)

```cmd
data_element create spline &
    spline_name = .model.force_curve &
    x           = 0.0, 5.0, 10.0, 15.0 &
    y           = 0.0, 100.0, 350.0, 600.0

! Use spline in a force FUNCTION=
force create direct single_component_force &
    single_component_force_name = .model.scf_nonlin &
    i_marker_name = .model.body.load_mkr &
    action_only   = on &
    function      = "AKISPL(DZ(.model.body.load_mkr), 0, .model.force_curve, 0)"
```

---

## See also

- [Function expressions index](../function-expressions/README.md)
- [IMPACT](../function-expressions/impact.md) / [BISTOP](../function-expressions/bistop.md) — contact forces
- [STEP](../function-expressions/step.md) — smooth force ramp
- [Constraints](constraints.md)
