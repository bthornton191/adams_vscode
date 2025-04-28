# FILE_MINUS_EXT

Returns the file name with its extension removed.

## Format
```java
FILE_MINUS_EXT (file_name)

```
## Arguments

 



**file_name**
: Character string containing the file name with or without a directory specification.



## Example

The following example illustrates the use of the `FILE_MINUS_EXT` function:

 

### Function  
```java
var set var=.file_no_ext string_value=(eval (FILE_MINUS_EXT ("my_file.dat")))
```

### Result  
```java
"my_file"
```

