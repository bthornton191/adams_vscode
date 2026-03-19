# model assemble

Allows you to merge several models into one big model.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `new_model_name` | A New Model | The model into which the models specified by 'model_names' will be merged. |
| `model_names` | An Existing Model | Specifies a list of existing models in Adams View, to be merged to create an assembled model. |
| `prefix` | String | This parameter specifies the list of prefixes that are applied to all entities at the part level as they are assembled into a destination model. |
| `suffix` | String | This parameter specifies the list of suffixes that are applied to all entities at the part level, as they are assembled into a destination model. |
| `translation` | Location | Specifies the translations (relative to the global origin) that are applied to the parts, polylines, and notes beneath the source model before it is merged with the destination model. |
| `rotation` | Operation | Specifies the rotations (about to the global origin) that are applied to the parts, polylines, and notes beneath the source model before it is merged with the destination model. |
| `duplicate_parts` | Dupl_Part_Action | Specifies what to do when a part in the destination model has the same name as a part in the source model. |
| `add_to_group_name` | A New or Existing Group | This parameter specifies a new or existing group into which Adams View will add all merged objects. |
