
# AVIEW_EDIT_FILE

This function will invoke given file, open in notepad window for the user to edit as they see fit. Also this function can be used to view status of the file. View/edit the specified configuration file, input file and so on. The program used to open the file depends on the environment variable: 

`MDI_AVIEW_TEXT_EDITOR`

However its default value is: C:\Windows\notepad.exe 

## Format 
```java
AVIEW_EDIT_FILE (STRING) 
```
```java
AVIEW_EDIT_FILE( "P:\\work\\aview.cmd" )
```
## Arguments 

 



**String** 
: Input full file path 


## Example 

The following example illustrates the use of the AVIEW_EDIT_FILE function:

 



### Function  
```java
var set var = view_file_status int = (eval(AVIEW_EDIT_FILE($f_input_file_name))) 
```

### Result  

It will open input file in a notepad window to edit or view. Return 1 on successful. 
