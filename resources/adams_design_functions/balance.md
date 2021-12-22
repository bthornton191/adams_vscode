# BALANCE

Finds a similarity transformation T such that B = T/A*T has, as nearly as possible, approximately equal row and column norms. T is a permutation of a diagonal matrix whose elements are integer powers of two so that the balancing does not introduce any round-off error, then returns B. 

## Format
```java
BALANCE(A)
```
## Arguments 

 



**A**
: A square matrix.  


## Example 

The following example illustrates the use of the BALANCE function:

 



### Function  
```java
BALANCE({{1,2},{3,4}})  
```

### Result  
```java
{{1,2}, {3,4}}  
```

>This portion of the Adams View Function Builder documentation, ©2006, has been reproduced here with permission from MathWorks, ©1994-2000 The MathWorks Inc. 