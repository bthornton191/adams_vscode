# DB_REFERENTS_EXHAUSTIVE

Lists a complete chain of the objects (of the specified type) referred to by a given object. That is immediate referents, referents of referents and so on.

## Format
```java
DB_REFERENTS_EXHAUSTIVE (Object Name, Object Type)
```
## Arguments

 



**Object Name**
: Name of a database object. 


**Object Type**
: Character string (see `DB_TYPE`). 


## Example

This function is a good way to interrogate parametric models to find all of objects of a given type that influence a certain object in the model. The following example stores the array of objects that are immediate referents, referents of referents and so on of **Marker_1**, in the variable **db06**:
```java
var set var = db06 obj=(eval(DB_REFERENTS_EXHAUSTIVE(Marker_1, "all")))
```