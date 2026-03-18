# LOC_PLANE_MIRROR

Returns an array of three numbers representing a location expressed in the global coordinate system of a location mirrored across the specified plane.

## Format
```
LOC_PLANE_MIRROR (Location, Plane Point Locations)
```

## Arguments

**Location**
: Array of numbers specifying a location expressed in the global coordinate system.

**Plane Point Locations**
: 3x3 matrix providing three non-colinear points describing a plane. The points are expressed in the global coordinate system.

## Example

In the following illustration, the LOC_PLANE_MIRROR function returns an array of three numbers representing a location:

### Function
```
LOC_PLANE_MIRROR({2,4,0},{{10,12,0},{14,12,0},{12,10,0}})
```

### Result
```
2, 4, 0
```
