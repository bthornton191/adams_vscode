# ORI_ALL_AXES

Returns a body-fixed 313 Euler sequence describing an orientation in which the first axis of a coordinate system object is parallel to, and co-directed with, a line defined by the first two points in a plane, and its second axis is parallel to the plane.

## Format
```
ORI_ALL_AXES (Plane Point Locations, Axes Names)
```

## Arguments

**Plane Point Locations**
: 3x3 matrix providing three non-colinear points describing a plane. The points are expressed in the global coordinate system.

**Axes Names**
: Character string indicating which two axes to orient.xy, yx, xz, zx, yz, and zy are the only possible values (character case is insignificant). Also, since each value defines a distinct orientation, xy is not the same as yx.

## Example

In the following illustration, the ORI_ALL_AXES function returns a body-fixed 313 Euler sequence describing an orientation, as specified.

### Function
```
ORI_ALL_AXES({{14,18,0},{10,14,0},{16,14,0}}, "xz")
```

### Result
```
45, 90, 180
```
