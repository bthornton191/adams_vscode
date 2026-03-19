# panel set twindow_function z_acc

The Z_ACC function returns the z-component of the difference between the global acceleration vector of the I_MARKER (i1) and the global acceleration vector of the J_MARKER (i2) as computed in the coordinate system of the R_MARKER (i3)

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | An Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | An Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
| `r_marker_name` | An Existing Marker | Specifies the marker used as the R_MARKER (i3) with respect to which you want adams to evaluate the function. |
| `reference_frame_marker` | An Existing Marker | The reference frame in which the second time derivative of the displacement vector is taken |
