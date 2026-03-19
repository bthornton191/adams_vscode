# file command read

Reads a command file and executes the commands contained within. The commands will be executed as if they were typed at the command line. Control will be returned after all the commands have been executed. If an error is detected in one of the commands and Adams View is unable to process the command, the system can react in one of several ways. This can be specified using the defaults command_file command, the default being to abort the file.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file that is to be read and executed. |
