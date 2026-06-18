# LOC_LOC

Returns an array of three numbers representing the transformation of coordinates location in a new coordinate system object.

## Format

```adams_cmd
LOC_LOC (Location, In Frame Object, To Frame Object)
```

## Arguments

 



**Location** 

: An array of numbers specifying a location as expressed in the original coordinate system. 


**In Frame Object**

: The original coordinate system object that expresses the location. 


**To Frame Object**

: The original coordinate system object into which the location is to be transformed. 


## Example

In the following illustration, the LOC_LOC function returns an array of three numbers representing the transformation of coordinates location in a new coordinate system object:

 



## Function 
```adams_cmd
LOC_LOC({-6, 12, 0}, marker_1, marker_2)  
```

## Result  
```adams_cmd
-2, 8, 0 (with respect to marker_2)  
```
