# simulation multi_run preview_doe

Allows you to see each configuration of your model for every design variable. Displays an alert box asking if you want to pause after each configuration. Select YES to pause.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies the name of an existing model. |
| `variable_name` | Existing Variables | Enters the name of the design variable that you want to vary. |
| `number_of_levels` | Integer | Specifies the number of levels to use when you run the design study or DOE. |
| `number_of_user_trials` | Integer | Enters the number of trials (simulations) and the trial matrix. |
| `user_matrix` | Integer | Specifies an integer |
| `rows_in_table` | Integer | Specifies an integer |
| `table_of_values` | Real | Specifies a real number. |
| `technique` | Full_factorial/user1/user2/user3 | Selects a DOE technique. |
| `matrix_file_name` | Filename | Specifies file name containing the matrix of values to be read from. |
