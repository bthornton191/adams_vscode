# DB_TYPE

Returns a string representing an object type.

## Format
```adams_cmd
DB_TYPE (Object Name)
```
## Argument

 



**Object Name**
: Name of a database object (see `SELECT_TYPE`). 


## Examples

The following example processes the part1 object only if it is a part:
```adams_cmd
if condition=(DB_TYPE(part1)=="part")
    list info part=(part1)
end  
```
