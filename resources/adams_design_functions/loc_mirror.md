# LOC_MIRROR

Returns an array of three numbers representing a location in the global coordinate system, which mirrors another location across a plane of a coordinate system object.

## Format
```
LOC_MIRROR (Location, Frame Object, Plane Name)
```

## Arguments

**Location**
: Array of numbers that specifies a location expressed in the global coordinate system.

**Frame Object**
: Coordinate system object that defines the plane of reflection.

**Plane Name**
: Character string that specifies one of the three planes in a coordinate system object. xy, yx, xz, zx, yz, and zy (character case is insignificant) are the only possible values. Character order is insignificant; that is, xy is the same as yx.

## Example

In the following illustration, the LOC_MIRROR function returns an array of three numbers representing a location:

### Function
```
LOC_MIRROR({7,7,0}, marker_1, "xy")
```

### Result
```
7, 5, 0 (in the global coordinate system)
```
