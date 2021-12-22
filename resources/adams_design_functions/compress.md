# COMPRESS

Returns an array consisting of the non-empty values in the input array. An entry in the array is empty for a value type as indicated below: 

* **Reals** - Zero 
* **KEYS** - Zero (that is, null_key) 
* **Integers** - Zero 
* **Strings** - The empty string or all spaces 

In cases where the entire input array is empty, `COMPRESS` returns an array with a single value consisting of zero for integer, real, or key arrays, and the empty string for string arrays. 

## Format 
```java
COMPRESS (any_array) 
```
## Arguments 

 



**any_array**
: `COMPRESS` can accept any type of array (integer, real, database object, or string). 

The array that is returned contains values of the same type.  


## Examples 
```java
variable create variable=my_ints int=1, 0, 0, 2, 0, 3, 0, 0
variable create variable=my_reals real=1.1,0.0, 2.2, 3.3,0.0, 0.0, 4.4, 0.0
variable create variable=my_strings str="  ", "a", "", " b", "", "", "c ", ""
variable create variable=my_strings2 str="  ", "", "", " "
```
```java
variable create variable=compressed_ints  int=(eval(COMPRESS(my_ints))) 
variable create variable=compressed_reals  rea=(eval(COMPRESS(my_reals)))
variable create variable=compressed_strings str=(eval(COMPRESS(my_strings)))
variable create variable=compressed_strings2  str=(eval(COMPRESS(my_strings2)))
```
`COMPRESS` produces the following: 
```java
compressed_ints = 1, 2, 3
compressed_reals = 1.1, 2.2, 3.3, 4.4
compressed_strings = "a", " b", "c "
compressed_strings2 = "" 
```