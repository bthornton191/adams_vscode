# Matrix Operations

Adams View provides a comprehensive set of functions for working with matrices and arrays: creating, transforming, querying, and performing algebraic operations.

## Quick reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `ALLM` | `ALLM(M)` | True if all elements are non-zero |
| `ANYM` | `ANYM(M)` | True if any element is non-zero |
| `APPEND` | `APPEND(M1, M2)` | Append one matrix to another (column-wise) |
| `BALANCE` | `BALANCE(A)` | Balance a matrix for numerical stability |
| `CLIP` | `CLIP(M, lo, hi)` | Clamp each element to \[lo, hi\] |
| `COLS` | `COLS(M)` | Number of columns |
| `COMPRESS` | `COMPRESS(M)` | Remove zero elements |
| `COND` | `COND(M)` | Condition number |
| `CONVERT_ANGLES` | `CONVERT_ANGLES(E, from, to)` | Convert Euler angle sequences |
| `CROSS` | `CROSS(M1, M2)` | Cross product (3×1 vectors) |
| `DET` | `DET(M)` | Determinant |
| `DMAT` | `DMAT(v)` | Diagonal matrix from a vector |
| `DOT` | `DOT(M1, M2)` | Dot product |
| `ELEMENT` | `ELEMENT(M, i, j)` | Extract element at row i, column j |
| `EXCLUDE` | `EXCLUDE(M, indices)` | Remove elements at specified indices |
| `INVERSE` | `INVERSE(M)` | Matrix inverse |
| `NORMALIZE` | `NORMALIZE(M)` | Normalise to unit magnitude |
| `PROD` | `PROD(M)` | Product of all elements |
| `RESHAPE` | `RESHAPE(M, shape)` | Reshape to new dimensions |
| `REVERSE` | `REVERSE(M)` | Reverse element order |
| `ROWS` | `ROWS(M)` | Number of rows |
| `SHAPE` | `SHAPE(M)` | Row × column dimensions |
| `SORT` | `SORT(M, dir)` | Sort elements |
| `SORT_BY` | `SORT_BY(M, by)` | Sort rows by a key column |
| `SORT_INDEX` | `SORT_INDEX(M, dir)` | Indices that would sort M |
| `STACK` | `STACK(M1, M2)` | Concatenate column-wise |
| `TILDE` | `TILDE(v)` | Skew-symmetric (cross-product) matrix |
| `TMAT` | `TMAT(E, ori_type)` | Transformation matrix from Euler angles |
| `TMAT3` | `TMAT3(E, ori_type)` | 3×3 rotation matrix variant |
| `TRANSPOSE` | `TRANSPOSE(M)` | Matrix transpose |
| `UNIQUE` | `UNIQUE(M)` | Remove duplicate elements |

---

## ALLM

Returns `1` (true) if all elements of the matrix are non-zero; `0` otherwise.

```
ALLM(M)
```

---

## ANYM

Returns `1` (true) if any element of the matrix is non-zero; `0` otherwise.

```
ANYM(M)
```

---

## APPEND

Appends (concatenates column-wise) two matrices. The number of rows must match.

```
APPEND(M1, M2)
```

---

## BALANCE

Balances a matrix for improved numerical conditioning.

```
BALANCE(A)
```

---

## CLIP

Clamps each element of a matrix to the closed interval `[lo, hi]`.

```
CLIP(M, lo, hi)
```

| Argument | Description |
|----------|-------------|
| `M` | Input matrix |
| `lo` | Lower bound |
| `hi` | Upper bound |

---

## COLS

Returns the number of columns in a matrix.

```
COLS(M)
```

---

## COMPRESS

Returns a 1-D array of all non-zero elements of a matrix.

```
COMPRESS(M)
```

---

## COND

Returns the condition number of a matrix (ratio of largest to smallest singular value).

```
COND(M)
```

---

## CONVERT_ANGLES

Converts a set of Euler angles from one rotation sequence to another.

```
CONVERT_ANGLES(E, from_type, to_type)
```

| Argument | Description |
|----------|-------------|
| `E` | 3-element Euler angle array |
| `from_type` | Source sequence string, e.g. `"body 313"`, `"space 123"` |
| `to_type` | Target sequence string |

---

## CROSS

Returns the cross product of two 3×1 or 1×3 vectors.

