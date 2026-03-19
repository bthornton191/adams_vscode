# panel set twindow_function primitive_joint

The PRIMITIVE_JOINT function returns the force COMPONENT caused by the PRIMITIVE_JOINT you identify in the JPRIM_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `jprim_name` | An Existing Primative Joint | Specifies an existing jprim |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
