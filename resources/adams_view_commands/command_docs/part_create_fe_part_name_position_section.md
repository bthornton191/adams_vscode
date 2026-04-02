# part create fe_part name_position_section

Allows you to create a finite element part by specifying its name, position, and cross-section properties.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `fe_part_name` | A New FE Part | Specifies the name of the new FE part. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `location` | Location | Specifies the initial location of the FE part. |
| `orientation` | Orientation | Specifies the initial orientation of the FE part using three rotation angles. |
| `fepart_type` | FE Part Type | Specifies the type of FE part. The default is beam_3d. |
| `coordinates` | True | Specifies that the part is defined using explicit coordinates. |
| `i_marker` | An Existing Marker | Specifies the marker at the I end (first end) of the FE part. |
| `j_marker` | An Existing Marker | Specifies the marker at the J end (second end) of the FE part. |
| `i_hard_point` | An Existing Design Point | Specifies the design point defining the I end location. |
| `j_hard_point` | An Existing Design Point | Specifies the design point defining the J end location. |
| `ref_curve` | An Existing Curve | Specifies one or more reference curves used to define the shape of the FE part. |
| `comments` | String | Specifies comments for the object being created or modified. |
| `material_type` | An Existing Material | Specifies the material assigned to the FE part. |
| `cratiok` | Real | Specifies the stiffness proportional Rayleigh damping coefficient. |
| `cratiom` | Real | Specifies the mass proportional Rayleigh damping coefficient. |
| `preload` | File | Specifies a file containing the preload matrix for the FE part. |
| `external` | Boolean | Specifies whether the FE part uses an external solver definition. |
| `faceting_tolerance` | Real | Specifies the faceting tolerance used for graphical display of the FE part. |
| `nodes_at_curve_points` | Boolean | Specifies whether to place nodes at explicit curve reference points. |
