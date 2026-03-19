# defaults adams_output

The ADAMS_OUTPUT command is used to set parameters that control the organization and statement format of Adams datasets written by VIEW.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `statement_order` | Markers_with_parts, Markers_where_used, Submodels_and_AdamsId, Submodels_and_ObjName, As_found_in_file | This controls the organization of the statements within the dataset. |
| `arguments_per_line` | Single/multiple | This controls how many arguments are written on each line of an Adams dataset statement. The default is a single argument per line. |
| `text_case` | Upper/lower/mixed | This controls the case of the text written for the statement's keywords and parameters. |
| `indent_spaces` | Integer | This controls the number of spaces after the comma in column one used to indent a continuation line of a statement. |
| `write_default_values` | On/off | This controls whether or not arguments that have default values are written explicitly into the dataset. The default is that the arguments with default values are not written into the datset. |
| `scientific_notation` | Integer | This controls the lower and upper powers of ten where the format for real numbers switches from a fixed point format to scientific notation. |
| `trailing_zeros` | On/off | This controls whether or not trailing zeros are printed for real numbers. |
| `decimal_places` | Integer | This controls how many places are written after the decimal point for real numbers. The default value is ten decimal places. |
| `zero_threshold` | Real | This specifies the threshold value for numbers being written to an Adams data set. |
| `round_off` | On/off | This turns the round off feature for real numbers on or off. The actual numbers of places retained during rounding off is controlled by the SIGNIFICANT_FIGURES argument. |
| `significant_figures` | Integer | This controls how many significant figures of a real number are retained during round off when it is enabled by setting the value of the ROUND_OFF argument to ON. |
| `active_only` | On/off | This controls the writing of inactive objects as comments.Default value is off. |
| `export_all_graphics` | On/off | On -Select Export All Graphics to write all the graphics into the dataset.Off - If this option is not checked, only the dataset graphics that are supported by the solver (such as BOX) and those that are referenced by contacts, are included in the dataset. |
