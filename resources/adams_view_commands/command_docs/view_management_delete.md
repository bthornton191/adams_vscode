# view management delete

The DELETE command may be used to delete a viewport from the screen. This operation can also be used to delete a set of saved view parameters (attributes) from the data base. If a view displayed on the screen is to be deleted, then the VIEW_NAME parameter is required. If the view to be deleted is not displayed (i.e. but stored in the database) the SAVED_VIEW_NAME parameter is required. The deletion of a view from the screen does not force the set of saved view attributes to be deleted from the database (in fact, if the attributes of a screen view have not been saved to the database prior to the attempt to delete it, a warning message will be issued).

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `view_name` | Existing View | Specifies a displayed view that is to be deleted. |
| `saved_view_name` | Existing View | The SAVED_VIEW_NAME parameter is used to specify a view that is not displayed. |
