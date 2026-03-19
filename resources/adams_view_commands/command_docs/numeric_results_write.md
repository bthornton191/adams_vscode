# numeric_results write

Allows you to write the contents of one or more result set components to the information window, a file, or both.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_component_name` | Existing Result Set Component | Identifies the existing result set. |
| `sort_by` | By_time/By_value | Specifies how numerical results are sorted as they are written to the terminal or to a file using the NUMERICAL_RESULTS WRITE command. |
| `order` | Sort_order | Specifies whether the result set component is to be listed in ascending or descending order. |
| `write_to_terminal` | On, Off | Specifies if the information requested is to be sent to the informational window or not. This parameter is most likely to be used in conjunction with the FILE_NAME parameter to get the information put into a file. |
| `above_value` | Real | The ABOVE_VALUE parameter is used as a critical value evaluator in the operation to be performed. |
| `below_value` | Real | The BELOW_VALUE parameter is used as a critical value evaluator in the operation to be performed. |
