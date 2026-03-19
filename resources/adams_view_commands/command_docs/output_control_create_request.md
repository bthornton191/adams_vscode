# output_control create request

Allows you to create a replica request. This replica request will be an exact copy of the original with the exception of the name.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `request_name` | String | Specifies the name of the new request to be created. You may later identify a request by typing its name. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `output_type` | Displacement/velocity/acceleration/force/user | Specifies whether you want the request to output displacement, velocity, acceleration, force, or user data. |
| `i_marker_name` | An existing triad | Specifies the marker for which you wish Adams to generate data. |
| `j_marker_name` | An existing triad | Specifies the marker with respect to which you wish Adams to generate the data. |
| `r_marker_name` | An existing triad | Specifies the marker with respect to which you want Adams to resolve the data. Adams computes the data identified by the I and J markers, then reports the data as x, y, and z components in the reference frame of the reference marker. Angular displacements, which are not vectors, are not affected by reference marker. If you do not supply this parameter, Adams will resolve the data in the ground reference frame. |
| `comment` | String | Specifies a comment for the request. The comment can contain up to 80 characters, and can be comprised of letters of the alphabet (a-z, A-Z), numbers (0-9), and underscores. You may also use spaces and special characters (*&^%$#) if you enclose the comment in quotation marks. |
| `user_function` | Real | Specifies up to 30 values for Adams to pass to a user-written subroutine. See the Adams User's Manual for information on writing user-written subroutines. |
| `title` | String | Specifies any of the eight alphanumeric headings for columns of request output in the request file. |
| `f1` | Function | Specifies the function expression that is the first component of the request that is being created or modified. The f1 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f2` | Function | Specifies the function expression that is the second component of the request that is being created or modified. The f2 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f3` | Function | Specifies the function expression that is the third component of the request that is being created or modified. The f3 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f4` | Function | Specifies the function expression that is the fourth component of the request that is being created or modified. The f4 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f5` | Function | Specifies the function expression that is the fifth component of the request that is being created or modified. The f5 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f6` | Function | Specifies the function expression that is the sixth component of the request that is being created or modified. The f6 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f7` | Function | Specifies the function expression that is the Seventh component of the request that is being created or modified. The f7 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `f8` | Function | Specifies the function expression that is the eight component of the request that is being created or modified. The f8 parameter allows you to generate user-defined output variables and have them reported by Adams to the request file. |
| `routine` | String | Specifies an alternative library and name for the user subroutine REQSUB. |
| `component_names` | String | This option is available only for XML format. By default, there are eight components per results set, and they have generic names, such as X, Y, Z, and MAG. You can specify more descriptive names for them or specify a particular unit label or unit type associated with each component. |
| `component_units` | String | This option is available only for XML format. Specify the unit dimension of the result set components. If you do not specify units, then the units of the components are predefined based upon standard request type (For example, length, velocity and acceleration) |
| `component_labels` | String | This option is available only for XML format. Specify the labels to be used when plotting the result set components. Labels can be strings that include white space. Quotes must be used to define the string if you see special characters or white space. |
| `results_name` | String | Specifies the name of the results set in which all result set components are placed. If there is an existing result set with this name, then the result set components are placed in that result set. |
| `variable_name` | String | Specifies one or more variables that represent the components associates with a request. This option is only available if the format of the results files is set to XML. |
