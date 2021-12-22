# CLIP

Returns an M x Numvals matrix of values extracted from an M x N matrix, where: 

* Output[I,1] = A[I,Start]
* Output[I,Numvals] = A[I,Start+Numvals-1]

The following conditions apply to the equations above: 

* I=1 to M
* 1 < Start < N
* Numvals < (N-Start+1)

## Format 
```java
CLIP (A, Start, Numvals) 
```
## Arguments 

 



**A**
: An M x N matrix of real values.  


**Start**
: The index to the first column of values to be included in the output.  


**Numvals**
: The number of columns to be included in the output.  


## Example 

The following example illustrates the use of the `CLIP` function:

 



### Function  
```java
CLIP( {[8, 10], [12,14], [16, 18]} , 1 ,1 )  
```

## Result  
```java
8, 12, 16  
```