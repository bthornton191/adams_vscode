# part modify point_mass initial_velocity

Allows you to modify initial velocities on an existing point_mass.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `point_mass_name` | An Existing Point_Mass | Specifies the point_mass to be modified. You use this parameter to identify the existing point_mass to be affected with this command. |
| `vm` | An Existing Marker | An Existing Marker |
| `vx` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the x-axis of the ground reference frame. |
| `no_vx` | True_Only | Specifies to "UNSET" the "vx" velocity initial condition for the specified part, if set. |
| `vy` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the y-axis of the ground reference frame. |
| `no_vy` | True_Only | Specifies to "UNSET" the "vy" velocity initial condition for the specified part, if set. |
| `vz` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the z-axis of the ground reference frame. |
| `no_vz` | True_Only | This is not the same as setting the value to zero. A zero velocity is not the same as "no" velocity. Therefore, by setting this parameter to true, there is no longer a velocity initial condition for this element. |
