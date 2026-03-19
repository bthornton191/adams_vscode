# Part create equation general_state_equation

Allows you to create an existing general_state_equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `general_state_equation_name` | An Existing Gse | Specifies the general state equation to create |
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
| `static_hold` | On/off | Indicates that the equations states are not changed during static and quasi-static analysis |
| `user_function` | Real | Specifies the constants to be passed to GSESUB |
| `implicit` | On/off | Indicates that the function expression or subroutine defines the implicit form of the equation (on). |
| `routine` | String | Specifies an alternative library and name for the user subroutine GSESUB. |
| `sample_offset` | Real | Specifies the simulation time at which the sampling of the discrete states is to start. All discrete states before SAMPLE_OFFSET are defined to be at the initial condition specified. SAMPLE_OFFSET defaults to zero when not specified. |
| `statics_only` | On/Off | When included (or set to On) will only activate GSE for statics. During dynamics the GSE will be inactive if set, and this should speed up the Solver solution during dynamics since less number of states are being solved. |
| `interface_routines` | Function | Specifies an alternative library and subroutine names for the user subroutines GSE_DERIV, GSE_UPDATE, GSE_OUTPUT, GSE_SAMP respectively. |
