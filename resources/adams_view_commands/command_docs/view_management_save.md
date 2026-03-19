# view management save

The SAVE command is used to save the current view attributes. These attributes can be restored with the 'VIEW MANAGE RESTORE' command. The attribute values include object location and orientation, render type, distance from viewing object and so on. The contents of the view are not saved. If the SAVED_VIEW_NAME parameter is used, the current values of the screen view will be saved into that view, and that view will replace the original view on the screen. Displayed views cannot be used with the SAVED_VIEW_NAME parameter.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | Existing View | Specifies the view name in which the current view attributes should be saved |
| `saved_view_name` | New or Existing View | The SAVED_VIEW_NAME parameter is used to specify a view that is not displayed. |
