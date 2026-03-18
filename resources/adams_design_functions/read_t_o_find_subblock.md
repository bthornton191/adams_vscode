# READ_T_O_FIND_SUBBLOCK

Searches the current block within the currently open file for a named subblock, which can then be further processed. Returns 1 on success and 0 if any errors occur.

## Format
```
READ_T_O_FIND_SUBBLOCK (Subblock Name)
```

## Arguments

**Subblock Name**
: Name of subblock to find in current block within currently open file. In the TO file, a subblock is a string separated by parentheses, for example, (Z_DATA). Not case sensitive.

## Example

[The following assumes this file has already been opened ("<acar_shared>/powertrains.tbl/V12_engine_map.pwr"), and the "ENGINE" block has been selected.]

### Function
```
READ_T_O_FIND_SUBBLOCK ("XY_DATA")
```

### Result
```
1
```
