# file text write

Indicates that output composed of the values_for_output is to be sent to the specified destination, using the given format.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the output text file. |
| `variable_name` | An Existing Vvar | Specifies a variable to which Adams View stores a formatted string. |
| `format_for_output` | String | Specifies the format for the output text. |
| `values_for_output` | String | Specifies the values that are to be placed in the output string. |
| `newline` | Boolean | Controls whether or not the command causes the output to terminate the line with this write command. |
