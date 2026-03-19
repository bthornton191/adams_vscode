# file parasolid write

Allows you to write the geometric definition of an Adams model or part from to the Parasolids file format. You can then read the Parasolid file into a CAD program.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file that is to be read. The proper extension is the default, but you can override it by supplying a different extension. |
| `type` | Ascii/binary/neutral | Specifies the type of file |
| `model_name` | Existing model | Specifies the Adams View model to be written to the CAD file. Adams View places each rigid body in the model on a separate level. |
| `analysis_name` | Existing analysis | Specifies the model at a particular simulation frame (time) of a particular analysis to export. |
| `frame_number` | Integer | Specifies the frame number (simulation output time step) at which to configure a model during the single_frame_display command. |
| `part_name` | Existing Part | Specifies the name of the Adams part from which the geometry is written to the iges file. |
| `active_only` | Boolean | Values: Yes or no |
