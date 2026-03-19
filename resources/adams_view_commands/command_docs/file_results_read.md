# file results read

Allows you to read a results file into Adams View so the information contained may be plotted, manipulated or viewed. When specifying the name of the results file to be read the extension RES will be appended by default. This may be overridden by specifying a different extension.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An Existing Model | Specifies an existing model |
| `analysis_name` | An Existing Analysis | Specifies the name of the analysis to store the Adams output in. |
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed. |
| `length` | Linear_units | Specifies the length units in the file, if different from the current default. |
| `mass` | Mass_units | Specifies the mass units in the file, if different from the current default. |
| `time` | Time_units | Specifies the time units in the file, if different from the current default. |
| `force` | Force_units | Specifies the force units in the file, if different from the current default. |
| `skip_time_interval` | Integer | Specifies whether or not to skip time steps by specifying a pattern of time steps to skip in the result file. This should be greater than or equal to 0. |
| `skip_contact_interval` | Integer | Specifies whether or not to skip contact steps by specifying a pattern of time steps to skip in the result file. This should be greater than or equal to 0. |
