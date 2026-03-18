# STOO

Performs an explicit conversion of a character string to a database object. You usually don't need to use STOO because Adams automatically coerces strings naming objects into database objects, when the context demands it. On the other hand, there are cases, when you need to explicitly convert a string to a database object so you can use it later. For example, you need to convert a string to a database object when you are synthesizing a name.

## Format
```
STOO (String)
```

## Arguments

**String**
: A character string representation of an object's name.
