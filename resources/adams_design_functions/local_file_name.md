# LOCAL_FILE_ NAME
Returns the local name of a file when given a name that may contain the directory specifications:
"/user/coop/source/dbase/file.dat" → "file.dat"
##Format
```java
LOCAL_FILE_NAME(full_file_name)
```

## Argument
 
**Full_file_name**
: Character string containing the full-file name.

## Example
The following example illustrates the use of the `LOCAL_FILE_NAME` function:

### Function
```java
var set var=$_self.file_name &
    string = (eval (LOCAL_FILE_NAME ("my_dir/my_file.dat")))
```

### Returns
```java
"my_file.dat"
```