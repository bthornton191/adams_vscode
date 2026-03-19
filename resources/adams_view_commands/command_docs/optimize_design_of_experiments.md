# optimize design_of_experiments

The DESIGN_OF_EXPERIMENTS command allows you to perform a number of analyses on a parametric model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies an existing model |
| `analysis_name` | Existing Analysis | Specifies an existing analysis |
| `user_executable` | String | Specifies the name of the user Adams executable to use for this analysis. If no values are specified, the standard Adams executable is run. |
| `brief` | On, Off | Specifies whether or not to display the brief form of the information about the analysis being submitted. If set to Off, the entire output from the Adams run will be displayed in the info_window. If set to On, only errors and warnings will be displayed. |
| `on_objective_error` | Stop, Continue | Indicates how Adams View should handle an invalid/nonexistent objective |
| `analysis_type` | Dynamics, Kinematics, Statics, Transient | Specifies which type of analysis you want Adams to perform. |
| `number_of_steps` | Integer | The number of values to be stored in each component of a result set being read from a file. |
| `end_time` | Real | Specifies the end time for a dynamic, kinematic, or quasi-static equilibrium analysis. |
| `initial_static` | Yes, No | Specifies whether or not Adams is to execute a static solution prior to the main simulation. |
| `adams_command_file` | String | Specifies the contents of the Adams command file to use to control the execution of the Adams simulation. |
| `do_not_run_solver` | True | When you set DO_NOT_RUN_SOLVER to TRUE (its only possible value), you are indicating that the DOE or optimization is to take place without using Adams Solver. This is only possible when you have a model whose design functions (objectives or constraints) are not dependent upon analysis results in any way. |
| `objective_name` | Existing Objective | Specifies the names of the objectives that are to be evaluated at every run during the Design of Experiments analysis. |
| `design_variables` | Existing Design Variable | The DESIGN_VARIABLES parameter allows you to specify which Adams View variables are to be modified for the DOE runs. Each variable must have its ALLOWED_VALUES specified for the DOE algorithms to operate. |
| `technique` | Doe Technique | When you perform a Design of Experiments analysis, you may select a built-in technique for creating the trial matrix. |
| `number_of_user_trials` | Integer | Use the NUMBER_OF_USER_TRIALS parameter with the USER_MATRIX parameter to indicate how many user trials are being entered. |
| `user_matrix` | Integer | The USER_MATRIX parameter specifies indexes to the levels for each variable. |
| `matrix_file_name` | String | Specifies the file in which the DOE trials are described |
