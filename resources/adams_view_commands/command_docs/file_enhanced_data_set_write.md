# file enhanced_data_set write

Allows you to write one or more Adams View entities to an enhanced data set file.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `entity_names` | An Existing Entity | Specifies the entity or entities to write to the file. |
| `file_name` | String | Specifies the name of the output file. |
| `format` | String | Specifies the output file format (e.g., command or data set). |
| `suppress_defaults` | Boolean | Specifies whether to omit parameters that have their default values from the output. |
| `inverse_define_objects` | Boolean | Specifies whether to write preprocessor object definitions in inverse/define form. |
| `full_name_strings` | Boolean | Specifies whether to write fully qualified object names. |
| `partial_name_strings` | Boolean | Specifies whether to write partial (relative) object names. |
| `header_comments` | String | Specifies comment text to include in the file header. |
| `ignore_fields` | String | Specifies field names to omit from the output. |
