# part modify equation linear_state_equation

Allows you to modify an existing linear_state_equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `linear_state_equation_name` | An Existing Lse | Specifies the linear state equation to modify |
| `new_linear_state_equation_name` | A New Lse | Specifies the name of a new linear state equation |
| `adams_id` | Integer | Specifies a integer used to identify this element in Adams data file |
| `comments` | String | Specifies the comments about the object being created or modified |
| `x_state_array_name` | An Existing Array | Specifies the array to represent the state array |
| `u_input_array_name` | An Existing Array | Specifies an array to be used as input or control of linear system |
| `y_output_array_name` | An Existing Array | Specifies an array name to be used as output array |
| `ic_array_name` | An Existing Array | Specifies the array name for stating the initial conditions of linear system |
| `a_state_matrix_name` | An Existing Matrix | Specifies the array to be used as state matrix |
| `b_input_matrix_name` | An Existing Matrix | Specifies the matrix to be used as control matrix |
| `c_output_matrix_name` | An Existing Matrix | Specifies the matrix to be used as output matrix |
| `d_feedforward_matrix_name` | An Existing Matrix | Specifies the feed-forward matrix name of the linear system |
| `static_hold` | On_off | Indicates that the equations states are not changed during static and quasi-static analysis |
