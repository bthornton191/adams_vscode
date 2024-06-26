# DZ

Returns an z component of translational displacement from one coordinate system object to another.

## Format
```java
DZ (Object 1, Object 2, Reference Frame)

```
## Arguments

 



**Object 1**
: Coordinate system object to which the translational displacement component is measured.


**Object 2** 
: Coordinate system object from which the translational displacement component is measured.


**Reference Frame** 
: Coordinate system object defining the z-axis; used to measure the translational displacement
component.



## Symbol
Mathematically, `DZ` is calculated as follows:
```java
DZ = [R_01 - R_02]•z_R
```
where:

* `R_01` is the displacement of the Object 1, `O1`, in the global
  coordinate system.

* `R_02` is the displacement of the Object 2, `O2`, in the global
  coordinate system.

* `z_R` is the unit vector along the z-axis of the Reference Frame, `R`.

## Example

In the following illustration, the `DZ` function returns the z component of the translational displacement from `marker_O2` to `marker_O1`, along the z-axis of `marker_R`:

 

### Function  
```java
DZ(marker_O1, marker_O2, marker_R)
```

### Result  
```java
0
```

