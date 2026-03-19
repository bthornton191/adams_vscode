# part create rigid_body initial_velocity

Allows you to create initial velocities on an existing part

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | An Existing Part | Specifies the part to be modified. You use this parameter to identify the existing part to affect with this command. |
| `vm` | An Existing Marker | An Existing Marker |
| `wm` | An Existing Marker | An Existing Marker |
| `vx` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the x-axis of the ground reference frame. |
| `no_vx` | True_Only | Specifies to "UNSET" the "vx" velocity initial condition for the specified part, if set. |
| `vy` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the y-axis of the ground reference frame. |
| `no_vy` | True_Only | Specifies to "UNSET" the "vy" velocity initial condition for the specified part, if set. |
| `vz` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the z-axis of the ground reference frame. |
| `no_vz` | True_Only | This is not the same as setting the value to zero. A zero velocity is not the same as "no" velocity. Therefore, by setting this parameter to true there is no longer a velocity initial condition for this element. |
| `wx` | Angular_Vel | Specifies the initial rotational velocity of the center-of-mass marker about its x-axis. |
| `no_wx` | True_Only | Specifies to "UNSET" the "wx" angular_velocity initial ondition for the specified part, if set. |
| `wy` | Angular_Vel | Specifies the initial rotational velocity of the center-of-mass marker about its y-axis. |
| `no_wy` | True_only | Specifies to "UNSET" the "wy" angular_velocity initial condition for the specified part, if set. |
| `wz` | Angular_vel | Specifies the initial rotational velocity of the center-of-mass marker about its z-axis. |
| `no_wz` | True_only | Specifies to "UNSET" the "wz" angular_velocity initial condition for the specified part, if set. |
