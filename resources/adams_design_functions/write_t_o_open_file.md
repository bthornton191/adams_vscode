# WRITE_T_O_OPEN_FILE

Open an TeimOrbit file for writing. Returns 1 on success and 0 if an error occurs.

## Format
```
WRITE_T_O_OPEN_FILE (Filename, Append)
```

## Arguments

**Filename**
: TeimOrbit file to write.

**Append**
: 1 = append to current file, 0 = create new file

## Example

### Function
```
WRITE_T_O_OPEN_FILE ("mdi_0001_new.spr", 0)
```

### Result
```
1
```
