# AY

Returns the angular displacement from one coordinate system object to another, and accounts for angle wrapping.

## Format
```java
AY (Object, Reference Frame)
```
## Arguments

 



**Object**
: Coordinate system object to which the angular displacement is measured. 


**Reference Frame** 
: Coordinate system object from which the angular displacement is measured, using a y-axis rotation. 


## Symbol

Mathematically, `AY` is calculated as follows (angle wrapping is accounted for):

```java
AY = atan2(z_o*x_R, z_o*z_R)
```

* `z_o` is the z-axis of the Object, O.
* `z_R` is the z-axis of the Reference Frame, R.
* `x_R` is the x-axis of the Reference Frame, R.


## Example

In the following illustration, the AY function returns the angle between the x-axes of marker_O and marker_R:

 



### Function  
```java
AY(marker_O, marker_R)  
```

### Result  
```java
35  
```



 



> **Note**   
>Because this function is independent of the rotation sequence, attempting y-axis and z-axis rotations in conjunction with it may return an output that doesn't make sense. 




> **Tip**   
>If you want to change the AY function so it does not account for angle wrapping, use the MOD function. For example, use the function:
>```java
>(MOD(AY(.model_1.PART_1.MAR_2, .model_1.ground.MAR_1)+PI,2*PI)-PI)
>```
>The MOD function achieves the cyclic effect and the +PI and -PI shift the curve accordingly.