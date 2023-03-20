# TERM_STATUS
Parses an Adams message file (usually with an .msg extension), and returns an array of simulation status codes corresponding to the tags: **A3TERM:STATUS** and **TERM:STATUS**.
This function is shorthand for the following expression:
`STACK(PARSE_STATUS(fileName, "A3TERM:STATUS"), PARSE_STATUS(fileName, "TERM:STATUS"))`

For complete details, see PARSE_STATUS.

> **Note**: This function returns its error codes as indicated in the expression above. First, it returns all the **A3TERM:STATUS** codes found in the file. Then, it returns all the **TERM:STATUS** codes that are appended to them.

## Format
```java
TERM_STATUS (fileName)
```
## Argument
 
**fileName**
: Name of the file in which to look for simulation status codes.

## Return Codes

| Return Value | Return Code | Description                                             |
|--------------|-------------|---------------------------------------------------------|
| 0            | NOERRS      | No errors                                               |
| -101         | INPERR      | Errors while opening ADAMS output files                 |
| -102         | BADSIT      | Site security checking not successful                   |
| -105         | ERINPT      | Errors while reading in ADAMS dataset                   |
| -117         | ERVRFY      | Model did not pass verification phase                   |
| -118         | ERMEMO      | Problem during memory initalization phase               |
| -119         | ERRVRS      | UCONFG Version mismatch                                 |
| -120         | ERRDIM      | UCONFG passes negative array dimensions                 |
| -121         | ERRLCK      | Lockup detected                                         |
| -122         | BADMEM      | Problem allocating memory                               |
| -123         | BADAMD      | Problem initiating AMD Command Parser                   |
| -124         | ERRSML      | Simulation failure detected                             |
| -125         | NOTCXX      | The Model is not compatible with the C++ solver         |
| -998         | TERMNT      | Current session terminated before completion            |
| -997         | INPTRM      | Session terminated before completion during input phase |
| -996         | PRFLER      | Program Fault was encountered                           |
| -995         | ERTERM      | Abnormal termination of Solver                          |
| -994         | SNHALT      | Sensor Halt was imposed                                 |
| -993         | TRMRCR      | Recursion encountered when trying to terminate          |
| -200         | QUITFL      | Quit Solver, control goes back to the driver            |
| 100          | BADCMD      | Erroneous command issued                                |


## Example
### Command
```java
variable create variable=status integer=(term_status("test.msg"))
```
### Returns 
An array of integers corresponding to the termination status codes found in the file test.msg.
