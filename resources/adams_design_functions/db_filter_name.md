# DB_FILTER_NAME

Returns an array of objects whose names match the filter parameters you specified.

## Format
```java
DB_FILTER_NAME (Objects to Filter, Filter String)
```
## Arguments

 



**Objects to Filter**
: Array of database objects 


**Filter String**
: Character string containing a wildcard sequence to use when matching object names. 


## Example

The following example assigns the color yellow to all the markers whose names start with a or c:

```java
marker attributes &
    marker = (EVAL(DB_FITLER_NAME(DB_CHILDREN(.model_1, "marker"), "[ac]*"))) &
    color = yellow
```