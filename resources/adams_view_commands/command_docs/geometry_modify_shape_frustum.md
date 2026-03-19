# geometry modify shape frustum

Allows for the modification of the frustum object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `frustum_name` | An Existing Frustum | Specifies the name of an existing frustum |
| `new_frustum_name` | A New Frustum | Specifies the name of the new frustum |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file |
| `comments` | String | Specifies comments for the object being created or modified. |
| `center_marker` | An Existing Marker | Specifies the marker at the center of a circle, an arc, the bottom of a cylinder, or the bottom of a frustum. |
| `angle_extent` | Angle | Specifies a subtended angle measured positive (according to the right-hand rule) about the z-axis of the center marker. |
| `length` | Length | Specifies the height of a cylinder or a frustum. |
| `side_count_for_body` | Integer | Specifies the number of flat sides Adams View draws on a cylinder or a frustum. |
| `top_radius` | Length | Specifies the radius at the top of a frustum. |
| `bottom_radius` | Length | Specifies the radius at the bottom of a frustum. |
| `segment_count_for_ends` | Integer | Specifies the number of straight line segments Adams View uses to draw the circles at the ends of a cylinder or a frustum. |
