# Database Navigation Functions

Functions for traversing the Adams View object hierarchy — finding ancestors, children, descendants, and dependency relationships.

## Quick reference

| Function | Description |
|----------|-------------|
| `DB_ANCESTOR` | First ancestor of a specific type |
| `DB_CHILDREN` | Immediate children of a specific type |
| `DB_DEL_PARAM_DEPENDENTS` | Parametric dependents to delete |
| `DB_DEL_UNPARAM_DEPENDENTS` | Non-parametric dependents to delete |
| `DB_DELETE_DEPENDENTS` | All dependents to delete |
| `DB_DEPENDENTS` | Objects that depend on a given object |
| `DB_DEPENDENTS_EXHAUSTIVE` | Exhaustive dependency tree |
| `DB_DESCENDANTS` | All descendants of a specific type |
| `DB_IMMEDIATE_CHILDREN` | Direct children of any type |
| `DB_OLDEST_ANCESTOR` | Topmost ancestor of a specific type |
| `DB_REFERENTS` | Objects referenced by a given object |
| `DB_REFERENTS_EXHAUSTIVE` | Exhaustive referent tree |
| `DB_TWO_WAY` | Objects with two-way dependency |

---

## DB_ANCESTOR

Returns the first ancestor of the specified type, traversing up the hierarchy. Returns `NONE` if no such ancestor exists.

```
DB_ANCESTOR(child, type)
```

| Argument | Description |
|----------|-------------|
| `child` | The object whose ancestor is sought |
| `type` | Object type string (see `DB_TYPE`) |

```adams_fn
DB_ANCESTOR(.model_1.part_1.marker_1, "model")
! returns .model_1
```

---

## DB_OLDEST_ANCESTOR

Returns the highest-level (topmost) ancestor of the specified type.

```
DB_OLDEST_ANCESTOR(child, type)
```

---

## DB_CHILDREN

Returns an array of child objects of a specified type directly under the given parent.

```
DB_CHILDREN(parent, type)
```

```adams_cmd
! List all markers in the default model
list entity &
    entity=(EVAL(SELECT_TEXT(DB_CHILDREN(DB_DEFAULT(system_defaults,"model"), "marker"))))
```

---

## DB_IMMEDIATE_CHILDREN

Returns an array of all direct children of the given object, regardless of type.

```
DB_IMMEDIATE_CHILDREN(parent)
```

---

## DB_DESCENDANTS

Returns all descendants (children, grandchildren, …) of the specified type below the given parent.

```
DB_DESCENDANTS(parent, type)
```

---

## DB_DEPENDENTS

Returns an array of all objects of `type` that depend on (are parametrically driven by) the given object.

```
DB_DEPENDENTS(object, type)
```

> **Tip**: Append `.self` to refer to the object reference rather than its value:
> `DB_DEPENDENTS(.model_1.DV_1.self, "marker")`

```adams_cmd
list_info &
    entity = (EVAL(DB_DEPENDENTS(.model_1.DV_1.self, "marker")))
```

---

## DB_DEPENDENTS_EXHAUSTIVE

Returns the full recursive dependency tree — all objects that ultimately depend on the given object.

```
DB_DEPENDENTS_EXHAUSTIVE(object, type)
```

---

## DB_DEL_PARAM_DEPENDENTS

Returns the parametric dependents of an object that would be deleted if the object were deleted.

```
DB_DEL_PARAM_DEPENDENTS(object)
```

---

## DB_DEL_UNPARAM_DEPENDENTS

Returns the non-parametric (unparameterised) dependents of an object that would be deleted if the object were deleted.

```
DB_DEL_UNPARAM_DEPENDENTS(object)
```

---

## DB_DELETE_DEPENDENTS

Returns all dependents (parametric and non-parametric) of an object that would be deleted along with it.

```
DB_DELETE_DEPENDENTS(object)
```

---

## DB_REFERENTS

Returns an array of objects that are referenced by (i.e., used by) the given object.

```
DB_REFERENTS(object, type)
```

---

## DB_REFERENTS_EXHAUSTIVE

Returns the full recursive referent tree.

```
DB_REFERENTS_EXHAUSTIVE(object, type)
```

---

## DB_TWO_WAY

Returns objects that have a two-way dependency with the given object (both depend on each other).

```
DB_TWO_WAY(object, type)
```

---

## See also

- [Database query functions](db-query.md)
- [Database metadata](db-metadata.md)
