# STR_DELETE
Returns a string that results from deleting a specified number of characters starting from a specified location on an input string.

## Format
```java
STR_DELETE (Input String, Starting Position, Number to Delete)
```

## Arguments
 
**Input String**
: Text string.

**Starting Position**
: Integer value indicating the start location.

**Number to Delete**
: Integer value indicating the number of characters to delete.

## Examples
The following function deletes the ninth character in the string and returns the resulting phrase:
 
### Function
```java
STR_DELETE ("This is your life", 9, 1)
```

### Result
```java
This is our life
```
In the following function, the out-of-range negative value (-100) of the Starting Position becomes 1:
 
### Function
```java
STR_DELETE ("This is your life", -100, 10)
```

### Result
```java
ur life
```
In the following function, the out of range positive value (100) of the Starting Position doesn't have any effect on the string:
 
### Function
```java
STR_DELETE ("This is your life", 100, 10)
```

### Result
```java
returns the original string
```