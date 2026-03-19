# part create point_mass name_and_position

Allows you to create a point mass by specifying its name and position. You must supply a unique name for the new part, or accept the name that Adams View generates for you.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `point_mass_name` | New Point Mass | Specifies the name of the point mass to create or modify. |
| `adams_id` | Integer | Assigns a unique ID number to the part. |
| `comments` | String | Adds comments about the part to help you manage and identify it. |
| `view_name` | Existing view | Specifies the view in which to display the part. |
| `location` | Location | Specifies x, y, and z coordinates defining the flexible body's location in a given reference frame defined in the parameter relative_to. |
| `orientation` | Orientation | Specifies the orientation method |
| `along_axis_orientation` | Location | Specifies the orientation method |
| `in_plane_orientation` | Location | Specifies the in_plane orientation method |
| `relative_to` | Existing Model, Part or Marker | Specifies a reference frame relative to which the location and orientation are defined. Leave blank or enter model name to use the global coordinate system. |
| `exact_coordinates` | X, Y, Z, PSI, THETA, PHI, NONE, ALL | Specifies as many as six part coordinates that Adams View is not to change as it solves for the initial conditions. |
