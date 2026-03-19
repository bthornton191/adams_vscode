# constraint modify joint cylindrical

Allows the modifcation of a cylindrical joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | New joint name | Specifies the name of an existing joint. |
| `new_joint_name` | New joint name | Specifies new name of the joint. You may use this name later to refer to this joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `translational_ic` | Length | Specifies the initial translational displacement on a translational or cylindrical joint. |
| `no_translational_ic` | True | Specifies that if a "translational" velocity initial condition has been set, to "UNSET" the "translational" velocity initial condition for the specified constraint. |
| `velocity_ic` | Velocity | Specifies the initial translational velocity on a translational or cylindrical joint. |
| `no_velocity_ic` | True | Specifies that if a VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `rotational_ic` | Real | Specifies the initial rotational displacement on a revolute or cylindrical joint. |
| `no_rotational_ic` | True | Specifies that if a "rotational" velocity initial condition has been set, to "UNSET" the "rotational" velocity initial condition for the specified constraint. |
| `angular_velocity_ic` | Angular_velocity | Specifies the initial angular velocity on a revolute or cylindrical joint. |
| `no_angular_velocity_ic` | True | Specifies that if an "angular_velocity" initial condition has been set, to "UNSET" the "angular_velocity" initial condition for the specified constraint. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |
