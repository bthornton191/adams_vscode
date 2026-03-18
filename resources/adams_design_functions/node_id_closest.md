# NODE_ID_CLOSEST

Returns an integer node ID associated with the node of a flexible body closest to a marker. If you set `intpt` to 1, `NODE_ID_CLOSEST` considers only the interface nodes.

## Format
```
NODE_ID_CLOSEST (marker, flex_body, intpt)
```

## Arguments

**marker**
: Name of the marker object.

**flex_body**
: Name of the flexible body object.

**intpt**
: Integer flag:

  * `1` — Consider only interface nodes.
  * `0` — Consider all nodes.

## Returns

If `NODE_ID_CLOSEST` finds no node, it returns an integer value of zero (0) with no warning.
