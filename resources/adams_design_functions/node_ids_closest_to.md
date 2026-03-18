# NODE_IDS_CLOSEST_TO

Returns array containing node IDs (integers) of the number (`num`) ofnodes on a flexible body closest to a specified marker.

## Format
```
NODE_IDS_CLOSEST_TO (marker, flex_body, num, intpt)
```

## Arguments

**marker**
: Name of the marker object.

**flex_body**
: Name of the flexible body object.

**num**
: Number of nodes requested.

**intpt**
: Integer flag:

  * `1` — Consider only interface nodes.
  * `0` — Consider all nodes.

## Returns

If `NODE_IDS_CLOSEST_TO` finds no nodes, it returns a single integer value of `-1` with no warning.
