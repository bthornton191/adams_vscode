# ude modify instance

Modifies a User Defined Element (UDE) instance; primarily for modifying its location orientation not its parameter values.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_name` | An existing UDE instance | Specifies the name of the UDE instance to be modified; note that UDE instances are children of models |
| `new_instance_name` | a new UDE instance | Specifies new name of the UDE instance. You may use this name later to refer to this UDE instance. |
| `comments` | string | Specifies comments for the UDE instance being created |
| `location` | location | Specifies the location of the origin of the UDE instance using three coordinates |
| `orientation` | orientation | Specifies the orientation of the UDE instance using three rotation angle |
| `relative_to` | an existing model, part or marker | Specifies the coordinate system to which the location coordinates and orientation angles correspond |
