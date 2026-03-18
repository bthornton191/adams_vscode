# WRITE_T_O_STRING

Writes an attribute to the current block with the specified string value. Returns 1 on success and 0 if errors occur.

## Format
```
WRITE_T_O_STRING (Attribute, Value)
```

## Arguments

**Attribute**
: Name of attribute to write

**Value**
: String value for specified attribute

## Example

### Function
```
WRITE_T_O_STRING ("ACTUATOR_TYPE", "TORQUE")
```

### Result
```
1
```
