# DB_EXISTS

Returns a 1 if the object you specified exists; returns a 0 if it doesn't.

## Format
```java
DB_EXISTS (Name String)
```
## Argument

 



**Name String**
: Character string representing the name of an object. 


## Example

The following function creates **marker_3** if **.mod1.par1** exists:
```java
if condition=(DB_EXISTS(".mod1.par1"))
    marker create marker=marker_3 
end  
```