# LOC_ON_AXIS

Returns an array of three numbers representing a location expressed in the global coordinate system, obtained from translating a certain distance along a specified axis of a coordinate system object.

## Format
```
LOC_ON_AXIS (Frame Object, Distance, Axis Name)
```

## Arguments

**Frame Object**
: Coordinate system object on whose axis you want your point to lie.

**Distance**
: Real number stating how far to move along the specified axis.

**Axis Name**
: Single-character string denoting the coordinate system axis. Valid values are x, y, and z (character case is insignificant).

## Example

In the following illustration, the LOC_ON_AXIS function returns an array of three numbers representing a location:

### Function
```
LOC_ON_AXIS(marker_2, 5, "x")
```

### Result
```
4, 11, 0
```
