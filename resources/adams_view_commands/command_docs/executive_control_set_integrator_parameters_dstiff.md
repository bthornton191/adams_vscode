# executive_control set integrator_parameters dstiff

The DSTIFF command specifies the integration error tolerance and other parameters for a dynamic analysis using the DASSL computer code.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `error_tolerance` | Real | Specifies the integration error tolerance. The ERROR_TOLERANCE parameter is also used to determine the convergence criterion for the corrector. The convergence tolerance is the value of ERROR_TOLERANCE parameter divided by 1000. |
| `hinit_time_step` | Real number | Specifies the initial time step to be attempted in the integrator. |
| `hmax_time_step` | Real number | Specifies the maximum integration step size Adams is to allow. |
| `kmax_integrator_order` | Integer | Specifies the maximum order of the integrator. Reducing KMAX may speed integration when damping is light and the equations are numerically stiff. |
| `maxit_corrector_iterations` | Integer | Specifies the maximum number of iterations that the corrector will take before the integrator backs off on the current value of the time step and tries a smaller value to achieve further progress. |
| `pattern_for_jacobian` | Yes/No | Specifies as many as ten character strings that together establish the pattern for evaluating the Jacobian matrix during Newton-Raphson iteration. |
| `watch_integrator_perf` | MONITOR, NO_MONITOR, INTERR, NO_INTERR, CORERR, NO_CORERR, | Specifies as many as nine character strings that together establish the aspects of integrator performance you want to watch. |
| `reconcile_vel_and_acc` | YES/NO | Reconciles the values of the displacements with the constraint equations in the problem. |
