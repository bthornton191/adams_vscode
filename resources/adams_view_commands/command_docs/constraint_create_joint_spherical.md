# constraint create joint spherical

Allows the creation of a spherical joint.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | New joint name | Specifies the name of the new joint. You may use this name later to refer to this joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. These markers are automatically generated using this method of joint creation. |
| `j_part_name` | Existing body | Specifies the part that is the second of two parts connected by this joint. Adams View connects one part at the J marker to the other at the I marker. These markers are automatically generated using this method of joint creation. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. The I and J markers will be automatically created at this location on the I_PART_NAME and J_PART_NAME respectively. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. The I marker is oriented based on the J marker orientation and the requirements of the particular constraint being created. These markers are created automatically. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | Existing body, part or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |
