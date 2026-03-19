# constraint create primitive_joint inline

Allows the creation of an inline joint primitive.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `jprim_name` | New primitive joint name | Specifies the name of the new jprim. You may use this name later to refer to this jprim. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_part_name` | Existing body | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | Existing body | Specifies the part that is the second of two parts connected by this joint. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | Existing model, part or marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | Existing marker | Specifies a marker on the first of two parts connected by this joint. |
| `j_marker_name` | Existing marker | Specifies a marker on the second of two parts connected by this joint. |
