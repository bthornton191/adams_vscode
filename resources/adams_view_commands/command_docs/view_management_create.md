# view management create

The create command allows you to create a new view by splitting an existing view either vertically or horizontally. Any of the view attribute parameters available can be set at the time of view creation. Also, the position of the view split (PICK or SCREEN_COORDS), the orientation of the model in the view (OBJECT_ORIENTATION), and the NEW_VIEW_NAME can be set at creation time. The parameters available include the status of the RENDER, PROJECTION, TRIAD_VISIBILITY, and NAME_VISIBILITY parameters. If not entered, these parameters will default to the same as in the viewport being split.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | Existing View | Each view created has a name associated with it. The view_name parameter is used to identify a view for a particular operation. |
| `new_view_name` | New View | A view name is a string of characters that identifies a viewport or set of viewport attributes stored in the database. |
| `object_orientation` | Angle | The OBJECT_ORIENTATION parameter provides control over the model (analysis_name) angular orientation in the viewport. |
| `eye` | Location | The EYE parameter provides control over the model (analysis_name) angular orientation in the viewport. |
| `screen_coords` | Real,real | Specifies an x,y location in a view on the Adams View screen. SCREEN_COORDS refers to a coordinate reference tied to the terminal screen. |
| `pick` | Location | Specifies a position in a view by picking with the mouse or pen. |
| `render` | Shaded, Wireframe, Solids, Pshaded, Psolids, Sshaded, Plot | The RENDER parameter controls how the graphics in a viewport should be drawn. |
| `projection` | Perspective, Orthographic | The PROJECTION parameter is used during the creation and modification of a view. |
| `triad_visibility` | On/off | The TRIAD_VISIBILITY parameter provides control over the visibility of the coordinate triad displayed at the lower left corner of a given view. The legal values of this parameter are ON and OFF. This is an optional parameter and if not entered, the triad visibility will be ON. |
| `name_visibility` | On/off | The NAME_VISIBILITY parameter provides control over the visibility of the view name displayed at the top center position of a given view. |
| `title_text` | String | Specifies the text that is to be used as a title for a panel GROUP. When a mutually EXCLUSIVE_GROUP is defined, this text serves as a name for the GROUPs as you cycle through them. |
