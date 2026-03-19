# simulation single_run scripted

Instead of letting Adams View set the commands to be run during an interactive simulation, you can create a simulation script. A simulation script lets you program the simulation and add advanced options to your simulation. Simulation scripts are useful when you have come up with a good set of simulation parameters that you want to repeat again and again. They are also needed for design study, design of experiment, and optimization simulations. For example, you can use a simulation script to activate and deactivate portions of your model or change solution settings during the simulation. Simulation scripts can do everything that the interactive controls can.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies an existing model. |
| `sim_script_name` | Existing Script Name | Enters the name of the script to be executed during simulation. |
| `reset_before_and_after` | Yes/no | Enters yes or no, depending on whether you want the simulation to be reset before and after the script is executed. |
