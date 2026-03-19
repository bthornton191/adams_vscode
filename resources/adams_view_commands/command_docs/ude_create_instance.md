# ude create instance

Creates a User Defined Element (UDE) instance.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `instance_name` | a new UDE instance | Specifies the name of the UDE instance to be created; note that UDE instances are children of models |
| `definition_name` | an existing UDE definition | Specifies the name of the UDE definition upon which this instance is based. |
| `comments` | string | Specifies comments for the UDE instance being created. |
| `location` | location | Specifies the location of the origin of the UDE instance using three coordinates. |
| `orientation` | orientation | Specifies the orientation of the UDE instance using three rotation angle. |
| `relative_to` | an existing model, part or marker | Specifies the coordinate system to which the location coordinates and orientation angles correspond. |
