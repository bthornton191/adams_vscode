# BACKUP_FILE

Renames the specified file to a backup file. The name of the backup file on Linux is file_name appended with %. On Windows, the last character of file_name is replaced with a q.

## Format
```java
BACKUP_FILE( file_name)
```
## Argument

 



**file_name** 
: String containing the name of the file to back up. 


## Example

The following example renames **foo.dat** to **foo.dat%** (on Linux) or **foo.daq** (on Windows):
```java
var set var=bkup int=(eval(BACKUP_FILE("foo.dat")))
```