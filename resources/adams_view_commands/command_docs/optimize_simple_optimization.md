# optimize simple_optimization

Allows you to run a single-objective optimization by systematically varying design variables to minimize or maximize an objective while satisfying constraints.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies the model to optimize. |
| `analysis_name` | A New Analysis | Specifies the name to assign to the analysis run during each optimization iteration. |
| `user_executable` | File | Specifies the name of a custom Adams executable to use for analysis runs. |
| `brief` | On/Off | Specifies whether brief output mode is used during optimization. |
| `analysis_type` | Analysis Type | Specifies the type of simulation to run at each iteration (e.g., transient, static, kinematic). |
| `number_of_steps` | Integer | Specifies the number of output steps for each simulation run. |
| `end_time` | Real | Specifies the simulation end time for each run. |
| `initial_static` | Boolean | Specifies whether an initial static analysis is performed before each dynamic simulation. |
| `adams_command_file` | String | Specifies the contents of an Adams command file used to control simulation execution. |
| `do_not_run_solver` | True | Specifies that the optimization is performed without running Adams Solver. |
| `objective_name` | An Existing Optimization Objective | Specifies the optimization objective to minimize or maximize. |
| `constraint_names` | An Existing Optimization Constraint | Specifies the optimization constraints to satisfy during the optimization. |
| `characteristic` | Analysis Characteristic | Specifies whether to minimize or maximize the objective. |
| `design_variables` | An Existing Design Variable | Specifies the design variables that the optimizer is allowed to vary. |
| `maximum_number_of_iterations` | Integer | Specifies the maximum number of optimization iterations. |
| `convergence_tolerance` | Real | Specifies the convergence tolerance for the optimization algorithm. |
| `differencing_technique` | String | Specifies the finite difference method used to compute gradients (e.g., forward or central difference). |
| `scaled_perturbation` | Real | Specifies the fractional perturbation applied to design variables when computing finite difference gradients. |
| `optimization_algorithm` | String | Specifies the optimization algorithm to use (e.g., MMFD). |
| `user_parameters` | Real | Specifies user-defined parameters passed to the optimization algorithm. |
| `update` | String | Specifies how the model is updated between iterations. |
| `iterations_before_rescale` | Integer | Specifies the number of iterations before the optimizer rescales the design variables. |
| `slp_convergence_iterations` | Integer | Specifies the number of sequential linear programming convergence iterations. |
| `on_objective_error` | String | Specifies the action taken when an objective evaluation error occurs (e.g., stop or continue). |
