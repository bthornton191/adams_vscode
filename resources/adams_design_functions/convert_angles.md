# CONVERT_ANGLES

Converts a body-fixed 313 sequence into a user-specified sequence. 

## Format 
```java
CONVERT_ANGLES (E, OriType) 
```
## Arguments 

 



**E**
: 3x1 or 1x3 Euler orientation sequence.  


**OriType**
: Character string describing the contents of E. To define the rotation sequence, enter space or body (character case is ignored), followed by three digits, such as 313 or 123.

The following list contains all the possible values for **OriType**:  
| Body-Fixed    | Space-Fixed |
|---------------|-------------|
|Body121        | Space121    |
| Body123       | Space123    |
| Body131       | Space131    |
| Body132       | Space132    |
| Body212       | Space212    |
| Body213       | Space213    |
| Body231       | Space231    |
| Body232       | Space232    |
| Body312       | Space312    |
| Body313       | Space313    |
| Body321       | Space321    |
| Body323       | Space323    |


## Example 

The following function converts input angles into a body-fixed 123 sequence: 
```java
CONVERT_ANGLES (E, "body123") 
```
This function is shorthand for: 
```java
ANGLES(TMAT(E, "body313"), OriType)
```
The current default orientation type string can be obtained with the expression: 
```java
USER_STRING(".system_defaults.orientation_type")
```