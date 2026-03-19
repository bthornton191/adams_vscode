# panel set twindow_function akima_spline

The AKIMA_SPLINE function uses the AKIMA method of interpolation to create a spline function across a set of data points.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | FUNCTION | Specifies the real variable that is the independent variable value along the x-axis of the spline. |
| `z` | FUNCTION | Specifies a real variable that is the second independent variable value along the z-axis of the surface being interpolated |
| `spline_name` | AN EXISTING SPLINE | Specifies an existing spline |
| `derivative_order` | INTEGER | An optional integer that specifies the order of the derivative at the interpolate value to be returned by CUBSPL.Range: 0 < iord < 2 |
