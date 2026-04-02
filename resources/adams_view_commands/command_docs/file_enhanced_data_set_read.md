# file enhanced_data_set read

Allows you to read an Adams enhanced data set file (.adm or .cmd) into Adams View, with options to control preprocessing and define symbols.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the enhanced data set file to read. |
| `mode` | String | Specifies the read mode. Options control whether the file is read in merge or replace mode. |
| `suppress_cpp` | Boolean | Specifies whether to suppress C preprocessor processing of the file before reading. |
| `defines` | String | Specifies preprocessor symbols to define when reading the file, in the form NAME or NAME=VALUE. |
