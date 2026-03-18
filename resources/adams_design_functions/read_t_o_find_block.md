# READ_T_O_FIND_BLOCK

Searches the currently open TeimOrbit file for a named block, which can then be further processed. Returns 1 on success and 0 if any errors occur.

## Format
```
READ_T_O_FIND_BLOCK (Block Name)
```

## Arguments

**Block Name**
: Name of block to find in TeimOrbit file. In the TO file, a block is a string separated by brackets, for example, [MDI_HEADER]. Not case sensitive.

## Example

[The following assumes this file has already been opened ("<acar_shared>/springs.tbl/mdi_0001.spr")]

### Function
```
READ_T_O_FIND_BLOCK ("SPRING_DATA")
```

### Result
```
1
```
