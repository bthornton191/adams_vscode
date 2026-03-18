# NODE_IDS_IN_VOLUME

Returns an array containing node IDs (integers) for all nodes on a flexible body, which reside inside the volume of the geometry object, geom. geom must be either a spherical ellipsoid or a cylinder.

## Format
```
node_ids_in_volume (flex_body, geom)
```

## Arguments

**flex_body**
: Name of the flexible body object.

**geom**
: Name of the geometry object. The geometry object must be either a cylinder or a spherical ellipsoid (that is, xscale==yscale==zscale).

## Returns

If NODE_IDS_IN_VOLUME finds no nodes, it returns a single integer value of -1 with no warning.
