# ude disassemble

Moves the basic Adams elements (for example: parts, force and so on.) that compose a User Defined Element (UDE) instance from the UDE instance and into the model in which the instance resided. The now emptied instance is then deleted from the model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_name` | An Existing UDE Instance | Specifies the name of an existing UDE instance to be disassembled. |
| `top_level_only` | Yes/No | If "top_level_only" is "yes", this command disassembles only the instance that is passed to the command. Otherwise, it recursively disassembles all the children of the input instance. |
