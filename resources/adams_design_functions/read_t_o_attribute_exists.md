# READ_T_O_ATTRIBUTE_EXISTS

Searches a TeimOrbit file for existence of an attribute in a specified block or subblock. Returns 1 if the block is found, otherwise 0.

## Format
```
READ_T_O_ATTRIBUTE_EXISTS (Filename, Block Name, SubBlock Name, Attribute Name)
```

## Arguments

**Filename**
: TeimOrbit file to read

**Block Name**
: Block to search for in file.

**SubBlock Name**
: SubBlock to search for in specified block. Pass a null string if no subblock is selected.

**Attribute Name**
: Attribute to search for in specified subblock.

## Example

### Function
```
READ_T_O_ATTRIBUTE_EXISTS ("<acar_shared>/springs.tbl/mdi_0001.spr", "SPRING_DATA", "", "FREE_LENGTH")
```

### Result
```
1
```
