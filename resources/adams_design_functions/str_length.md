# STR_LENGTH
Returns a numerical value corresponding to the length of a string.

## Format
```adams_cmd
STR_LENGTH (Input String)
```

## Arguments
 
**Input String**
: Text String.

## Examples
The following example illustrates the use of the `STR_LENGTH` function:
 
### Function
```adams_cmd
STR_LENGTH ("Hello there")
```
### Result
```adams_cmd
11
```
The following function returns 10 because the double slash marks (//) concatenated the two strings into one:
 
### Function
```julia
STR_LENGTH ("Hello" // "there")
```
### Result
```adams_cmd
10
```
