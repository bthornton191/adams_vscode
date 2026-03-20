# Model, Parts, and Markers — CMD Reference

## Units

Set units **before** creating any geometry so that all subsequent values are interpreted correctly.

```cmd
defaults units &
    length = mm &
    force  = newton &
    mass   = kg &
    time   = sec
```

Common unit systems:

| System | length | force | mass | time |
|--------|--------|-------|------|------|
| IPS | inch | pound_force | pound_mass | sec |
| MKS (SI) | meter | newton | kg | sec |
| mmNs | mm | newton | tonne | sec |
| CGS | cm | dyne | gram | sec |

---

## Create a Model

```cmd
model create model_name = MY_MODEL
```

---

## Create a Rigid Part

```cmd
part create rigid_body name_and_position &
    part_name   = .my_model.link_a &
    location    = 0.0, 0.0, 100.0 &
    orientation = 0.0D, 0.0D, 0.0D
```

- `location` = x, y, z position of the part reference marker, in model units.
- `orientation` = psi, theta, phi (Body-313 Euler angles, degrees by convention here — append `D`).
- Do **not** specify `adams_id` — Adams auto-assigns all IDs.

## Set Part Mass Properties

```cmd
part modify rigid_body mass_properties &
    part_name = .my_model.link_a &
    mass      = 1.5 &
    ixx       = 1200.0 &
    iyy       = 1200.0 &
    izz       = 50.0 &
    ixy       = 0.0 &
    izx       = 0.0 &
    iyz       = 0.0
```

- Inertia values are about the center of mass marker, in mass × length² units.
- Adams **auto-creates** `.my_model.link_a.cm` and positions it at the part reference origin when this command runs. The `cm` marker is then available for use in other commands.
- **Do not pass `center_of_mass_marker`** here — `.cm` does not exist yet when the command is issued, and Adams will error: `No Marker was found because 'cm' does not exist`. Only specify `center_of_mass_marker` if you want to redirect the CM to a different, already-existing marker (unusual).

## Create a Point Mass

```cmd
part create point_mass name_and_position &
    point_mass_name = .my_model.ball &
    location        = 50.0, 0.0, 0.0

! Create the CM marker BEFORE setting mass properties
marker create &
    marker_name = .my_model.ball.cm &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D

part modify point_mass mass_properties &
    point_mass_name       = .my_model.ball &
    mass                  = 0.5 &
    center_of_mass_marker = .my_model.ball.cm
```

- A point mass has no rotational inertia — useful for pendulum bobs, concentrated masses.
- Use `name_and_position` to create and position it.
- Create the `.cm` marker explicitly **before** calling `mass_properties`.
- Pass `center_of_mass_marker` to link the CM marker in the `mass_properties` call.
- **Do NOT use `constraint create joint fixed`** with a point mass — it only supports `spherical` joints, `atpoint`, `inline`, and `inplane` joint primitives.

---

## Create a Marker

```cmd
marker create &
    marker_name = .my_model.link_a.pin_mkr &
    location    = 0.0, 0.0, 0.0 &
    orientation = 0.0D, 0.0D, 0.0D
```

- `location` is in the coordinate frame of the parent part.
- `orientation` (psi, theta, phi) rotates the marker axes. Use `90D` etc. to align axes.

## Modify a Marker

```cmd
marker modify &
    marker_name = .my_model.link_a.pin_mkr &
    location    = 0.0, 0.0, 25.0 &
    orientation = 0.0D, 90.0D, 0.0D
```

---

## Floating Markers

Floating markers (`floating_marker`) are not fixed to a part — their position is determined by a constraint or force element at runtime. Used internally by certain force types.

```cmd
marker create floating_marker &
    floating_marker_name = .my_model.link_a.float_mkr
```

---

## See also

- [Naming conventions](../naming-conventions.md)
- [Constraints](constraints.md)
- [Forces](forces.md)
- [Geometry](geometry.md)
