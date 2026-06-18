# UNIQUE_FULL_NAME

Returns a text string containing a unique full name for the specified type of object. If no default parent exists for the type you specified, `UNIQUE_FULL_NAME` returns an empty string.



## Format 
```adams_cmd
UNIQUE_FULL_NAME(Type) 
```
## Arguments

**Type**
: Text string that represents an entity type.

## Example
The following example illustrates the use of the `UNIQUE_FULL_NAME` function:

### Function
```adams_cmd
UNIQUE ({9, 1, 1})
```

### Result
```adams_cmd
1.0, 9.0
```


 
