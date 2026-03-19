# constraint modify joint translational

Allows the modification of an existing translational joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | An Existing Joint | Specifies the joint to modify. You use this parameter to identify the existing joint to affect with this command. |
| `new_joint_name` | A New Joint | A New Joint |
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
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
