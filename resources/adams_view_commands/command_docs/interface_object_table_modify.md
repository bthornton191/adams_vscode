# interface object_table modify

Allows you to modify the contents of an existing object_table.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `object_table _name` | An Existing GI_otable | Specifies the name of an existing object_table to be modified |
| `new_object_table_name` | A New GI_otable | Specifies a new name for an existing object_table |
| `enabled` | Boolean | Activates the object_table |
| `help_text` | String | Specifies the help text |
| `documentation_text` | String | Specifies the documentation text |
| `units` | Int_units | Specifies the object_table size as pixel or relative to Adams window |
| `horiz_resizing` | Int_h_resize | Specifies the attachment and scaling option for the object_table |
| `vert_resizing` | Int_v_resize | Specifies the attachment and scaling option for the object_table |
| `location` | Real | Specifies the location of the object_table on the dialog box |
| `height` | Real | Specifies the height of the object_table in terms of relative units or pixel |
| `width` | Real | Specifies the width of the object_table field in terms of relative units or pixel |
| `commands` | String | Specifies the command to be executed |
| `cell select commands` | String | Specifies the command to be executed whenever any cell is selected |
| `entity type` | Ent | Specifies the entity types to be listed in the object_table |
| `fields_for_columns` | String | Specifies the fields associated with the object to be entered in the columns |
| `column_widths` | Integer | Specifies the column width for a object_table to be created |
| `filter_function` | An Existing Expr Func | Specifies the type of filter to be applied for listing the object types |
| `displayed entities` | An Existing Entity | Specifies the list of entities to be displayed |
| `parent entity` | An Existing Entity | Specifies the parent entity to which the object belongs |
| `sorting column index` | Integer | Specifies the index of the column to be sorted |
| `type of sort` | Sort_type | Specifies the mode of sorting the table contents |
| `ground reference frame` | Boolean | Specifies the ground reference frame |
| `editable` | Boolean | Specifies whether the table contents can be edited or not |
