# panel set acf_twindow generate_state_matrix

Specifies that you want linearize the model and generate a state matrix representation of the linearized model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file that the state matrices are to be written to. |
| `matrix_format` | Matrix_x/matlab | Specifies the state matrices will be output in either MATRIX_X format or MATLAB format. |
| `plant_input_name` | Existing pinput | Specifies an existing plant_input. |
| `plant_output_name` | Existing poutput | Specifies an existing plant_output. |
| `plant_state_name` | Existing plant state | Specifies an existing plant state. |
| `reference_marker` | Existing marker | Specify a marker that will serve as the reference. |
