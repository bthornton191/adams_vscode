# LOC_ON_LINE

Returns an array of three numbers representing the global coordinates of a location along a line defined by two points.

## Format
```
LOC_ON_LINE (Line Point Locations, Distance)
```

## Arguments

**Line Point Locations**
: 3x2 matrix containing two points describing a line. The coordinates of the points are expressed in the global coordinate system.

**Distance**
: Real number, measured from the first point, that determines how far to move along the line.

## Example

In the following illustration, the LOC_ON_LINE function returns an array of three numbers representing the global coordinates of a location:

### Function
```
LOC_ON_LINE({{7,5,0},{15,11,0}}, 7)
```

### Result
```
12.6, 9.2, 0.0
```
