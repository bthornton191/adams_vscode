# panel set twindow_function spring_damper

The SPRING_DAMPER function returns a force COMPONENT for the SPRING_DAMPER you identify in the SPRING_DAMPER_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `spring_damper_name` | Existing Spring_damper | Specifies an existing spring_damper. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values. |
| `component` | FM, FX, FY, FZ, TM, TX, TY, TZ | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
