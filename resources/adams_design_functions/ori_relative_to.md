# ORI_RELATIVE_TO

Returns an orientation of a coordinate system object as specified by an angle. This parametric representation of `ORI_RELATIVE_TO` maintains the relationship regardless of how other objects are moved.
This function is shorthand for `ORI_ORI(Orientation, Frame Object, To Frame Object)` where the To Frame Object is the underlying parameter. The underlying parameter determines the proper coordinate system object for the transformations.

## Format

```java
ORI_RELATIVE_TO (Body313 Rotations, Frame Object)
```

## Arguments

 

**Body313 Rotations** 
: Array of body-fixed 313 Euler rotations jiexpressed in a coordinate system object.


**Frame Object**
: Coordinate system object in which each sequence in angle is expressed.


## Returns
**Location**
: Array of body-fixed 313 Euler rotations in **global coordinates**.

## Example

The following example illustrates the use of the `ORI_RELATIVE_TO` function:

 



## Function 
```java
ORI_RELATIVE_TO({marker_1.orientation}, marker_2)
```

## Result  
```java
180, 90, 180
```
