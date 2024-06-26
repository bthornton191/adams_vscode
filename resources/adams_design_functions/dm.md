# DM

Returns the magnitude of the translational displacement from one coordinate system object to another.

## Format
```java
DM (Object 1, Object 2)

```
## Arguments

 



**Object 1**
: Coordinate system object to which the translational displacement magnitude is measured.


**Object 2** 
: Coordinate system object from which the translational displacement magnitude is measured.


## Symbol
Mathematically, `DM` is calculated as follows:
```java
DM = √([R_01 - R_02]•[R_01 - R_02])
```
where:

* `R_01` is the displacement of the Object 1, `O1`, in the global coordinate system.

* `R_02` is the displacement of the Object 2, `O2`, in the global coordinate system.

## Example

In the following illustration, the `DM` function returns a number greater than or equal to 0.

 

### Function  
```java
DM(marker_O1, marker_O2)
```

### Result  
```java
12
```

