# function modify

A function allows you to define a new function in terms of an Adams View expression. The function modify command allows you to modify an existing user written function.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `function_name,` | Existing Expr_function | Specifies the name of the user-written function you are modifying. You should choose a name which is meaningfully related to the operation that the function is performing. |
| `new_function_name` | New Expr_function | Allows you to change the name of an already existing function. When you change the function's name, all references to it also change. |
| `text_of_expression,` | String | The TEXT_OF_EXPRESSION parameter defines the computation to be performed by the function. |
| `argument_names` | String | The ARGUMENT_NAMES parameter allows you to specify the names of the formal arguments in your function. |
| `type` | Array, Integer, Location_orientation, Object, Real, String | The TYPE parameter of a function indicates the type of the returned value. |
| `omments` | String | The COMMENTS parameter allows you to add comments to the function for documentation purposes. The strings are stored in the database and written to command files. |
| `category` | User, String, Math, Modelling, Loc_ori, Matrix_array, Database_object, Misc | Specifies which category this function should be classified under. |
