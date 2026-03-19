# panel set twindow_function impact

The IMPACT function models collisions. It evaluates a function that turns on when the distance between the I and the J markers falls below a nominal FREE_LENGTH (i.e. x1), (i.e. when two parts collide). As long as the distance between the I and the J markers is greater than the FREE_LENGTH, the force is zero. An example of a system you can model with the IMPACT function is a ball impacting the ground.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Run Time Function | Specifies the run time function. |
| `dx` | Function | Specifies a real variable that communicates the time derivative of x to the function. |
| `free_length` | Real | Specifies the non-angular FREE_LENGTH of the independent variable, x. |
| `boundary_penetration` | Real | Specifies a positive real variable that is the non-angular boundary penetration at which Adams applies full damping. |
| `angular_free_length` | Angle | Specifies the ANGULAR_FREE_LENGTH of the independent variable, x. |
| `angular_boundary_penetration` | Angle | Specifies a positive real variable that is the angular boundary penetration at which Adams applies full damping. |
| `stiffness` | Real | A non-negative real variable that specifies the stiffness of boundary surface interaction. |
| `force_exponent` | Real | Specifies a positive real variable that is the exponent of the force deformation characteristic. |
| `max_damping_coefficient` | Real | Specifies a non-negative real variable that is the maximum damping coefficient. |
