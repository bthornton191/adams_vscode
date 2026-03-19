# panel set twindow_function torque_vector

The TORQUE_VECTOR function returns a force COMPONENT for the TORQUE_VECTOR you identify in the TORQUE_VECTOR_NAME

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `torque_vector_name` | An Existing Vtorque | Specifies an existing torque_vector. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values |
| `component` | All_components | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | An Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
