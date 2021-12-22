# ANGLES

Returns a 3x1 matrix containing angles from the transformation matrix in D. 

## Format 
```java
ANGLES (D, OriType) 
```
## Arguments 

 



**D**
: 3 x 3 matrix of direction cosines. 


**OriType** 
: Character string specifying the Euler sequence that is desired as output. To define the rotation sequence, enter space or body (character case is ignored), followed by three digits, such as 313 or 123.  


## Example 

The following function performs the inverse of the TMAT function: 
```java
ANGLES(DCOS, "body313")
```
You can obtain the current default orientation type string with this expression: 
`(user_string(".system_defaults.orientation_type")`)