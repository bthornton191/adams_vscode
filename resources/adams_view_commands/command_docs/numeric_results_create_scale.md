# numeric_results create scale

Allows you to multiply all the elements of a result set component, either real or complex, by some value and then add a constant value. The form of the equation is:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_component_name` | An Existing Component | Identifies the component of an existing result set. |
| `new_result_set_component_name` | A New Component | Allows you to identify where the new data components are to be stored. |
| `a_scale_value` | Real | The A_SCALE_VALUE parameter is used as a constant coefficient in the scale operation for manipulating numeric results. |
| `b_offset_value` | Real | Specifies the constant real value that is to be added to a scaled RESULT_SET_COMPONENT |
| `units` | Units_Type_With_Calc | Allows you to specify the type of units to be used for the new result set component. |
