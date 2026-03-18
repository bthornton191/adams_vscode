# NODE_IDS_WITHIN_RADIUS

Returns an array of node IDs (integers) associated with all the nodes of a flexible body within a radius of a marker. If you set `intpt` to 1, `NODE_IDS_WITHIN_RADIUS` only considers interface nodes.

## Format
```
NODE_IDS_WITHIN_RADIUS (marker, flex_body, radius, intpt)
```

## Arguments

**marker**
: Name of the marker object.

**flex_body**
: Name of the flexible body object.

**radius**
: Radius around marker to check for nodes.

**intpt**
: Integer flag:

  * `1` — Consider only interface nodes.
  * `0` — Consider all nodes.

## Returns

If `NODE_IDS_WITHIN_RADIUS` finds no nodes, it returns a single integer value of `-1` with no warning.
