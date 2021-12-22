# ALLM

Returns the logical product of the elements of a matrix. If all values are nonzero, then the result is nonzero. 

## Format 
```java
ALLM (M) 
```
## Argument

 



**M**
: A matrix of arbitrary shape.  


## Examples 

The following examples illustrate the use of the ALLM function:

 



### Function  
```java
ALLM({1, 0, 1})  
```

### Result  
```java
0  
```

 



### Function  
```java
ALLM({1, 2, 3})  
```

### Result  
```java
1  
```


 



### Function  
```java
ALLM({[1, 1], [1, 0]})  
```

### Result  
```java
0  
```