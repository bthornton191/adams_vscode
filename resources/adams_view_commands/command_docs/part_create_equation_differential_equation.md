# part create equation differential_equation

Allows you to create or modify a user-defined differential equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `differential_equation_name` | New Equation | Specifies the name of the equation to be created or modified |
| `adams_id` | Integer | Assigns a unique ID number to the equation. |
| `comments` | String | Adds any comments about the equation to help you manage and identify it. |
| `initial_condition` | Real | Specifies the initial value of the differential equation at the start of the simulation. |
| `no_initial_condition` | True_only | Unsets the velocity initial condition for the specified equation (true) so it no longer has a velocity initial condition. |
| `function` | Function | Specifies a function expression or defines and passes constants to a user-written subroutine to define the differential equation. |
| `user_function` | Real | Specifies up to 30 values for Adams Solver to pass to a user-written subroutine. |
| `routine` | String | Specifies an alternative library and name for the user subroutine DIFSUB. |
| `static_hold` | On/off | Indicates that equation states are not permitted to change during static and quasi-static simulations (on). |
| `implicit` | On/off | Indicates that the function expression or subroutine defines the implicit form of the equation (on). |
