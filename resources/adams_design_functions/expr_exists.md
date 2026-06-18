# EXPR_EXISTS

Returns a 1 if an expression exists in a given field of an object that you specify; returns a 0 if 
it does not.


## Format
```adams_cmd
EXPR_EXISTS(Object Field)
```

## Arguments
 
**Object Field**
: Character string denoting the name of an object suffixed with a field name.

## Example
The following examples assume that you created a marker as follows:
```adams_cmd
marker create marker=mar1 location=(loc_relative_to({0,0,0}, mar2)) ori=1,2,3 
```

### Function
```adams_cmd
EXPR_EXISTS(".mar1.location")
```

### Result
```adams_cmd
1 (true)
```

### Function
```adams_cmd
EXPR_EXISTS(".mar1.orientation")
```

### Result
```adams_cmd
0 (false)
```
