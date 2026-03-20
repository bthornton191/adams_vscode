# Constraints — CMD Reference

Constraints remove degrees of freedom between parts. All joint commands follow the pattern:

```cmd
constraint create joint <type> &
    joint_name     = .model.joint_name &
    adams_id       = <n> &
    i_marker_name  = .model.part_a.i_mkr &
    j_marker_name  = .model.part_b.j_mkr
```

The **I marker** is on the moving part; the **J marker** is on the reference (or other) part.

---

## Joint Types

### Revolute (1 rotational DOF)

```cmd
constraint create joint revolute &
    joint_name    = .model.rev_knee &
    adams_id      = 1 &
    i_marker_name = .model.lower_leg.knee_mkr &
    j_marker_name = .model.upper_leg.knee_mkr
```

- Allows rotation about the **z-axis** of the J marker.
- Removes 5 DOF (3 translational + 2 rotational).

### Translational / Prismatic (1 translational DOF)

```cmd
constraint create joint translational &
    joint_name    = .model.trans_slider &
    adams_id      = 2 &
    i_marker_name = .model.slider.axis_mkr &
    j_marker_name = .model.guide.axis_mkr
```

- Allows translation along the **z-axis** of the J marker.
- Removes 5 DOF.

### Spherical / Ball-and-Socket (3 rotational DOF)

```cmd
constraint create joint spherical &
    joint_name    = .model.sph_shoulder &
    adams_id      = 3 &
    i_marker_name = .model.arm.ball_mkr &
    j_marker_name = .model.body.socket_mkr
```

- Allows rotation in all three axes; no translation.
- Removes 3 DOF.

### Cylindrical (1 translational + 1 rotational DOF along same axis)

```cmd
constraint create joint cylindrical &
    joint_name    = .model.cyl_shaft &
    adams_id      = 4 &
    i_marker_name = .model.shaft.axis_mkr &
    j_marker_name = .model.housing.bore_mkr
```

- Allows both rotation and translation along the z-axis of J marker.
- Removes 4 DOF.

### Fixed / Weld (0 DOF)

```cmd
constraint create joint fixed &
    joint_name    = .model.fix_bracket &
    adams_id      = 5 &
    i_marker_name = .model.bracket.ref_mkr &
    j_marker_name = .model.frame.mount_mkr
```

- Removes all 6 DOF — parts move together rigidly.

### Planar (3 DOF: 2 translational in plane + 1 rotation about normal)

```cmd
constraint create joint planar &
    joint_name    = .model.plane_contact &
    adams_id      = 6 &
    i_marker_name = .model.block.face_mkr &
    j_marker_name = .model.table.surface_mkr
```

- Constrains the I marker's z-axis to remain in the xy-plane of J marker.

### Universal / Hooke (2 rotational DOF)

```cmd
constraint create joint universal &
    joint_name    = .model.univ_shaft &
    adams_id      = 7 &
    i_marker_name = .model.shaft_in.u_mkr &
    j_marker_name = .model.shaft_out.u_mkr
```

---

## Coupler (Gear / Rack-and-Pinion)

```cmd
constraint create complex_joint coupler &
    coupler_name        = .model.gear_1_2 &
    joint_name          = .model.rev_gear1, .model.rev_gear2 &
    type_of_freedom     = rot_rot &
    motion_multipliers  = 1.0, -0.5
```

- **Full command**: `constraint create complex_joint coupler` — `constraint create coupler` is not valid.
- `motion_multipliers` define the gear ratio: applies `motion_multipliers[1] * ω1 + motion_multipliers[2] * ω2 = 0`. For a 3:1 ratio with opposite directions: `motion_multipliers = 1.0, -0.333`.
- `type_of_freedom`: `rot_rot` (both rotational), `trans_trans` (both translational), or `rot_trans` (mixed).

---

## Motion Generator

Prescribes a position, velocity, or acceleration profile on a joint DOF.

```cmd
constraint create motion_generator &
    motion_name      = .model.motion_1 &
    joint_name       = .model.rev_actuator &
    type_of_freedom  = rotational &
    time_derivative  = displacement &
    function         = "STEP(TIME, 0, 0, 2, 180D)"
```

- `type_of_freedom`: `rotational` or `translational`
- `time_derivative`: `displacement` (default), `velocity`, or `acceleration`. **Always specify this explicitly** — omitting it when your function defines velocity (e.g. a HAVSIN ramp of angular velocity) will cause Adams to treat the function as displacement.
- `function`: any valid FUNCTION= expression
- The motion **replaces** the joint DOF with the prescribed trajectory; the joint reaction force is computed by the solver.

### Example: Velocity ramp using HAVSIN

```cmd
! Ramp angular velocity 0 → 120 deg/s over 0.5 s, then hold
constraint create motion_generator &
    motion_name      = .model.motion_drive &
    joint_name       = .model.rev_input &
    type_of_freedom  = rotational &
    time_derivative  = velocity &
    function         = "HAVSIN(TIME, 0.0, 0.5, 0.0, 120D)"
```

---

## See also

- [Forces](forces.md) — apply loads rather than constrain motion
- [Scripting](scripting.md) — loop over joints in parametric models
