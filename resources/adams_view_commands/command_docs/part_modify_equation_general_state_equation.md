# part modify equation general_state_equation

Allows you to modify an existing general_state_equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_state_equation_name` | An Existing Gse | Specifies the general state equation to modify |
| `new_general_state_equation_name` | A New Gse | Specifies the name of a new general state equation |
| `adams_id` | Integer | Specifies a integer used to identify this element in Adams data file |
| `comments` | String | Specifies the comments about the object being created or modified |
| `state_equation_count` | Integer | Specifies the number of state equations to be used to define the system |
| `discrete_state_equation_count` | Integer | Specifies the number of discrete state equations to be used to define the system |
| `output_equation_count` | Integer | Specifies the number of output equations to be used to define the system |
| `x_state_array_name` | An Existing Array | Specifies the array to represent the state array |
| `u_input_array_name` | An Existing Array | Specifies an array to be used as input or control of linear system |
| `y_output_array_name` | An Existing Array | Specifies an array name to be used as output array |
| `ic_array_name` | An Existing Array | Specifies the array name for stating the initial conditions of linear system |
| `discrete_state_array_name` | An Existing Array | Specifies the array to represent the discrete state array |
| `discrete_ic_array_name` | An Existing Array | Specifies the array name for stating the initial conditions of linear system |
| `df_dx_method` | Gse_xxflag | Specifies how to compute the matrix of partial derivatives of the state equations with respect to the states |
| `df_du_method` | Gse_flag | Specifies whether or not and how to compute the matrix of partial derivatives of the state equations with respect to the inputs |
| `dg_dx_method` | Gse_flag | Specifies whether or not and how to compute the matrix of partial derivatives of the output equations with respect to the states |
| `dg_du_method` | An Existing Matrix | Specifies whether or not and how to compute the matrix of partial derivatives of the output equations with respect to the inputs |
| `discrete` | True_only | Specifies discrete GSE |
| `sample_period` | Real | Specify sampling time |
| `static_hold` | On_off | Indicates that the equations states are not changed during static and quasi-static analysis |
| `user_function` | Real | Specifies the constants to be passed to GSESUB |
