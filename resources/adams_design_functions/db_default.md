# DB_DEFAULT

Returns the default object of a given type. Uses the database object named system_defaults to specify the default object.

## Format
```adams_cmd
DB_DEFAULT (Defaults Object Name, Object Type)
```
## Arguments

 



**Defaults Object Name**
: Name of the defaults in the database, always system_defaults. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

The following function creates a variable that is the default part:

```adams_cmd
var create var=default_part &
    object_value=(DB_DEFAULT(system_defaults, "part"))
```
