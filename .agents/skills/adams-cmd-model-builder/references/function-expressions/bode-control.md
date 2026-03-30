# Bode / Control Functions

These functions compute frequency-response data (gain and phase) for linear dynamic systems defined in Adams View, and provide Butterworth filter design utilities.

## Quick reference

| Function | Description |
|----------|-------------|
| `BODEABCD` | Bode response from ABCD state-space matrices |
| `BODELSE` | Bode response from an Adams linear state equation element |
| `BODELSM` | Bode response from a linear state model |
| `BODESEQ` | Bode response from a state equation array |
| `BODETFCOEF` | Bode response from transfer-function coefficient arrays |
| `BODETFS` | Bode response from an Adams transfer function element |
| `BUTTER_DENOMINATOR` | Butterworth filter denominator coefficients |
| `BUTTER_FILTER` | Filter a curve using a Butterworth filter |
| `BUTTER_NUMERATOR` | Butterworth filter numerator coefficients |

---

## OUTTYPE values (common to all BODE functions)

All BODE functions use an `OUTTYPE` flag to control output and sampling:

| OUTTYPE | Output | Sampling |
|---------|--------|----------|
| 0 | Gain + Phase | Fixed linear step size |
| 1 | Gain only | Fixed linear step size |
| 2 | Phase only | Fixed linear step size |
| 3 | Gain + Phase | FREQARG linearly-spaced samples |
| 4 | Gain only | FREQARG linearly-spaced samples |
| 5 | Phase only | FREQARG linearly-spaced samples |
| 6 | Gain + Phase | FREQARG log-spaced samples |
| 7 | Gain only | FREQARG log-spaced samples |
| 8 | Phase only | FREQARG log-spaced samples |

When `OUTTYPE` is 0–2, `FREQARG` is the step size. When `OUTTYPE` is 3–8, `FREQARG` is the number of samples.

---

## BODEABCD

Returns gain and/or phase values for the frequency response of a linear system specified by ABCD state-space matrices.

```
BODEABCD(outtype, outindex, A, B, C, D, freq_start, freq_end, freq_arg)
```

| Argument | Description |
|----------|-------------|
| `outtype` | Output/sampling flag (see table above) |
| `outindex` | `0` = all outputs; `n` = nth output only |
| `A, B, C, D` | Adams View matrices containing linear state matrices |
| `freq_start` | First frequency of requested range |
| `freq_end` | Last frequency of requested range |
| `freq_arg` | Step size or sample count (depends on `outtype`) |

---

## BODELSE

Returns gain and/or phase values for an Adams View linear state equation (LSE) element.

```
BODELSE(outtype, outindex, lse, freq_start, freq_end, freq_arg)
```

| Argument | Description |
|----------|-------------|
| `outtype` | Output/sampling flag |
| `outindex` | `0` = all outputs; `n` = nth output |
| `lse` | Adams linear state equation entity |
| `freq_start` | First frequency |
| `freq_end` | Last frequency |
| `freq_arg` | Step size or sample count |

---

## BODELSM

Returns gain and/or phase values for a linear state model.

```
BODELSM(outtype, outindex, lsm, freq_start, freq_end, freq_arg)
```

---

## BODESEQ

Returns gain and/or phase values from a state equation defined by arrays.

```
BODESEQ(outtype, outindex, A, B, C, D, freq_start, freq_end, freq_arg)
```

---

## BODETFCOEF

Returns gain and/or phase for a system defined directly by transfer-function numerator and denominator coefficient arrays.

```
BODETFCOEF(outtype, numerator, denominator, freq_start, freq_end, freq_arg)
```

| Argument | Description |
|----------|-------------|
| `outtype` | Output/sampling flag |
| `numerator` | Array of numerator polynomial coefficients |
| `denominator` | Array of denominator polynomial coefficients |
| `freq_start` | First frequency |
| `freq_end` | Last frequency |
| `freq_arg` | Step size or sample count |

---

## BODETFS

Returns gain and/or phase values for an Adams View transfer function element.

```
BODETFS(outtype, tfs, freq_start, freq_end, freq_step)
```

| Argument | Description |
|----------|-------------|
| `outtype` | Output/sampling flag |
| `tfs` | Adams transfer function entity |
| `freq_start` | First frequency |
| `freq_end` | Last frequency |
| `freq_step` | Step size or sample count |

---

## BUTTER_NUMERATOR

Returns the numerator coefficients for a Butterworth filter.

```
BUTTER_NUMERATOR(n, wn, ftype, is_digital)
```

| Argument | Description |
|----------|-------------|
| `n` | Filter order (integer) |
| `wn` | Cutoff frequency array (one or two elements) |
| `ftype` | `"low"`, `"high"`, `"pass"`, or `"stop"` |
| `is_digital` | Boolean — `1` for digital, `0` for analogue |

```adams_fn
BUTTER_NUMERATOR(6, {0.1951, 0.4081}, "pass", 1)
! returns {0.0005, 0, 0.0070, 0, -0.0094, 0, 0.0070, 0, -0.0028, 0, 0.0005}
```

---

## BUTTER_DENOMINATOR

Returns the denominator coefficients for a Butterworth filter.

```
BUTTER_DENOMINATOR(n, wn, ftype, is_digital)
```

Arguments are identical to `BUTTER_NUMERATOR`.

---

## BUTTER_FILTER

Filters a curve using a Butterworth filter of a specified order and cutoff frequency.

```
BUTTER_FILTER(x, y, ftype, order, cutoff, is_analog, is_two_pass)
```

| Argument | Description |
|----------|-------------|
| `x` | 1×N array of x-axis (usually time) values |
| `y` | 1×N array of signal values |
| `ftype` | `"low"`, `"high"`, `"pass"`, or `"stop"` |
| `order` | Filter order (integer) |
| `cutoff` | Cutoff frequency array (one or two elements, in Hz) |
| `is_analog` | Boolean — use analogue filtering |
| `is_two_pass` | Boolean — use zero-phase (bidirectional) filtering |

```adams_fn
! Low-pass Butterworth, 4th order, 10 Hz cutoff, zero-phase
filtered = BUTTER_FILTER(time_array, signal, "low", 4, {10}, 0, 1)
```

---

## See also

- [Signal processing functions](signal-processing.md)
- [Window functions](window-functions.md)
