# group modify

Allows the modification of an existing Adams View groups.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `group_name` | Group Name | Specifies the name of the existing group to be modified. |
| `new_group_name` | New Group Name | Specifies the new name for the group. You may us e this name later to refer to this group. |
| `comments` | String | Specifies comments for the group being created or modified. |
| `objects_in_group` | Entity | Specify the objects to be in the group. |
| `type_filter` | Entity Type | Specify the type of objects allowed. |
| `expand_groups` | Yes/no | Specify a Boolean value |
| `expr_active` | Integer | EXPR_ACTIVE allows you to set the activity of the group using an integer value, which allows parameterization. |
