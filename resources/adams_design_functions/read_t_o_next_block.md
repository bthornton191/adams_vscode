# READ_T_O_NEXT_BLOCK

Moves to the next block in the currently open TeimOrbit file. Returns a string with the block type, or a null string if there is no next block in the file.

## Format
```
READ_T_O_NEXT_BLOCK ()
```

## Arguments

None

## Example

[The following assumes this file has already been opened ("<acar_shared>/driver_controls.tbl/constant_radius_cornering.dcf"), and the previous read was in the "EXPERIMENT" block]

### Function
```
READ_T_O_NEXT_BLOCK()
```

### Result
```
"STEADY_STATE"
```
