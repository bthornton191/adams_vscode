# simulation multi_run optimization

In general, an optimization problem is described as a problem of minimizing or maximizing an objective function over a selection of design variables, while satisfying various constraints on the design and state variables of the system.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | Existing Model | Specifies the name of the model. |
| `sim_script_name` | Existing Simulation Script | Enters the name of your simulation script or uses the default. |
| `variable_name` | Existing Variable | Specifies an existing variable name that has to be used for the optimization study. |
| `constraint_ names` | Existing Optimization Constraint | Specifies the names of the constraints. |
| `characteristic` | Minimize/maximize | Specifies whether to minimize or maximize the characteristic |
| `output_characteristic` | Minimum/maximum/ Average/ Last_value/ Absolute_minimum/ Absolute_maximum/ Rms/ Standard_deviation | If you are using a measure, set the design objective’s value. For a measure, enter minimum, maximum, average, last_value, absolute_minimum,rms,standard_deviation and absolute_maximum of the measure. |
| `objective_name` | Existing Objective | Enters the name of the design objective. |
| `measure_name` | Existing Measure | Enters the name of an existing measure to be used for the doe. |
