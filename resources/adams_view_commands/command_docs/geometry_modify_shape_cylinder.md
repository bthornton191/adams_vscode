# geometry modify shape cylinder

Allows modification of the cylinder object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `cylinder_name` | An Existing Cylinder | Specifies the cylinder to modify |
| `new_cylinder_name` | A New Cylinder | A NEW CYLINDER |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `center_marker` | An Existing Marker | Specifies the marker at the center of a circle, an arc, the bottom of a cylinder, or the bottom of a frustum |
| `angle_extent` | Angle | Specifies a subtended angle measured positive (according to the right-hand rule) about the z-axis of the center marker. |
| `length` | Length | Specifies the height of a cylinder or a frustum. |
| `radius` | Length | Specifies the radius of a circle, an arc, or a cylinder. |
| `ref_radius_by_marker` | An Existing Marker | Specifies the radius of a circle, an arc, or a cylinder to be the distance from the center marker Z axis to this radius marker. |
| `side_count_for_body` | Integer | Specifies the number of flat sides Adams View draws on a cylinder or a frustum. |
| `segment_count_for_ends` | Integer | Specifies the number of straight line segments Adams View uses to draw the circles at the ends of a cylinder or a frustum. |
