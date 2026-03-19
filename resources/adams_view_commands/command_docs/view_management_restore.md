# view management restore

This command is used to reset view attributes to the saved values. These saved attribute values include object location and orientation, render type, distance from viewing object and so on. The restore command will not affect the contents of the view. When the view is created, the saved attribute values are the same as the original values. The 'VIEW MANAGEMENT SAVE' command will save the current attributes. If the SAVED_VIEW_NAME parameter is used, the saved values of that view will be restored, otherwise the saved values of the screen view will be restored. Displayed views cannot be used with the saved_view_name parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | Existing View | Specifies the view name in which the current view attributes should be restored to. |
| `saved_view_name` | New or Existing View | The SAVED_VIEW_NAME parameter is used to specify a view that is not displayed. |
