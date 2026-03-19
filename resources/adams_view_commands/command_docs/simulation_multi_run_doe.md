# simulation multi_run doe

Allows you to use a set of simulations that help you adjust parameters related to doe.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model. |
| `sim_script_name` | An Existing Sim_script | Enters the name of your simulation script or use the default. |
| `variable_names` | An Existing Var | Enters the name of the design variable that you want to vary. |
| `number_of_levels` | Integer | Specifies the number of levels of the variable |
| `objective_names` | An Existing Objective | Enters the name of the design objective. |
| `measure_name` | An Existing Measure | Specifies the name of an existing measure. |
| `output_characteristic` | Output_characteristic | If you are using a measure set the design objective’s value. |
| `number_of_user_trials` | Integer | Enters the number of trials (simulations) and the trial matrix. |
| `user_matrix` | Integer | Specifies indexes to the levels for each variable. |
| `technique` |  | Selects a DOE technique. |
| `rows_in_table` |  |  |
| `table_of_values` |  |  |
| `matrix_file_name` | String | Specifies the file in which the DOE trials are described. |
