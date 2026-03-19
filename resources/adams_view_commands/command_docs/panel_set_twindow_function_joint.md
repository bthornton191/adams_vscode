# panel set twindow_function joint

The JOINT function returns the force COMPONENT for the JOINT you identify in the JOINT_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `joint_name` | An Existing Joint | Specifies an existing joint |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
