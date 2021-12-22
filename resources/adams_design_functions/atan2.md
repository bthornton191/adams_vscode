# ATAN2

Returns the arc tangent of two expressions, each representing a numerical value. x1 and x2 themselves can be expressions.

## Format 
```java
ATAN2(x1, x2)
```
## Arguments

 



**x1** 
: Any valid expression that evaluates to a real number. 


**x2** 
: Any valid expression that evaluates to a real number.  


## Example

The following function shows the arc tangent of the expression a/b where a is the x component of the distance between **marker_2** and **marker_1** and b is the y component of the distance between **marker_2** and **marker_1**. The location of **marker_1** and **marker_2** is shown in the figure below.

 



### Function  
```java
ATAN2 (DX(marker_2, marker_1, marker_2), DY(marker_2, marker_1, marker_2))  
```

### Result  
```java
45  
```