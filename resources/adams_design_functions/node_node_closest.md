# NODE_NODE_CLOSEST

Returns an integer node ID associated with a node of the flexible body, `new_flex`, closest to node `old_node_id`, on the flexible body `old_flex`. If `intpt` is set to 1, only the interface nodes are considered.

## Format
```
NODE_NODE_CLOSEST(old_flex, new_flex, old_node_id, intpt)
```

## Arguments

**old_flex**
: The old flexible body.

**new_flex**
: The new flexible body.

**old_node_id**
: The node ID on the old flexible body.

**intpt**
: An integer flag:

  * `1` — Consider only interface nodes.
  * `0` — Consider all nodes.


## Example

The following example:


### Function
```
variable set variable = tmp &   integer=(eval(node_node_closest(old_part, new_part, old_node_id, 1)))
```

### Result
the ID of the interface node on `new_part` closest to the location of the `old_node_id` on `old_part`.
