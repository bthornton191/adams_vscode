# UNIQUE_FILE_NAME

Returns a string that is the name of a non-existent file. It is the file system analogous to the database `UNIQUE_NAME` function.

## Format 
```adams_cmd
UNIQUE_FILE_NAME(Initial File Name) 
```
## Arguments

**Initial File Name**
: Prefix to use when creating the unique name.

## Examples 

The following example illustrates the use of the `UNIQUE_FILE_NAME` function:




### Function  
```adams_cmd
UNIQUE_FILE_NAME("test")
```

### Result  
```adams_cmd
test_1
```

 
