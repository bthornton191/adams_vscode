# EXPR_REFERENCES

Returns a number of the references to the expression. If no reference is found, `EXPR_REFERENCES` 
returns a 0 value.


## Format
```adams_cmd
EXPR_REFERENCES (Expression)
```

## Arguments
 
**Expression**
: A character string name of a database field.

## Example
```adams_cmd
var set var=load_dep int=(eval(expr_references(".mod.par.mar.loc")))
```
