# CHEBY — Chebyshev Polynomial

Evaluates a polynomial expressed in the Chebyshev basis with up to 31 coefficients. Offers better numerical conditioning than standard monomials (POLY) when fitting measured data or when large polynomial orders are needed.

## Format

```
CHEBY(x, Shift, c0, c1, c2, ..., cN)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable |
| `Shift` | Required | Horizontal shift applied before evaluation (same role as in `POLY`) |
| `c0, c1, ..., cN` | Required | Chebyshev expansion coefficients; `c0` is the coefficient of T₀, `c1` of T₁, etc. Up to 31 coefficients |

**Equation:**

$$\text{CHEBY} = \sum_{k=0}^{N} c_k \, T_k(x - \text{Shift})$$

where $T_k$ is the Chebyshev polynomial of the first kind of degree $k$.

## When to use CHEBY vs POLY

| Scenario | Use |
|----------|-----|
| Expressing a curve fitted via Chebyshev regression | `CHEBY` |
| Simple low-order polynomial (quadratic, cubic) | `POLY` |
| Large-degree polynomial where round-off matters | `CHEBY` |

## Example

```adams_fn
! Chebyshev polynomial with three terms
CHEBY(TIME, 0, 5.0, 3.0, -1.0)
```

## See also

- [POLY](poly.md) — standard monomial polynomial with same interface
