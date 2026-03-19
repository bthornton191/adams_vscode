# geometry create shape plane

Allows you to create a two-dimensional box.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `plane_name` | New Plane Name | Specifies the name of the plane to be created. |
| `adams_id` | Integer | Assigns a unique ID number to the plane. |
| `comments` | String | Adds any comments about the plane that you want to enter to help you manage and identify it. |
| `ref_marker_name` | Existing Marker | Specifies the reference marker used to locate and orient the plane. |
| `x_minimum` | Real | Specifies the location of one corner of the plane in coordinates relative to the reference marker |
| `x_maximum` | Real | Specifies the location of the opposite corner of the plane in coordinates relative to the reference marker. |
| `y_minimum` | Real | Specifies the location of one corner of the plane in coordinates relative to the reference marker. If all values are positive, the values indicate the lower left corner of the plane. |
| `y_maximum` | Real | Specifies the location of the opposite corner of the plane in coordinates relative to the reference marker. |
