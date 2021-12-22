# DB_TYPE

Returns a string representing an object type.

## Format
```java
DB_TYPE (Object Name)
```
## Argument

 



**Object Name**
: Name of a database object (see `SELECT_TYPE`). 


## Examples

The following example processes the part1 object only if it is a part:
```java
if condition=(DB_TYPE(part1)=="part")
    list info part=(part1)
end  
```