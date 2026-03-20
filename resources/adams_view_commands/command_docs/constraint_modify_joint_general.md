# constraint modify joint general

Allows the modification of an existing joint, including changing its type.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | Existing joint | Specifies the name of the joint to be modified. |
| `new_joint_name` | New joint name | Specifies the new name of the joint. You may use this name later to refer to this joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `type` | Enum | Specifies the new type of the joint. Valid values: `translational`, `revolute`, `cylindrical`, `universal`, `spherical`, `planar`, `rackpin`, `screw`, `convel`, `fixed`, `hooke`, `atpoint`, `inline`, `inplane`, `orientation`, `parallel_axes`, `perpendicular`, `point_point`. |
| `translational_ic` | Length | Specifies the initial translational displacement on a translational or cylindrical joint. |
| `no_translational_ic` | True | Specifies that if a "translational" initial condition has been set, to "UNSET" the translational initial condition for the specified constraint. |
| `velocity_ic` | Velocity | Specifies the initial translational velocity on a translational or cylindrical joint. |
| `no_velocity_ic` | True | Specifies that if a VELOCITY_IC has been set via any means, to "UNSET" the velocity initial condition. |
| `rotational_ic` | Real | Specifies the initial rotational displacement on a revolute or cylindrical joint. |
| `no_rotational_ic` | True | Specifies that if a "rotational" initial condition has been set, to "UNSET" the rotational initial condition for the specified constraint. |
| `angular_velocity_ic` | Angular velocity | Specifies the initial angular velocity on a revolute or cylindrical joint. |
| `no_angular_velocity_ic` | True | Specifies that if an "angular_velocity" initial condition has been set, to "UNSET" the angular velocity initial condition for the specified constraint. |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `j_part_name` | Existing body | Specifies the part that is the second of two parts connected by this joint. Adams View connects one part at the J marker to the other at the I marker. |
| `location` | Location | Specifies the location used to define the position of the joint. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | Existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |

## Example

Change an existing revolute joint to a spherical joint:

```
constraint modify joint general &
    joint_name = .model_1.JOINT_1 &
    type = spherical
```
