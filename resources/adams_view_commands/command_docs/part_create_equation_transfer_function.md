# part create equation transfer_function

Allows you to create or modify a user-defined transfer function.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `transfer_function_name` | New TFSISO | Specifies the name of the equation to be created or modified |
| `adams_id` | Integer | Assigns a unique ID number to the equation. |
| `comments` | String | Adds comments about the equation to help you manage and identify it. |
| `x_state_array_name` | Existing Array | Specifies the array that defines the state variable array for the transfer function. |
| `u_input_array_name` | Existing Array | Specifies the array that defines the input (or control) for the transfer function. The array must be an inputs (U) array. If you specified the size of the array when you created it, it must be one. |
| `y_output_array_name` | Existing Array | Specifies the array that defines the output for the transfer function. |
| `static_hold` | On/off | Indicates that equation states are not permitted to change during static and quasi-static simulations (on). |
| `numerator_coefficients` | Real | Specifies the coefficients of the polynomial in the numerator of the transfer function. |
| `denominator_coefficients` | Real | Specifies the coefficients of the polynomial in the denominator of the transfer function. |
| `ic_array_name` | Existing Adams Array | Specifies an existing Adams array. |
