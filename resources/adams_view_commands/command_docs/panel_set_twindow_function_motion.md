# panel set twindow_function motion

The MOTION function returns the force COMPONENT caused by the MOTION you identify in the MOTION_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `motion_name` | An Existing Motion | Specifies an existing motion generator. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
