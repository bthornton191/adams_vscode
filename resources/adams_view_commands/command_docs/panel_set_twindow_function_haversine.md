# panel set twindow_function haversine

Configures the panel test window function to return a haversine (smooth step) transition value.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Real | The independent variable. |
| `begin_at` | Real | Value of `x` where the transition begins. |
| `end_at` | Real | Value of `x` where the transition ends. |
| `angular_begin_at` | Real | Angular (radian) value of `x` where the transition begins. |
| `angular_end_at` | Real | Angular (radian) value of `x` where the transition ends. |
| `initial_function_value` | Real | Function value before the transition. |
| `final_function_value` | Real | Function value after the transition. |
| `angular_initial_function_value` | Real | Function value before the transition when using angular specification. |
| `angular_final_function_value` | Real | Function value after the transition when using angular specification. |
