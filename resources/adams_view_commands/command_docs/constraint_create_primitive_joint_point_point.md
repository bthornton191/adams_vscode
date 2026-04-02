# constraint create primitive_joint point_point

Allows the creation of a point-to-point joint primitive. This constraint removes three translational degrees of freedom between two parts, allowing a specified offset between their connection points.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `jprim_name` | A New Primitive Joint | Specifies the name of the new primitive joint. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_part_name` | An Existing Body | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | An Existing Body | Specifies the part that is the second of two parts connected by this joint. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this joint. |
| `offset` | Length | Specifies a constant offset distance between the I and J markers. |
