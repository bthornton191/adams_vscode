# LOC_RELATIVE_TO

Returns an array of three numbers representing the transformation of coordinates location in a new coordinate system object.

## Format

```java
LOC_RELATIVE_TO (Location, Frame Object)
```

## Arguments
**Location** 
: Array of numbers specifying a location expressed in a coordinate system object.


**Frame Object**
: Coordinate system object.

## Returns
**Location**
: Array of numbers specifying a location **expressed in coordinate system of expression parent (see Notes below)**.

## Example

In the following illustration, the `LOC_RELATIVE_TO` function returns an array of three numbers representing a location:

 



## Function 
```java
LOC_RELATIVE_TO({16,8,0}, marker_2)
```

## Result  
```java
-4, 22, 0
```

## Notes 
Special care should be taken when using the `LOC_RELATIVE_TO()` function when it involves nested expressions as arguments involving parameters of database entities such as markers. A marker's location is stored relative to the coordinate system of the part that owns the marker and all part locations are stored relative to the coordinate system of the model that owns the parts. So any expression involving `LOC_RELATIVE_TO` which belongs to the marker database entity will automatically return the location relative to the coordinate system of the part that owns the marker. Consider the following example in which the node_id parameter of a flexible body f1 is parameterized using the following expression:

`(LOC_TO_FLEXBODY_NODEID(.mod1.f1, LOC_RELATIVE_TO({0.0, 0.0, 0.0}, .mod1.tst)))`

If this expression is evaluated using the Function Builder, the results produced will be different from the actual evaluation of the node_id expression in the database. This is because the expression evaluation is always relative to the parent expression. In the case of the function builder expression evaluation, there is no parent expression, hence the `LOC_RELATIVE_TO()` function will return the global location whereas when the same expression is evaluated in the database, the `LOC_RELATIVE_TO()` will return the location relative to the flexible body f1 which is the parent of the node_id.

An alternative to `LOC_RELATIVE_TO()` in these situations would be to use `LOC_LOC()` specifying 0 as the third argument as shown below:

`(LOC_TO_FLEXBODY_NODEID(.mod1.f1, LOC_LOC({0.0, 0.0, 0.0}, .mod1.tst,0)))`

In this case the location returned by `LOC_LOC()` will always be without any parent reference frame and hence will return consistent values when evaluated using the function builder or in the database.