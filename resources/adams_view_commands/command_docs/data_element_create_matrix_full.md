# data_element create matrix full

Allows you to create a FULL MATRIX.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `matrix_name` | Matrix name | Specifies the name of the new matrix. You may use this name later to refer to this matrix. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `row_count` | Integer | Specifies the number of rows (M) in the matrix.Used in the definition of a full matrix. |
| `column_count` | Integer | Specifies the number of columns (N) in the matrix used in the definition of a full matrix. |
| `values` | Real | Specifies the real number values that you enter to populate a FULL MATRIX. |
| `result_set_component_names` | Existing component | You can only use a result set component as matrix values using full format and entering all the values stored in the result set component. |
| `input_order` | By_column,by_row | Specifies the order the values that you input will appear in for a FULL MATRIX format (all of the M by N entries will be specific numeric values |
| `units` | String | Allows you to specify the type of units to be used for this object. |
