# panel set twindow_function ay

The AY function returns the rotational displacement of the I_MARKER (i1) about the y-axis of the J_MARKER (i2). This value is computed as follows: Assuming that rotations about the other two axes (x-, z-axes) of marker i2 are zero. Then AY is the angle between the two x-axes (or the two z-axes). Mathematically, AY is calculated as:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `i_marker_name` | Existing marker | Specifies an existing marker used as the I_MARKER (i1) in the evaluation of the function. |
| `j_marker_name` | Existing marker | Specifies an existing marker used as the J_MARKER (i2) in the evaluation of the function. |
