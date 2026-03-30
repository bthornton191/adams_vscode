# Table Functions

Functions for reading data from Adams View table widgets (grid controls used in dialogs and macros).

## Quick reference

| Function | Description |
|----------|-------------|
| `TABLE_COLUMN_SELECTED_CELLS` | Selected cell indices in a column |
| `TABLE_GET_CELLS` | Cell contents for a row/column range |
| `TABLE_GET_DIMENSION` | Number of rows or columns |
| `TABLE_GET_REALS` | Numeric values from a column range |
| `TABLE_GET_SELECTED_COLS` | Indices of selected columns |
| `TABLE_GET_SELECTED_ROWS` | Indices of selected rows |

---

## TABLE_GET_CELLS

Returns an array of strings representing the contents of the cells within a specified row/column range. Values are returned in column order.

```
TABLE_GET_CELLS(table, start_row, end_row, start_col, end_col, blank_behavior, ignore_trailing_blanks)
```

| Argument | Description |
|----------|-------------|
| `table` | Data/object table reference |
| `start_row` / `end_row` | 1-based row range |
| `start_col` / `end_col` | 1-based column range |
| `blank_behavior` | `"Blank"` = empty string; `"Zero"` = use 0; `"Failure"` = fail on blank |
| `ignore_trailing_blanks` | Boolean — ignore trailing blank cells in rows/columns |

---

## TABLE_GET_DIMENSION

Returns the number of rows or columns in a table.

```
TABLE_GET_DIMENSION(table, rows_or_cols)
```

| Argument | Description |
|----------|-------------|
| `table` | Data/object table reference |
| `rows_or_cols` | `"rows"` or `"cols"` |

---

## TABLE_GET_REALS

Returns an array of real numbers from the table within the specified column range.

```
TABLE_GET_REALS(table, start_row, end_row, start_col, end_col)
```

---

## TABLE_COLUMN_SELECTED_CELLS

Returns an array of 1-based row indices of the currently selected cells in a specified column.

```
TABLE_COLUMN_SELECTED_CELLS(table, col)
```

---

## TABLE_GET_SELECTED_COLS

Returns an array of 1-based column indices of the currently selected columns.

```
TABLE_GET_SELECTED_COLS(table)
```

---

## TABLE_GET_SELECTED_ROWS

Returns an array of 1-based row indices of the currently selected rows.

```
TABLE_GET_SELECTED_ROWS(table)
```

---

## See also

- [GUI selection functions](gui-select.md)
- [Array helper functions](array-helpers.md)
