# Window Functions

Window functions weight a data array to reduce spectral leakage before applying an FFT or Welch PSD. Each function listed below applies a named window to an input array.

Both short and long names are available — `BARTLETT` and `BARTLETT_WINDOW` are equivalent, and so on.

## Quick reference

| Function | Short alias | Window shape |
|----------|-------------|--------------|
| `BARTLETT` / `BARTLETT_WINDOW` | `BARTLETT` | Triangular, zero endpoints |
| `BLACKMAN` / `BLACKMAN_WINDOW` | `BLACKMAN` | Three-term cosine sum (low sidelobe) |
| `HAMMING` / `HAMMING_WINDOW` | `HAMMING` | Raised cosine (α = 0.54) |
| `HANNING` / `HANNING_WINDOW` | `HANNING` | Raised cosine (α = 0.5) — also called Von Hann |
| `PARZEN` / `PARZEN_WINDOW` | `PARZEN` | Piecewise cubic (de la Vallée Poussin) |
| `RECTANGULAR` / `RECTANGULAR_WINDOW` | `RECTANGULAR` | Uniform weighting (no windowing) |
| `TRIANGULAR` / `TRIANGULAR_WINDOW` | `TRIANGULAR` | Symmetric triangular, non-zero endpoints |
| `WELCH` / `WELCH_WINDOW` | `WELCH` | Parabolic (quadratic) window |

All functions share the same signature:

```
WINDOW_NAME(a)
```

| Argument | Description |
|----------|-------------|
| `a` | 1×N array of input values |

Returns a 1×N array of the windowed (weighted) values.

---

## BARTLETT

Applies the Bartlett (triangular) window. The first and last elements are multiplied by zero.

```adams_fn
BARTLETT({1, 2, 3, 4, 2})
! returns {0, 1, 3, 2, 0}
```

---

## BLACKMAN

Applies the Blackman window — a three-term cosine sum that provides very low sidelobe levels at the cost of a wider main lobe.

```adams_fn
BLACKMAN({1, 2, 3, 4, 2})
```

---

## HAMMING

Applies the Hamming window (α = 0.54). Reduces the highest sidelobe compared to the Hanning window.

```adams_fn
HAMMING({1, 2, 3, 4, 2})
```

---

## HANNING

Applies the Hanning (Von Hann) window (α = 0.5). A commonly used general-purpose window.

```adams_fn
HANNING({1, 2, 3, 4, 2})
```

---

## PARZEN

Applies the Parzen window (de la Vallée Poussin) — a piecewise cubic window with very low sidelobe levels.

```adams_fn
PARZEN({1, 2, 3, 4, 2})
```

---

## RECTANGULAR

Applies a rectangular (flat-top / "no") window — equivalent to no windowing. All elements are multiplied by 1. Useful as a baseline.

```adams_fn
RECTANGULAR({1, 2, 3, 4, 2})
! returns {1, 2, 3, 4, 2}  (unchanged)
```

---

## TRIANGULAR

Applies a symmetric triangular window with non-zero endpoints (unlike Bartlett).

```adams_fn
TRIANGULAR({1, 2, 3, 4, 2})
```

---

## WELCH

Applies the Welch (parabolic) window.

```adams_fn
WELCH({1, 2, 3, 4, 2})
```

---

## Usage with PSD / PWELCH

```adams_fn
! Compute Welch PSD with Hamming window
window   = HAMMING(SERIES(0, 1, 256))
psd_vals = PWELCH(signal, window, 128, 256, sample_rate)
```

---

## See also

- [Signal processing functions](signal-processing.md)
- [Bode / control functions](bode-control.md)
