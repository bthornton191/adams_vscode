# geometry create shape cylinder

Allows for creation of a cylinder object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `cylinder_name` | A New Cylinder | Specifies the name of the new cylinder. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `center_marker` | An Existing Marker | Specifies the marker at the center of the bottom face of the cylinder. The cylinder is extruded along the Z axis of this marker. |
| `angle_extent` | Angle | Specifies the angular sweep of the cylinder in radians. The default is 2π (full cylinder). |
| `length` | Length | Specifies the length of the cylinder along the Z axis of the center marker. |
| `radius` | Length | Specifies the outer radius of the cylinder. |
| `ref_radius_by_marker` | An Existing Marker | Specifies an existing marker to use as a reference for the cylinder radius instead of an explicit value. |
| `side_count_for_body` | Integer | Specifies the number of polygonal facets used to approximate the cylindrical surface for display. |
| `segment_count_for_ends` | Integer | Specifies the number of segments used to approximate the circular end faces for display. |
