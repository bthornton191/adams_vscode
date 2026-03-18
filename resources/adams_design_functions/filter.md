# FILTER

Returns a 1xN array of filtered input values, where N is the number of input values. The coefficients of the transfer function define the filter.

## Format
```
FILTER (Independent Variable, Dependent Variable, Numerator Coefficients, Denominator Coefficients, Filtering Method)
```

## Arguments

**Independent Variable**
: A 1xN array of independent values.

**Dependent Variable**
: A 1xN array of dependent values as a function of the independent values.

**Numerator Coefficients**
: A set of numerator coefficients in the transfer function.

**Denominator Coefficients**
: A set of denominator coefficients in the transfer function. The number of denominator coefficients can't be lower than the number of numerator coefficients.

**Filtering Method**
: There are two filtering methods:

  * **Continuous** — The continuous (or analog) filter transforms the input data into frequency space, passes it through the transfer function, and returns it to physical space. A nonzero value indicates the use of the continuous filter. The notation used in the transfer function equations is:
    * `a` — user-supplied numerator coefficient
    * `b` — user-supplied denominator coefficient
    * `z` — dependent value
    * `n` — number of numerator coefficients
    * `m` — number of denominator coefficients

  * **Discrete** — The discrete (or digital) filter applies the transfer function directly to the input data stream in physical space. A value of 0 indicates the use of the discrete filter.
