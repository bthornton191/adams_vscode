# ORI_ONE_AXIS

Returns a body-fixed 313 Euler rotation sequence expressed in the global coordinate system when given a line that is parallel to, and co-directed with, a specified axis. The resulting rotation about the directed axis is arbitrary with ORI_ONE_AXIS.

## Format
```
ORI_ONE_AXIS (Line Point Locations, Axes Name)
```

## Arguments

**Line Point Locations**
: A 3x2 matrix containing two points that describe a line. The points are expressed in the global coordinate system.

**Axed Name**
: A single character string indicating which axis is to be oriented along the line. The only possible values are x, y, or z (character case is insignificant).

## Example

In the following illustration, the ORI_ONE_AXIS function returns a body-fixed 313 Euler sequence:

### Function
```
ORI_ONE_AXIS({{10,16,0}, {8,16,0}}, "x")
```

### Result
```
180, 180, 0
```
