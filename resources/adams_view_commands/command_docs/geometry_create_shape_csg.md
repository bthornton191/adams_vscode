# geometry create shape csg

Allows you to create a Constructive Solid Geometry (CSG) object by performing a boolean operation between two existing solid geometry objects.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `csg_name` | A New CSG | Specifies the name of the new CSG object. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `base_object` | An Existing Geometry | Specifies the base geometry object on which the boolean operation is performed. |
| `object` | An Existing Geometry | Specifies the tool geometry object applied to the base object in the boolean operation. |
| `type` | CSG Type | Specifies the type of boolean operation to perform. Options are union, intersection, or subtraction. |
