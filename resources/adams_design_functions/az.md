# AZ

Returns the angular displacement from one coordinate system object to another, and accounts for angle wrapping.

## Format
```java
AZ (Object, Reference Frame)
```
## Arguments

 



**Object**
: Coordinate system object to which the angular displacement is measured. 


**Reference Frame** 
: Coordinate system object from which the angular displacement is measured, using a y-axis rotation. 


## Symbol

Mathematically, `AZ` is calculated as follows (angle wrapping is accounted for):

```java
AZ = atan2(x_o*y_R, x_o*x_R)
```

* `x_o` is the x-axis of the Object, O.
* `x_R` is the x-axis of the Reference Frame, R.
* `y_R` is the y-axis of the Reference Frame, R.


## Example

In the following illustration, the AZ function returns the angle between the x-axes of marker_O and marker_R:

 



### Function  
```java
AZ(marker_O, marker_R)  
```

### Result  
```java
35  
```



 



> **Note**   
>Because this function is independent of the rotation sequence, attempting y-axis and x-axis rotations in conjunction with it may return an output that doesn't make sense.




> **Tip**   
>If you want to change the AZ function so it does not account for angle wrapping, use the MOD function. For example, use the function:
>```java
>(MOD(AZ(.model_1.PART_1.MAR_2, .model_1.ground.MAR_1)+PI,2*PI)-PI)
>```
>The MOD function achieves the cyclic effect and the +PI and -PI shift the curve accordingly.