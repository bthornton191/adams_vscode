# executive_control modify sensor

Allows you to modify a sensor. You may reverse this creation at a later time with an UNDO command.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `sensor_name` | String | Specifies the name of the sensor you wish to modify |
| `new_sensor_name` | String | Specifies the name of the new sensor. You may use this name later to refer to this sensor. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified |
| `compare` | GE, EQ, LE | Specifies what kind of comparison is to be made to initiate the action by the SENSOR. |
| `codgen` | ON/OFF | Specifies that Adams is to generate a new pivot sequence for matrix factorization when the event that Adams is sensing has the specified relationship to VALUE. |
| `dt` | Real | Specifies that the time between consecutive output steps should be redefined. This is done when Adams first senses that the FUNCTION specified has the same relationship as specified to VALUE. Adams uses this value until it is changed. |
| `halt` | On/OFF | Specifies that execution should be terminated when the FUNCTION that Adams is sensing has the specified relationship to VALUE. |
| `value` | Real | Specifies the non-angular VALUE you want to relate to the FUNCTION that Adams is sensing. |
| `error` | Real | Specifies the absolute non-angular value of allowable error between VALUE and the value of the FUNCTION that Adams is sensing. |
| `angular_value` | Real | Specifies the angular VALUE you want to relate to the FUNCTION that Adams is sensing. |
| `angular_error` | Real | Specifies the absolute angular value of allowable error between VALUE and the value of the FUNCTION that Adams is sensing. |
| `print` | On/OFF | Specifies that Adams should write data to the request, graphics, and output files when the FUNCTION that Adams is sensing has the specified relationship to VALUE. |
| `restart` | On/OFF | Specifies that Adams should restart the integration when the FUNCTION that Adams is sensing has the specified relationship to VALUE. Adams reinitializes the integration step size to HINIT and reduces the integration order to one. |
| `return` | On/OFF | Specifies that Adams should stop the simulation and return to the command level when the FUNCTION that Adams is sensing has the specified relationship to VALUE. |
| `stepsize` | Real | Specifies that Adams should redefine the trial integration step size when the FUNCTION that Adams is sensing has the specified relationship to VALUE. This change is temporary and lasts only for the next step. If this step size is unsatisfactory for convergence or if it generates too much error, Adams tries one or more different step sizes. |
| `yydump` | On/OFF | Specifies that Adams should dump the state variable vector when the FUNCTION that Adams is sensing has the specified relationship to VALUE. |
| `function` | Function | Specifies a FUNCTION expression to define the sensor. |
| `user_function` | Real | Specifies a list of constants that are to be passed to a user-written subroutine to define the sensor. |
