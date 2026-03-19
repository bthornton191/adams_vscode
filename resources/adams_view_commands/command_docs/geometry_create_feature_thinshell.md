# geometry create feature thinshell

Allows you to hollow out one or more faces of a solid object to create a shell.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `thin_shell_name` | A New Thin_shell | Specifies the name of the thinshell to be created or modified. |
| `subids` | Integer | Specifies the Parasolid tag(s) identifying the face(s) that will be removed to create the thinshell. |
| `thickness` | Length | Specifies the thickness of the remaining shell after you hollow the object. |
| `locations` | Location | Specifies the location(s) of the face(s) that will be removed to create the thinshell. |
