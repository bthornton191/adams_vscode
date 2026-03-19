# ude connect

Connects the output parameters of one User Defined Element (UDE) instance to the input parameters of another. The UDE instances need not be instances of the same UDE definition.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_name` | An Existing UDE Instance | Specifies the name of an existing UDE whose output parameters will be connected to the input parameters of the UDE specified for to_instance_name. |
| `to_instance_name` | An Existing UDE Instance | Specifies the name of an existing UDE whose input parameters will be connected to the output parameters of the UDE specified for instance_name. |
