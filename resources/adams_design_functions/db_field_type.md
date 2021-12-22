# DB_FIELD_TYPE

Returns a string that describes the type of data in a field beneath the object type you specified.

## Format
```java
DB_FIELD_TYPE (Object Type, Field Name)
```
## Arguments

 



**Object Type**
: Name of a database object (see `DB_TYPE`). 


**Field Name**
: Character string. 


## Example

The following example determines that the width field on the Graphic_Interface_Dialog_Box object is of the type REAL (keep the expression on one line):

 



### Function 
```java
var create var=var6 &
    string=(DB_FIELD_TYPE("Graphic_Interface_Dialog_Box", "width"))  
```

## Result  
```java
"REAL"  
```