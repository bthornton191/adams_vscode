# constraint modify joint revolute

Allows the modification of a revolute joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | Existing joint | Specifies the name of the joint to be modified. You may use this name later to refer to this joint. |
| `new_joint_name` | New joint name | Specified the name of the new joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `rotational_ic` | Real | Specifies the initial rotational displacement on a revolute or cylindrical joint. |
| `no_rotational_ic` | True | Specifies that if a "rotational" velocity initial condition has been set, to "UNSET" the "rotational" velocity initial condition for the specified constraint. |
| `angular_velocity_ic` | Real | Specifies the initial angular velocity on a revolute or cylindrical joint. |
| `no_angular_velocity_ic` | True | Specifies that if an "angular_velocity" initial condition has been set, to "UNSET" the "angular_velocity" initial condition for the specified constraint. |
| `friction_enabled` | Yes/No/Preload_only | The constant default value will be used if this parameter is omitted. |
| `delta_v` | Real | Real number should be greater than zero. |
| `maximum_deformation` | Real | Real number should be greater than zero. |
| `mu_dyn_rot` | Real | A real number greater than or equal to 0 |
| `mu_stat_rot` | Real | A real number greater than or equal to 0 |
| `max_fric_rot` | Torque | A real number greater than or equal to 0 |
| `preload_radial` | Force | A real number greater than or equal to 0 |
| `preload_axial` | Force | A real number greater than or equal to 0 |
| `inner_radius` | Length | A real number greater than or equal to 0 |
| `outer_radius` | Length | A real number greater than or equal to 0 |
| `relative_to` | Existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |
