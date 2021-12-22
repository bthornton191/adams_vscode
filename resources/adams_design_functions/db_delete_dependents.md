# DB_DELETE_DEPENDENTS

Returns an array of objects that are dependents of the object you specified. Each of the objects in the array normally prevent the specified object from being deleted.

## Format
```java
DB_DELETE_DEPENDENTS (Object Name)
```
## Argument

 



**Object Name**
: Name of a database object. 


## Example

The following function returns an alert if par_1 has dependent objects:

```java
if condition=(DB_OBJECT_COUNT(DB_DELETE_DEPENDENTS(.model_1.par_1)>0))
    ! take action as needed here
end
```