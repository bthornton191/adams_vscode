# data_element modify curve

Allows you to modify an existing curve.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `curve_name` | An Existing Curve | Specifies an existing curve object |
| `new_curve_name` | A New Acurve | Specifies the name of the new curve. You may use this name later to refer to this curve. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `closed` | Boolean | Specifies if the curve meets at the ends. |
| `matrix_name` | An Existing Matrix | Specifies the name of an existing MATRIX containing the data for the curve. |
| `fit_type` | Fit_type | Specifies the way the curve is to be fit through the points contained in the MATRIX. |
| `segment_count` | Integer | Specifies the number of polynomial segments Adams uses for fitting the curve points when FIT_TYPE is set to CURVE_POINTS. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `minimum_parameter` | Real | Specifies the minimum value of the curve parameter only for a user-written curve. |
| `maximum_parameter` | Real | Specifies the maximum value of the curve parameter only for a user-written curve. |
