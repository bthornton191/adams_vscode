# UNITS_CONVERSION_FACTOR

Returns the numeric conversion factor from the given unit value to the current default units.

## Format
```java
UNITS_CONVERSION_FACTOR (UnitsValue)
```

## Arguments
 
**UnitsValue**
: A units value string defining the units from which you want to convert.

## Example
The following illustrates the use of the UNITS_CONVERSION_FACTOR function:
 
 
### Function

```java
UNITS_CONVERSION_FACTOR("inch")
```

## Result
Returns `12.0` if the default length units are set to foot.
