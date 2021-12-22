# APPEND

Returns the rows of one matrix appended to the rows of another matrix. The two matrixes must have the same number of rows. If one matrix is an NxM matrix and the other matrix is an NxP matrix, then APPEND returns an Nx(M+P) matrix. 

## Format 
```java
APPEND (M1,M2) 
```
## Arguments 

 



**M1** 
: A matrix of arbitrary shape.  


**M2** 
: A matrix with the same number of rows as M1.  


## Example 

The following example illustrates the use of the APPEND function: 

 



### Function  
```java
APPEND(M1, M2)  
```

## Returns  
```java
{{1,2,3,11,12,13,14}, {4,5,6,15,16,17,18}} 
1,2,3,11,12,13,14 
                       4,5,6,15,16,17,18  
```

Matrixes M1 and M2 are defined as follows: 
```java
M1 = {{1,2,3},{4,5,6}} 
       1,2,3                                 
               4,5,6
```
```java
M2 = {{11,12,13,14},{15,16,17,18}} 
       11,13,14,15 
                     15,16,17,18 
```