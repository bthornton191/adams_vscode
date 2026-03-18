# ORI_ALONG_AXIS

Returns the alignment of a specified axis from one coordinate system object to another. This function has an underlying parameter that allows it to express the resulting orientation in the proper coordinate system object.

## Format
```
ORI_ALONG_AXIS (From Frame, To Frame, Axis Name)
```

## Example

In the following illustration, the ORI_ALONG_AXIS function returns the alignment of a specified axis:

### Function
```
ORI_ALONG_AXIS(marker_1, marker_2, "y")
```

### Result
```
315, 0, 0
```
