# model generate_ids

This command sets the adams_ids of all objects that are descendents of the specified models. The adams_ids can be set to positive integers, as required by Adams Solver or can be all set to zero.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_names` | String | Existing model name (s) whose descendents will have their adams_ids set. |
| `zero_ids` | yes/no | If set to yes, adams_ids will be set to zero.If set to no, adams_ids will be set to positive integers. |
