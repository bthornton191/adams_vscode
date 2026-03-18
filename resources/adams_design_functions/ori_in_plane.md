# ORI_IN_PLANE

Returns an orientation by directing one of the axes and defining one of the planes within a coordinate system object. ORI_IN_PLANE has an underlying parameter that allows it to express the resulting orientation in the proper coordinate system object.

## Format
```
ORI_IN_PLANE (Frame Object 1, Frame Object 2, Frame Object 3, Directed Axes & Coordinate)
```

## Example

In the following illustration, the ORI_IN_PLANE function returns an orientation of a plane whose z-axis is defined from marker_1 (100.0, 100.0, 0.0) to marker_2 (300.0, 300.0, 0.0) and whose y-axis is in the plane defined by marker_1, marker_2 and marker_3 (350.0, 100.0, 0.0):

### Function
```
ORI_IN_PLANE(marker_1, marker_2, marker_3, "z_zy")
```

### Result
```
135, 90, 90
```
