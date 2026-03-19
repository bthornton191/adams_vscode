# panel set acf_twindow static_simulation

Specifies the type of analysis you want Adams to perform is static.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `number_of_steps` | Integer | Specifies the number of values to be stored in each component of a result set being read from a file. |
| `step_size` | Real | Specifies the size of the output step for a dynamic, kinematic, or quasi-static equilibrium analysis in model time units. STEP_SIZE must be greater than zero. |
| `end_time` | Real | Specifies the end time for a dynamic, kinematic, or quasi-static equilibrium analysis. |
| `duration` | real | Specifies the duration for a dynamic, kinematic, or quasi-static equilibrium analysis in model time units. The DURATION must be greater than zero. |
