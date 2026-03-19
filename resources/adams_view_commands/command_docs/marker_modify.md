# marker modify

Allows you to modify an existing marker.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `marker_name` |  |  |
| `new_marker_name` | A New Marker | Specifies the name of the new marker. You may use this name later to refer to this marker. |
| `adams_id` | ADAMS_ID | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `location` | Location | Specifies the location of the origin of a coordinate system (for example, marker or part). |
| `preserve_location` | True only | An optional parameter, which when specified means that the marker location is to be retained as specified (for example, marker on a flexible body will not be snapped to the nearest node). |
| `node_id` | Integer | Specifies a node_id on a flexible body that Adams view will use to determine the location at which it will place a marker. |
| `orientation` | Orientation | Specifies the orientation of a coordinate system (for example, marker or part) using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (for example, marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part OR Marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `curve_name` | An existing Curve | Specifies the curve name on which to create a marker |
| `velocity` | Real | Specifies the initial conditions |
| `vx` | Real | Specifies the initial conditions |
| `vy` | Real | Specifies the initial conditions |
| `vz` | Real | Specifies the initial conditions |
| `reference_marker_name` | An Existing Marker | Specifies an existing marker which acts as a reference |
