# GUI Selection Functions

Functions that display interactive Adams View dialogs or navigators to let the user select objects, files, text, or types at script runtime. All must be wrapped in `EVAL()` to prevent unwanted parameterisation.

## Quick reference

| Function | Description |
|----------|-------------|
| `PICK_OBJECT` | Pick an object by clicking in the viewport |
| `SELECT_DIRECTORY` | Browse for a directory |
| `SELECT_FIELD` | Select a field from a dialog |
| `SELECT_FILE` | Browse for a file |
| `SELECT_MULTI_TEXT` | Select multiple text items from a list |
| `SELECT_OBJECT` | Select an object from the Database Navigator |
| `SELECT_OBJECTS` | Select multiple objects |
| `SELECT_REQUEST_IDS` | Select request IDs |
| `SELECT_TEXT` | Select text from a list |
| `SELECT_TYPE` | Select an object type |

---

## PICK_OBJECT

Prompts the user to click an object in the Adams View viewport and returns the selected object.

```
PICK_OBJECT(prompt)
```

---

## SELECT_DIRECTORY

Displays a directory browser and returns the selected path.

```
SELECT_DIRECTORY(title, default_dir)
```

---

## SELECT_FIELD

Displays a dialog for selecting a field and returns the selection.

```
SELECT_FIELD(object, prompt)
```

---

## SELECT_FILE

Displays the File Navigator and returns the selected file name.

```
SELECT_FILE(file_filter, directory)
```

| Argument | Description |
|----------|-------------|
| `file_filter` | Wildcard pattern for filtering file display (e.g. `"*.cmd"`) |
| `directory` | Starting directory |

```adams_cmd
var create var=chosen_file string_value=(EVAL(SELECT_FILE("*.cmd", getcwd())))
```

---

## SELECT_MULTI_TEXT

Displays a list and returns multiple selected text items as an array of strings.

```
SELECT_MULTI_TEXT(title, items)
```

---

## SELECT_OBJECT

Displays the Database Navigator and returns the selected object.

```
SELECT_OBJECT(parent, wildcard, type)
```

| Argument | Description |
|----------|-------------|
| `parent` | Database object defining the scope |
| `wildcard` | Name filter pattern |
| `type` | Object type string to display |

---

## SELECT_OBJECTS

Displays the Database Navigator and returns an array of selected objects.

```
SELECT_OBJECTS(parent, wildcard, type)
```

---

## SELECT_REQUEST_IDS

Displays a dialog for selecting request IDs and returns the selection.

```
SELECT_REQUEST_IDS(simulation)
```

---

## SELECT_TEXT

Displays a scrollable list and returns the selected text item.

```
SELECT_TEXT(items)
```

---

## SELECT_TYPE

Displays a type-selection dialog and returns the chosen type string.

```
SELECT_TYPE(prompt)
```

---

## See also

- [Alert functions](alert-functions.md)
- [File system functions](file-system.md)
