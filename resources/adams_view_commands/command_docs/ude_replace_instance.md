# ude replace instance

Replaces the "type" (that is, the definition) associated with the instance. This is useful, for example, when there are multiple modeling methods for the same physical item and one wants to switch between them.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_name` | An Existing UDE Instance | Specifies the name of an existing UDE instance whose UDE definition will be replaced. |
| `with_type` | An Existing UDE Definition | Specifies the name of an existing UDE definition that will replace the UDE definition upon which the UDE instance specified in "instance_name" is based. The definition specified here as "with_type" must be of the same "class" of UDE definitions as defined via the "isa" argument when ude create definition or ude modify definition. |
