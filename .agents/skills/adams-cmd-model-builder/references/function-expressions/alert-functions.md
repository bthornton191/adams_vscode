# Alert and Utility Functions

Miscellaneous utility functions for displaying alerts, checking Boolean states, computing aggregate mass properties, and macro discovery.

## Quick reference

| Function | Description |
|----------|-------------|
| `ALERT` | Display a modal dialog with up to 3 buttons |
| `ALERT2` | Simplified two-button alert |
| `ALERT3` | Simplified three-button alert |
| `FILE_ALERT` | Display alert from a file |
| `ON_OFF` | Convert integer Boolean to `"on"` / `"off"` string |
| `AGGREGATE_MASS` | Compute aggregate mass properties for bodies |
| `SECURITY_CHECK` | Verify a security token |
| `FIND_MACRO_FROM_COMMAND` | Find a macro key from its command string |

---

## ALERT

Displays a modal alert dialog. Recommended to wrap in `EVAL()` to prevent parameterisation.

```
ALERT(type, message, button1, button2, button3, default)
```

| Argument | Description |
|----------|-------------|
| `type` | `"Error"`, `"Warning"`, `"Information"`, `"Working"`, or `"Question"` |
| `message` | Message text |
| `button1` | Label for the first button |
| `button2` | Label for the second button (empty string to hide) |
| `button3` | Label for the third button (empty string to hide) |
| `default` | Default button number (1, 2, or 3) |

Returns the number of the button the user clicked.

```adams_cmd
! Confirm before deleting
var create var=choice integer=(EVAL(ALERT("Question","Delete all parts?","Yes","No","",1)))
if condition=(choice == 1)
    ! proceed with delete
end
```

---

## ALERT2

Simplified two-button alert dialog.

```
ALERT2(type, message, button1, button2, default)
```

---

## ALERT3

Simplified three-button alert dialog.

```
ALERT3(type, message, button1, button2, button3, default)
```

---

## FILE_ALERT

Displays an alert dialog whose message is read from a file.

```
FILE_ALERT(type, file_name, button1, button2, button3, default)
```

---

## ON_OFF

Returns the string `"on"` or `"off"` based on an integer Boolean value.

```
ON_OFF(state)
```

| Argument | Description |
|----------|-------------|
| `state` | Integer: `1` = on, `0` = off |

```adams_fn
ON_OFF(1)   ! returns "on"
ON_OFF(0)   ! returns "off"
```

Useful for building command strings dynamically:

```adams_cmd
part attributes part=.model.PART_1 active=(ON_OFF(is_active))
```

---

## AGGREGATE_MASS

Computes and returns aggregate mass properties for one or more bodies.

```
AGGREGATE_MASS(objects, reference_frame, type_string)
```

| Argument | Description |
|----------|-------------|
| `objects` | Single object or array of models, bodies, or tires |
| `reference_frame` | Reference frame for cm position and inertia angles; `0` = global |
| `type_string` | `"mass"` (1 real), `"cm_pos"` (3 reals), `"im_ang"` (3 reals), `"inertias"` (6 reals), or `"all"` (13 reals) |

```adams_fn
AGGREGATE_MASS({PART_2, PART_3}, 0, "mass")
! returns total mass of PART_2 and PART_3
```

---

## SECURITY_CHECK

Verifies a security token and returns a Boolean result.

```
SECURITY_CHECK(token)
```

---

## FIND_MACRO_FROM_COMMAND

Returns the key (name) of the macro that is bound to a given command string. Returns `None` if no macro is found.

```
FIND_MACRO_FROM_COMMAND(command_str)
```

---

## See also

- [GUI selection functions](gui-select.md)
- [File system functions](file-system.md)
