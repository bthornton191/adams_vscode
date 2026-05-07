# executive_control set integrator_parameters gstiff

Allows you to set the parameters for the GSTIFF (Gear Stiff) integrator used in dynamic simulations.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies the model for which the GSTIFF integrator parameters are set. |
| `error_tolerance` | Real | Specifies the error tolerance used by the integrator to control step size. |
| `hinit_time_step` | Time | Specifies the initial time step size. |
| `hmax_time_step` | Time | Specifies the maximum allowable time step size. |
| `hmin_time_step` | Time | Specifies the minimum allowable time step size. |
| `kmax_integrator_order` | Integer | Specifies the maximum integration order for the GSTIFF integrator. |
| `maxit_corrector_iterations` | Integer | Specifies the maximum number of corrector iterations per time step. |
| `pattern_for_jacobian` | Boolean | Specifies whether a sparse pattern is used for Jacobian computation. |
