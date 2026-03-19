# part create external_system initial_velocity

Allows you to create initial velocities on an existing external system part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `external_system_name` | Existing external system | You use this parameter to identify the existing external system part to affect with this command. |
| `vm` | Existing marker | Specifies the marker representing the translational velocity. |
| `wm` | Existing marker | Specifies the marker representing the rotational velocity about it. |
| `vx` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the x-axis of the ground reference frame. |
| `no_vx` | True_only | Specifies to "UNSET" the "vx" velocity initial condition for the specified part, if set. |
| `vy` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the y-axis of the ground reference frame. |
| `no_vy` | True_only | Specifies to "UNSET" the "vy" velocity initial condition for the specified part, if set. |
| `vz` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the z-axis of the ground reference frame. |
| `no_vz` | True_only | This is not the same as setting the value to zero. A zero velocity is not the same as "no" velocity. Therefore, by setting this parameter to true there is no longer a velocity initial condition for this element. |
| `wx` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its x-axis. |
| `no_wx` | True_only | Specifies to "UNSET" the "wx" angular_velocity initial condition for the specified part, if set. |
| `wy` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its y-axis. |
| `no_wy` | True_only | Specifies to "UNSET" the "wy" angular_velocity initial condition for the specified part, if set. |
| `wz` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its z-axis. |
| `no_wz` | True_only | Specifies to "UNSET" the "wz" angular_velocity initial condition for the specified part, if set. |
