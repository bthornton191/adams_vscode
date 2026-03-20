# ARYVAL — Array Element Value

Returns the value of a single element from an Adams **array** data element.

## Format

```
ARYVAL(Array Name, Element Number)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Array Name` | Required | Full dot-path object name of the array element (e.g., `.MODEL.MY_ARRAY`) |
| `Element Number` | Required | 1-based integer index of the element to return |

The first argument is an **object name**; the second is a **1-based integer**.

## Creating an array data element

```cmd
data_element create array &
    array_name = .MODEL.STATE_VEC &
    adams_id = 1 &
    size = 4
```

Array elements are often populated by user-written subroutines (ARYSUBROUTINE) or by state equations.

## Using ARYVAL in a FUNCTION= expression

```adams_fn
! Read the 3rd element of a state vector array
ARYVAL(.MODEL.STATE_VEC, 3)

! Use array element as input to a STEP
STEP(ARYVAL(.MODEL.SENSOR_DATA, 1), 0.0, 0.0, 1.0, 1000.0)
```

## Notes

- Element indices are **1-based** (first element = 1, not 0).
- If the index exceeds the array size, the solver returns 0 and issues a warning.
- Commonly used with co-simulation data exchange or user-subroutine-populated arrays.

## See also

- [VARVAL](varval.md) — read a scalar variable element
