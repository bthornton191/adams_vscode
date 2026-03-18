# UNIQUE_LOCAL_NAME

Returns a name of the form BASE_1, where BASE is a prefix that you supply and the number (1 in this case) is computed by the function. The returned name is unique for children of the specified parent.

## Format
```
UNIQUE_LOCAL_NAME (Parent, Base)
```

## Arguments

**Parent**
: The object defining the search domain for children.

**Base**
: A character string specifying the prefix part of the name to be produced.

## Example

The following illustrates the UNIQUE_LOCAL_NAME function:

### Function
```
UNIQUE_LOCAL_NAME(.model_1, "PAR")
```

### Result
```
Returns PAR_2 if PAR_1 already exists.
```
