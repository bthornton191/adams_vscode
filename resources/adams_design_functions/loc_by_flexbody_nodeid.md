# LOC_BY_FLEXBODY_NODEID

Returns the location as a three-dimensional vector of a node on a flexible body.

## Format
```
loc_by_flexbody_nodeid (flex_body, node_id)
```

## Returns

If the node ID does not exist in the flexible body, LOC_BY_FLEXBODY_NODEID returns a location at the origin (0, 0, 0) with no warning.
