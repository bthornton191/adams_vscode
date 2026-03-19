# data_element create array general_array

Allows you to create a general_array. Creates a one-dimensional array of real numbers that can be accessed in user-written subroutines. This array is identical in definition to the IC_ARRAY. The GENERAL_ARRAY has been provided to maintain consistency with the ARRAY available in Adams version 5.2.1.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `array_name,` | Array name | Specifies the name of the new array. You may use this name later to refer to this array. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `size` | Integer | Specifies the size of an array. |
| `numbers` | Real | Allows you to enter a one dimensional array of real numbers when using the IC_ARRAY of the GENERAL_ARRAY. The number of entries should match the value of the SIZE parameter. |
