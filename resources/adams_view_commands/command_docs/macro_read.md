# macro read

Allows you to create a macro by reading the commands to be executed from a file. Thus, instead of creating a new macro from the scratch, an existing command file can be used as a template.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `macro_name` | String | Specifies the name of an existing macro. |
| `file_name` | String | Specifies the name of the file that is to be read, written, or executed. |
| `user_entered_command` | String | Specifies the command string to be entered by the user to execute the macro. |
| `wrap_in_undo` | Yes/No | Specifies whether or not to the entire macro can be undone with a single undo command. |
| `help_file` | String | Specifies the text that is to be used as the command or topic string when getting help on a macro. |
| `help_string` | String | Specifies the text that is to be used as the command or topic string when getting help on a macro. |
| `create_panel` | Yes/No | Allows the user to specify if a panel is to be created for the specified macro. |
