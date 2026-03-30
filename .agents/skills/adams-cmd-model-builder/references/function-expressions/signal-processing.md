# Signal Processing Functions

Adams View provides a set of functions for analysing signals in the frequency domain, computing spectral estimates, and applying digital or analogue filters to data arrays.

## Quick reference

| Function | Signature | Description |
|----------|-----------|-------------|
| `FFTMAG` | `FFTMAG(a, n)` | FFT magnitude array |
| `FFTPHASE` | `FFTPHASE(a, n)` | FFT phase array |
| `FREQUENCY` | `FREQUENCY(a, n)` | Frequency array corresponding to FFT output |
| `PSD` | `PSD(values, n)` | Power spectral density (periodogram) |
| `PWELCH` | `PWELCH(x, window, noverlap, nfft, fs)` | Welch power spectral density estimate |
| `FILTER` | `FILTER(t, y, num, den, method)` | Apply transfer-function filter |
| `FILTFILT` | `FILTFILT(t, y, num, den)` | Zero-phase forward-backward filter |
| `RESAMPLE` | `RESAMPLE(x, y, n)` | Resample to a new number of points |
| `DETREND` | `DETREND(y)` | Remove linear trend from a signal |
| `UNWRAP` | `UNWRAP(phase)` | Unwrap phase angles |

---

## FFTMAG

Returns an array of magnitudes from the FFT of the input values. Useful for identifying natural frequencies in a data stream.

```
FFTMAG(a, n)
```

| Argument | Description |
|----------|-------------|
| `a` | 1×N array of real input values |
| `n` | FFT size (≥ number of input values). If odd, returns `(n+1)/2` values; if even, returns `n/2+1` values |

```adams_fn
FFTMAG({0,1,4,9,16}, 5)
! returns {12.0, 7.1968, 4.2197}
```

---

## FFTPHASE

Returns an array of phase angles (radians) from the FFT of the input values.

```
FFTPHASE(a, n)
```

| Argument | Description |
|----------|-------------|
| `a` | 1×N array of real input values |
| `n` | FFT size (same conventions as `FFTMAG`) |

---

## FREQUENCY

Returns the frequency array (in Hz) that corresponds to the output of `FFTMAG` or `FFTPHASE`.

```
FREQUENCY(a, n)
```

| Argument | Description |
|----------|-------------|
| `a` | Same time-series input passed to `FFTMAG`/`FFTPHASE` |
| `n` | FFT size |

---

## PSD

Computes the power spectral density using the periodogram estimate (as defined in *Numerical Recipes*, equations 12.7.5).

```
PSD(values, n)
```

| Argument | Description |
|----------|-------------|
| `values` | 1×N array of input values from which FFT coefficients are computed |
| `n` | Number of output values (≥ number of inputs, ≥ 2) |

```adams_fn
PSD({0,1,4,9,16}, 7)
! returns {144.0, 250.786, 167.080, 91.006, 51.367, 38.688, 17.016}
```

---

## PWELCH

Estimates the power spectral density using Welch's method (averaged periodogram over overlapping segments).

```
PWELCH(x, window, noverlap, nfft, fs)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N input signal array |
| `window` | Window function array (e.g. from `HAMMING`) |
| `noverlap` | Number of overlapping samples between segments |
| `nfft` | FFT size |
| `fs` | Sample frequency (Hz) |

---

## FILTER

Applies a transfer-function filter to a time series. Supports both continuous (analogue) and discrete (digital) modes.

```
FILTER(t, y, numerator, denominator, method)
```

| Argument | Description |
|----------|-------------|
| `t` | 1×N array of independent variable values (usually time) |
| `y` | 1×N array of dependent variable values |
| `numerator` | Array of numerator coefficients of the transfer function |
| `denominator` | Array of denominator coefficients (length ≥ length of numerator) |
| `method` | `0` = discrete (digital); non-zero = continuous (analogue) |

---

## FILTFILT

Zero-phase digital filtering — applies the filter forwards and then backwards, eliminating phase distortion.

```
FILTFILT(t, y, numerator, denominator)
```

| Argument | Description |
|----------|-------------|
| `t` | 1×N independent variable array |
| `y` | 1×N dependent variable array |
| `numerator` | Numerator coefficients of the transfer function |
| `denominator` | Denominator coefficients |

---

## RESAMPLE

Resamples a signal to a new number of points using Fourier-based resampling.

```
RESAMPLE(x, y, n)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N independent variable array |
| `y` | 1×N dependent variable array |
| `n` | Desired number of output points |

---

## DETREND

Removes a least-squares linear trend from a signal.

```
DETREND(y)
```

| Argument | Description |
|----------|-------------|
| `y` | 1×N array of signal values |

---

## UNWRAP

Unwraps phase angles by replacing jumps greater than π with their 2π complement.

```
UNWRAP(phase)
```

| Argument | Description |
|----------|-------------|
| `phase` | 1×N array of phase angles (radians) |

---

## See also

- [Window functions](window-functions.md) — window functions for spectral analysis
- [Bode / control functions](bode-control.md) — frequency response analysis
- [Spline interpolation](spline-interpolation.md)
