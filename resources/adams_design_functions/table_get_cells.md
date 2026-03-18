# TABLE_GET_CELLS

Returns an array of strings representing the contents of the cells within the specified row/column range. Values are retrieved in column order.

## Format
```
TABLE_GET_CELLS (O_table, Start_row, End_row, Start_col, End_col, Behavior, Ignore trailing blanks)
```

## Arguments

**O_table**
: Data/object table of interest.

**Start_row / End_row**
: The 1-based starting and ending rows of interest.

**startCol, endCol**
: The 1-based integer starting and ending columns of interest.

**Behavior**
: String that indicates how to treat blank cells. The options are: ■Blank = use an empty string. ■Zero = use a 0 for the contents of the cell. ■Failure = cause the entire retrieval to fail

**Ignore trailing blanks**
: Boolean value that indicates if the blanks at the ends of columns are to be ignored when retrieving values. Applicable only when an entire row or column is being processed.
