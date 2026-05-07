# panel set twindow_function contact

Configures the panel test window function to return a contact force measurement.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `contact_name` | Object | Name of the contact to query. |
| `return_value_on_marker` | Object | Marker on which to compute the return value. |
| `component` | Integer | Force component to return (e.g., 1=x, 2=y, 3=z, 4=magnitude). |
| `reference_marker` | Object | Reference marker for expressing the force components. |
