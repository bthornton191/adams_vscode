# ORI_GLOBAL

Resolves an angle expressed in a coordinate system object to the global coordinate system. ORI_GLOBAL is the shorthand for ORI_ORI.

## Format
```
ORI_GLOBAL(Orientation, Frame Object)
```

## Arguments

**Orientation**
: Array of body-fixed 313 Euler rotations to be transformed to the global coordinate system.

**Frame Object**
: Coordinate system object in which each sequence in the angle is expressed.

## Example

In the following illustration, the ORI_GLOBAL function returns an orientation, as specified:

### Function
```
ORI_GLOBAL({marker_2.orientation}, marker_1)
```

### Result
```
270, 0, 0
```
