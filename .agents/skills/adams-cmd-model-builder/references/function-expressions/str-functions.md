# String Functions

Adams View provides a comprehensive set of string manipulation functions. String literals use double quotes; strings can be concatenated with the `//` operator.

## Quick reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `STATUS_PRINT` | `STATUS_PRINT(text)` | Display text in all status bars |
| `STR_CASE` | `STR_CASE(str, case)` | Change string case |
| `STR_CHR` | `STR_CHR(n)` | Character from ASCII code |
| `STR_COMPARE` | `STR_COMPARE(s1, s2)` | Compare two strings |
| `STR_DATE` | `STR_DATE()` | Current date string |
| `STR_DELETE` | `STR_DELETE(str, start, len)` | Delete a substring |
| `STR_FIND` | `STR_FIND(base, search)` | First occurrence index |
| `STR_FIND_COUNT` | `STR_FIND_COUNT(base, search)` | Count occurrences |
| `STR_FIND_IN_STRINGS` | `STR_FIND_IN_STRINGS(strings, search)` | Search in array of strings |
| `STR_FIND_N` | `STR_FIND_N(base, search, n)` | Nth occurrence index |
| `STR_INSERT` | `STR_INSERT(base, insert, pos)` | Insert string at position |
| `STR_IS_REAL` | `STR_IS_REAL(str)` | True if string is a valid real number |
| `STR_IS_SPACE` | `STR_IS_SPACE(str)` | True if string is all whitespace |
| `STR_LENGTH` | `STR_LENGTH(str)` | Number of characters |
| `STR_MATCH` | `STR_MATCH(str, pattern)` | Wildcard match |
| `STR_MERGE_STRINGS` | `STR_MERGE_STRINGS(strings, sep)` | Join array of strings |
| `STR_PRINT` | `STR_PRINT(value)` | Convert value to string |
| `STR_REMOVE_WHITESPACE` | `STR_REMOVE_WHITESPACE(str)` | Strip whitespace |
| `STR_REPLACE_ALL` | `STR_REPLACE_ALL(str, old, new)` | Replace all occurrences |
| `STR_SPLIT` | `STR_SPLIT(str, sep)` | Split into array |
| `STR_SPRINTF` | `STR_SPRINTF(fmt, values)` | C-style formatted string |
| `STR_SUBSTR` | `STR_SUBSTR(str, start, len)` | Extract substring |
| `STR_TIMESTAMP` | `STR_TIMESTAMP()` | Current timestamp string |
| `STR_XLATE` | `STR_XLATE(str, from, to)` | Character-by-character translation |

---

## STATUS_PRINT

Displays a string in all Adams View status bars and returns the string.

```
STATUS_PRINT(text)
```

```adams_fn
STATUS_PRINT("Processing...")
```

---

## STR_CASE

Returns a string with the case modified.

```
STR_CASE(str, case)
```

| Argument | Description |
|----------|-------------|
| `str` | Input string |
| `case` | `1` = UPPER; `2` = lower; `3` = Mixed; `4` = Sentence |

```adams_fn
STR_CASE("this is a TEST!", 1)   ! returns "THIS IS A TEST!"
STR_CASE("HELLO WORLD", 2)       ! returns "hello world"
```

---

## STR_CHR

Returns a single-character string corresponding to an ASCII code.

```
STR_CHR(n)
```

---

## STR_COMPARE

Compares two strings lexicographically. Returns `0` if equal, negative if `s1 < s2`, positive if `s1 > s2`.

```
STR_COMPARE(s1, s2)
```

---

## STR_DATE

Returns a string containing the current date.

```
STR_DATE()
```

---

## STR_DELETE

Deletes `length` characters starting at `start` from a string.

```
STR_DELETE(str, start, length)
```

---

## STR_FIND

Returns the 1-based index of the first occurrence of `search` in `base`. Returns `0` if not found.

```
STR_FIND(base, search)
```

