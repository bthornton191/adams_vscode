# LOC_CYLINDRICAL

Returns an array of three numbers that are the Cartesian coordinates (x, y, z) for a point equivalent to the cylindrical coordinates (r,  , z) for the same point. Both sets of coordinates are relative to the global coordinate system origin and axes. The relationship between the coordinates is:

## Format
```
LOC_CYLINDRICAL (R, Theta, Z)
```

## Arguments

**R**
: The radius of the circle on which the point lies.

**Theta ()**
: Rotation about the z-axis starting from the x-axis. The positive or negative sense of the rotation is defined by the right-hand rule.

**Z**
: Distance along the global z-axis.

## Example

In the following illustration, the LOC_CYLINDRICAL function returns an array of three numbers that are the Cartesian coordinates for a point.

### Function
```
LOC_CYLINDRICAL(1,30,0)
```

### Result
```
0.866, 0.5, 0
```
