# panel set twindow_function field

The FIELD function returns the force COMPONENT for the FIELD you identify in the FIELD_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `field_name` | Existing Field | Specifies an existing bushing. |
| `return_value_on_marke` | Marker_type | Specifies for which marker on the force element (i or j) the function will return force values. |
| `component` | FM, FX, FY, FZ, TM, TX, TY, TZ | Specifies the specific COMPONENT of force or torque that the function is to return for the force element. |
| `reference_marker` | Existing Marker | Specifies a marker that provides a reference coordinate system for the function. |
