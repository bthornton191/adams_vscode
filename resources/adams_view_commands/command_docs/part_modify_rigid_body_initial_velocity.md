# part modify rigid_body initial_velocity

Allows you to set or modify the initial translational and rotational velocity conditions of one or more rigid body parts.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | An Existing Part | Specifies one or more rigid body parts whose initial velocity is to be set. |
| `vm` | An Existing Marker | Specifies a marker that defines the coordinate system used to express the translational velocity components. |
| `wm` | An Existing Marker | Specifies a marker that defines the coordinate system used to express the rotational velocity components. |
| `vx` | Velocity | Specifies the initial translational velocity in the X direction of the VM marker. |
| `no_vx` | True | Clears any previously set initial velocity in the X direction. |
| `vy` | Velocity | Specifies the initial translational velocity in the Y direction of the VM marker. |
| `no_vy` | True | Clears any previously set initial velocity in the Y direction. |
| `vz` | Velocity | Specifies the initial translational velocity in the Z direction of the VM marker. |
| `no_vz` | True | Clears any previously set initial velocity in the Z direction. |
| `wx` | Angular Velocity | Specifies the initial angular velocity about the X axis of the WM marker. |
| `no_wx` | True | Clears any previously set initial angular velocity about the X axis. |
| `wy` | Angular Velocity | Specifies the initial angular velocity about the Y axis of the WM marker. |
| `no_wy` | True | Clears any previously set initial angular velocity about the Y axis. |
| `wz` | Angular Velocity | Specifies the initial angular velocity about the Z axis of the WM marker. |
| `no_wz` | True | Clears any previously set initial angular velocity about the Z axis. |
