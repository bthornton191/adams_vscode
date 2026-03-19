# file wavefront read

Allows you to read a Wavefront .obj file into Adams View. Adams View only interprets vertex, face, and group information. Smoothing groups, textures, and material properties are ignored.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed. |
| `model_name` | New or Existing Model | Specifies the name of a new or existing Adams View MODEL onto which the geometry created from reading a Wavefront .obj will be placed. |
| `part_name` | New or Existing Body | Specifies the name of a new or existing Adams View PART onto which the geometry created from reading a Wavefront .obj will be placed. |
| `geometry_placed,` | Relative_to_part, Relative_to_ground | Allows you specify whether the coordinates in the wavefront file are to be interpreted as relative to the part or relative to ground. Adams View writes wavefront files with the coordinates relative to the parts. |
| `scale_factor,` | Real | Allows you to specify the amount to scale the geometry that is read in from a Wavefront .obj file. The geometry will be scaled uniformly in the x, y, and z directions. |
| `set_read_only` | Yes/No | Allows you to specify that all shells created as a result of reading in a wavefront file are to be tagged as read-only. This means that any file writing commands (such as file wavefront write or file iges write) will not output the read-only shells. There is no way to remove the read-only setting once the shells have been created. |
