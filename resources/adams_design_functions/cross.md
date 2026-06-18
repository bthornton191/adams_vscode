# CROSS

Returns the cross-product of two matrices. 

## Format 
```adams_cmd
CROSS (M1, M2) 
```
## Arguments 

 



**M1**
: First matrix.  


**M2**
: Second matrix. 


>**Note**:  
>`CROSS` will only accept 3x1 or 1x3 arrays.

## Example
The following example illustrates the use of the CROSS function:

 



### Function  
```adams_cmd
CROSS({1,0,0}, {0,1,0})  
```

### Result  
```adams_cmd
{0, 0, 1}  
```
