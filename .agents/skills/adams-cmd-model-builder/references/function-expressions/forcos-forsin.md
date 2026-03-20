# FORCOS / FORSIN — Fourier Series

Evaluate a finite Fourier cosine or sine series with up to 31 terms.

## Formats

```
FORCOS(x, Shift, Frequency, c0, c1, c2, ..., cN)
FORSIN(x, Shift, Frequency, c0, c1, c2, ..., cN)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable |
| `Shift` | Required | Horizontal shift: series is evaluated at `(x - Shift)` |
| `Frequency` | Required | Angular frequency ω (rad per unit of x). Append `D` to specify in degrees, e.g. `360D` for one cycle per unit |
| `c0, c1, ..., cN` | Required | Fourier coefficients (up to 31). `c0` is the DC term; `c1, c2, ...` are the amplitudes of successive harmonics |

**Equations:**

$$\text{FORCOS} = c_0 + c_1 \cos(\omega(x-s)) + c_2 \cos(2\omega(x-s)) + \cdots$$

$$\text{FORSIN} = c_0 + c_1 \sin(\omega(x-s)) + c_2 \sin(2\omega(x-s)) + \cdots$$

where $s$ is the shift and $\omega$ is the frequency.

> The frequency is in **radians per unit of x** by default. Use the `D` suffix for degrees per unit.

## Examples

```adams_fn
! Cosine series: DC=0, fundamental at 2π rad/sec (1 Hz), amplitude 10
FORCOS(TIME, 0, 6.2832, 0, 10.0)

! Same but specify frequency in degrees: 360 deg/sec = 1 Hz
FORCOS(TIME, 0, 360D, 0, 10.0)

! Sine series shifted by 0.5 s, with two harmonics
FORSIN(TIME, 0.5, 6.2832, 0, 5.0, 2.5)
```

## Difference between FORCOS and FORSIN

| Function | Harmonics use | DC term |
|----------|--------------|---------|
| `FORCOS` | cosines | `c0` |
| `FORSIN` | sines | `c0` |

The two can be combined using arithmetic: `FORCOS(...) + FORSIN(...)`.

## See also

- [SHF](shf.md) — simple harmonic function (single sine term with amplitude, frequency, phase, offset)
- [POLY](poly.md), [CHEBY](cheby.md) — polynomial alternatives
