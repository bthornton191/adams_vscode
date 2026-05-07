# optimize constraint create

Allows you to create an optimization constraint that limits the range or value of a design objective during optimization.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `constraint_name` | A New Optimization Constraint | Specifies the name of the new optimization constraint. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `allowable_value` | Real | Specifies the allowable limit value for the constraint. |
| `indifference_value` | Real | Specifies the indifference value; differences smaller than this are considered insignificant. |
| `result_set_component` | String | Specifies the result set component used to evaluate the constraint. |
| `output_characteristic` | Output Characteristic | Specifies which characteristic of the result set component is used (e.g., maximum, minimum, or RMS). |
| `measure_name` | An Existing Measure | Specifies a measure whose value is used to evaluate the constraint. |
| `function_name` | An Existing Expression Function | Specifies an expression function whose value is used to evaluate the constraint. |
| `variable_name` | An Existing Design Variable | Specifies a design variable whose value is used as the constraint value. |
| `macro_name` | An Existing Macro | Specifies a macro that computes the constraint value. |
