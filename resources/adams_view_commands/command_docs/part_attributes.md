# part attributes

Allows you to set attributes for a part:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `part_name` | Existing Part | Specifies the rigid body to be modified |
| `flexible_body_name` | Existing Flex Body | Specifies the flexible body to be modified |
| `external_system_name` | Existing external system | Specifies an external system to be modified |
| `point_mass_name` | Existing Point Mass | Specifies the point mass to be modified |
| `equation_name` | Existing Equation | Specifies the equation to be modified |
| `fe_node_name` | Existing FE_Node | Specifies the FE_Node to be modified |
| `scale_of_icons` | Real | Specifies the amount by which you want to scale the icons. |
| `size_of_icons(mutually exclusive with scale_of_icons)` | Length | Specifies the size, in modeling units, the Adams View icons will appear. |
| `visibility` | On/off/toggle | Specifies the visibility of the part in a view: |
| `name_visibility` | On/off/toggle | Specifies whether or not you want the name of the part displayed in the view |
| `color` | Existing Color | Specifies the color of the part. |
| `entity_scope` |  | Controls how a color modification is to affect a particular graphic entity. |
| `active` | On/off/no_opinion | Sets the activation status of the part during a simulation. |
| `dependents_active` |  | See explanation for active parameter. |
