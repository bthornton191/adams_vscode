# DB_COUNT

Returns the number of values in a given field of the object you specified.

## Format
```java
DB_COUNT (Object Name, Field Name)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Field Name**
:  Character string. 


## Example

The following function creates a variable with an integer value of 3:

```java
var create var=xx real_value=1,2,5
var create var=nn &
    integer_value=(DB_COUNT(xx.self, "real_value"))
```