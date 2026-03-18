# WRITE_T_O_UNITS

Write units to file based on string variable containing an array of strings corresponding to the units, obtained via a call to "get_units". Return 1 on success and 0 if errors occur.

## Format
```
WRITE_T_O_UNITS (Variable)
```

## Arguments

**Variable**
: String variable containing an array of strings corresponding to the units length, angle, force, mass and time. If there is no string at the corresponding index, no unit is written to the file.

## Example

### Function
```
acar toolkit get_units variable=.mdi.my_unit_varWRITE_T_O_UNITS (.mdi.my_unit_var.self)
```

### Result
```
1
```
