## STR_REPLACE_ALL
Returns a string constructed by replacing all the occurrences of the sub string in an input string with another string
## Format
```java
STR_REPLACE_ALL (Destination String, Old Sub String, New Replace String)
```
 
## Arguments
**Destination String**
: Text string.

**Old Sub String**
: Text string.

**New Replace String**
: Text string.

## Example
The following function returns string constructed by replacing all the occurrence of old sub string with new string
 
### Function
```java
str_replace_all("aabbccaaaeeffaaaa","aa","cba")
```
### Result
```java
"cbabbcccbaaeeffcbacba"
```
 