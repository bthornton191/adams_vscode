# simulation script modify

Allows you to modify an existing simulation script.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `sim_script_name` | An Existing Sim_script | Specifies the name of the script to be created |
| `comments` | String | Enters comments for the script to be created, if any. |
| `initial_static` | Yes/no | Sets static simulation to be performed before the dynamic simulation |
| `type` | Trans_type | Specifies the type of simulation to be run |
| `number_of_steps` | Integer | Represents the total number of times you want Adams View to provide output information over your entire simulation |
| `step_size` | Integer | Represents the amount of time, in current model units, between output steps. |
| `end_time` | Time | Specifies the absolute point in time at which you want the simulation to stop. |
| `duration` | Time | Specifies the amount of time over which you want the simulation to run. |
| `commands` |  | Enters a set of Adams View commands, including commands that change the model or Adams Solver settings |
| `solver_commands` |  | A set of Adams Solver commands, including commands that change the model or Adams Solver settings. |
