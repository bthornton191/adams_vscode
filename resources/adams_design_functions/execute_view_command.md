# EXECUTE_VIEW_COMMAND

Returns a numerical value indicating whether `EXECUTE_VIEW_COMMAND` succeeded or failed in executing 
an Adams View command. If the command was successful, `EXECUTE_VIEW_COMMAND` returns a 1; otherwise, 
it returns a 0.



## Format
```java
EXECUTE_VIEW_COMMAND (Command)
```

## Arguments
 
**Command**
: Character string containing an Adams View command.

## Example
The following example illustrates the use of the `EXECUTE_VIEW_COMMAND` function:

### Function
```shell
EXECUTE_VIEW_COMMAND("marker create marker=" // UNIQUE_NAME("mar"))
```

### Result
```java
returns a 1 and creates a marker with a unique name
```
