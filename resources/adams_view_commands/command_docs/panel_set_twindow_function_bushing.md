# panel set twindow_function bushing

The BUSHING function returns a force COMPONENT for the BUSHING you identify in the BUSHING_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `bushing_name` | Existing Bushing | Specifies an existing bushing. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values. |
| `component` | FM, FX, FY, FZ, TM, TX, TY, TZ | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
