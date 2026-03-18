# PARAM_STRING

Returns a parameter's values as they appear in an Adams command file.

## Format
```
PARAM_STRING (Object Field)
```

## Arguments

**Object Field**
: Character string denoting the name of an object followed by a field name (for example, mar1.orientation).

## Example

The following examples assume that you created a marker as follows:

### Function
```
PARAM_STRING("mar1.location")
```

### Result
```
"(LOC_RELATIVE_TO({0, 0, 0}, .mod1.ground.mar2))"
```
