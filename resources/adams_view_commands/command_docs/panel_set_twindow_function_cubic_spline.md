# panel set twindow_function cubic_spline

The CUBIC_SPLINE function uses the standard cubic method of interpolation to create a spline function across a set of data points

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Function | Specifies the real variable that is the independent variable value along the x-axis of the spline. |
| `z` | Function | Specifies a real variable that is the second independent variable value along the z-axis of the surface being interpolated |
| `spline_name` | An Existing Spline | Specifies an existing spline |
| `derivative_order` | Integer | An optional integer that specifies the order of the derivative at the interpolate value to be returned by CUBSPL.Range: 0 < iord < 2 |
