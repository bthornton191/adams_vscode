# panel set twindow_function dx

The DX function returns the x-component of the translational displacement vector from J_MARKER (i2) to I_MARKER (i1), as expressed in R_MARKER (i3) coordinate system.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | An Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | An Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
| `r_marker_name` | An Existing Marker | Specifies the marker used as the R_MARKER (i3) with respect to which you want Adams to evaluate the function. |
