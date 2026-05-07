# executive_control set dynamics_parameters bdf_parameters

Allows you to set backward differentiation formula (BDF) integrator parameters for dynamic simulations.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies the model for which the BDF parameters are set. |
| `predictor_coefficients` | String | Specifies the predictor coefficient strategy for the BDF integrator. |
| `high_order_bias` | Real | Specifies a bias factor favoring higher-order integration steps. |
| `low_order_bias` | Real | Specifies a bias factor favoring lower-order integration steps. |
| `same_order_bias` | Real | Specifies a bias factor favoring maintaining the current integration order. |
| `stability` | Real | Specifies the stability factor for the BDF integrator. |
| `cr_adapt_tolerance` | Real | Specifies the tolerance used during corrector-based step adaptation. |
| `cr_relative_error` | Real | Specifies the relative error tolerance for the corrector. |
| `cr_absolute_error` | Real | Specifies the absolute error tolerance for the corrector. |
| `cr_error_scaling` | Real | Specifies scaling factors applied to corrector error evaluation. |
| `cr_maximum_iterations` | Integer | Specifies the maximum number of corrector iterations per time step. |
| `cr_pattern_for_jacobian` | Boolean | Specifies whether a sparse pattern is used for Jacobian computation. |
| `watch_corrector_perf` | String | Specifies performance monitoring options for the corrector. |
