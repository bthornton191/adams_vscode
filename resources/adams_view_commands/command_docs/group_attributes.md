# group attributes

Allows the specification of attributes to be set on a group

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `group_name` | An Existing Group | Specifies the group to be modified. You use this parameter to identify the existing group to be affected with this command. |
| `scale_of_icons` | Real | Specifies a unit-less scale factor to apply to the current icon size. |
| `size_of_icons` | Real | Specifies the size, in modeling units, the Adams View icons will appear in. |
| `visibility` | On / Off / No_opinion / Toggle | Specifies the visibility of graphic entities |
| `name_visibility` | On / Off / No_opinion / Toggle | The NAME_VISIBILITY parameter provides control over the visibility of the view name displayed at the top center position of a given view. |
| `color` | An Existing Color | Specifies the color the modeling entity should be drawn in. |
| `line_thickness` | Real | Specifies the thickness of the line for a curve |
| `line_type` | Line_style | This parameter allows the selection of the line type for a curve. |
| `entity_scope` | Color_scope | The ENTITY_SCOPE parameter is used to control how a color modification is to affect a particular graphic entity. |
| `active` | On / Off / No_opinion | Controls the activity of the group and thereby all objects in the group. Specifying no_opinion leaves the existing activity state unchanged.When you set ACTIVE=OFF, that element is written to the data set as a comment. |
| `dependents_active` | On / Off / No_opinion | Specifies whether dependents of the objects are to be acted upon in the same way as the active parameter does. |
| `member_dependents_active` | On / Off / No_opinion | Controls the activity of the dependents of all objects in the group |
