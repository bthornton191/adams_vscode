# ALERT

Returns an alert box using the labels you specify. It is recommended to use `EVAL()` function when using `ALERT`, both to avoid unnecessary parameterization and for it to function properly.

## Format
```java
ALERT (Type, Message Text, Button 1 Label, Button 2 Label, Button 3 Label, Default Choice)
```
## Arguments

 



**Type**
: Text string indicating the type of alert box. There are five types from which to choose:

* Error 
* Warning 
* Information 
* Working 
* Question  

**Message Text**
: Text string making up the alert box message. 


**Button 1 Label**
: Text string describing a command button. 


**Button 2 Label**
: Text string describing a command button. 


**Button 3 Label**
: Text string describing a command button. 


**Default Choice**
: Integer value (1, 2 or 3) indicating which command button is the default choice. 


## Example

The following function creates an alert box:

 



### Function  
```java
ALERT("Information", "Create a test?", "Yes", "No", "Cancel", 2)  
```

### Result  

Alert box with "No" as the default choice  
