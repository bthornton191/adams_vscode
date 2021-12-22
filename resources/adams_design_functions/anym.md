# ANYM

Returns the logical sum of the elements of a matrix. If any value is nonzero, the result is nonzero. 

## Format 
```java
ANYM (M) 
```
## Argument 

 



**M**
: A matrix of arbitrary shape. 


## Examples 

The following examples illustrate the use of the ANYM function:

 



### Function  
```java
ANYM({8, 0, 1})  
```

### Result  
```java
1  
```

 



### Function  
```java
ANYM({0, 0, 0})  
```

### Result  
```java
0  
```

 



### Function  
```java
ANYM({[4, 0], [0, 0]})  
```

### Result  
```java
1  
```