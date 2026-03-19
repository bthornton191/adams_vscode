# interface model_browser mbfilter create

Allows you to create a filter object in the database.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `mbfilter_name` | String | Name of the filter |
| `objects_in_mbfilter` | String | List of objects in the mbfilter. Used for saving non-dynamic filters to command models |
| `dynamic: true or false` | Boolean | To set the state of the filter to static or dynamic |
| `name_filters` | String | List of name filters for the model browser filter |
| `type_filters:` | String | List of type filters for the model browser filter |
| `state_filters:` | String | List of the object state filters for the model browser filter |
