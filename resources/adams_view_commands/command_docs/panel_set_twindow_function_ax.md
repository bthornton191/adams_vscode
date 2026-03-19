# panel set twindow_function ax

The AX function returns the rotational displacement of the I_MARKER (i1) about the x-axis of the J_MARKER (i2). This value is computed as follows: Assuming that rotations about the other two axes (y-, z-axes) of marker i2 are zero, then, AX is the angle between the two y-axes (or the two z-axes). Mathematically, AX is calculated as:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
