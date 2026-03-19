# constraint create joint revolute

Allows the creation of a revolute joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | New joint | Specifies the name of the new joint. You may use this name later to refer to this joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `rotational_ic` | Real | Specifies the initial rotational displacement on a revolute or cylindrical joint. |
| `no_rotational_ic` | True | Specifies that if a "rotational" velocity initial condition has been set, to "UNSET" the "rotational" velocity initial condition for the specified constraint. |
| `angular_velocity_ic` | Real | Specifies the initial angular velocity on a revolute or cylindrical joint. |
| `no_angular_velocity_ic` | True | Specifies that if an "angular_velocity" initial condition has been set, to "UNSET" the "angular_velocity" initial condition for the specified constraint. |
| `friction_enabled` | Yes/No/Preload_only | The constant default value will be used if this parameter is omitted |
| `delta_v` | Real | Real number should be greater than zero. |
| `maximum_deformation` | Real | Real number should be greater than zero. |
| `mu_dyn_rot` | Real | A real number greater than or equal to 0 |
| `mu_stat_rot` | Real | A real number greater than or equal to 0 |
| `max_fric_rot` | Torque | A real number greater than or equal to 0 |
| `preload_radial` | Force | A real number greater than or equal to 0 |
| `preload_axial` | Force | A real number greater than or equal to 0 |
| `inner_radius` | Length | A real number greater than or equal to 0 |
| `outer_radius` | Length | A real number greater than or equal to 0 |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `j_part_name` | Existing body | Specifies the part that is the second of two parts connected by this joint. Adams View connects one part at the J marker to the other at the I marker. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | Existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |
