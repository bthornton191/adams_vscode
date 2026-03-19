# callback modify

Allows you to modify an existing callback routine.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `callback_name` | Existing callback | Specifies the name of the callback to be modified. |
| `adams_id` | Integer | Assigns an unique id to the callback entity. |
| `routine` | String | Specifies an alternative library and user subroutine name. |
| `priority` | Integer | Used by the Solver to order existing CBKSUBS and call subroutines according to their priority. Solver will sort from higher to lower priority. |
