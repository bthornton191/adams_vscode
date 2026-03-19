# executive_control set dynamics_parameters dynamic_solver

The EXECUTIVE_CONTROL SET DYNAMICS_PARAMETERS DYNAMIC_SOLVER command defines the two fundamental components of the mathematical methods for a dynamic solution: the form of the equations and the integration algorithm.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `ordinary_differential_equations` | Ode-type | Causes Adams to reduce the equations governing the dynamics of the problem to a system of ordinary differential equations. The value assigned to the argument specifies the algorithm for doing the reduction. For the 7.0 release, COORDINATE_PARTITIONING is the only option available. |
| `ode_integrator` | ODE_INTEGRATOR | Specifies the numerical method for integrating the ODEs. For the 7.0 release, the value, Adams, is the only option available. |
| `differential_and_algebraic_equations` | STANDARD_INDEX_THREE/LAGRANGIAN_CONSTRAINED/ STABILIZED_INDEX_TWO/ PENALTY | Causes Adams to integrate the full set of Euler-Lagrange differential and algebraic equations. The value assigned to this argument indicates the form of the equations. |
| `dae_integrator` | BDF/BDF_FIXED | Specifies the numerical method for integrating the DAEs. For the 7.0 release, the value, BDF, is the only option available. |
