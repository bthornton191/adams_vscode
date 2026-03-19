# file graphics read

Allows you to read a graphics file into Adams View, so the information contained may be animated, manipulated or viewed. When specifying the name of the graphics file to be read, the extension .GRA will be appended by default. This may be overridden by specifying a different extension.

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
