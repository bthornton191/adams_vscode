# panel set twindow_function x_wdt

The X_WDT function returns the x-component of the difference between the angular acceleration vector of the I_MARKER (i1) in ground and the angular acceleration vector of the J_MARKER (i2) in ground, as computed in the coordinate system of the R_MARKER (i3).

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
| `reference_frame_marker` | Existing marker | Specifies the reference frame marker. |
| `r_marker_name` | Existing marker | Specifies the marker used as the R_MARKER (i3) with respect to which you want Adams to evaluate the function. If you do not supply this parameter, Adams will evaluate the function in the ground reference frame. |
