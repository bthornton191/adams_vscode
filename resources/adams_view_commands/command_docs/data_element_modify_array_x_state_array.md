# data_element modify array x_state_array

Allows you to modify an existing x_state_array.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `array_name` | An Existing Array | Specifies the name of an existing array |
| `new_array_name` | A New Array | Specifies the name of the new array. You may use this name later to refer to this array. |
| `adams_id` | Adams_id | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `size` | Integer | Specifies the size of an array. In cases where Adams calculates the SIZE differently from the SIZE that the user supplies, Adams returns an error or warning message. |
