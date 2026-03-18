# READ_T_O_UNITS

Reads the units specified in the currently open TeimOrbit file into the specified string variable. The variable contains strings for the units in this order:  length, force, angle, mass, time. If the unit is not present in the TO file, the current unit is returned. Function returns 1 on success and 0 if errors occur.

## Format
```
READ_T_O_UNITS (Unit Variable)
```

## Arguments

**Variable**
: String variable that will hold an array of unit strings read from the currently open TeimOrbit file. Note that it is necessary to pass the "self" attribute to this function.

## Example

The following example illustrates the use of the READ_T_O_UNITS function:

### Function
```
acar toolkit get_units variable=.mdi.units_tempREAD_T_O_UNITS( .mdi.units_temp.self )
```

### Result
```
1
```
