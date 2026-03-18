# TABLE_GET_REALS

Returns an array of reals representing the contents of the cells within the specified row/column range. Values are retrieved in column order.

## Format
```
TABLE_GET_REALS (o_table, startRow,endRow,startCol,endCol, blankBehavior, ignoreTrailingBlanks)
```

## Arguments

**o_table**
: Data/object table of interest.

**startRow, endRow**
: The 1-based integer starting and ending rows of interest.

**startCol, endCol**
: The 1-based integer starting and ending columns of interest.

**blankBehavior**
: String indicating how to treat blank cells: ■zero- use a zero for the contents of the cell. ■failure-causes the entire retrieval to fail.

**ignoreTrailingBlanks**
: Boolean value (an integer of 1 or 0) to indicate if the blanks at the ends of columns are to be ignored altogether when retrieving values. Applicable only for the cases where an entire single row or column is being processed. Returns an array of reals representing the contents of the cells within the specified row/column range. Values are retrieved in column order.
