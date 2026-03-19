# optimize fit_response_surface

The FIT_RESPONSE_SURFACE command fits a surface of arbitrary polynomial degree to a given set of result set components. Usually, the dependent data is the response component produced by a DOE, and the independent data values are the design variable values used to compute the response.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `result_set_name` | Result Set Name | This parameter allows you to identify a result set name |
| `dependent_variable` | Existing Component | The DEPENDENT_VARIABLE specifies the result set which is the left-hand side of the fit equation. |
| `independent_variables` | Existing Component | The INDEPENDENT_VARIABLES specify the result sets which are the right-hand side of the fit equation. DEPENDENT_VARIABLE = F(INDEPENDENT_VARIABLES) Usually, these result sets were the experimental values of the design variables in an experiment. |
| `polynomial_degrees` | Integer | The POLYNOMIAL_DEGREES parameter specifies the highest degree for each of the indpendent variables. |
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed. |
