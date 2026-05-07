# panel set acf_twindow mkb_matrix

Configures the MKB (Mass/Stiffness/Damping) matrix export settings for an ACF test window panel.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Name of the output file for the MKB matrix. |
| `matrix_format` | String | Format specification for the exported matrix. |
| `original` | Boolean | Whether to export the original (unreduced) matrices. |
| `plant_input_name` | String | Name of the plant input marker or definition. |
| `plant_output_name` | String | Name of the plant output marker or definition. |
| `plant_state_name` | String | Name of the plant state definition. |
| `reference_marker` | Object | Marker used as the reference frame for the matrix export. |
| `damping` | Real | Damping value to include in the matrix export. |
