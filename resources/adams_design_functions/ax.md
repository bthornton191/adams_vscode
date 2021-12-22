# AX

Returns the angular displacement from one coordinate system object to another, and accounts for angle wrapping.

## Format
```java
AX (Object, Reference Frame)
```
## Arguments

 



**Object**
: Coordinate system object to which the angular displacement is measured. 


**Reference Frame** 
: Coordinate system object from which the angular displacement is measured, using an x-axis rotation. 


## Symbol
Mathematically, `AX` is calculated as follows (angle wrapping is accounted for):
```java
AX = atan2(-z_o*y_R, z_o*z_R)
```
where:

* `z_o` is the z-axis of the Object, O.

* `y_R` is the y-axis of the Reference Frame, R.

* `z_R` is the z-axis of the Reference Frame, R.

## Example

In the following illustration, the AX function returns the angle between the y-axes of marker_O and marker_R:

 



### Function  
```java
AX(marker_O, marker_R)  
```

### Result  
```java
35  
```



 



> **Note**   
>Because this function is independent of the rotation sequence, attempting y-axis and z-axis rotations in conjunction with it may return an output that doesn't make sense. 




> **Tip**   
>If you want to change the AX function so it does not account for angle wrapping, use the MOD function. For example, use the function:
> 
>```java
>(MOD(AX(.model_1.PART_1.MAR_2, .model_1.ground.MAR_1)+PI,2*PI)-PI)
>```
>
>The MOD function achieves the cyclic effect and the +PI and -PI shift the curve accordingly.

