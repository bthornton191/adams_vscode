# PARSE_STATUS

Parses an Adams message file (usually with an .msg extension), and returns an array of integer status codes corresponding to the given search tag.

## Format
```
PARSE_STATUS(fileName, tag)
```

## Arguments

**fileName**
: Name of the message file in which to search for status codes.

**tag**
: Character string indicating the status coes to extract.
