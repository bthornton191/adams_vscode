# interface data_table set row

Allows you to alter the rows in a data table field.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `data_table _name` | An Existing GI_data_table | Specifies the name of an existing data table |
| `use_row_selected` | True_only | Specifies the range of rows to be altered |
| `range` | Integer | Specifies the range of rows to be altered |
| `indices` | Integer | Specifies the range of rows to be altered |
| `strings` | String | Specifies the new STRING contents for the cells in the row |
| `reals` | Real | Specifies the new REAL contents for the cells in the row |
| `repeat_strings` | Boolean | Specifies whether same STRING or REAL contents will be inserted to all marked cells |
| `action` | Col_action | Specifies the mode of insertion of new contents in to the cells of the row |
| `enabled` | Boolean | Specifies if the rows are read only or editable |
