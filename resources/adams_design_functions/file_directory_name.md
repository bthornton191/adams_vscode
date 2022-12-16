# FILE_DIRECTORY_NAME
Returns a directory name from the file specification.

## Format
```java
FILE_DIRECTORY_NAME(file_name)
```

## Argument
 
**file_name**
: Character string containing the local or full-file name.

## Example
The following example illustrates the use of the `FILE_DIRECTORY_NAME` function:

### Function
```java
var set var=$_self.dir string_value=
(eval (FILE_DIRECTORY_NAME ("my_dir/my_file.dat")))
```
### Returns
```java
"my_dir"
```