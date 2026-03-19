# panel set twindow_function dy

The DY function returns the y-component of the translational displacement vector from J_MARKER (i2) to I_MARKER (i1), as expressed in the R_MARKER (i3) coordinate system. J_MARKER (i2) may not be specified, in which case, it defaults to ground. Similarly, the R_MARKER (i3) may not be specified, in which case it defaults to ground. Mathematically, DY is calculated as follows:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
| `r_marker_name` | Existing Marker | Specifies the marker used as the R_MARKER (i3) with respect to which you want Adams to evaluate the function. If you do not supply this parameter, Adams will evaluate the function in the ground reference frame. |
