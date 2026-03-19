# group delete

Allows the deletion of an Adams View group. When objects in a group are deleted, they are deleted in the same manner as other delete operations in Adams View. That is, they are checked for dependent objects, and if any dependencies are found the object can not be deleted.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `group_name` | Existing group | Specifies the group to delete. |
