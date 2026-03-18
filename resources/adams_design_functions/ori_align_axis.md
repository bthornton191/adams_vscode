# ORI_ALIGN_AXIS

Returns an orientation that aligns one axis of a coordinate system object with an axis of another. It only aligns one axis and leaves the others in unspecified orientations.

## Format
```
ORI_ALIGN_AXIS (Frame Object, Axis Spec)
```

## Arguments

**Frame Object**
: Coordinate system object defining the alignment.

**Axis Spec**
: Character string defining the type of alignment.All of the valid strings are xx, xy, xz, yx, yy, yz, zx, zy, zz, x+x, x+y, x+z, y+x, y+y, y+z, z+x, z+y, z+z, x-x, x-y, x-z, y-x, y-y, y-z, z-x, z-y, and z-z. The first character defines the axis of the result. The last character defines the axis of the coordinate system object to which the result is aligned. For example, xy aligns the x-axis of the result with the y-axis of the coordinate system object.You can insert either "-" or "+" as the middle character. For example, if you insert "-" as in z-z, this indicates that the z-axis of the result is to be aligned in the opposite direction of the z-axis in frame.The Axis Spec parameters xx, x+x, yy, y+y, zz, and z+z are identity values resulting in the global orientation of the coordinate system object. You can, however, compute this orientation more efficiently by using the function ORI_GLOBAL.

## Example

In the following illustration, the ORI_ALIGN_AXIS function returns all the angles of rotation associated with a body-fixed 313 rotation sequence:

### Function
```
ORI_ALIGN_AXIS(marker_1, "z-z")
```

### Result
```
90, 180, 0
```
