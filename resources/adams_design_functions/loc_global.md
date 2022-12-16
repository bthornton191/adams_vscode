# LOC_GLOBAL
Returns an array of three numbers representing the global coordinates of a location obtained from transforming the local coordinates by a specified location.

## Format
```java
LOC_GLOBAL (Location, Frame Object)
```

## Arguments
**Location**
: Array of numbers that specify a location expressed relative to a local coordinate system.

**Frame Object**
: Coordinate system object in which the local coordinates are expressed.

## Returns
**Location**
: Array of numbers that specify a location expressed in **gobal coordinates**.

## Example
In the following illustration, the `LOC_GLOBAL` function returns an array of three numbers representing the global coordinates of a location:
 
## Function
```java
LOC_GLOBAL({-5, -8, 0}, marker_1)
```

## Result
```java
14, 12, 0 (in the global coordinate system)
```

[Read more...](https://help.hexagonmi.com/bundle/adams_2022.3/page/adams_help/Adams_Basic_Package/view_fn/viewfn_design/TOC.LOC.GLOBAL.xhtml)
