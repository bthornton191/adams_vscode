# panel set twindow_function bistop_slot

The BISTOP_SLOT function models a gap element.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Function | Specifies a real variable that is the distance variable you want to use to compute the force. |
| `dx` | Function | Specifies a real variable that communicates the time derivative of x to the function |
| `lower_bound` | Real | Specifies a real variable that is the non-angular lower bound of x. |
| `upper_bound` | Real | A real variable that specifies the non-angular upper bound of the independent variable x. |
| `boundary_penetration` | Real | Specifies a positive real variable that is the non-angular boundary penetration at which Adams applies full damping. |
| `angular_lower_bound` | Angle | Specifies a real variable that is the angular lower bound of x. |
| `angular_upper_bound` | Angle | A real variable that specifies the angular upper bound of the independent variable x |
| `angular_boundary_penetration` | Angle | Specifies a positive real variable that is the angular boundary penetration at which Adams applies full damping. |
| `stiffness` | Real | A non-negative real variable that specifies the stiffness of boundary surface interaction. |
| `force_exponent` | Real | Specifies a positive real variable that is the exponent of the force deformation characteristic. |
| `max_damping_coefficient` | Real | Specifies a non-negative real variable that is the maximum damping coefficient |
