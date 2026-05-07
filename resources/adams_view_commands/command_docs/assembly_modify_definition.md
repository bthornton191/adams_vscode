# assembly modify definition

Allows you to modify an existing assembly definition.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `definition_name` | An Existing Assembly Definition | Specifies the assembly definition to modify. |
| `new_definition_name` | A New Assembly Definition | Specifies a new name for the assembly definition. |
| `isa` | String | Specifies the parent assembly definition that this definition inherits from. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `objects` | An Existing Entity | Specifies the objects included in the assembly definition. |
| `parameters` | String | Specifies the parameter names associated with this assembly definition. |
| `input_parameters` | String | Specifies the input parameter names for this assembly definition. |
| `output_parameters` | String | Specifies the output parameter names for this assembly definition. |
| `expose_contents` | Boolean | Specifies whether the internal objects of the assembly are visible at the parent level. |
| `create_macros` | Boolean | Specifies whether to automatically create macro commands for this assembly definition. |
