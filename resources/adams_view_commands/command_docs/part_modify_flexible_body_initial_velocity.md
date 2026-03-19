# part modify flexible_body initial_velocity

Allows you to create initial velocities on an existing part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing flex body | Specifies the name of the flexible body |
| `vm` | Existing marker | Specifies a marker about whose axes the translational velocity vector components will be specified. |
| `wm` | Existing marker | Specifies a marker about whose axes the angular velocity vector components will be specified. |
| `vx` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the x-axis of the ground reference frame. |
| `no_vx` | True_only | Unsets the vx velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `vy` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the y-axis of the ground reference frame. |
| `no_vy` | True_only | Unsets the vy velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `vz` | Velocity | Specifies the initial translational velocity of the center-of-mass marker along the z-axis of the ground reference frame. |
| `no_vz` | True_only | Unsets the vz velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `wx` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its x-axis. |
| `no_wx` | True_only | Unsets the wx velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `wy` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its y-axis. |
| `no_wy` | True_only | Unsets the wy velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
| `wz` | Angular_velocity | Specifies the initial rotational velocity of the center-of-mass marker about its z-axis. |
| `no_wz` | True_only | Unsets the wz velocity initial condition for the specified part (true) so it no longer has a velocity initial condition. |
