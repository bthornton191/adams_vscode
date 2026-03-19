# file stereo_lithography read

Allows you to import stereo lithography (SLA) geometry into Adams. As you import the SLA geometry, you associate the geometry with an existing part or you create a new part with which to associate it.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed |
| `part_name` | An Existing Partf | Specifies the name of an existing Adams View PART onto which the translated geometry will be placed |
| `scale` | Real | Specifies the scale factor to be applied to the size of the geometry created in Adams View |
| `location` | Location | Specifies the translational position where the geometry in the IGES file is to be located relative to the Adams View part lprf |
| `orientation` | Orientation | Specifies the angular position where the geometry in the IGES file is to be oriented relative to the Adams View part lprf |
| `relative_to` | An Existing Model, Part Or Marker | Specifies the coordinate system that location coordinates and orientation angles correspond to |
