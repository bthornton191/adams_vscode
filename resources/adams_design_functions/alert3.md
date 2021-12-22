# ALERT3

Displays the contents of the variable on separate lines and presents an alert window with up to three buttons containing specified labels. It is recommended to use `EVAL()` function when using `ALERT3`, both to avoid unnecessary parameterization and for it to function properly.

## Format 
```java
ALERT3 (var, type, b1, b2, b3, choice) 
```
## Arguments 

 



**var** 
: A reference to a string variable.  


**type**
: A character string indicating the type of alert box. These values come from the ALERT function: 

* Error 
* Warning 
* Information 
* Working 
* Question  

**b1** 
: A character string to display on button 1. 


**b2** 
: A character string to display on button 2. 


**b3** 
: A character string to display on button 3. 


**choice** 
: An integer designating the default button number. 


## Example 
```java
var set var=msg str="Out of", "disk", "space"
var set var=OK int=(ALERT3 (msg.self, "ERROR", "OK", "Cancel", "", 1))
```