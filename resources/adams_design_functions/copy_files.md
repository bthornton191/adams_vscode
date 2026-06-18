# COPY_FILES 

Copies a file to the specified location. Returns 1 if successful. 

## Format
```adams_cmd
COPY_FILES(String Source_File_Path, String Target_File_Path)
```
## Argument

 



**Source**
: Character string containing the full-file name to be copy. 


**Target**
: Character string containing the full-path where to copy. 


## Example

### Function
```adams_cmd
COPY_FILES( "P:\\work\\aview.log", "D:\\Some_Dir" )
```
### Returns
```adams_cmd
1
```
