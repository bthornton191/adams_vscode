# constraint create joint cylindrical

Allows the creation of a cylindrical joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | New joint name | Specifies the name of the new joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `translational_ic` | Length | Specifies the initial translational displacement on a translational or cylindrical joint. |
| `no_translational_ic` | True | Specifies to "UNSET" the "translational" velocity initial condition for the specified constraint, if set. |
| `velocity_ic` | Velocity | Specifies the initial translational velocity on a translational or cylindrical joint. |
| `no_velocity_ic` | True | Specifies to "UNSET" the velocity initial condition, if a VELOCITY_IC is set via any means. |
| `rotational_ic` | Real | Specifies the initial rotational displacement on a revolute or cylindrical joint. |
| `no_rotational_ic` | True | Specifies to "UNSET" the "rotational" velocity initial condition for the specified constraint, if set. |
| `angular_velocity_ic` | Angular_velocity | Specifies the initial angular velocity on a revolute or cylindrical joint. |
| `no_angular_velocity_ic` | True | Specifies to "UNSET" the "angular_velocity" initial condition for the specified constraint, if set. |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | Existing body | Specifies the part that is the second of two parts connected by this joint. |
| `location` | location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | Existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of the two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of the two parts connected by this joint. |
