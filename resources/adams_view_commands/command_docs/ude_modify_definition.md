# ude modify definition

Modifies a User Defined Element (UDE) definition.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `definition_name` | An existing UDE definition | Specifies the name of the UDE definition to be modified; note that the name must also include the parent library in which the UDE definition will reside (UDE definitions are not children of models) |
| `new_definition_name` | New UDE definition | Specifies new name of the UDE definition. You may use this name later to refer to this UDE definition. |
| `isa` | An existing UDE Definition | Specifies the name of an existing UDE definition in the same “class” as the UDE definition being modified here. That is, UDE instances can only be replaced with UDE definitions that are of the same “class” (a grouping defined by this “isa” argument). Note that both the input and output parameters must match to be able to replace between UDE definitions. |
| `comments` | string | Specifies comments for the UDE definition being created |
| `objects` | existing entity/entities | Specifies the set of objects that make up the UDE definition |
| `parameters` | existing design variable(s) | Design variables used to control the parameterization of the UDE (spring stiffness for example) |
| `input_parameters` | design variable(s) of type object | Entities outside the UDE referenced by the UDE (typically a reference marker). The parameter itself is an object variable containing the marker reference. |
| `output_parameters` | design variable(s) of type object | Entities inside the UDE that should be accessible outside the UDE (often a marker that can be used as reference for another UDE or other entities). This parameter is an object variable containing the object that should be referenced. |
| `expose_contents` | on / off | When set to ON, then instances of UDE definition will expose their constituent objects in the model browser. |
