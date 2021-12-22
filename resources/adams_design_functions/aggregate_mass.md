# AGGREGATE_MASS

Calculates and stores aggregate mass information, which you can then use in parametrics or store in variables for future use.

## Format
```java
aggregate_mass(array_of_objects, reference_frame_key, type_string)
```
## Arguments

 



**array_of_objects** 
: A single object or an array of objects of the type models, bodies, and tires. If you specify a model, it must be the only object passed in. 


**reference_frame_key**
: A reference frame for reporting the aggregate mass center of mass (cm) position and inertia marker angles. If you enter none, the default is with respect to the global coordinate system. 


**type_string**
: The type of aggregate mass information desired. The choices are:

* mass - Mass value (one real)
* cm_pos - Center of mass location (three reals)
* im_ang - Inertia marker angles (three reals)
* inertias - Inertia properties (six reals)
* all - Returns all of the above (13 reals) 


## Examples

### Computing Mass

The following example provides the mass of PART_2 and PART_3:
```java
AGGREGATE_MASS( {PART_2, PART_3} , 0 , "mass" )
```
Note that the objects must be in an array; therefore, the curly braces are required. In this example, the reference frame key has been set to zero because the value of mass is independent of the reference frame.

### Computing CM Location

The following example returns the location of the cm for the aggregation of PART_2 and PART_3. The location array will be computed and reported with respect to the ground.MARKER_3 reference frame.
```java
AGGREGATE_MASS( {PART_2, PART_3} , ground.MARKER_3 ,"CM_Pos" )
```
### Obtaining Inertia Matrix Entries

The following example returns the off-diagonal entries of the inertia matrix for the aggregation of PART_2 and PART_3 in the ground reference frame. Note that array indexing has been used to return the 4th, 5th, and 6th entries from the returned array.
```java
AGGREGATE_MASS( {PART_2, PART_3} , 0 , "inertias" )[4:6]
```
Alternatively, you can use the all type string and use array indexing to extract only the last three values. In this example, the computation is relative to PART_2.MARKER_1.
```java
AGGREGATE_MASS({PART_2,PART_3}, PART_2.MARKER_1 , "All")[11:13]
```

> **Note**   
>If you use the option all, use a no_units temporary variable to get all of the quantities at once, and then pass it to individual variables with the proper unit setting. 
