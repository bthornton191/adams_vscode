# constraint create joint translational

Allows the creation of a translational joint. A translational joint is a single-degree-of-freedom joint that allows translational displacement of one part relative to another.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | A New Joint | Specifies the name of the new joint. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `translational_ic` | Length | Specifies the initial translational displacement on a translational or cylindrical joint. |
| `no_translational_ic` | True_only | Specifies that if a "translational" velocity initial condition has been set, to "UNSET" the "translational" velocity initial condition for the specified constraint. |
| `velocity_ic` | Velocity | Specifies the initial translational velocity on a translational or cylindrical joint. |
| `no_velocity_ic` | True_only | Specifies that if a VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `friction_enabled` | Enable_friction | Enable_friction |
| `delta_v` | Real | Real |
| `maximum_deformation` | Real | Real |
| `mu_dyn_trans` | Real | Real |
| `mu_stat_trans` | Real | Real |
| `max_fric_trans` | Real | Real |
| `preload_x` | Force | Force |
| `preload_y` | Force | Force |
| `height` | Real | Specify a height for the info window. |
| `width` | Real | Specify a width for the info window. |
| `i_part_name` | An Existing Body | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | An Existing Body | Specifies the part that is the second of two parts connected by this joint. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this joint. |
