# ELEMENT

Indicates if a real value is an element of an array.


## Format
```java
ELEMENT(A, X)
```

## Arguments
 
**A**
: An array.

**X**
: A real number.

## Example
Assume that the array in the following function contains the values 1 through 10:
 
### Function
```java
ELEMENT(.MOD1.A,3)
```

### Result
```java
true
```
### Function
```java
ELEMENT(.MOD1.A,11)
```

### Result
```java
false
```
