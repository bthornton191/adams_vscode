# ORI_FRAME_MIRROR

Returns an orientation that has the specified axes mirrored about a plane within a coordinate system object.

## Format
```
ORI_FRAME_MIRROR (Body Fixed 313 Angles, Frame Object, Plane Name, Axes Name)
```

## Example

In the following illustration, the ORI_FRAME_MIRROR function returns an orientation, as specified:

### Function
```
ORI_FRAME_MIRROR({6,14,0}, marker_1, "xz", "xz")
```

### Result
```
174, 14, 180
```
