# geometry modify curve nurb_curve

Allows modification of an existing NURB curve.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `nurb_curve_name` | An Existing NURB Curve | Specifies the name of the existing NURB curve to modify. |
| `new_nurb_curve_name` | A New NURB Curve | Specifies a new name for the NURB curve. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `degree` | Integer | Specifies the polynomial degree of the NURB curve. |
| `rational` | Boolean | Specifies whether the NURB curve is rational (weighted control points). |
| `periodic` | Boolean | Specifies whether the NURB curve is periodic (closed). |
| `control_points` | Location | Specifies the control point locations that define the shape of the NURB curve. |
| `weights` | Real | Specifies the weights associated with each control point for rational curves. |
| `knots` | Real | Specifies the knot vector that controls the parameterization of the NURB curve. |
