# part modify fe_part nodal_ics

Allows you to prescribe nodal initial velocities on an existing FE Part.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_node_name` | Existing fe node | Specifies the name ID of the fe node for the fe part (required) |
| `vx` | Velocity | Specifies the initial translational velocity for the fe node along the x-axis of the FE Part’s LPRF or vm if specified. |
| `vy` | Velocity | Specifies the initial translational velocity for the fe node along the y-axis of the FE Part’s LPRF or vm if specified. |
| `vz` | Velocity | Specifies the initial translational velocity for the fe node along the z-axis of the FE Part’s LPRF or vm if specified. |
| `wx` | Angular_velocity | Specifies the initial rotational velocity for the fe node about the x-axis of the FE Part’s LPRF or wm if specified. |
| `wy` | Angular_velocity | Specifies the initial rotational velocity for the fe node about the y-axis of the FE Part’s LPRF or wm if specified. |
| `wz` | Angular_velocity | Specifies the initial rotational velocity for the fe node about the z-axis of the FE Part’s LPRF or wm if specified. |
