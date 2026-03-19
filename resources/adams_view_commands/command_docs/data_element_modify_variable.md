# data_element modify variable

Allows you to modify an existing variable.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `variable_name` | An Existing Solvar | Specifies the name of an existing variable |
| `new_variable_name` | A New Solvar | Specifies the name of the new variable. You may use this name later to refer to this variable. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `initial_condition` | Real | Specifies the initial value of the user_defined differential variable and, optionally, an approximate value of the initial time derivative. |
| `function` | Function | Specifies the function expression definition that is used to compute the value of this variable. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. |
| `routine` | String | String |
