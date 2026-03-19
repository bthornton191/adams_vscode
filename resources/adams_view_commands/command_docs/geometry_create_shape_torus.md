# geometry create shape torus

Allows for creation of the torus object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `torus_name` | A New Torus | Specifies the name of the new torus |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `center_marker` | An Existing Marker | Specifies the marker at the center of a circle, an arc, the bottom of a cylinder, or the bottom of a frustum. |
| `angle_extent` | Angle | Specifies a subtended angle measured positive (according to the right-hand rule) about the z-axis of the center marker. |
| `major_radius` | Length | The parameter is used to specify the radius for the circular spine of the torus. |
| `minor_radius` | Length | The parameter is used to specify the radius for the circular cross-sections of the torus. |
| `side_count_for_perimeter` | Integer | The parameter is used to specify the number of circular cross-sections to create along the spine of the torus. |
| `segment_count` | Integer | The SEGMENT_COUNT parameter is used to specify the number of sides for each of the circular cross-sections of the torus. |
