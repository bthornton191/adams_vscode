# STR_FIND
Returns the starting location of the first occurrence of a string within another string. If there is no match, it returns a 0.
## Format
```java
STR_FIND (Base String, Search String)
```
## Arguments
 
**Base String**
: Text string.

**Search String**
: Text string.

## Examples
The following examples illustrate the use of the STR_FIND function:
 
### Function
```java
STR_FIND ("Hello", "l")
```

### Result
```java
3
```
 
### Function
```java
STR_FIND ("Hello", "o")
```

### Result
```java
5
```
The following function uses a second character in its search criteria to return 4, because letter "l" appears twice in the word hello:
 
### Function
```java
STR_FIND ("Hello", "lo")
```

### Result
```java
4
```