```adams_fn
STR_FIND("Hello", "l")    ! returns 3
STR_FIND("Hello", "xyz")  ! returns 0
```

---

## STR_FIND_COUNT

Returns the number of occurrences of `search` in `base`.

```
STR_FIND_COUNT(base, search)
```

---

## STR_FIND_IN_STRINGS

Searches an array of strings for those containing `search`. Returns matching strings or their indices.

```
STR_FIND_IN_STRINGS(strings, search)
```

---

## STR_FIND_N

Returns the 1-based index of the Nth occurrence of `search` in `base`.

```
STR_FIND_N(base, search, n)
```

---

## STR_INSERT

Inserts `insert_str` into `base` at position `pos`.

```
STR_INSERT(base, insert_str, pos)
```

---

## STR_IS_REAL

Returns `1` if the string can be parsed as a real number; `0` otherwise.

```
STR_IS_REAL(str)
```

---

## STR_IS_SPACE

Returns `1` if the string consists entirely of whitespace; `0` otherwise.

```
STR_IS_SPACE(str)
```

---

## STR_LENGTH

Returns the number of characters in a string.

```
STR_LENGTH(str)
```

```adams_fn
STR_LENGTH("Hello there")    ! returns 11
STR_LENGTH("Hello" // "there")  ! returns 10
```

> Use `//` to concatenate strings.

---

## STR_MATCH

Returns `1` if `str` matches a wildcard `pattern`; `0` otherwise. Wildcards: `*` (any sequence), `?` (any single character).

```
STR_MATCH(str, pattern)
```

---

## STR_MERGE_STRINGS

Joins an array of strings into a single string, inserting `separator` between each element.

```
STR_MERGE_STRINGS(strings, separator)
```

---

## STR_PRINT

Converts a numeric or other value to its string representation.

```
STR_PRINT(value)
```

---

## STR_REMOVE_WHITESPACE

Returns a copy of the string with all leading and trailing whitespace removed.

```
STR_REMOVE_WHITESPACE(str)
```

---

## STR_REPLACE_ALL

Returns a copy of `str` with every occurrence of `old` replaced by `new`.

```
STR_REPLACE_ALL(str, old, new)
```

```adams_fn
STR_REPLACE_ALL("aabbccaaaeeffaaaa", "aa", "cba")
! returns "cbabbcccbaaeeffcbacba"
```

---

## STR_SPLIT

Splits `str` on `separator` and returns an array of trimmed substrings.

```
STR_SPLIT(str, separator)
```

```adams_fn
STR_SPLIT(" apple; orange; grape ", ";")
! returns {"apple", "orange", "grape"}
```

---

## STR_SPRINTF

Constructs a string using a C-style format string.

```
STR_SPRINTF(format, {values})
```

| Argument | Description |
|----------|-------------|
| `format` | A C-language format string (e.g. `"%s = %.3f"`) |
| `values` | Array of values to substitute |

```adams_fn
STR_SPRINTF("The %s of %s is %03d%%.", {"value", "angle", 2})
! returns "The value of angle is 002%"
```

---

## STR_SUBSTR

Returns a substring starting at position `start` of length `len`.

```
STR_SUBSTR(str, start, len)
```

```adams_fn
STR_SUBSTR("This is one string", 9, 8)
! returns "one stri"
```

---

## STR_TIMESTAMP

Returns a string containing the current date and time.

```
STR_TIMESTAMP()
```

---

## STR_XLATE

Translates characters in `str`, replacing each character found in `from_chars` with the corresponding character in `to_chars`.

```
STR_XLATE(str, from_chars, to_chars)
```

---

## String concatenation operator

The `//` operator concatenates two strings:

```adams_fn
"Model_" // STR_PRINT(index)    ! e.g. "Model_3"
```

---

## See also

- [Type conversion functions](type-conversion.md) — STOI, STOR, STOO
- [Database functions](db-query.md) — DB_ functions that return strings
