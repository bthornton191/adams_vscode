# STR_FIND_N
Returns the numerical position of a character in a string found within another string. Returns 0 if not found. Overlapping matches are not included.

## Format
```java
STR_FIND_N (Base String, Search String, Nth Occurrence)
```

## Arguments
 
**Base String**
: Text string.

**Search String**
: Text string.

**Nth Occurance**
: Integer value indicating the number of string occurrences to be found.

## Examples
The following function returns 10 because the second occurrence of string an begins at character position 10:
 
### Function
```java
STR_FIND_N("meant human", "an", 2)
```

### Result
```java
10
```
The following function returns 16 because the overlapping, matching #'s from 43### to 55###9 are not included, so the third occurrence of string ## begins at character position 16:
 
### Function
```java
STR_FIND_N("43### 55###9 22##5", "##", 3)
```

### Result
```java
16
```
