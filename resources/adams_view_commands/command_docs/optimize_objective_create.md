# optimize objective create

Allows you to create an optimization objective that defines the goal (quantity to minimize or maximize) for the optimization.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `objective_name` | A New Optimization Objective | Specifies the name of the new optimization objective. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `allowable_value` | Real | Specifies the allowable target value for the objective. |
| `indifference_value` | Real | Specifies the indifference value; differences smaller than this are considered insignificant. |
| `result_set_component` | String | Specifies the result set component used to evaluate the objective. |
| `output_characteristic` | Output Characteristic | Specifies which characteristic of the result set component is used (e.g., maximum, minimum, or RMS). |
| `measure_name` | An Existing Measure | Specifies a measure whose value is used to evaluate the objective. |
| `function_name` | An Existing Expression Function | Specifies an expression function whose value is used to evaluate the objective. |
| `n_components` | Integer | Specifies the number of objective components when using a vector objective. |
| `variable_name` | An Existing Design Variable | Specifies a design variable whose value is used as the objective value. |
| `macro_name` | An Existing Macro | Specifies a macro that computes the objective value. |
