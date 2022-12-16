# UNIQUE_NAME_IN_HIERARCHY

Returns a text string that is a unique database name, taking into account the inherent hierarchy in the given input.This function is essentially a smarter form of `UNIQUE_NAME`. If an entity `myname_1` already exists under `.model_1`, then `UNIQUE_NAME_IN_HIERARCHY(“.model_1.myname”)` would return `.model_1.myname_2` ensuring that the output is truly unique in the hierarchy specified in the input. Note that an entity `myname_2` might already exist under a different model, but the value returned would still be `.model_1.myname_2` as this name is still unique within the hierarchy of `.model_1`.

## Format
```java
UNIQUE_NAME_IN_HIERARCHY (Base Name)
```

## Arguments
 
**Base Name**
: Starting point for a unique database name.

## Example
The following example illustrates the use of the UNIQUE_NAME_IN_HIERARCHY function:
Assume that an object stat_1 already exists in the database.
 
### Function

```java
UNIQUE_NAME_IN_HIERARCHY("stat")
```

## Result
```java
stat_2
```
[Learn more about database functions](file:///C:/Program%20Files/MSC.Software/Adams/2022_2_886672/help/adams_view_fn/200_sys_supplied.html#ww1004102)
 