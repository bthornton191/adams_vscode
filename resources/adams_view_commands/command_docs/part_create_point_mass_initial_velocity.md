# part create point_mass initial_velocity

Allows you to create initial velocities on an existing point mass.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `point_mass_name` | Existing point_mass | Specifies the name of an existing point mass. |
| `vm` | Existing marker | Specifies a marker about whose axes the translational velocity vector components will be specified. |
| `vx` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the x-axis of the ground reference frame. |
| `no_vx` | True_only | Unsets the vx velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `vy` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the y-axis of the ground reference frame. |
| `no_vy` | True_only | Unsets the vy velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `vz` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the z-axis of the ground reference frame. |
| `no_vz` | True_only | Unsets the vz velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
