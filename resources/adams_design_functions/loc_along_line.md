# LOC_ALONG_LINE

Returns an array of three numbers defining a location expressed in the global coordinate system. The location is a specified distance along the line from one coordinate system object to another.

## Format
```
LOC_ALONG_LINE (Object for Start Point, Object for Point on Line, Distance)
```

## Arguments

**Object for Start Point**
: Coordinate system object defining the starting point of the line.

**Object for Point on Line**
: Coordinate system object defining a point on the line.

**Distance**
: Distance along the line.

## Example

In the following illustration, the LOC_ALONG_LINE function returns an array of three numbers representing a location:

### Function
```
LOC_ALONG_LINE(marker_2, marker_1, 5)
```

### Result
```
7.5, 9.5, 0
```
