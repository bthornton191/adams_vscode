# executive_control set integrator_parameters wstiff

Allows you to set the parameters for the WSTIFF (Wielenga Stiff) integrator used in dynamic simulations.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies the model for which the WSTIFF integrator parameters are set. |
| `error_tolerance` | Real | Specifies the error tolerance used by the integrator to control step size. |
| `hinit_time_step` | Time | Specifies the initial time step size. |
| `hmax_time_step` | Time | Specifies the maximum allowable time step size. |
| `hmin_time_step` | Time | Specifies the minimum allowable time step size. |
| `kmax_integrator_order` | Integer | Specifies the maximum integration order for the WSTIFF integrator. |
| `maxit_corrector_iterations` | Integer | Specifies the maximum number of corrector iterations per time step. |
| `pattern_for_jacobian` | Boolean | Specifies whether a sparse pattern is used for Jacobian computation. |
| `watch_integrator_perf` | String | Specifies performance monitoring options for the integrator. |
| `reconcile_vel_and_acc` | Boolean | Specifies whether velocities and accelerations are reconciled after each time step. |
