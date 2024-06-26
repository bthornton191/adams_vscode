# EXPR_REFERENCE

Returns a string containing the name of the reference to the expression. If no expression is found, 
`EXPR_REFERENCE` returns an empty string. Similarly, if the reference index is out of bounds, it 
returns an empty string.


## Format
```java
EXPR_REFERENCE (Expression, Reference)
```

## Arguments
 
**Expression**
: A character string name of a database field.
 
**Reference**
: A numeric index into the list of references to that field.

## Example
```java
var set var=load_dep str=(eval(expr_reference(".mod.par.mar.loc", 1))) 
```
