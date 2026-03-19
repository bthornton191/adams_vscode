# executive_control set numerical_integration_parameters

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `integrator_type` | GSTIFF, WSTIFF, DSTIFF, ABAM, CPBDF, HASTIFF, SI2_GSTIFF | Specifies the integrator type to be used |
| `solver_type` | CALAHAN, HARWELL | Specifies the Solver type |
| `error_tolerance` | Real | Specifies the error tolerance. Should be greater than 0. |
| `pattern_for_jacobian` | Yes/No | Specifies the pattern for jacobian. Can take up to 10 boolean values. |
| `maxit_corrector_iterations` | Integer | Should be an integer greater than 0 |
| `hinit_time_step` | Real | Should be a real number greater than 0 |
| `hmin_time_step` | Real | Should be a real number greater than 0 |
| `hmax_time_step` | Real | Should be a real number greater than 0 |
| `adaptivity` | Real | Specify the adaptivity |
| `scale` | Real | Specify the scale |
| `kmax_integrator_order` | Integer | Specify the integrator order. Integer specified should be greater than 0 and less than or equal to 12. |
| `interpolate` | Yes/No | Indicates whether interpolation is allowed. That is, indicates whether the integrator can choose integration steps independent of output steps and the interpolate results for the output step times. |
| `reconcile` | ALL, DISPLACEMENTS, NONE | Corrects interpolated results before Adams writes them to the output files to satisfy the constraint equations. |
| `repartition_threshold` | Real number | Allows some control of the re-partitioning of coordinates into independent and dependent coordinates. |
| `corrector_resolution_factor` | Real | Specifies the corrector resolution factor |
| `fixed_iterations` | Integer | Specify the number of iterations per integration step for the GSTIFF and HHT method. Should be an integer greater than 0. |
| `hratio` | Integer | Specify the number of times the step size goes into the output sampling rate (that is, hratio=dtout/h) for the GSTIFF and HHT method. Should be an integer greater than 0 and it is relevant if fixed_iterations is specified. |
| `max_error` | Real | Specifies the amount of error above which the user would like Adams Solver to stop trying to solve the problem for the GSTIFF and HHT method. Value should be positive real and it is relevant if fixed_iterations is specified. |
