# macro create

A macro is a single command that you create to execute a series of Adams View commands. To create a macro, you give Adams View the list of commands you want executed, as well as the new command (i.e., the macro) that will execute them.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `macro_name` | String | Specifies the name of the new macro. |
| `user_entered_command` | String | Specifies the command string to be entered by the user to execute the macro. |
| `commands_to_be_ executed` | String | Specifies the list of Adams View commands to be executed. |
| `wrap_in_undo` | Yes/No | Specifies whether or not to the entire macro can be undone with a single undo command. |
| `help_file` | String | Specifies the text that is to be used as the command or topic string when getting help on a macro. |
| `help_string` | String | Specifies the text that is to be used as the command or topic string when getting help on a macro. |
| `create_panel` | Yes/No | Allows the user to specify if a panel is to be created for the specified macro. |
| `security_code` |  |  |
