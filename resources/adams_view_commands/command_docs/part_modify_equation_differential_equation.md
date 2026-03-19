# part modify equation differential_equation

Allows you to modify an existing user defined differential equation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `differential_equation_name` | An Existing Equation | Specifies the differential_equation to be modified. You use this parameter to identify the existing differential_equation tobe affected with this command. |
| `new_differential_equation_name` | A New Equation | Specifies the name of the new differential_equation. You may use this name later to refer to this differential_equation. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `initial_condition` | Real | Specifies the initial value of the user_defined differential variable and, optionally, an approximate value of the initial time derivative. |
| `no_initial_condition` | True_Only | Specifies that if an initial condition has been set, to "UNSET" the initial condition for the specified DIFFERENTIAL_EQUATION. |
| `function` | Function | Specifies an expression, or defines and passes constants to a user-written subroutine to define the differential equation. |
| `static_hold` | On_Off | Indicates that equation states are not permitted to change during static and quasi-static analysis. |
| `implicit` | On_Off | Specifies that the FUNCTION expression or the DIFSUB subroutine defines the implicit form of your differential equation. |
