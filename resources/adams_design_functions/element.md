# ELEMENT

Indicates if a real value is an element of an array.


## Format
```adams_cmd
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
```adams_cmd
ELEMENT(.MOD1.A,3)
```

### Result
```adams_cmd
true
```
### Function
```adams_cmd
ELEMENT(.MOD1.A,11)
```

### Result
```adams_cmd
false
```
