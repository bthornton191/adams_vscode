# executive_control set kinematics_parameters

KINEMATICS_PARAMETERS allow control over the kinematic simulation in Adams. Kinematics parameters include error tolerances and other parameters for kinematic analyses. You would set these parameters only when you are requesting a kinematic analysis and you want to change one or more of the tolerances and parameters from the default values.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | String | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `alimit` | Real number | Specifies the maximum angular increment Adams is to allow per iteration. Can take a real value greater than zero. |
| `error` | Real number | Specifies the maximum relative displacement error Adams is to allow. Can take a real value greater than zero. |
| `maxit` | Integer number | Specifies the maximum number of iterations Adams is to allow for finding static equilibrium in a static equilibrium analysis. Can take an integer value greater than zero. |
| `aerror` | Real number | Specifies the maximum acceleration error Adams is to allow for each time step during a kinematic solution. |
| `amaxit` | Integer number | Specifies the maximum number of iterations Adams is to allow for finding accelerations at a point in time during a kinematics solution. |
| `tlimit` | Real number | Specifies the maximum translational increment Adams is to allow per iteration. |
| `hmax` | Real number | Real number |
| `pattern_for_jacobian` | Yes/No | Specifies as many as ten character strings that together establish the pattern for evaluating the Jacobian matrix during Newton-Raphson iteration. |
| `apattern_for_jacobian` | Yes/No | Specifies as many as ten character strings that together establish the pattern for Jacobian evaluations during acceleration solution. |
