# LOC_LOCAL

Returns an array of three numbers representing a location obtained by transforming a location expressed in the global coordinate system, to a new local coordinate system object.

## Format
```
LOC_LOCAL (Location, Frame Object)
```

## Arguments

**Location**
: An array of numbers specifying a location expressed in the global coordinate system.

**Frame Object**
: A new local coordinate system into which the locations are to be transformed.

## Example

In the following illustration, the LOC_LOCAL function returns an array of three numbers representing a location:

### Function
```
LOC_LOCAL({-4, -7, 0}, marker_2)
```

### Result
```
-23, 11, 0 (in the marker_2 coordinate system)
```
