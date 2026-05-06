# Functions: Harmonic, Series, and Sweep

## SHF(x, x0, a, w, phi, b)
Simple harmonic function: `a * SIN(w*(x-x0) - phi) + b`
- **x:** independent variable (typically TIME)
- **x0:** time offset; **a:** amplitude; **w:** frequency (rad/time; append D for deg/time); **phi:** phase shift (rad); **b:** bias
- **Returns:** real
- **Use for:** sinusoidal motions, vibration forcing, rotating imbalance

## POLY(x, x0, a0, a1, …, a30)
Polynomial: `Σ aⱼ·(x-x0)ʲ` — up to 31 coefficients (j = 0 to 30).
- **x:** independent variable; **x0:** shift (evaluate polynomial at x-x0)
- **Returns:** real
- **Notes:** Up to degree 30. Evaluated in exactly the order listed — not Horner form. Large coefficients with high-degree terms can cause numerical overflow; normalise x first.

## CHEBY(x, x0, a0, a1, …, a30)
Chebyshev polynomial series: `Σ aⱼ·Tⱼ(x-x0)` — up to 31 coefficients.
- Same argument structure as POLY.
- Uses recursive: T₀=1, T₁=x-x0, Tⱼ=2(x-x0)Tⱼ₋₁−Tⱼ₋₂
- **Returns:** real
- **Use when:** fitting tabular data over a fixed domain with Chebyshev approximation

## FORCOS(x, x0, w, a0, a1, …, a30)
Fourier cosine series: `a0 + Σ aⱼ·COS(j·w·(x-x0))`
- **x, x0:** independent variable and offset; **w:** fundamental frequency (rad/time)
- **Returns:** real
- **Use for:** periodic forcing functions defined by Fourier coefficients

## FORSIN(x, x0, w, a0, a1, …, a30)
Fourier sine series: `a0 + Σ aⱼ·SIN(j·w·(x-x0))`
- Same structure as FORCOS but with SIN.
- **Returns:** real

## SWEEP(x, a, x0, f0, x1, f1, dx)
Sinusoidal with linearly increasing frequency (linear chirp): `a·SIN(phase(x))`
- **x:** independent variable; **a:** amplitude; **x0, x1:** sweep start/end; **f0, f1:** start/end frequency (Hz); **dx:** activation ramp interval
- **Returns:** real
- **Notes:** `dx > 0` required to avoid phase discontinuity when x0 > 0. Phase computed by integrating instantaneous frequency. Use for resonance search and frequency response studies.

## INVPSD(x, id, f0, f1, nf, linlog, seed)
Regenerates a random time signal from a Power Spectral Density SPLINE.
- **id:** SPLINE element with PSD vs. frequency data; **f0, f1:** frequency range (Hz); **nf:** number of frequency components (2–200); **linlog:** 0=linear, 1=log domain; **seed:** integer randomisation seed (1–20)
- **Returns:** real
- **Notes:** Same seed always yields the same phase angles. Up to 20 unique seeds per simulation. Use for fatigue and road surface vibration inputs.
