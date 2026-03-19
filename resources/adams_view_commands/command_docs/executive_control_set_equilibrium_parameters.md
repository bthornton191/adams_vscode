# executive_control set equilibrium_parameters

Controls the error tolerance and other parameters for execution of static equilibrium and quasi-static equilibrium analyses.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An existing model | Specify an existing model. |
| `dynamic` | yes/no | Specifies if dynamic simulation needs to be performed or not to find the static equilibrium. |
| `alimit` | real | Specifies the maximum angular increment allowed per iteration. |
| `error` | real | Specifies the relative correction convergence threshold. |
| `imbalance` | real | Specifies the equation imbalance convergence threshold. |
| `maxit` | integer | Specifies the maximum number of iterations allowed for finding static equilibrium. |
| `pattern_for_jacobian` | string | Specifies the pattern for evaluating Jacobian matrix. |
| `stability` | real | Specifies the fraction of mass and damping matrices to be added to stiffness matrix to stabilize the iteration process. |
| `tlimit` | real | Specifies the maximum translational increment allowed per iteration during static simulations. |
| `global_damping` | real | Specifies the coefficient for global damping applied to all bodies during static simulations performed using dynamic analyses. |
| `settling_time` | real | Specifies the maximum time allowed to reach equilibrium during static simulations performed using dynamic analyses. |
| `acceleration_error` | real | Specifies the maximum acceleration error allowed during static simulations performed using dynamic analyses. |
| `kinetic_energy_error` | real | Specifies the maximum kinetic energy error allowed in static simulations performed using dynamic analyses. |
| `static_method` | original/advanced/aggressive/all | Specifies the type of static method to be selected to perform static equilibrium analyses. |
| `atol` | real | Specifies the absolute tolerance value. |
| `rtol` | real | Specifies the relative tolerance value. |
| `maxitl` | integer | Specifies the maximum number of allowed inner non-linear iterations. |
| `etamax` | real | Specifies the maximum error tolerance for residual in the inner iteration. |
| `eta` | real | Specifies the inner iteration error control parameter. |
