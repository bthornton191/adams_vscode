# panel set twindow_function single_component_force

The SINGLE_COMPONENT_FORCE function returns the force COMPONENT for the SINGLE_COMPONENT_FORCE you identify in the SINGLE_COMPONENT_FORCE_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `single_component_force_name` | An Existing Single-component Force | Specifies an existing single_component_force. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
