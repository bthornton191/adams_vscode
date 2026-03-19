# panel set twindow_function az

The AZ function returns the rotational displacement of the I_MARKER (i1) about the z-axis of the J_MARKER (i2). This value is computed as follows: Assume that rotations about the other two axes (x-, y-axes) of marker i2 are zero. Then AZ is the angle between the two x-axes (or the two y-axes). Mathematically, AZ is calculated as:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing Marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing Marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
