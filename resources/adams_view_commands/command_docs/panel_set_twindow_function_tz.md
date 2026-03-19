# panel set twindow_function tz

The TZ function returns the z-component of the net torque acting at the I_MARKER (i1), as computed in the coordinate system of the R_MARKER (i3). All force elements acting between the I_ and J_MARKERs (i1 and i2) are included in the calculation of the torque, unless the force element is an action-only type of force. You should omit specification of the J_MARKER (i2) and the R_MARKER (i3), to find the z-component of an action-only torque element acting at the I_MARKER (i1).

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
| `r_marker_name` | Existing Marker | Specifies the marker used as the R_MARKER (i3) with respect to which you want Adams to evaluate the function. If you do not supply this parameter, Adams will evaluate the function in the ground reference frame. |
