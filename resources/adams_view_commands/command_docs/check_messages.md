# check_messages

This command provides you with a way to monitor an Adams simulation while it is running in batch mode. This is done by querying the Adams message data base using some filter and sorting parameters.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the Adams message file that is to be read. |
| `faults` | boolean | Specifies that the messages of type PROGRAM FAULT are to be reported. |
| `errors` | boolean | Specifies that the messages of type ERROR are to be reported. |
| `warnings` | boolean | Specifies that the messages of type WARNING are to be reported. |
| `info` | boolean | Specifies that the messages of type INFO are to be reported. |
| `sort_by_time` | boolean | Specifies in what order the messages of all types are to be reported. |
