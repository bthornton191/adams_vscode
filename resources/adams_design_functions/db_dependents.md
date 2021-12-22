# DB_DEPENDENTS

Returns an array of all objects of a given type that are dependents of the object you specified.

## Format
```java
DB_DEPENDENTS (Object Name, Object Type)
```
Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

The following example lists information about all marker objects that depend on the design variable, **DV_1**. Note that **.self** is appended to **DV_1** so the functions refers to the design variable object **DV_1** and not the value in **DV_1**.

```java
list_info &
    entity = (EVAL(DB_DEPENDENTS(.model_1.DV_1.self, "marker")))
```