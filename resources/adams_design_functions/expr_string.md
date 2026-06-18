# EXPR_STRING

Returns a text string containing an expression in a given field of an object that you specify.


## Format
```adams_cmd
EXPR_STRING (Object Field)
```

## Arguments
 
**Object Field**
: Character string denoting the name of an object suffixed with a field name.

## Examples
The following examples assume that you created a marker as follows:

```adams_cmd
marker create marker=mar1 location=(loc_relative_to({0,0,0}, mar2)) ori=1,2,3 
```

### Function
```adams_cmd
EXPR_STRING("mar1.location")
```

### Result
```adams_cmd
"(LOC_RELATIVE_TO({0, 0, 0}, .mod1.ground.mar2))"
```

### Function
```adams_cmd
EXPR_STRING(".mar1.orientation")
```

### Result
```adams_cmd
" " (an empty string)
```

