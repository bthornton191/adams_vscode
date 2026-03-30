# Unique Name / Units Functions

Functions for generating unique names and IDs for database objects, and for working with physical units.

## Unique name functions

| Function | Description |
|----------|-------------|
| `UNIQUE_FILE_NAME` | Unique temporary file name |
| `UNIQUE_FULL_NAME` | Unique fully-qualified object name for a type |
| `UNIQUE_ID` | Unique integer ID for objects of a type |
| `UNIQUE_LOCAL_NAME` | Unique local (leaf) name within a parent |
| `UNIQUE_NAME` | Unique name built from a base string |
| `UNIQUE_NAME_IN_HIERARCHY` | Unique name within a specific hierarchy |
| `UNIQUE_PARTIAL_NAME` | Unique partial (short) name |

## Units functions

| Function | Description |
|----------|-------------|
| `UNITS_CONVERSION_FACTOR` | Numeric factor from one unit to current default |
| `UNITS_STRING` | Unit string associated with an object field |
| `UNITS_TYPE` | Unit type (e.g. `"length"`, `"force"`) of a field |
| `UNITS_VALUE` | Value converted to current default units |

---

## UNIQUE_NAME

Returns a unique database name built from a base string. Appends a suffix (e.g. `_1`, `_2`) until the name is not already taken.

```
UNIQUE_NAME(base_name)
```

```adams_fn
UNIQUE_NAME("stat")   ! returns "stat_1" (or next available)
```

---

## UNIQUE_FULL_NAME

Returns a unique fully-qualified name for a new object of the given type. Returns an empty string if no default parent exists for that type.

```
UNIQUE_FULL_NAME(type)
```

---

## UNIQUE_LOCAL_NAME

Returns a unique local (leaf) name for a new object within its default parent context.

```
UNIQUE_LOCAL_NAME(type)
```

---

## UNIQUE_PARTIAL_NAME

Returns a unique partial (non-fully-qualified) name for a new object.

```
UNIQUE_PARTIAL_NAME(type)
```

---

## UNIQUE_NAME_IN_HIERARCHY

Returns a unique name within a specified hierarchy (parent object).

```
UNIQUE_NAME_IN_HIERARCHY(parent, type)
```

---

## UNIQUE_ID

Returns a unique integer ID for objects of a specified type. Useful when you need to assign explicit IDs.

```
UNIQUE_ID(type)
```

```adams_cmd
var create var=marker_id integer=(EVAL(UNIQUE_ID("marker")))
```

---

## UNIQUE_FILE_NAME

Returns a unique temporary file name string.

```
UNIQUE_FILE_NAME()
```

---

## UNITS_CONVERSION_FACTOR

Returns the numeric factor to convert from a specified unit to the current default units.

```
UNITS_CONVERSION_FACTOR(units_value)
```

```adams_fn
UNITS_CONVERSION_FACTOR("inch")
! returns 12.0  (if default length unit is foot)
```

---

## UNITS_STRING

Returns the unit string (e.g. `"kg/mm**3"`) associated with a named object field.

```
UNITS_STRING(object_field)
```

```adams_fn
UNITS_STRING(".mod1.part1.density")
! returns "kg/mm**3"
```

---

## UNITS_TYPE

Returns the physical quantity type (e.g. `"length"`, `"mass"`, `"force"`) of an object field.

```
UNITS_TYPE(object_field)
```

---

## UNITS_VALUE

Returns the numeric value of a field converted to the current default units.

```
UNITS_VALUE(object_field)
```

---

## See also

- [Database metadata](db-metadata.md)
- [Database query functions](db-query.md)
- [String functions](str-functions.md)
