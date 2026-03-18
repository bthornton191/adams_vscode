# LOC_PERPENDICULAR

Returns a location normal to a plane, one unit away from the first point in the plane. LOC_PERPENDICULAR can also be used to orient a marker by directing an axis toward a point one unit away from the first point in the plane.

## Format
```
LOC_PERPENDICULAR (Plane Point Locations)
```

## Arguments

**Plane Point Locations**
: 3x3 matrix providing three non-colinear points describing a plane.

## Example

The following example illustrates the use of the LOC_PERPENDICULAR function:

### Function
```
LOC_PERPENDICULAR({{10,12,0},{14,12,0},{12,10,0}})
```

### Result
```
10, 12, 1
```
