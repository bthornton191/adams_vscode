# LOC_INLINE

Returns an array of three numbers representing the transformation and normalization of coordinates for a location you specified. The location's coordinates are originally expressed in terms of one coordinate system and then transformed to the equivalent coordinates, as expressed relative to a new coordinate system.

## Format
```
LOC_INLINE (Location, In Frame Object, To Frame Object)
```

## Arguments

**Location**
: Array of three numbers specifiying a location expressed in terms of the original coordinate system.

**In Frame Object**
: Starting coordinate system object in which location coordinates are input.

**To Frame Object**
: New coordinate system into which the location coordinates are transformed.

## Example

In the following illustration, the LOC_INLINE function returns an array of three numbers representing the transformation and normalization of coordinates for a specified location:

### Function
```
LOC_INLINE({-8, -2, 0}, marker_1, marker_2)
```

### Result
```
0.8, 0.6, 0.0
```
