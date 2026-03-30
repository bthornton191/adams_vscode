# Eigenvalue Functions

Functions for computing eigenvalues and eigenvectors of matrix pairs `(A, B)` — i.e., solutions to the generalised eigenvalue problem `A·v = λ·B·v`.

## Quick reference

| Function | Returns |
|----------|---------|
| `EIG_DI` | Imaginary parts of generalised eigenvectors |
| `EIG_DR` | Real parts of generalised eigenvectors |
| `EIG_VI` | Imaginary parts of generalised eigenvalues |
| `EIG_VR` | Real parts of generalised eigenvalues |
| `EIGENVALUES_I` | Imaginary components of generalised eigenvalues (alias) |
| `EIGENVALUES_R` | Real components of generalised eigenvalues (alias) |

All functions take the same two arguments:

```
EIG_xx(A, B)
```

| Argument | Description |
|----------|-------------|
| `A` | Square matrix |
| `B` | Square matrix of the same size as `A` |

---

## EIG_DI — Imaginary eigenvector components

Returns a vector of the imaginary components of the generalised eigenvectors.

```adams_fn
EIG_DI({{1,2},{3,4}}, {{5,6},{7,8}})
! returns {4.99E-08, 0.0, 0.0, -4.99E-08}
```

---

## EIG_DR — Real eigenvector components

Returns a vector of the real components of the generalised eigenvectors.

```adams_fn
EIG_DR({{1,2},{3,4}}, {{5,6},{7,8}})
! returns {1.0, 0.0, 0.0, 1.0}
```

---

## EIG_VI — Imaginary eigenvalue components

Returns a vector of the imaginary components of the generalised eigenvalues.

---

## EIG_VR — Real eigenvalue components

Returns a vector of the real components of the generalised eigenvalues.

---

## EIGENVALUES_I

Alias for `EIG_DI`. Returns imaginary components of the generalised eigenvalues.

```adams_fn
EIGENVALUES_I({{1,2},{3,4}}, {{5,6},{7,8}})
! returns {5.77E-09, 6.70E-09, -5.77E-09, -6.70E-09}
```

---

## EIGENVALUES_R

Alias for `EIG_DR`. Returns real components of the generalised eigenvalues.

---

## See also

- [Matrix operations](matrix-operations.md)
- [Bode / control functions](bode-control.md)
