# ORI_PLANE_MIRROR

Returns a sequence of body-fixed 313 Euler rotations by performing a mirroring of orientations. Using an orientation, ORI_PLANE_MIRROR produces a new sequence describing an orientation that mirrors the specified axes.

## Format
```
ORI_PLANE_MIRROR (Angles, Plane Point Locations, Axes Names)
```

## Arguments

**Angles**
: Array of body-fixed 313 Euler rotation sequences expressed in the global coordinate system.

**Plane Point Locations**
: 3x3 matrix providing three non-colinear points described in a plane. The points are expressed in the global coordinate system.

**Axes Names**
: Character string indicating which axes to mirror.xy, yx, xz, zx, yz, and zy are the only possible values (character case is insignificant). Character order is insignificant; that is, xy is the same as yx.

## Example

In the following illustration, the ORI_PLANE_MIRROR function returns a sequence of body-fixed 313 Euler rotations:

### Function
```
ORI_PLANE_MIRROR({marker_1.orientation},{{18,6,0},{18,12,0},{21,6,0}}, "xy")
```

### Result
```
0, 0, 0
```
