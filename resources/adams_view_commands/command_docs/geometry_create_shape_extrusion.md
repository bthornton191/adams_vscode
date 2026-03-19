# geometry create shape extrusion

Allows for creation of the extrusion object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `extrusion_name` | A New Extrusion | Specifies the name of the new extrusion. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `reference_marker` | An Existing Marker | Specifies the marker used to place and orient an extrusion. |
| `profile_curve` | An Existing Gwire | Specifies the object used to define the profile of the extrusion. |
| `points_for_profile` | Location | Specifies the points used to define the profile of the extrusion. The points are relative to the extrusion's reference marker. |
| `path_curve` | An Existing Gwire | Specifies the object used to define the path of the extrusion. |
| `path_points` | Location | Specifies the points used to define the path of the extrusion. |
| `length_along_z_axis` | Length | Specifies the legth along the Z axis of the reference marker to extrude the profile curve of the extrusion. |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates are with respect to. |
| `analytical` | Boolean | Boolean |
