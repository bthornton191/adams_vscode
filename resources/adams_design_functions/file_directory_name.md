# FILE_EXISTS
Returns a 1 if a file exists, and a 0 if it doesn't.

## Format
```adams_cmd
FILE_EXISTS(file_name)
```

## Argument
 
**file_name**
: The name of the file you're looking for.

## Example
For the following examples, assume that a file named aview.log% exists, and avkiew.log% does not.

### Function
```adams_cmd
FILE_EXISTS(aview.log%)
```
### Returns
```adams_cmd
1
```

### Function
```adams_cmd
FILE_EXISTS(avkiew.log%)
```
### Returns
```adams_cmd
0
```
