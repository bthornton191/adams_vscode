# panel set acf_twindow reload

Restart a simulation from a previously saved model or simulation state.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `save_type` | ADAMS_SAVE_TYPE | Specifies the type of file to be SAVEd or RELOADed |
| `file_name` | STRING | Specifies the name of the file that is to be read, written, or executed. |
| `output_prefix` | STRING | Specifies a new base (root) name for the output files (.REQ, .RES, .GRA, .OUT, etc.) from the simulation which follows this RELOAD command. |
| `title` | STRING | This parameter allows the specification of the XY plot title. |
