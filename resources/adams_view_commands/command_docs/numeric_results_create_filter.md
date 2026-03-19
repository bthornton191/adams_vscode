# numeric_results create filter

Allows you to test each value of the component; if the value is above the specified maximum value, or below the specified minimum value, set it to zero. For example: If the component is a discrete sampling of a sinusoidal wave with an amplitude of one (1), and filter is requested with a maximum value of .9 (above_value=.9), all the values corresponding to 'sin (x) > .9' will be set to 0.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_component_name` | An Existing Component | Identifies the component of an existing result set. |
| `new_result_set_component_name` | A New Component | This parameter allows you to identify where the new data components are to be stored. |
| `below_value` | Real | The BELOW_VALUE parameter is used as a critical value evaluator in the operation to be performed. |
| `above_value` | Real | The ABOVE_VALUE parameter is used as a critical value evaluator in the operation to be performed. |
| `units` | Units_Type_With_Calc | Allows you to specify the type of units to be used for the new result set component. |
