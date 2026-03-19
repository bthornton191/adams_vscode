# executive_control set dynamics_parameters integrator_parameters

The EXECUTIVE_CONTROL SET DYNAMICS_PARAMETERS INTEGRATOR_PARAMETERS command controls parameters common to multiple integrators.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | AN EXISTING MODEL | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `relative_error` | Real | Specifies a relative error tolerance for the integrator |
| `absolute_error` | Real | Specifies the absolute error tolerance for the integrator. The absolute error tolerance will by bounded by the value of ABSOLUTE_ERROR. |
| `error_scaling` | Real number | Real number should be > 0. Can take 1-16 values. |
| `continue_on_failure` | Yes/no | When the CONTINUE_ON_FAILURE argument is set to YES, it allows the code to continue the simulation with a set of relaxed error tolerances when the specified conditions cannot be met. Otherwise, when set to NO, the control of the Adams simulation will be returned to the command level. |
| `step_maximum` | Integer | The maximum number of integration steps that the code will take between output steps. |
| `init_time_step` | Real number | Real number should be > 0 |
| `max_time_step` | Real number | Real number should be > 0 |
| `min_time_step` | Real number | Real number should be > 0 |
| `max_integrator_order` | Integer | Integer should be greater than 0 and less than or equal to 12 |
| `interpolate` | Yes/No | Indicates whether interpolation is allowed. That is, indicates whether the integrator can choose integration steps independent of output steps and the interpolate results for the output step times. |
| `watch_integrator_perf` | MONITOR, NO_MONITOR, ERROR_IN_INTEGRATOR, NO_ERROR_IN_INTEGRATOR, | Provides the user with a means for observing the progress of the simulation by causing Adams to write information about the status and performance of the integration to the screen. |
| `reconcile` | ALL, DISPLACEMENTS, NONE | Corrects interpolated results before Adams writes them to the output files to satisfy the constraint equations. |
