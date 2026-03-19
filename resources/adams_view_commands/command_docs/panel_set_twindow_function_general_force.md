# panel set twindow_function general_force

The GENERAL_FORCE function returns the force COMPONENT for a GENERAL_FORCE you identify in the GENERAL_FORCE_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_force_name` | An Existing Genforce | Specifies an existing general force. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
