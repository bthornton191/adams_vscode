# ORI_LOCAL

Returns an orientation, expressed in the global frame, in the local frame of the coordinate system object. ORI_LOCAL is the shorthand for ORI_ORI.

## Format
```
ORI_LOCAL (Orientation, Frame Object)
```

## Arguments

**Orientation**
: Array of body-based 313 Euler rotations expressed in the global coordinate system.

**Frame Object**
: Coordinate system object into which the rotations are to be transformed.

## Example

The following example illustrates the use of the ORI_LOCAL function.

### Function
```
ORI_LOCAL({marker_1.orientation}, marker_2)
```

### Result
```
90, 0, 0
```
