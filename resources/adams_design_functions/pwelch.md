# PWELCH

Estimate the power spectral density (PSD) of a signal using Welch's method. Here we use MATLAB to compute the PSD. This way the sum of the PSD is equal to the time-integral squared amplitude of the original signal.

## Format
```
PWELCH (a, nFft, Fs, win, nOverLap) returns ARRAY
```

## Arguments

**a**
: An array indicating the sequence of signal to estimate the power spectral density.

**nFft**
: An integer indicating the length of FFT to be used.

**Fs**
: A real value indicating the frequency of the signal.

**win**
: An array indicating the array of the window to be used.

**nOverLap**
: An integer indicating the number of overlaps.
