# measure create computed

Adams View computed measures allow you to create measures in the Adams View expression language that can be evaluated before a simulation or any time after. You build them using design-time functions and typically use them in the initial model set up.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `measure_name` | New measure name | Specifies name of the computed measure |
| `text_of_expression` | String | The TEXT_OF_EXPRESSION parameter defines the computation to be performed by the function. Remember that the value of this argument should be a character string, NOT an expression. |
| `units` | String | Specifies units of the measure. |
| `create_measure_display` | Yes/No | Specifies whether the strip chart has to be displayed of the measure. |
| `legend` | String | Specifies the text that will appear at the top of the created measure. |
| `comments` | String | Specifies any comments. |
