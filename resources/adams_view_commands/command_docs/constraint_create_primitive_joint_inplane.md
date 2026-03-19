# constraint create primitive_joint inplane

Allows the creation of an inplane joint primitive.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `jprim_name` | A NEW PRIMITIVE JOINT | Specifies the name of the new jprim. |
| `adams_id` | ADAMS_ID | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | STRING | Specifies comments for the object being created or modified. |
| `i_part_name` | AN EXISTING BODY | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | AN EXISTING BODY | Specifies the part that is the second of two parts connected by this joint. |
| `location` | LOCATION | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | ORIENTATION | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | LOCATION | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | LOCATION | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | AN EXISTING MODEL, PART OR MARKER | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | AN EXISTING MARKER | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | AN EXISTING MARKER | Specifies a marker on the second of two parts connected by this joint. |
