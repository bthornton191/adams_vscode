# STEP

Returns an array of y values, on a step curve, corresponding to the x values.

## Format
```
STEP (A, xo, ho,x1,h1)
```

## Arguments

**A**
: An array of x values.

**xo**
: Value of x at which the step starts ramping from ho to h1.

**ho**
: Value of h when x is less than or equal to xo.

**x1**
: Value of x at which the step function reaches h1.

**h1**
: Value of h when x is greater than or equal to h1.
