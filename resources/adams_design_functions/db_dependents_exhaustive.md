# DB_DEPENDENTS_EXHAUSTIVE

Lists a complete chain of dependents (of the specified type) for a given object. That is immediate dependents, dependents of dependents and so on.

## Format
```java
DB_DEPENDENTS_EXHAUSTIVE (Object Name, Object Type)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


Example

This function is a good way to interrogate parametric models to find all of the objects of a certain type in a model that are somehow influenced by another object like a design variable. The following example lists information about all marker objects that depend on the design variable DV_1 or that are further down the dependency chain (dependents of the first-degree dependent, their dependents and so on). Note that .self is appended to DV_1 so the functions refers to the design variable object DV_1 and not the value in DV_1.
```java
list_info entity &
    entity_name = (EVAL(DB_DEPENDENTS_EXHAUSTIVE(.model_1.DV_1.self,"marker")))
```