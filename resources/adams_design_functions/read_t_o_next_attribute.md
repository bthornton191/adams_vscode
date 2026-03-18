# READ_T_O_NEXT_ATTRIBUTE

Reads the next attribute in the file. Returns a null string if there are no more attributes in the file.

## Format
```
READ_T_O_NEXT_ATTRIBUTE ()
```

## Arguments

None

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf"), and the previous read was at the start of the "STEADY_STATE" block]

### Function
```
READ_T_O_NEXT_ATTRIBUTE ()
```

### Result
```
ACTUATOR_TYPE = 'TORQUE'
```
