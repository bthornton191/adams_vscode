# DB_ACTIVE

Returns a Boolean value indicating that the object will or will not take part in simulations. Activity checking is done recursively and through the group mechanism, so you get a true indication as to whether this element is truly active (accessing the attr.active field will not tell you this).

 



>Note:   
>This function will **NOT** work reliably in the "spreadsheet" mode, and therefore must be enclosed in an `EVAL()` function call. 


## Format
```java
DB_ACTIVE (object)
```
## Argument

 



**object**
: A database object about which activity information is desired. 


## Example

The following is an illustration of how the `DB_ACTIVE` function is used:
```java 
if condition=(EVAL(DB_ACTIVE(.model_1.part_1)))     

    ! Then the part and all of
    ! its children will be included in 
    ! subsequent simulations
    
end                                                 
```