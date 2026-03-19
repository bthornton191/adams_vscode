# ude replace type_of_instance

Replaces the all UDE instances of one definition with another. This is useful, for example, when there are multiple modeling methods for the same physical item and one wants to switch between them, and there are multiple instances of that item in the model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_type` | An Existing UDE Definition | Specifies the UDE definition on which all the instances to be replaced are based. |
| `parent` | An Existing Model | Specifies the parent object, typically a model, representing the boundary of the search are for UDE instances that are based on instance_type. |
| `with_type` | An Existing UDE Definition | All the UDE instances which are currently based on the UDE definition specified in instance_type will be replaced such that they will now be based upon the UDE definition specified here. |
