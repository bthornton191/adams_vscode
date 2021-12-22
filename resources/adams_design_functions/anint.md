# ANINT

Returns the nearest integer whose magnitude is not larger than the real value of an expression that represents a numerical value. 

`ANINT(x)` evaluates to different values under different conditions, as defined below: 

`ANINT(x) = int(x + .5)` if x > 0

`ANINT(x) = int(x - .5)` if x < 0

The value of the mathematical function `ANINT` of a variable x is equal to x if x is an integer. If x is not an integer, then `ANINT(x)` is equal to the integer nearest to x whose magnitude is not greater than the magnitude of x. 

## Format
```java
ANINT(x) 
```
##Argument 

 



**x** 
: Any valid expression that evaluates to a real number. 


## Examples 

The following examples illustrate the use of the ANINT function:

 



### Function  
```java
ANINT(-4.6)  
```

### Result  
```java
-5  
```

 



### Function  
```java
ANINT(4.6)  
```

### Result  
```java
5  
```