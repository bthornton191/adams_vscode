# panel set twindow_function force_vector

Configures the panel test window function to return a component of a force vector element.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `force_vector_name` | Object | Name of the force vector element to query. |
| `return_value_on_marker` | Object | Marker on which the force is computed. |
| `component` | Integer | Force component to return (e.g., 1=x, 2=y, 3=z, 4=magnitude). |
| `reference_marker` | Object | Reference marker for expressing the force components. |
