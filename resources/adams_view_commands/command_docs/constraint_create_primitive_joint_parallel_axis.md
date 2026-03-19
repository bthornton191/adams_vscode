# constraint create primitive_joint parallel_axis

Allows creation of a parallel axis joint primitive.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `jprim_name` | A New Primative Joint | Specifies the name of the new jprim. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `i_part_name` | An Existing Body | Specifies the part that is the first of two parts connected by this joint. |
| `j_part_name` | An Existing Body | Specifies the part that is the second of two parts connected by this joint. |
| `location` | Location | Specifies the locations to be used to define the position of a constraint during its creation. |
| `orientation` | Orientation | Specifies the orientation of the J marker for the constraint being created using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles are with respect to. |
| `i_marker_name` | An Existing Marker | Specifies a marker on the first of two parts connected by this joint. Adams View connects one part at the I marker to the other at the J marker. |
| `j_marker_name` | An Existing Marker | Specifies a marker on the second of two parts connected by this joint. |
