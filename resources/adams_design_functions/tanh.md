# TANH

Returns the hyperbolic tangent of an expression that represents a numerical value:

## Format
```
TANH(x)
```

## Arguments

**x**
: Any valid expression that evaluates to a real number.

## Example

Using a hyperbolic tangent, the following function defines a smooth step function that transitions from a value of -1 to 1. The smoothness is controlled by the modifier, in this case 5.

### Function
```
TANH(5*(TIME-1.5))
```

### Result
```
-6.99
```
