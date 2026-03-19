# panel set twindow_function beam

The BEAM function returns the COMPONENT of a force due to BEAM you identify in the BEAM_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `beam_name` | Existing beam | Specifies an existing beam. |
| `return_value_on_marker` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values. |
| `component` | FM, FX, FY, FZ, TM, TX, TY, TZ | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
