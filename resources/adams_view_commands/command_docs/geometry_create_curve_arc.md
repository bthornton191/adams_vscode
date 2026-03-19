# geometry create curve arc

Allows for creation of the arc object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `arc_name` | A New Arc | Specifies the name of the new arc. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `center_marker` | An Existing Marker | Specifies the marker at the center of a circle, an arc, the bottom of a cylinder, or the bottom of a frustum. |
| `angle_extent` | Angle | Specifies a subtended angle measured positive (according to the right-hand rule) about the z-axis of the center marker |
| `radius` | Length | Specifies the radius of a circle, an arc, or a cylinder. |
| `ref_radius_by_marker` | An Existing Marker | Specifies the radius of a circle, an arc, or a cylinder to be the distance from the center marker Z axis to this radius marker. |
| `segment_count` | Integer | Specifies the number of straight line segments Adams View uses to draw a circle or an arc. |
| `close` | Arc_closure | Specifies the type of closure to perform when Adams View creates the arc. |
