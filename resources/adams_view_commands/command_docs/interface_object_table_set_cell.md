# interface object_table set cell

Allows you to alter the contents of single or multiple cells in a object tableThe object_table is used to list one or more types of objects in a modeling environment. For example, a type of entities like link, center_marker or properties like mass, inertia can be selectively listed and displayed using this command. The objects listed can be edited, or copied as required.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `object_table _name` | An Existing GI_otable | Specifies the name of the object_table in which the cells are to be altered |
| `use_cell_selected` | True_only | Specifies the cell to be altered directly |
| `row_range` | Integer | Specifies the range of rows to be altered |
| `use_row_selected` | True_only | Specifies the row in which cells are altered |
| `object_rows` | An Existing Entity | Specifies the row to be altered by entering the object name for the row |
| `use_column_selected` | True_only | Specifies the column in which the cells are altered |
| `column_range` | Integer | Specifies the range of columns in which the cells are to be altered |
| `field_name_of_column` | String | Specifies the column in which the cells are altered by entering the field name |
| `string` | String | Specifies the new contents of the cell |
| `action` | Col_action | Specifies the mode of insertion of new contents |
