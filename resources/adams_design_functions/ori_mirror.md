# ORI_MIRROR

Returns an orientation by performing a mirroring of the given orientations that reflect the specified axes.

## Format
```
ORI_MIRROR (Body Fixed 313 Angles, Frame Object, Plane Name, Axes Name)
```

## Arguments

**Body Fixed 313 Angles**
: Array of body-fixed 313 Euler rotation sequences, expressed in a coordinate system object.

**Frame Object**
: Coordinate system object that defines the plane of reflection.

**Plane Name**
: Character string selecting one of three planes in the coordinate system object.The only possible values are: xy, yx, xz, zx, yz, and zy (character case is insignificant). Character order is insignificant; that is, xy is the same as yx.

**Axes Name**
: Character string indicating which axes to mirror.The only possible values are: xy, yx, xz, zx, yz, and zy (character case is insignificant). Character order is insignificant; that is, xy is the same as yx.

## Example

In the following illustration, the ORI_MIRROR function returns an orientation, as specified:

### Function
```
ORI_MIRROR({{10,8,0}}, marker_1, "xy", "xy")
```

### Result
```
190, 8, 180
```
