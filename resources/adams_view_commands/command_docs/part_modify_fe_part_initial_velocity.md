# part modify fe_part initial_velocity

Allows you to create initial velocities on an existing FE Part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_part_name` | Existing fe part | Specifies the name of the fe part (required) |
| `vm` | Existing marker | Specifies a marker about whose axes the translational velocity vector components will be specified (optional). Default reference frame is FE Part’s local part reference frame. |
| `wm` | Existing marker | Specifies a marker about whose axes the angular velocity vector components will be specified (optional). If wm is not specified, the reference frame for the initial angular velocities is the FE Part’s local reference frame. |
| `vx` | Velocity | Specifies the initial translational velocity of all nodes of FE Part along the x-axis of the FE Part’s LPRF or vm if specified. |
| `vy` | Velocity | Specifies the initial translational velocity of all nodes of FE Part along the y-axis of the FE Part’s LPRF or vm if specified. |
| `vz` | Velocity | Specifies the initial translational velocity of all nodes of FE Part along the z-axis of the FE Part’s LPRF or vm if specified. |
| `wx` | Angular_velocity | Specifies the initial rotational velocity of all nodes of FE Part about the x-axis of the FE Part’s LPRF or wm if specified. |
| `wy` | Angular_velocity | Specifies the initial rotational velocity of all nodes of FE Part about the y-axis of the FE Part’s LPRF or wm if specified. |
| `wz` | Angular_velocity | Specifies the initial rotational velocity of all nodes of FE Part about the z-axis of the FE Part’s LPRF or wm if specified. |
