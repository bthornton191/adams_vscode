# STR_INSERT

Returns a string constructed by inserting a string into another string at a specified insertion point.

## Format
```
STR_INSERT (Destination String, Source String, Insert Position)
```

## Arguments

**Destination String**
: Text string.

**Source String**
: Text string.

**Insert Position**
: Integer value noting the destination point in the string where the insertion is to occur.

## Example

For the following function, blank spaces are needed in the Source String, before and after the text, in order to return the desired output:

### Function
```
STR_INSERT ("That'sfolks", " all ", 7)
```

### Result
```
That's all folks
```
