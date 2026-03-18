# WRITE_T_O_INTEGER

Writes an attribute to the current block with the specified integer value. Returns 1 on success and 0 if errors occur.

## Format
```
WRITE_T_O_INTEGER (Attribute, Value)
```

## Arguments

**Attribute**
: Name of attribute to write

**Value**
: Integer value for specified attribute

## Example

### Function
```
WRITE_T_O_INTEGER ("CONTROL_VALUE", 4)
```

### Result
```
1
```
