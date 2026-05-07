# geometry modify shape csg

Allows modification of an existing Constructive Solid Geometry (CSG) object.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `csg_name` | An Existing CSG | Specifies the name of the existing CSG object to modify. |
| `new_csg_name` | A New CSG | Specifies a new name for the CSG object. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `type` | CSG Type | Specifies the type of boolean operation. Options are union, intersection, or subtraction. |
| `explode` | Boolean | Specifies whether to explode the CSG object, separating it into its component geometries. |
| `explode_children` | Boolean | Specifies whether to recursively explode any child CSG objects during the explode operation. |
