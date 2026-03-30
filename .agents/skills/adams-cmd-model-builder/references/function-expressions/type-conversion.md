# Type Conversion Functions

Adams View provides explicit type conversion functions for converting between strings, integers, real numbers, and database objects. Adams typically performs these coercions automatically, but explicit conversion is sometimes required when synthesizing names or working with parametric expressions.

## STOI — String to Integer

```
STOI(string)
```

Converts a string representation of a number to an integer. Usually not needed because Adams automatically coerces strings to integers when the context demands it.

| Argument | Description |
|----------|-------------|
| `string` | A character string representation of a number |

```adams_fn
STOI("42")     ! returns 42
```

---

## STOR — String to Real

```
STOR(string)
```

Converts a string representation of a number to a real number. Usually not needed because Adams automatically coerces strings to reals when the context demands it.

| Argument | Description |
|----------|-------------|
| `string` | A character string representation of a number |

```adams_fn
STOR("3.14")   ! returns 3.14
```

---

## STOO — String to Object

```
STOO(string)
```

Converts a character string to a database object reference. Useful when synthesising object names programmatically (e.g., building a name from a prefix and a variable), since automatic coercion does not always apply in those contexts.

| Argument | Description |
|----------|-------------|
| `string` | The full or relative name of a database object |

```adams_cmd
! Build a marker name and use it in an expression
marker_name = "MODEL_1.PART_1.MARKER_" // RTOA(index)
marker_obj  = STOO(marker_name)
```

---

## See also

- [ABS / Math functions](abs.md)
- [DB_EXISTS / Database query](db-query.md)
