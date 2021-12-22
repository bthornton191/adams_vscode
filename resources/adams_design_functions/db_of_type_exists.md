# DB_OF_TYPE_EXISTS

Returns a 1 if an object with the name and type you specified exits; returns a 0 if it does not exist. Distinguishes between objects with the same name but different type, and is especially useful when full path name isn't known. 

## Format 
```java
DB_OF_TYPE_EXISTS (Name String, Object Type) 
```
## Argument 

 



**Name String**
: Character string representing the name of an object. 


**Object Type**
: Character string, see `DB_TYPE`. 


## Example 
```java
if condition=(DB_OF_TYPE_EXISTS(".mod1.par1.node1", "marker"))
    
    marker copy &
        marker = .mod1node1 &
        new_marker = .mod1.ground.node1 

end
```