# executive_control set initial_conditions_parameters

Allows you to set the parameters used when solving for initial conditions prior to simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies the model for which the initial conditions parameters are set. |
| `alimit` | Angle | Specifies the maximum change in angle allowed per iteration during initial conditions assembly. |
| `error` | Real | Specifies the convergence error tolerance for translational constraints during initial conditions assembly. |
| `maxit` | Integer | Specifies the maximum number of iterations for translational initial conditions assembly. |
| `aerror` | Real | Specifies the convergence error tolerance for angular constraints during initial conditions assembly. |
| `amaxit` | Integer | Specifies the maximum number of iterations for angular initial conditions assembly. |
| `tlimit` | Length | Specifies the maximum change in translation allowed per iteration during initial conditions assembly. |
| `pattern_for_jacobian` | Boolean | Specifies whether a sparse pattern is used for Jacobian computation during translational assembly. |
| `apattern_for_jacobian` | Boolean | Specifies whether a sparse pattern is used for Jacobian computation during angular assembly. |
