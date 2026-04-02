# file iges write

Allows you to write geometry from an Adams View model to an IGES file.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the IGES file to write. |
| `model_name` | An Existing Model | Specifies the model whose geometry is exported. |
| `analysis_name` | An Existing Analysis | Specifies the analysis from which a deformed configuration is exported. |
| `frame_number` | Integer | Specifies the frame number of the animation to export when an analysis is specified. |
| `part_name` | An Existing Part | Specifies one or more specific parts to export instead of the entire model. |
| `active_only` | Boolean | Specifies whether to export only the currently active (visible) geometry. |
