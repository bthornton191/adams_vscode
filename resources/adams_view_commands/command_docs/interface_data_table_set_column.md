# interface data_table set column

Allows you to alter the columns in a data table field.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `data_table _name` | An Existing GI_data_table | Specifies the name of an existing data table. |
| `widths` | Integer | Specifies the new widths for existing columns. |
| `labels` | String | Specifies the new labels for existing columns. |
| `use_column_selected` | True_only | Specifies the range of columns to be altered. |
| `range` | Integer | Specifies the range of columns to be altered. |
| `indices` | Integer | Specifies the range of columns to be altered. |
| `strings` | String | Specifies the new STRING contents for the cells. |
| `reals` | Real | Specifies the new REAL contents for the cells. |
| `integers` | Integer | Specifies the new INTEGER contents for the cells. |
| `repeat_strings` | Boolean | Specifies whether same STRING or REAL will be inserted to all marked cells; valid options are yes/no. |
| `enabled` | Boolean | Specifies if the columns are read only or editable; valid options are yes/no. |
| `action` | Col_action | Specifies the mode of insertion of new contents in to the cells; valid options are replace/append/prefix. |
| `value_type` | text_type | Specifies column's cell text as string, integer, real or default. |
| `db_object_type` | Ent | Specifies the entity type for column. |
| `push_button_label` | String | Specifies push button label for column. |
| `push_button_command` | String | Specifies the command to be executed on push button click. |
| `option_menu_choices` | String | Specifies option menu choices for column on option change. |
| `option_menu_command` | String | Specifies the command to be executed. |
| `toggle_button_label` | String | Specifies toggle button label for column on toggles buttons state change. |
| `toggle_button_command` | String | Specifies the command to be executed. |
