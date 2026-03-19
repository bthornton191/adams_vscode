# simulation single_run transient

Enables Adams View to perform either a:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies an existing model. |
| `initial_static` | Yes/no | Specifies whether or not Adams is to execute a static solution prior to the main simulation. |
| `type` | Dynamic/ Kinematic/ Static/ Auto_select | Select a type of simulation to run: |
| `number_of_steps` | Integer | Represents the total number of times you want Adams View to provide output information over your entire simulation |
| `step_size` | Real | Represents the amount of time, in current model units, between output steps. |
| `end_time` | Real | Specifies the absolute point in time at which you want the simulation to stop. |
| `duration` | Real | Specifies the amount of time over which you want the simulation to run. The DURATION must be greater than zero. |
| `forever` | True | Boolean value specifying whether or not the simulation has to run forever. |
