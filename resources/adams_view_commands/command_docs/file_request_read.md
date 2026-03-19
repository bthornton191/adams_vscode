# file request read

Allows you to read a request file into Adams View so the information contained may be plotted, manipulated or viewed. When specifying the name of the request file to be read, the extension .REQ will be appended by default. This may be overridden by specifying a different extension.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name(required)` | String | Specifies the name of the file that is to be read. |
| `model_name(optional)` | New or Existing Model | Specifies a new or an existing model. |
| `analysis_name(optional)` | New or Existing Analysis | Specifies the name of the analysis in which to store output files. |
| `length(optional)` | Mm, Cm, Meter, Km, Inch, Foot,mile. | Specifies the length units in the file, if different than the current default. |
| `force(optional)` | Newton, Knewton, Dyne, Pound_force, Kpound_force, Kg_force, Ounce_force, Millinewton, Centinewton, Poundal. | Specifies the force units in the file, if different from the current default. |
| `mass(optional)` | Kg, Gram, Pound_mass, Kpound_mass, Slug, Ounce_mass, And Tonne. | Specifies the mass units in the file, if different from the current default. |
| `time(optional)` | Millisecond, Second, Minute, and Hour. | Specifies the time units in the file, if different from the current default. |
| `disk_based_results (optional)` | Yes/No | Specifies whether or not to store data on disk. Enter either yes or no. |
| `request_ids(optional)` | Integer | Specifies a list of integers corresponding to the Adams IDs of the requests you want read from the file. If blank, then Adams reads all requests from the file. |
| `time_step_skip (optional)` | Integer | Specifies whether or not to skip time steps by specifying a pattern of time steps to skip. |
