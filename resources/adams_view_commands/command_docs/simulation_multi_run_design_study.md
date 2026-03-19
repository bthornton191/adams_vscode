# simulation multi_run design_study

A set of simulations that help you adjust a parameter in your model to measure its effect on the performance of your model. For example, you can run a design study to determine the optimal length required for a driving link in a stamping machine required to make a stamp hit a box.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model. |
| `sim_script_name` | An Existing Sim_script | Specifies the name of your simulation script, or the default is used. |
| `variable_name` | An Existing Vvar | Enters the name of the design variable that you want to vary |
| `number_of_levels` | Integer | If you specified only a range for the design variable, enter the number of levels (values) you want to use in the Default Levels text box. |
| `measure_name` | An Existing Measure | Specifies the name of an existing measure to be used for the doe. |
| `objective_name` | An Existing Objective | Enters the name of the design objective. |
| `output_characteristic` | Output_characteristic | Output_characteristic |
