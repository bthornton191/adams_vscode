# move object

Allows you to set the position of a part or marker.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `marker_name` | An Existing Marker | Specifies the marker to be modified. You use this parameter to identify the existing marker to be affected with this command. |
| `part_name` | An Existing Part | Specifies the part to be modified. You use this parameter to identify the existing part to be affected with this command. You may identify a part by typing its name or by picking it from the screen. |
| `flexible_body_name` | An Existing Flex_body | Specifies the name of an existing flexible body to modify. You may identify a flexible body by typing its name, by selecting it from the database navigator's select list or by picking its graphical representation from the screen, whichever is most convenient. |
| `point_mass_name` | An Existing Point_mass | Specifies the point_mass to be modified. You use this parameter to identify the existing point_mass to be affected with this command. |
| `geometry_name` | An Existing Geometric Entity | Specifies the geometry to be modified. You use this parameter to identify the existing geometry to be affected with this command. |
| `constraint_name` | An Existing Constraint | Specifies the constraint to be modified. You use this parameter to identify the existing constraint to be affected with this command. |
| `force_name` | An Existing Force | Specifies the force to be modified. You use this parameter to identify the existing force to be affected with this command. |
| `group_name` | An Existing Group | Specifies the group to be modified. You use this parameter to identify the existing group to be affected with this command. You may identify a group by typing its name. |
| `entity_name` | An Existing Entity | Specifies an existing entity |
| `c1` | Real | Specifies the first location coordinate to be applied to the marker or part you wish to move. Check the current COORDINATE SYSTEM TYPE by using the command LIST_INFO DEFAULTS. This first location coordinate will be of the current coordinate system type. |
| `c2` | Real | Specifies the second location coordinate to be applied to the marker or part you wish to move. Check the current COORDINATE SYSTEM TYPE by using the command LIST_INFO DEFAULTS. This first location coordinate will be of the current coordinate system type. |
| `c3` | Real | Specifies the third location coordinate to be applied to the marker or part you wish to move. Check the current COORDINATE SYSTEM TYPE by using the command LIST_INFO DEFAULTS. This first location coordinate will be of the current coordinate system type. |
| `a1` | Real | Specifies the first orientation angle to be applied to the marker or part you wish to move. Check the current ORIENTATION TYPE using the command LIST_INFO DEFAULTS, to confirm which axis this angle will be applied to. |
| `a2` | Real | Specifies the second orientation angle to be applied to the marker or part you wish to move. Check the current ORIENTATION TYPE using the command LIST_INFO DEFAULTS, to confirm which axis this angle will be applied to. |
| `a3` | Real | Specifies the third orientation angle to be applied to the marker or part you wish to move. Check the current ORIENTATION TYPE using the command LIST_INFO DEFAULTS, to confirm which axis this angle will be applied to. |
| `csmodel_name` | An Existing Model | Specifies an existing model's global origin to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `cspart_name` | An Existing Part | Specifies an existing part to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csmarker_name` | An Existing Marker | Specifies an existing marker to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csview_name` | An Existing View | Specifies an existing view's origin to use as the coordinate system in a MOVE, or PANEL SET POSITION & ORIENTATION command. |
| `csentity_name` | An Existing Entity | Specifies that the MOVE OBJECT command should be done by adding the coordinates to the existing position of the object(s) being moved |
| `incrementally` | Boolean | Boolean |
