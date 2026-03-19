# executive_control set dynamics_parameters coord_partitioning_parameters

The COORD_PARTITIONING_PARAMETERS command allows you to control the coordinate partitioning algorithm for the Adams-Bashforth-Moulton integrator. This command affects the coordinate partitioning as well as the iterative solutions for the dependent displacements and the accelerations and Lagrange multipliers.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `dd_relative_error` | Real | Specifies the relative error tolerance for the iterative solution of the displacements of the dependent coordinates. The relative error for the displacements will be bounded by a minimum of DD_RELATIVE_ERROR and the integration error tolerance. |
| `dd_absolute_error` | Real | Specifies the absolute error tolerance for the iterative solution of the displacements of the dependent coordinates. The absolute error for the displacements will be bounded by a minimum of dd_absolute_error and 1/100-th of the integration error tolerance. |
| `dd_maximum_iterations` | Integer | Specifies the maximum number of iterations allowed for the modified Newton-Raphson algorithm to converge to the displacements for the dependent coordinates. |
| `dd_pattern_for_jacobian` | Yes/No | Indicates the pattern of yes’s and no’s for reevaluating the Jacobian matrix during the modified Newton-Raphson iterative solution for the displacements of the dependent coordinates. |
| `repartition_threshold` | Real | Allows some control over the re-partitioning of coordinates into independent and dependent coordinates. |
| `al_relative_error` | Real | Specifies the relative error tolerance for the iterative solution of the accelerations and the Lagrange multipliers (i.e. constraint forces). |
| `al_absolute_error` | Real | Specifies the absolute error tolerance for the iterative solution of the accelerations and the Lagrange multipliers (i.e. constraint forces). |
| `al_maximum_iterations` | Integer | Specifies the maximum number of iterations allowed for the modified Newton-Raphson algorithm to converge to the accelerations and the Lagrange multipliers. |
| `al_pattern_for_jacobian` | Yes/No | Indicates the pattern of yes's and no's for reevaluating the Jacobian matrix during the modified Newton-Raphson iterative solution for the accelerations and the Lagrange multipliers. |
| `scaling` | Yes/No | No action will be taken if this parameter is not specified. |
| `scale_factor` | Real | Allows you to specify the amount to scale the geometry that is read in from a Wavefront .obj file. The geometry will be scaled uniformly in the x, y, and z directions. |
| `watch_partitioning_perf` | ERROR_IN_ITERATION, NO_ERROR_IN_ITERATION, FAILURE_IN_ITERATION, | Provides the user with a means for observing the progress of the simulation by causing Adams to write information about the performance of coordinate partitioning calculations onto the screen. |
