# geometry modify shape block

Allows modification of the block object

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `block_name` | An Existing Block | Specifies the block to modify |
| `new_block_name` | A New Block | Specifies the name of the new block |
| `comments` | String | Specifies comments for the object being created or modified. |
| `corner_marker` | An Existing Marker | Specifies the marker that defines the anchor point for the definition of a block. |
| `diag_corner_coords` | Length | Specifies the location (x, y, z) of the opposite diagonal corner from the corner_marker for a block. These coordinates are with respect to the corner marker x, y, and z axes. This location, along with the corner_marker, define the boundaries of the block. |
