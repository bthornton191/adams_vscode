# ORI_ORI

Returns an orientation that represents the same orientation as expressed in the local frame of one coordinate system object, to the local frame of another coordinate system object. Given an orientation expressed in one coordinate system object, ORI_ORI produces a new orientation (representing the same orientation) that is expressed in another coordinate system object.

## Format
```
ORI_ORI (Orientation, From Frame Object, To Frame Object)
```

## Arguments

**Orientation**
: Array of body-fixed 313 Euler rotations.

**From Frame Object**
: Coordinate system object in which each sequence in the angle is expressed.

**To Frame Object**
: Coordinate system object into which the rotations are to be transformed.

## Example

In the following illustration, the ORI_ORI function returns an orientation, as specified:

### Function
```
ORI_ORI({marker_1.orientation}, marker_1, marker_2)
```

### Result
```
180, 90, 90
```
