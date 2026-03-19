# variable set

Allows you to set the value of an existing Adams View variable.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `variable_name` | String | Specifies an existing Adams View variable. You may identify an Adams View variable by typing its name. |
| `comments` | String | Allows you to store a multi-line comment describing the Adams View variable. |
| `real_value` | Real | Assigns a real number to be stored in this Adams View variable. |
| `units` | String | Allows you to specify the type of units to be used if the variable is defined to be an object only. |
| `range` | Real, Real | Specifies range of values allowed for this variable. |
| `allowed_values` | Real, Real | Specifies allowed values for this variable. |
| `delta_type` | ABSOLUTE/RELATIVE/PERCENT_RELATIVE | ABSOLUTE default value will be used if this parameter is omitted. |
| `use_range` | Yes/No | Specifies whether the range specified above should be applied on the variable. |
| `use_allowed_values` | Yes/No | Specifies whether the allowed values specified above should be applied on the variable |
| `integer_value` | Integer | Assign an integer number to be stored in this Adams VIEW variable |
| `string_value` | String | Assign a string to be stored in this Adams View variable. |
| `object_value` | Existing entity | Assign an existing object to be stored in this Adams View variable. |
| `index` | Integer | Specifies the location at which to store the values in the variable. |
