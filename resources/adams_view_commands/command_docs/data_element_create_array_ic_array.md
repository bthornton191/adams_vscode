# data_element create array ic_array

Allows you to create an ic_array. This element creates a one-dimensional array of real numbers that can be accessed in user-written subroutines. You can use an IC_ARRAY to designate define initial conditions array for an LINEAR_STATE_EQUATION or GENERAL_STATE_EQUATION. In that case, you should ensure that the value of the SIZE parameters the same as the X_STATE_ARRAY (state variable) of the associated LINEAR_STATE_EQUATION or GENERAL_STATE_EQUATION.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `array_name,` | Array name | Specifies the name of the new array. You may use this name later to refer to this array. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `size` | Integer | Specifies the size of an array. |
| `numbers` | Real | Allows you to enter a one dimensional array of real numbers when using the IC_ARRAY of the GENERAL_ARRAY. The number of entries should match the value of the SIZE parameter. |
