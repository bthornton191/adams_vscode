# Database Query Functions

Functions for checking object existence and retrieving collections of objects from the Adams View database.

## Quick reference

| Function | Description |
|----------|-------------|
| `DB_ACTIVE` | Check if an object is active for simulation |
| `DB_CHANGED` | Check if an object has been modified |
| `DB_COUNT` | Count objects of a type under a parent |
| `DB_EXISTS` | Check if a named object exists |
| `DB_OBJ_EXISTS` | Check if an object reference exists |
| `DB_OBJ_EXISTS_EXHAUSTIVE` | Exhaustive existence check |
| `DB_OBJ_FROM_NAME_TYPE` | Get object from name and type |
| `DB_OF_CLASS` | Check if an object belongs to a class |
| `DB_OF_TYPE_EXISTS` | Check if any object of a type exists |
| `DB_OBJECT_COUNT` | Count of objects of a given type |

---

## DB_ACTIVE

Returns `1` if the object is active (will participate in simulations), `0` otherwise. Checks recursively through parent hierarchy and group membership.

> **Note**: Must be wrapped in `EVAL()` when used in spreadsheet mode.

```
DB_ACTIVE(object)
```

```adams_cmd
if condition=(EVAL(DB_ACTIVE(.model_1.part_1)))
    ! Part is active — proceed
end
```

---

## DB_CHANGED

Returns `1` if the object has been modified since the last save or checkpoint; `0` otherwise.

```
DB_CHANGED(object)
```

---

## DB_COUNT

Returns the number of child objects of a specified type under a parent object.

```
DB_COUNT(parent, type)
```

| Argument | Description |
|----------|-------------|
| `parent` | Parent database object |
| `type` | Object type string (see `DB_TYPE`) |

---

## DB_EXISTS

Returns `1` if the named object exists in the database; `0` otherwise.

```
DB_EXISTS(name_string)
```

```adams_cmd
if condition=(DB_EXISTS(".mod1.par1"))
    marker create marker=marker_3
end
```

---

## DB_OBJ_EXISTS

Returns `1` if the specified object reference exists; `0` otherwise.

```
DB_OBJ_EXISTS(object)
```

---

## DB_OBJ_EXISTS_EXHAUSTIVE

Performs an exhaustive (recursive) existence check for an object.

```
DB_OBJ_EXISTS_EXHAUSTIVE(object)
```

---

## DB_OBJ_FROM_NAME_TYPE

Returns the database object matching a given name and type string.

```
DB_OBJ_FROM_NAME_TYPE(name, type)
```

---

## DB_OF_CLASS

Returns `1` if `object` is a member of the named class; `0` otherwise.

```
DB_OF_CLASS(object, class_name)
```

```adams_cmd
if cond=(DB_OF_CLASS(myobject, "marker"))
    marker attribute marker=(myobject) color=red
end
```

---

## DB_OF_TYPE_EXISTS

Returns `1` if at least one object of the specified type exists under the given parent; `0` otherwise.

```
DB_OF_TYPE_EXISTS(parent, type)
```

---

## DB_OBJECT_COUNT

Returns the total count of objects of a given type in the database.

```
DB_OBJECT_COUNT(type)
```

---

## See also

- [Database navigation](db-navigation.md)
- [Database metadata](db-metadata.md)
- [Unique name / ID functions](unique-units.md)
