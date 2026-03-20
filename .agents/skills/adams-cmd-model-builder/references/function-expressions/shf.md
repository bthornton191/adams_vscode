# SHF — Simple Harmonic Function

Returns a single-frequency sinusoidal value with controllable amplitude, frequency, phase shift, and average (DC offset).

## Format

```
SHF(x, x0, a, omega, phi, b)
```

## Arguments

| Argument | Req | Description |
|----------|-----|-------------|
| `x` | Required | The independent variable (typically `TIME`) |
| `x0` | Required | Shift of the independent variable (horizontal offset) |
| `a` | Required | Amplitude |
| `omega` | Required | Angular frequency (rad per unit of `x`). Append `D` for degrees |
| `phi` | Required | Phase shift (radians). Append `D` for degrees |
| `b` | Required | Average value (DC offset) |

**Equation:**

$$\text{SHF} = a \cdot \sin\!\bigl(\omega(x - x_0) - \phi\bigr) + b$$

## Examples

```adams_fn
! 10 mm amplitude, 1 Hz (ω = 2π rad/s), no phase, no offset
SHF(TIME, 0, 10.0, 6.2832, 0, 0)

! Same with degrees: 360D means 360 degrees per second = 1 cycle/s
SHF(TIME, 0, 10.0, 360D, 0, 0)

! Phase shifted by 25 degrees, DC offset of 5
SHF(TIME, 25D, PI, 360D, 0, 5)
! = PI * sin(360D * (TIME - 25D) - 0) + 5
```

## Notes

- To express frequency in Hz: `omega = 2 * PI * freq_hz`
- The phase shift argument `phi` shifts the waveform **rightward** (positive phi = delayed start)
- The shift `x0` also delays the waveform (equivalent to a negative phase for a sine)

## See also

- [FORCOS / FORSIN](forcos-forsin.md) — multi-harmonic Fourier series
