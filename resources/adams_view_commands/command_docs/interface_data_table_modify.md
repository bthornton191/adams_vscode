# interface data_table modify

Allows you to modify existing data table

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `data_table _name` | An Existing GI_data_table | Specifies the name of an existing data table |
| `new_data_table_name` | A New GI_data_table | Specifies a new name for the existing data table |
| `enabled` | Boolean | Activates the data table |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the data table size as pixel or relative to Adams window |
| `horiz_resizing` | Int_h_resize | Specifies the attachment and scaling option for the data table |
| `vert_resizing` | Int_v_resize | Specifies the attachment and scaling option for the data table |
| `location` | Real | Specifies the location of the data table on the dialog box |
| `height` | Real | Specifies the height of the data table in terms of relative units or pixel |
| `width` | Real | Specifies the width of the data table field in terms of relative units or pixel |
| `cell select commands` | String | Specifies the command to be executed for selecting a cell |
| `commands` | String | Specifies the command to be executed |
| `editable` | Boolean | Allows editing the data table contents |
| `auto_add_rows` | Boolean | When paste area differs in size from copied selection, then it will auto generate the rows to match copied selection. |
