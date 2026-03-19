# geometry create feature blend

Creates a chamfer or fillet (blend) on a vertex or edge on a rigid body.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `blend_name` | A New Blend | Specifies the name of the blend to be created or modified. |
| `subtype` | Sub_type | Specifies whether you are creating the blend on an edge or vertex: |
| `subids` | Integer | Specifies the Parasolid tags identifying the vertices or edges based on the selected subtype. |
| `chamfer` | Boolean | Specifies whether or not to chamfer the edge or vertex |
| `radius1` | Length | Specifies the width of the chamfer bevel or radius of the fillet. |
| `radius2` | Length | Specifies the end radius for a fillet. Adams View uses the value you enter for radius1 as the starting radius of the variable fillet. |
| `reference_marker` | An Existing Marker | Specifies the marker that is used to define the location of the blend. |
| `locations` | Location | Specifies the location of the vertices or edges used to define the blend relative to the reference marker. |
