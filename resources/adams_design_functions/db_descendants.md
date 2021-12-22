# DB_DESCENDANTS

Returns the objects of a given type, activity, and number of levels beneath the parent. 

## Format
```java
DB_DESCENDANTS (Object Name, Object Type, Activity Flag, Levels)
```
## Arguments

 



**Object Name**
: Name of the parent object under which to search. 


**Object Type**
: Character string (see `DB_TYPE`). 


**Activity Flag**
: Integer flag whose value determines which objects to return:
* -1 = return objects that are inactive, or are children of inactive models
* 0 = return all objects regardless of activity
* 1 = return all objects whose parent model is active. If the Object Type is "model", only return active models.
* 2 = return active objects whose parent model is also active 


**Levels**
: Integer flag whose value determines which objects to return:
* 0 = all objects (exhaustive search) below parent
* 1 = immediate children of parent
* 2 = one or two levels below parent 


## Example

The following function creates a variable that stores all design variables whose parent model is active and exist within the first two levels below **model_1**:
```java
variable create variable=variable_list &
    object_value=(DB_DESCENDANTS (.model_1, "variable", 1, 2))
```