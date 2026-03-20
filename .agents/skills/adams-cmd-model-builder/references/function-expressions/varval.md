# VARVAL — State Variable Value

Returns the current run-time value of an Adams **algebraic variable** data element.

## Format

```
VARVAL(Variable Name)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `Variable Name` | Required | Full dot-path object name of the variable element (e.g., `.MODEL.MY_VAR`) |

The argument is an **object name**, not a numeric ID.

## Creating a variable to read back

```cmd
data_element create variable &
    variable_name = .MODEL.REL_VEL &
    adams_id = 1 &
    function = "VR(.MODEL.BODY.i_mkr, .MODEL.ground.j_mkr, .MODEL.ground.j_mkr)"
```

## Using VARVAL in a FUNCTION= expression

```adams_fn
! Use the variable value to control a force
STEP(VARVAL(.MODEL.REL_VEL), -10.0, -500.0, 10.0, 500.0)

! Nest several variables to build a control law
VARVAL(.MODEL.CONTROL_OUTPUT)
```

## Notes

- `VARVAL` is the standard way to read another element's result inside a `FUNCTION=` expression.
- You can chain multiple variables to build modular, readable expressions.
- The variable element can be defined using any other `FUNCTION=` expression, including sensors, displacements, forces, and splines.

## See also

- [ARYVAL](aryval.md) — read an element from an array data element
- [AKISPL](akispl.md) / [CUBSPL](cubspl.md) — evaluate spline data elements
