# ALERT2

Displays the contents of the variable on separate lines and presents an OK button. It always returns 1. It is recommended to use `EVAL()` function when using `ALERT2`, both to avoid unnecessary parameterization and for it to function properly.

## Format 
```java
ALERT2 (var, type) 
```
## Arguments 

 



**var** 
: A reference to a string variable. 


**type **
: A character string indicating the type of alert box. These values come from the ALERT function: 

* Error 
* Warning 
* Information 
* Working 
* Question  

## Example 
```java
var set var=msg str="Out of", "disk", "space" 
var set var=OK int=(EVAL(ALERT2 (msg.self, "ERROR")))
```