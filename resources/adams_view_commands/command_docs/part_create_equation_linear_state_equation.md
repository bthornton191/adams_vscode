# part create equation linear_state_equation

Allows you to create a linear_state_equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `linear_state_equation_name` | A New Lse | Specifies the name of the new linear_state_equation. |
| `adams_id` | Adama_Id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `x_state_array_name` | An Existing Array | Specifies the array in the model which will be used as the state array for this linear system. |
| `u_input_array_name` | An Existing Array | Specifies the array name in the current model which will be used as the input (or control) array for this linear system (LINEAR_STATE_EQUATION). |
| `y_output_array_name` | An Existing Array | Specifies the array name in your model which will be used as the output array for this linear system (LINEAR_STATE_EQUATION) |
| `ic_array_name` | An Existing Array | Specifies the array in the model which will be used as the initial conditions array for this linear system (LINEAR_STATE_EQUATION). |
| `a_state_matrix_name` | An Existing Matrix | Specifies the matrix in the model which is used as the state matrix for this linear system (LINEAR_STATE_EQUATION). |
| `b_input_matrix_name` | An Existing Matrix | Specifies the matrix in the model which is used as the control matrix for this linear system (LINEAR_STATE_EQUATION). |
| `c_output_matrix_name` | An Existing Matrix | Specifies the matrix in the model which is used as the output matrix for this linear system (LINEAR_STATE_EQUATION). |
| `d_feedforward_matrix_name` | An Existing Matrix | Specifies the matrix in your model which is used as the feedforward matrix for this linear system (LINEAR_STATE_EQUATION). |
| `static_hold` | On_Off | Indicates that equation states are not permitted to change during static and quasi-static analysis. |
