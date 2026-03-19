# model merge

Allows you to merge one model into another. The 'model_name' model is the source of the objects being merged and the 'into_model_name' model is the destination model. The rotation is performed on the model and then it is translated.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model |
| `into_model_name` | An Existing Model | The model into which the model specified by 'model_name' will be merged. |
| `translation` | Location | This parameter specifies the translations (relative to the global origin) that are applied to the parts, polylines, and notes beneath the source model, before it is merged with the destination model. |
| `rotation` | Orientation | This parameter specifies the rotations (about the global origin) that are applied to the parts, polylines, and notes beneath the source model before it is merged with the destination model. |
| `duplicate_parts` | Dupl_Part_Action | This parameter specifies what to do when a part in the destination model has the same name as a part in the source model. |
| `add_to_group_name` | A New Or Existing Group | This parameter specifies a new or existing group into which Adams View will add all the merged objects. |
