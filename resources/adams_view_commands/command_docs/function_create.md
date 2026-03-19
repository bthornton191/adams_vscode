# function create

A function allows you to define a new function in terms of an Adams View expression. The function create command allows you to create a function. You may reverse this creation at a later time with an UNDO command.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `function_name` | New Expr_function | Specifies the name of the user-written function you are creating or modifying. You should choose a name which is meaningfully related to the operation that the function is performing. |
| `text_of_expression` | String | The TEXT_OF_EXPRESSION parameter defines the computation to be performed by the function. |
| `argument_names` | String | The ARGUMENT_NAMES parameter allows you to specify the names of the formal arguments in your function. |
| `type` | Array, Integer, Location_orientation, Object, Real, String | The TYPE parameter of a function indicates the type of the returned value. |
| `comments` | String | Allows you to add comments to the function for documentation purposes. The strings are stored in the database and written to command files. |
| `category` | User, String, Math, Modelling, Loc_ori, Matrix_array,database_object, Misc | Specifies which category this function should be classified under. |
