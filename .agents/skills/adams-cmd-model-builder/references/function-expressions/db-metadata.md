# Database Metadata Functions

Functions for reading type information, field names, default objects, and expression strings from the Adams View database.

## Quick reference

| Function | Description |
|----------|-------------|
| `DB_DEFAULT` | Default object of a given type |
| `DB_DEFAULT_NAME` | Name of the default object |
| `DB_DEFAULT_NAME_FOR_TYPE` | Default name string for a type |
| `DB_FIELD_FILTER` | Filter string for a field |
| `DB_FIELD_TYPE` | Type of a field value |
| `DB_FILTER_NAME` | Name of a filter |
| `DB_FILTER_TYPE` | Type string for a filter |
| `DB_FULL_NAME_FROM_SHORT` | Resolve short name to full name |
| `DB_FULL_TYPE_FIELDS` | All fields of an object type |
| `DB_SHORT_NAME` | Short (leaf) name of an object |
| `DB_TYPE` | Type string of an object |
| `DB_TYPE_FIELDS` | Field names for a type |
| `EXPR_STRING` | Expression text for an object field |
| `PARAM_STRING` | Parameter values as command text |
| `USER_STRING` | String value of an object field |

---

## DB_DEFAULT

Returns the default object of a specified type (using the `system_defaults` settings object).

```
DB_DEFAULT(system_defaults, type)
```

```adams_cmd
var create var=default_part &
    object_value=(DB_DEFAULT(system_defaults, "part"))
```

---

## DB_DEFAULT_NAME

Returns the name of the current default object for a given type.

```
DB_DEFAULT_NAME(system_defaults, type)
```

---

## DB_DEFAULT_NAME_FOR_TYPE

Returns the default name string used when creating new objects of a given type.

```
DB_DEFAULT_NAME_FOR_TYPE(type)
```

---

## DB_FIELD_FILTER

Returns the filter string associated with a specific field of an object.

```
DB_FIELD_FILTER(object, field)
```

---

## DB_FIELD_TYPE

Returns a string describing the data type of a specific field value.

```
DB_FIELD_TYPE(object, field)
```

---

## DB_FILTER_NAME

Returns the name of a filter object.

```
DB_FILTER_NAME(filter)
```

---

## DB_FILTER_TYPE

Returns the type string associated with a filter.

```
DB_FILTER_TYPE(filter)
```

---

## DB_FULL_NAME_FROM_SHORT

Resolves a short or partial object name to its fully-qualified name, given the object type. Useful when there could be ambiguity between models and analyses.

```
DB_FULL_NAME_FROM_SHORT(short_name, type)
```

```adams_fn
DB_FULL_NAME_FROM_SHORT("joint1", "constraint")
! returns ".model_1.joint1"
```

---

## DB_FULL_TYPE_FIELDS

Returns all field names for a given object type.

```
DB_FULL_TYPE_FIELDS(type)
```

---

## DB_SHORT_NAME

Returns the leaf (short) name of a fully-qualified object.

```
DB_SHORT_NAME(object)
```

```adams_fn
DB_SHORT_NAME(.model_1.part_1.marker_1)
! returns "marker_1"
```

---

## DB_TYPE

Returns a string identifying the type of a database object.

```
DB_TYPE(object)
```

```adams_cmd
if condition=(DB_TYPE(part1) == "part")
    list info part=(part1)
end
```

---

## DB_TYPE_FIELDS

Returns the field names defined for a given type string.

```
DB_TYPE_FIELDS(type)
```

---

## EXPR_STRING

Returns the expression text stored in a specific field of an object (the raw expression as it would appear in a command file, including any parameterisation).

```
EXPR_STRING(object_field)
```

```adams_fn
EXPR_STRING("mar1.location")
! returns "(LOC_RELATIVE_TO({0, 0, 0}, .mod1.ground.mar2))"
```

---

## PARAM_STRING

Returns the parameter values of a field in the form used by Adams command files.

```
PARAM_STRING(object_field)
```

```adams_fn
PARAM_STRING("mar1.location")
! returns "(LOC_RELATIVE_TO({0, 0, 0}, .mod1.ground.mar2))"
```

---

## USER_STRING

Returns the string value stored in a string-type field of an object.

```
USER_STRING(object_field)
```

---

## See also

- [Database query functions](db-query.md)
- [Database navigation](db-navigation.md)
- [Unique name / ID functions](unique-units.md)