```
CROSS(M1, M2)
```

```adams_fn
CROSS({1,0,0}, {0,1,0})
! returns {0, 0, 1}
```

---

## DET

Returns the determinant of a square matrix.

```
DET(M)
```

```adams_fn
DET({[1,2,0],[2,2,-1],[3,1,1]})
! returns -8.0
```

---

## DMAT

Creates a diagonal matrix from a vector.

```
DMAT(v)
```

---

## DOT

Returns the dot product of two matrices.

```
DOT(M1, M2)
```

```adams_fn
DOT({1,1,0}, {1,0,1})
! returns 1
```

---

## ELEMENT

Returns the element at row `i`, column `j` of a matrix.

```
ELEMENT(M, i, j)
```

---

## EXCLUDE

Returns a copy of the matrix with elements at the specified indices removed.

```
EXCLUDE(M, indices)
```

---

## INVERSE

Returns the inverse of a square matrix. Generates an error if no inverse exists.

```
INVERSE(M)
```

```adams_fn
INVERSE({[1,2,0],[2,1,-1],[3,1,1]})
! returns {[-.25,.25,.25],[.625,-.125,-.125],[.125,-.625,.375]}
```

---

## NORMALIZE

Returns a normalised version of the input matrix (unit magnitude).

```
NORMALIZE(M)
```

```adams_fn
NORMALIZE({3,4,5})
! returns {0.424, 0.566, 0.707}
```

---

## PROD

Returns the product of all elements in a matrix.

```
PROD(M)
```

---

## RESHAPE

Creates a new matrix from an existing one with new dimensions specified by a shape descriptor.

```
RESHAPE(M, shape)
```

| Argument | Description |
|----------|-------------|
| `M` | Source matrix |
| `shape` | 1- or 2-element array `{rows, cols}` |

```adams_fn
RESHAPE({1,0,0,0,1,0,0,0,1}, {3,3})
! returns 3x3 identity matrix
```

---

## REVERSE

Returns the elements of a matrix in reversed order.

```
REVERSE(M)
```

---

## ROWS

Returns the number of rows in a matrix.

```
ROWS(M)
```

---

## SHAPE

Returns a 2-element array `{num_rows, num_cols}` giving the dimensions of a matrix.

```
SHAPE(M)
```

---

## SORT

Returns the matrix elements sorted in ascending or descending order.

```
SORT(M, direction)
```

| Argument | Description |
|----------|-------------|
| `M` | Input matrix |
| `direction` | `"a"` (ascending) or `"d"` (descending) |

```adams_fn
SORT({3,2,1}, "a")
! returns {1, 2, 3}
```

---

## SORT_BY

Sorts the rows of a matrix by the values in a specified column.

```
SORT_BY(M, by)
```

---

## SORT_INDEX

Returns the indices that would sort the matrix (without sorting the matrix itself).

```
SORT_INDEX(M, direction)
```

---

## STACK

Concatenates two matrices column-wise. Both must have the same number of columns.

```
STACK(M1, M2)
```

```adams_fn
STACK({[1,2],[3,4]}, {[1,1],[2,2]})
! returns {[1,2,1,1],[3,4,2,2]}
```

---

## TILDE

Returns the skew-symmetric (cross-product) matrix of a 3-element vector.

```
TILDE(v)
```

---

## TMAT

Returns a 3×3 transformation matrix from a body-fixed or space-fixed Euler angle sequence.

```
TMAT(E, ori_type)
```

| Argument | Description |
|----------|-------------|
| `E` | 3×1 Euler angle array |
| `ori_type` | Rotation sequence string, e.g. `"body 313"` or `"space 123"` |

---

## TMAT3

Returns a 3×3 rotation matrix variant.

```
TMAT3(E, ori_type)
```

Arguments are identical to `TMAT`.

---

## TRANSPOSE

Returns the transpose of a matrix.

```
TRANSPOSE(M)
```

```adams_fn
TRANSPOSE({1,2,3})
! returns {[1],[2],[3]}
```

---

## UNIQUE

Returns the unique (deduplicated) elements of a matrix.

```
UNIQUE(M)
```

---

## See also

- [Statistics functions](statistics.md)
- [Array helper functions](array-helpers.md)
- [Eigenvalue functions](eigenvalue.md)
