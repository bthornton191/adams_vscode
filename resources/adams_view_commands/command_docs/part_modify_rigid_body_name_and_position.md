# part modify rigid_body name_and_position

Allows you to modify an existing rigid body part's name and position.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | An Existing Part | Specifies the part to be modified. You use this parameter to identify the existing part to be affected with this command. |
| `new_part_name` | A New Part | Specifies the name of the new part. You may use this name later to refer to this part. |
| `ground_part` | Boolean | Boolean |
| `adams_id` | Adams_Id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `view_name` | An Existing View | Specifies the view in which to display this part. |
| `location` | Location | Specifies the location of the origin of a coordinate system (e.g. marker or part). |
| `orientation` | Orientation | Specifies the orientation of a coordinate system (e.g. marker or part) using three rotation angles. |
| `along_axis_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes. Adams View will assign an arbitrary rotation about the axis. |
| `in_plane_orientation` | Location | Specifies the orientation of a coordinate system (e.g. marker or part) by directing one of the axes and locating one of the coordinate planes. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
| `exact_coordinates` | Exact_Coordinates | Specifies as many as six part coordinates that Adams is not to change as it solves for the initial conditions. |
