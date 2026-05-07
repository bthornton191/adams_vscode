# group objects attributes

Allows you to set or modify the display attributes of all objects in a group.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `group_name` | An Existing Group | Specifies the group whose objects' display attributes are to be modified. |
| `scale_of_icons` | Real | Specifies a scale factor applied to icon sizes for objects in the group. |
| `size_of_icons` | Length | Specifies the absolute icon size for objects in the group. |
| `visibility` | On/Off | Specifies whether the objects in the group are visible. |
| `name_visibility` | On/Off | Specifies whether name labels of the objects in the group are visible. |
| `transparency` | Integer | Specifies the transparency level of the objects, from 0 (opaque) to 100 (fully transparent). |
| `lod` | Real | Specifies the level-of-detail threshold for objects in the group. |
| `color` | An Existing Color | Specifies the display color of the objects in the group. |
| `line_thickness` | Real | Specifies the line thickness for rendered wireframe objects in the group. |
| `line_type` | String | Specifies the line type for rendered wireframe objects in the group. |
| `entity_scope` | String | Specifies the scope of entities affected by the attribute changes. |
| `active` | On/Off | Specifies whether the objects in the group are active in the simulation. |
| `dependents_active` | On/Off | Specifies whether dependent entities of the group objects are active. |
| `type_filter` | String | Specifies a filter limiting which object types within the group are affected. |
