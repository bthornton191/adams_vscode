# Flexible Body Node Functions

Functions for querying node IDs on flexible bodies — finding the closest node to a location, filtering nodes by volume or interface status, and finding nearby nodes.

## Quick reference

| Function | Description |
|----------|-------------|
| `NODE_ID_CLOSEST` | Node ID closest to a marker |
| `NODE_IDS_CLOSEST_TO` | Array of node IDs closest to a location |
| `NODE_IDS_IN_VOLUME` | Node IDs inside a geometry volume |
| `NODE_ID_IS_INTERFACE` | Check if a node is an interface node |
| `NODE_IDS_WITHIN_RADIUS` | Node IDs within a radius of a point |
| `NODE_NODE_CLOSEST` | Closest node between two flexible bodies |

---

## NODE_ID_CLOSEST

Returns the integer node ID of the node on a flexible body that is closest to a marker.

```
NODE_ID_CLOSEST(marker, flex_body, interface_only)
```

| Argument | Description |
|----------|-------------|
| `marker` | Name of the marker object |
| `flex_body` | Name of the flexible body object |
| `interface_only` | `1` = consider only interface nodes; `0` = consider all nodes |

Returns `0` if no node is found (no warning).

---

## NODE_IDS_CLOSEST_TO

Returns an array of node IDs on a flexible body that are closest to a specified location.

```
NODE_IDS_CLOSEST_TO(flex_body, location, n)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `location` | `{x, y, z}` reference point |
| `n` | Number of closest nodes to return |

---

## NODE_IDS_IN_VOLUME

Returns an integer array of all node IDs on a flexible body that lie inside a geometry volume. The geometry must be a cylinder or a spherical ellipsoid (`xscale == yscale == zscale`).

```
NODE_IDS_IN_VOLUME(flex_body, geom)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `geom` | Name of the geometry object (cylinder or spherical ellipsoid) |

Returns `{-1}` if no nodes are found (no warning).

---

## NODE_ID_IS_INTERFACE

Returns `1` if the specified node is an interface node; `0` otherwise.

```
NODE_ID_IS_INTERFACE(flex_body, node_id)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `node_id` | Integer node ID to test |

---

## NODE_IDS_WITHIN_RADIUS

Returns an integer array of all node IDs on a flexible body within a specified radius of a point.

```
NODE_IDS_WITHIN_RADIUS(flex_body, location, radius)
```

| Argument | Description |
|----------|-------------|
| `flex_body` | Name of the flexible body |
| `location` | `{x, y, z}` centre point |
| `radius` | Search radius |

---

## NODE_NODE_CLOSEST

Returns the node ID of the node on the second flexible body that is closest to a specified node on the first flexible body.

```
NODE_NODE_CLOSEST(flex_body_1, node_id_1, flex_body_2)
```

---

## See also

- [LOC_ functions](loc-functions.md) — `LOC_BY_FLEXBODY_NODEID`, `LOC_TO_FLEXBODY_NODEID`
