# interface object_table set row

Allows you to alter the contents of single or multiple rows in a object_table

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `object_table _name` | An Existing GI_otable | Specifies the name of the object_table in which the cells are to be altered |
| `use_row_selected` | True_only | Specifies a row to be altered |
| `row_range` | Integer | Specifies the range of multiple rows to be altered |
| `object_rows` | An Existing Entity | Specifies the object name listed in the row |
| `new_row_entity` | An Existing Entity | Specifies the new object which will be added to the table |
| `row_action` | Row_action | Specifies the mode of insertion of new row |
| `strings` | String | Specifies the new contents of the cells in a modified row |
