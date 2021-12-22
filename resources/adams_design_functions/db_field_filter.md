# DB_FIELD_FILTER

Returns an array, from a given array of field names, containing a subset of the original array. The values in the array must meet the requirements that you specify in filter parameters.

## Format
```java
DB_FIELD_FILTER (Filter Strings, Field Strings)
```
## Arguments

 



**Filter Strings**
: Array of character strings that is similar to the macro parameter specification language used in Adams View:
* **object_type**: *database_object_type* uses the type specified as the database_object_type for field lookups. The value of database_object_type is one of the values returned by the function `SELECT_TYPE` (but cannot be a class name).
* **t**: *type* selects all fields that can hold an object of type. type can be the following subset of types from the macro language: 

    | If type is |The field holds|
    |-------------|-------------|
    |Bool|A boolean value. |
    |String|Strings |
    |Real|Real numbers |
    |Integer|Integer numbers |
    |Point|Ordered triples, such as location and orientation. |
    |Database_object_type|A database object |
  
* **c**: *n* where n>=0; n=0 means an open array, n>0 means a fixed array of length exactly equal to n. 
* **alias**: *boolean* indicates whether the field is or is not an alias for some other field. Values for boolean are: 
  * **True** = field must be an alias. 
  * **False** = field must not be an alias.
    
    >If you do not specify an alias, then the field can be either an alias or not. 
* **assoc**: *relation* indicates the field has a particular relationship to the object. Values for relation are: 
  * Child 
  * Reference 
  * Twoway  


**Field Strings**
: List of field names you want to filter. 


## Example

The following is a typical calling sequence that produces all the real scalar fields for the spring damper object:

```java
var set var=tt &
    str = (EVAL(DB_FIELD_FILTER({"object_type=spring_damper", "t=real", "c=1"}, DB_TYPE_FIELDS("spring_damper"))))
```