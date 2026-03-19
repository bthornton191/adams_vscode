# numeric_results create dynamic_polyline

Allows you to create a result set which specifies time dependent locations for polylines.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `polyline_name` | An Existing Polyline | Specifies an existing POLYLINE |
| `vertex` | Integer | Specifies the vertex this result set corresponds to. |
| `x_result_set_component_name` | An Existing Component | Specifies the name of a result set component to be used to drive the vertex in the X direction over time. |
| `y_result_set_component_name` | An Existing Component | Specifies the name of a result set component to be used to drive the vertex in the Y direction over time. |
| `z_result_set_component_name` | An Existing Component | Specifies the name of a result set component to be used to drive the vertex in the Z direction over time. |
| `relative_to` | An Existing Model,Part OR Marker | Specifies the coordinate system that location coordinates and orientation angles correspond to. |
