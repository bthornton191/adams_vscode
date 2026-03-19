# panel set twindow_function polynomial

The POLYNOMIAL function evaluates a standard polynomial at a user specified value x. The SHIFT (i.e. x0) and the COEFFICIENTS (i.e. a0, a1,..., a30) parameters are used to define the constants for the polynomial. The standard polynomial is defined as:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `x` | Run Time Function | Specifies the run time function. |
| `shift` | Real | Specifies a real variable that is a non-angular shift in a Chebyshev polynomial, Fourier Cosine series, Fourier Sine series, or polynomial function.Or, a phase shift in the independent variable x, for a simple_harmonic_function. |
| `angular_shift` | Angle | Specifies a real variable that is a angular shift in a Chebyshev polynomial, Fourier Cosine series,Fourier Sine series, or polynomial function.Or, a phase shift in the independent variable x, for a simple_harmonic_function. |
| `coefficients` | Real | Specifies the non-angular real variables that define as many as thirty-one coefficients (a0, a1,..., a30) for the series or polynomial. |
| `angular_coefficients` | Angle | Specifies the angular real variables that define as many as thirty-one coefficients (a0, a1,..., a30) for the series or polynomial. |
