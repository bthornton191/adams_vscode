# callback create

Allows you to create multiple callback routines within a single model. This allows the design of HPC solutions in the user space. It provides a clear framework for users who implement complex user subroutines to design memory management and parallel simulations running along Adams simulation.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `callback_name` | New callback | Specifies the name of the callback to be created. |
| `adams_id` | Integer | Assigns an unique id to the callback entity. |
| `routine` | String | Specifies an alternative library and user subroutine name. |
| `priority` | Integer | Used by the Solver to order existing CBKSUBS and call subroutines according to their priority. Solver will sort from higher to lower priority. |
