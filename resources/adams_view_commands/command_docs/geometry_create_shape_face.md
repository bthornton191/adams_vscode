# geometry create shape face

Allows you to create a face geometry object by trimming a surface with boundary loops.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `face_name` | A New Face | Specifies the name of the new face. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `surface` | An Existing Surface | Specifies the underlying surface geometry on which the face is defined. |
| `loops` | An Existing Curve | Specifies one or more closed wire curves that define the boundary loops of the face. |
| `surf_sense` | Boolean | Specifies the orientation of the surface normal relative to the underlying surface definition. |
